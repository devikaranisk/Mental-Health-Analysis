import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pandas as pd
import joblib
import smtplib


# ==========================
# Paths
# ==========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # project root
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
USER_FILE = os.path.join(BASE_DIR, "users.json")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = "your_secret_key"  # needed for session

# ==========================
# Load trained model & label encoder
# ==========================
clf = joblib.load(os.path.join(BASE_DIR, "backend", "model.pkl"))
le = joblib.load(os.path.join(BASE_DIR, "backend", "label_encoder.pkl"))

# Load text-based model
text_model = joblib.load(os.path.join(BASE_DIR, "backend", "logistic_regression_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "backend", "tfidf_vectorizer.pkl"))

# ==========================
# Symptom list
# ==========================
symptoms = [
    "inability_to_control",
    "social_isolation",
    "low_energy",
    "difficulty_being_patient",
    "intense_anger",
    "feeling_detached_from_oneself",
    "sleep_disturbance",
    "feeling_easily_tired",
    "intrusive_memories",
    "fear_of_gaining_weight",
    "nightmares",
    "excessive_fear_of_mistakes",
    "unpredictable_behavior",
    "chest_pain",
    "giving_up_important_activites",
    "fatigue",
    "hearing_voices",
    "presence_of_two_or_more_distinct_identities",
    "sadness",
    "mood_changes",
    "hot _flashes",
    "physical_aches_and_pains",
    "increased_activity",
    "feeling_of_detachment",
    "feeling_on_edge",
    "angry_outbursts",
    "flact_affect",
    "physical_symptoms_in_social_settings",
    "nausea",
    "sleep_problem_from_obsessive_thinking",
    "mind_going_blank",
    "emotional_instability",
    "avoidance_of_situations_that_trigger_obsession",
    "changes_in_body_weight_shape",
    "difficulty_controlling_anger",
    "loss_of_interest",
    "muscle_tension",
    "interrupting_others",
    "irritability",
    "significant_weight_loss",
    "excessive_talking",
    "forgetfulness_in_daily_activities",
    "trembling",
    "inability_to_stay_seated",
    "using_more_of_the_substance",
    "rapid_speech",
    "eating_large_amounts_of_food",
    "recurrent_suicidal_behavior,self_harm",
    "restlessness",
    "chronic_feelings_of_emptiness",
    "vomiting",
    "strong_carvings",
    "hallucination",
    "continued_use_despite_social_problems",
    "flashbacks",
    "easily_distracted",
    "difficulty_speaking",
    "abnormal_behavior",
    "memory_loss",
    "lack_of_motivation",
    "avoidance_of_reminders_of_the_trauma",
    "severe_anxiety",
    "headache",
    "changes_in_weight",
    "negative_changes",
    "time_consuming_rituals",
    "feeling_of_guilt",
    "thoughts_of_death ",
    "decreased_need_for_sleep",
    "rapid_heartbeat",
    "sweating",
    "disorganized_thinkung",
    "avoidance_of_social_activity",
    "repetitve_behaviors",
    "sudden_intense_fear",
    "difficulty_functioning_in_daily_life",
    "intense_fear_of_social_situations",
    "low_self-esteem",
    "feeling_of_worthless",
    "dizziness",
    "extreme_restriction_of_food_intake",
    "intense_fear_of_abandonment",
    "social_withdrawal",
    "shortness_of_breath",
    "depressive_symptoms",
    "impulsive_behaviors",
    "feeling_disconnected_from_surroundings",
    "avoid_eating_in_public",
    "hypervigilance",
    "fear_of_losing",
    "sudden_shift_in_mood",
    "spending_a_lot_time_recovering_from_the_substance",
    "stomachaches",
    "required_perfectness",
    "suicidal_thoughts",
    "difficulty_making_eye_contact",
    "frequently_losing_items",
    "delusion",
    "extreme_sensitivity_to_criticism",
    "physical_and_psychological_problems",
    "inability_to_feel_pleasure",
    "overthinking",
    "identity_disturbance",
    "difficulty_sustaining_attention",
    "neglecting_responsibilites",
    "difficulty_concentrating",
    "neglect_of_personal_hygiene",
    "impulsivity",
    "tolerance",
    "excessive_fear_of_embarrassment",
    "significant_weight_gain",
    "blackouts",
    "panic",
    "change_body_image",
    "loss_of_pleasure",
    "excessive_worry",
    "unwanted_thoughts",
    "rapid_heartbeat_during_social_interactions",
    "trouble_concentrating ",
    "significant_distress_in_daily_life",
    "difficulty_concentrating ",
    "unstable_interpersonal_relationships",
    "low_mood",
    "withdrawal_symptoms",
    "poor_organizational_skill",
    "fidgeting",
    "irritable_mood"
]

# ==========================
# Helper Functions
# ==========================
def load_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

# ==========================
# Routes
# ==========================
@app.route("/")
def home():
    return render_template("login.html")  # default page

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form.to_dict()
        users = load_users()

        # check duplicate
        for u in users:
            if u["email"] == data["email"]:
                return jsonify({"message": "User already exists"}), 400

        new_id = max([u["id"] for u in users], default=0) + 1
        data["id"] = new_id
        users.append(data)
        save_users(users)

        return jsonify({"message": "Registration successful!"}), 201

    # if GET request → render registration page
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        users = load_users()
        
        for u in users:
            if u["email"] == email and u["password"] == password:
                # Store only the user's ID in the session
                session["user_id"] = u["id"]
                return redirect(url_for("index"))
        
        return jsonify({"message": "Invalid credentials"}), 401

    # GET request → show login page
    return render_template("login.html")


def get_logged_in_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    users = load_users()
    for u in users:
        if u["id"] == user_id:
            return u
    return None

@app.route("/index", methods=["GET", "POST"])
def index():
    user = get_logged_in_user()
    if not user:
        return redirect(url_for("login"))
    
    return render_template("index.html", symptoms=symptoms)

@app.route("/logout")
def logout():
    session.pop("user_id", None)  # remove user_id from session
    return redirect(url_for("login"))  # redirect to login page


@app.route("/predict", methods=["POST"])
def predict():
    if "user_id" not in session:
        return redirect(url_for("home"))

    data = request.form
    sample = {symptom: int(data.get(symptom, 0)) for symptom in symptoms}
    df = pd.DataFrame([sample])
    
    pred = clf.predict(df)[0]
    pred_disease = le.inverse_transform([pred])[0]

    # Render the page with the prediction
    return render_template("index.html", symptoms=symptoms, prediction=pred_disease)






@app.route("/predict_text", methods=["GET", "POST"])
def predict_text():
    if "user_id" not in session:
        return redirect(url_for("home"))

    prediction = None
    if request.method == "POST":
        statement = request.form.get("statement")
        if statement:
            X_tfidf = vectorizer.transform([statement])
            pred = text_model.predict(X_tfidf)[0]
            prediction = f"Predicted Status: {pred}"

    return render_template("predict_text.html", prediction=prediction)








# ==========================
# Run Flask
# ==========================
if __name__ == "__main__":
    app.run(debug=True)
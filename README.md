📖 Introduction

This project is a Flask-based machine learning web application that analyzes adolescent mental health.
It supports multi-modal inputs:

✅ Text-based input

✅ Video input

The system predicts possible mental health conditions and provides an option for 108 emergency support, along with storing doctor and parent contact information during client registration.

🔑 Features

👤 Client Registration & Login – Secure registration with personal details + doctor/parent contacts.

📝 Form-based Symptom Input – Clients tick/select symptoms in a form, and the ML model predicts possible mental health conditions

🎥 Video Input Analysis – Allows video-based input for deeper emotion/behavior assessment.

🚨 Emergency Support – 108 emergency option available; doctor/parent details stored for future integration.

🔒 Authentication – Session-based login/logout for secure access.

🛠 Tech Stack

Backend: Flask (Python)

Frontend: HTML, CSS, JavaScript

ML Models: Logistic Regression, TF-IDF Vectorizer, Scikit-learn

Data Handling: Pandas, Joblib, CSV files

Emergency Support: 108 integration

🚀 Future Enhancements

📧 Automatic SMS Alerts – Notify doctors/parents instantly in emergencies.

📈 Real-time Dashboards – Visual insights into client’s mental health trends and progress.

📱 Mobile-friendly UI – Responsive design for easy access on smartphones and tablets.


⚙ Prerequisites

Python  – [ Download Python](https://www.python.org/downloads/) 

Visual Studio code(prefered code editor) -[ https://code.visualstudio.com/download.](https://code.visualstudio.com/download)

GitHub -[https://desktop.github.com/download/](https://desktop.github.com/download/)


🛠 Installation & Run
1. Clone the repository
<pre> ''' 
  git clone https://github.com/<USERNAME>/Mental-health-analysis.git
  cd Mental-health-analysis
'''</pre>

Create a virtual environment
<pre>'''
  python -m venv venv
  # macOS / Linux
  source venv/bin/activate
  # Windows (PowerShell)
  .\venv\Scripts\Activate.ps1
'''</pre>

Install dependencies
<pre>''' 
  pip install -r requirements.txt
'''</pre>

Or manually if requirements.txt is missing:
<pre>'''
  pip install Flask pandas joblib scikit-learn
'''</pre>

Run the Flask app
<pre>''' 
  python app.py
'''</pre>

✅ Step-by-Step Testing & Verification
1. Register a New Client
  
  Fill in the registration form with:
  
  Client Info: name, email, password, phone
  
  Doctor Info: name, email, phone
  
  Parent/Guardian Info: name, email, phone
  
  Expected: users.json is created/updated.

  Example curl command (copyable):
  curl -X POST \
    -F "name=Test Client" \
    -F "email=test@example.com" \
    -F "password=pass123" \
    -F "phone=9876543210" \
    -F "doctor_name=Dr X" \
    -F "doctor_email=drx@example.com" \
    -F "doctor_phone=9123456780" \
    -F "parent_name=Parent Y" \
    -F "parent_email=parenty@example.com" \
    -F "parent_phone=9988776655" \

2. Login

  Enter your registered email and password.
  
  Expected: Redirects to the dashboard/index page.

3. Check Dashboard & Symptom Form

  Tick some symptoms (e.g., sadness, sleep_disturbance, low_energy).
  
  Submit the form.
  
  Expected: Prediction is displayed (from model.pkl & label_encoder.pkl).

4. Test Video Input

  Upload a short video (mp4) or record a new one.
  
  Submit the video.
  
  Expected: File stored under static/uploads/ (or analyzed if video model exists).

5. Test Emergency (108)

  Click the Emergency / 108 button.
  
  Expected: Modal or alert shows 108 and stored doctor/parent contacts.

6. Verify Stored Contacts

  Open users.json
  
  Expected: Doctor and parent contact details are correctly saved.

7. Logs & Troubleshooting

  Check the terminal running python app.py for errors or stack traces.
  
  Common Issues:
  
  Issue	                                            Solution
  FileNotFoundError                                	Place model.pkl & label_encoder.pkl in backend/
  Port conflict	                                    Stop other apps using port 5000 or change Flask port
  JSON read/write errors	                          Check permissions for users.json

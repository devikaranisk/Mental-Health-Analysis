const form = document.getElementById("symptomForm");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(form);

  // Convert FormData to JSON object
  const data = {};
  formData.forEach((value, key) => {
    data[key] = parseInt(value);  // Convert string "1" to number 1
  });

  const response = await fetch("/predict", {
    method: "POST",
    body: formData  // you can keep FormData or send JSON
  });

  const result = await response.json();

  // Display actual prediction from backend
  resultDiv.innerHTML = `Predicted Disease: ${result.prediction}`;
});

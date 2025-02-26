from flask import Flask, request, render_template
import numpy as np
import pickle

app = Flask(__name__)

# Load trained model and encoders
model = pickle.load(open("career_model.pkl", "rb"))
le_interest = pickle.load(open("le_interest.pkl", "rb"))
le_career = pickle.load(open("le_career.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        logical = float(request.form["logical"])
        verbal = float(request.form["verbal"])
        quantitative = float(request.form["quantitative"])
        interest = le_interest.transform([request.form["interests"]])[0]

        # Prepare input and make prediction
        input_features = np.array([[logical, verbal, quantitative, interest]])
        prediction = model.predict(input_features)
        career_result = le_career.inverse_transform(prediction)[0]

        return render_template("index.html", prediction=career_result)

    return render_template("index.html", prediction=None)

if __name__ == "__main__":
    app.run(debug=True)

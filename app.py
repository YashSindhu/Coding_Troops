from flask import Flask, request, render_template
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore
import pickle
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("firebase_credentials.json")  # Ensure this file is in your project folder
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load trained ML model and encoders
model = pickle.load(open("career_model.pkl", "rb"))
le_interest = pickle.load(open("le_interest.pkl", "rb"))
le_career = pickle.load(open("le_career.pkl", "rb"))

# Web Scraping Function - Fetch job listings from Indeed
def scrape_jobs(job_title="Data Scientist"):
    job_title = job_title.replace(" ", "+")
    url = f"https://www.indeed.com/jobs?q={job_title}&l=USA"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    job_data = []
    jobs = soup.find_all("div", class_="job_seen_beacon")

    for job in jobs[:5]:  # Limit to top 5 results
        title = job.find("h2", class_="jobTitle").text if job.find("h2") else "N/A"
        company = job.find("span", class_="companyName").text if job.find("span") else "N/A"
        salary = job.find("div", class_="salary-snippet").text if job.find("div", class_="salary-snippet") else "Not Provided"

        # Store jobs in Firebase
        db.collection("job_listings").add({"title": title, "company": company, "salary": salary})
        
        job_data.append({"title": title, "company": company, "salary": salary})

    return job_data

@app.route("/", methods=["GET", "POST"])
def predict():
    jobs = []
    if request.method == "POST":
        # Get user input
        logical = float(request.form["logical"])
        verbal = float(request.form["verbal"])
        quantitative = float(request.form["quantitative"])
        interest = request.form["interests"]

        # Convert interest into numerical format
        interest_encoded = le_interest.transform([interest])[0]

        # Make career prediction
        input_features = np.array([[logical, verbal, quantitative, interest_encoded]])
        prediction = model.predict(input_features)
        career_result = le_career.inverse_transform(prediction)[0]

        # Scrape relevant job listings for the predicted career
        jobs = scrape_jobs(career_result)

        return render_template("index.html", prediction=career_result, jobs=jobs)

    return render_template("index.html", prediction=None, jobs=[])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

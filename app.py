import os
import json
from flask import Flask, request, render_template
from firebase_admin import credentials, initialize_app, firestore

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin SDK using environment variable
firebase_json = os.getenv("FIREBASE_CREDENTIALS")

if firebase_json:
    try:
        firebase_dict = json.loads(firebase_json)  # Convert string to dictionary
        cred = credentials.Certificate(firebase_dict)  # Pass dictionary directly
        initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase initialized successfully!")
    except Exception as e:
        print(f"🚨 Error initializing Firebase: {e}")
        db = None  # Avoid crashes
else:
    print("🚨 FIREBASE_CREDENTIALS environment variable not set.")
    db = None  # Avoid crashes

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    jobs = []
    
    if request.method == "POST":
        try:
            logical = float(request.form["logical"])
            verbal = float(request.form["verbal"])
            quantitative = float(request.form["quantitative"])
            interest = request.form["interests"]

            # Dummy prediction logic (Replace with AI model)
            career_map = {
                "Tech": "Software Engineer",
                "Business": "Marketing Manager",
                "Arts": "Graphic Designer",
                "Science": "Research Scientist"
            }
            prediction = career_map.get(interest, "Unknown Career")

            # Retrieve job listings from Firestore (only if Firestore is initialized)
            if db:
                jobs_ref = db.collection("job_listings").limit(5).stream()
                jobs = [doc.to_dict() for doc in jobs_ref]
            else:
                print("⚠️ Firestore database not available.")

        except Exception as e:
            print(f"🚨 Error processing request: {e}")

    return render_template("index.html", prediction=prediction, jobs=jobs)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("DEBUG_MODE", "False").lower() == "true")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
from transformers import pipeline

# Load dataset
df = pd.read_csv("career_data.csv")

# Encode categorical features
le_interest = LabelEncoder()
le_career = LabelEncoder()
df["interests"] = le_interest.fit_transform(df["interests"])
df["career"] = le_career.fit_transform(df["career"])

# Split data into training and testing sets
X = df.drop("career", axis=1)
y = df["career"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoders
pickle.dump(model, open("career_model.pkl", "wb"))
pickle.dump(le_interest, open("le_interest.pkl", "wb"))
pickle.dump(le_career, open("le_career.pkl", "wb"))

print("Model trained and saved successfully!")


# Load a pre-trained NLP model
career_analyzer = pipeline("text-classification", model="distilbert-base-uncased")

def predict_career(user_input):
    result = career_analyzer(user_input)[0]["label"]
    return result

# Example
print(predict_career("I love coding and problem-solving."))


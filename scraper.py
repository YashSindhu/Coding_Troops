import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase_credentials.json")  # Download this from Firebase
firebase_admin.initialize_app(cred)
db = firestore.client()

def scrape_jobs(job_title="Data Scientist"):
    job_title = job_title.replace(" ", "+")
    url = f"https://www.indeed.com/jobs?q={job_title}&l=USA"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("div", class_="job_seen_beacon")

    for job in jobs:
        title = job.find("h2", class_="jobTitle").text if job.find("h2") else "N/A"
        company = job.find("span", class_="companyName").text if job.find("span") else "N/A"
        salary = job.find("div", class_="salary-snippet").text if job.find("div", class_="salary-snippet") else "Not Provided"

        # Store in Firebase
        db.collection("job_listings").add({
            "title": title,
            "company": company,
            "salary": salary
        })


# Run scraper
scrape_jobs("AI Engineer")


def scrape_jobs(job_title="Data Scientist"):
    job_title = job_title.replace(" ", "+")
    url = f"https://www.indeed.com/jobs?q={job_title}&l=USA"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    job_data = []
    jobs = soup.find_all("div", class_="job_seen_beacon")

    for job in jobs:
        title = job.find("h2", class_="jobTitle").text if job.find("h2") else "N/A"
        company = job.find("span", class_="companyName").text if job.find("span") else "N/A"
        salary = job.find("div", class_="salary-snippet").text if job.find("div", class_="salary-snippet") else "Not Provided"
        job_data.append({"Title": title, "Company": company, "Salary": salary})

    return pd.DataFrame(job_data)

# Run the scraper
df = scrape_jobs("AI Engineer")
df.to_csv("jobs_data.csv", index=False)
print("Scraped job data saved successfully!")

from flask import Flask,render_template_string, request
import requests
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Job Finder</title>
<style>
  body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; background: #f5f5f5; padding: 20px; }
  h1 { color: #2c3e50; }
  .search-box { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
  input[type=text] { width: 70%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
  button { background: #2c3e50; color: white; padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; }
  .job-card { background: white; padding: 16px; border-radius: 10px; margin-bottom: 12px; border-left: 4px solid #2c3e50; }
  .job-title { font-size: 16px; font-weight: bold; color: #2c3e50; }
  .job-company { color: #666; margin: 4px 0; }
  .match { color: #27ae60; font-weight: bold; }
  .email-box { background: #f8f9fa; padding: 12px; border-radius: 6px; margin-top: 10px; font-size: 13px; white-space: pre-wrap; }
</style>
</head>
<body>
<h1>🤖 Job Finder & Email Generator</h1>
<div class="search-box">
  <form method="POST">
    <input type="text" name="skills" placeholder="Enter your skills e.g. python, flask, api" value="{{ skills }}">
    <button type="submit">Find Jobs</button>
  </form>
</div>
{% for job in jobs %}
<div class="job-card">
  <div class="job-title">{{ job.title }}</div>
  <div class="job-company">{{ job.company }}</div>
  <div class="match">Match: {{ job.match }}%</div>
  <div class="email-box">{{ job.email }}</div>
</div>
{% endfor %}
{% if searched and not jobs %}

<div style="background:white;padding:20px; border-radius:10px; color:#e74c3c; text-align:center;">
    NO jobs found for "{{skills}}" -try python , react , marketing or design!
</div>
{% endif %}

</body>
</html>
"""
@app.route("/",methods=["GET","POST"])
def index():
    jobs=[]
    skills=""
    searched = False
    if request.method == "POST":
        skills = request.form["skills"]
        my_skills = [s.strip().lower() for s in skills.split(",")]
        response = requests.get(f"https://remotive.com/api/remote-jobs?search={skills}")
        all_jobs = response.json()["jobs"]
        good_jobs = []
        for job in all_jobs:
            tags =[tag.lower() for tag in job["tags"]]
            matched =[s for s in my_skills if s in tags]
            if matched:
                match_pct = round(len(matched)/len(my_skills)*100,2)
                good_jobs.append({"title": job["title"],"company": job["company_name"],"match": match_pct,"matched_skills": ", ".join(matched)})
        good_jobs = sorted(good_jobs, key= lambda x: -x["match"])[:5]
        searched = True
        for job in good_jobs:
            prompt =f"Write a short professional job application email for {job['title']} at {job['company']}. My name is Araj. Skills: Python, Flask, Claude API, pandas, web scraping. Under 100 words."
            message = client.messages.create(model="claude-sonnet-4-6", max_tokens=200, messages=[{"role": "user", "content": prompt}])
            job["email"] = message.content[0].text
            jobs.append(job)

    return render_template_string(HTML,jobs=jobs,skills=skills,searched=searched)
if __name__ == "__main__":
    app.run(debug=True)


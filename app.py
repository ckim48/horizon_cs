from flask import Flask, render_template, request
from openai import OpenAI
import json
app = Flask(__name__) # Creating an empty web app.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/main')
def main():
    return render_template('main.html')


# Scenario
# Time period (ex) in 2035 or after a new government policy)
# Place: rurual vs city, south korea vs usa
# describe the view of different stakeholder. ex) if taxi driver is replaced by AI
# driver vs company vs customer vs government  --> they might have different opinion of replacing taxi driver with AI.
#  ++ social impact, economic impact with the realistic numbers ( details about the cost we need for replacing job with AI)

# Options --> related to the pace of adapation --> speed & scope
# option A --> replace all the taxi driver in 2 yeaers in rural , then replacd all the taxi driver in next 3 years in main cities.

# Generate a scenario, and options for decision-making using GPT model.
def generate_scenario(job):
    system = (
        "You are an instructional designer creating, short ethical scenario"
        "about AI replacing human jobs. The should be realistic, neutral, and suitable for high school student."
        "focus on human impact, tradeoffs, and decision-making."
    )
    prompt = f""" 
    Create one scenario about AI replacing the job: {job}.
    Return STRICT JSON with this schema.
    {{
        "title" : "string (less than 40 characters)",
        "scenario_text": string (100-150 words)",
        "options": [
            {{"id": "opt1", "label": "button label","rationale": "1-2 sentence explanation"}},
            {{"id": "opt2", "label": "button label","rationale": "1-2 sentence explanation"}},
            {{"id": "opt3", "label": "button label","rationale": "1-2 sentence explanation"}},
            {{"id": "opt4", "label": "button label","rationale": "1-2 sentence explanation"}},
        ],
    }}
    """
    response = client.chat.completions.create(
        model = "gpt-4.1-mini",
        temperature= 0.6, # 0 --> deterministic/consistent content.  1 ---> creative content.
        response_format={"type": "json_object"},
        messages = [
            {"role":"system", "content": system},
            {"role":"user","content": prompt}
        ]
    )
    result = response.choices[0].message.content
    data = json.loads(result)
    title = data["title"]
    scenario_text = data["scenario_text"]
    options = data["options"]

    return title, scenario_text, options

@app.route('/scenario' , methods=["GET","POST"])
def scenario():
    if request.method == "POST":
        job = request.form.get("job").strip()
        title, scenario_text, options = generate_scenario(job)
        return render_template("scenario_result.html",title=title, scenario_text=scenario_text,options =options  )
    return render_template('scenario.html')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
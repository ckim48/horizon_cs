from flask import Flask, render_template, request, redirect, url_for, flash
from openai import OpenAI
import sqlite3
import json
app = Flask(__name__) # Creating an empty web app.
app.config["SECRET_KEY"] = "abc"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password") # what user put on login

        conn = sqlite3.connect('app.db') # connecting to DB
        cur = conn.cursor()

        # Get password in form of object for the given username from the DB
        row = cur.execute("SELECT password from Users where username = ?",(username,))
        print(row.fetchone())
        if row.fetchone() is None: # username is not in our DB --> login fail
            flash('Wrong username or password')
            return render_template('login.html')
        db_password = row.fetchone()[0] # for getting password from the object in form of String value
        conn.close()

        if password == db_password:  # login success
            flash('Wrong username or password')
            return redirect(url_for('index')) # go to homepage
        return render_template('login.html') # when login fail stay on login page

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST": # when users send their username/password --> so we should save them into our DB.
        username = request.form.get("username") # we get what user put on the input for the username
        password = request.form.get("password") # something for the password

        conn = sqlite3.connect('app.db') # connecting to DB
        cur = conn.cursor() # for creating an object for executing SQL code in Python

        # will add the username and password to our DB --> allowing the user to register on our website
        cur.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
        conn.commit() # Saving DB
        conn.close() # Disconnecting with DB
        return redirect(url_for('login')) # done with the register so send user to the login page
    return render_template('register.html')

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
from flask import Flask, render_template

app = Flask(__name__) # Creating an empty web app.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
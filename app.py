from flask import Flask, g, render_template, request

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main_better.html")

@app.route('/submit/', methods = ['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')



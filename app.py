from flask import Flask, g, render_template, request

import sqlite3
import string

from numpy import insert

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main_better.html")

@app.route('/submit/', methods = ['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try: 
            insert_message(request)
            return render_template('submit.html', thanks = True)
        except:
            return render_template('submit.html', error = True)

@app.route('/view/', methods = ['POST', 'GET'])
def view():
    results = random_message(5)
    try:
        return render_template('view.html', results = results)
    except:
        return render_template('view.html')
        

def get_message_db():
    if 'message_db' not in g:
        g.message_db = sqlite3.connect("messages_db.sqlite")
   
    cmd = \
    """
    CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    handle TEXT NOT NULL,
    message TEXT NOT NULL
    );
    """
    c = g.message_db.cursor()
    c.execute(cmd)

    return g.message_db

def insert_message(request):
    message = request.form['message']
    handle = request.form['handle']
    db = get_message_db()
    c = db.cursor()
    current_row_number = (c.execute("SELECT COUNT(*) FROM messages")).fetchone()[0]
    current_row_number += 1
    c.execute(f"INSERT INTO messages VALUES ({current_row_number},'{handle}','{message}')")
    db.commit()
    db.close()

def random_message(n):
    db = get_message_db()
    c = db.cursor()
    c.execute(f"SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT {n}")
    results = c.fetchall()
    return results

from flask import Flask, g, render_template, request

import sqlite3
import string

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")

# tell what URL should trigger our function
@app.route('/submit/', methods = ['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try: 
            # insert the entry
            insert_message(request)

            # output the thankyou note
            return render_template('submit.html', thanks = True)
        except:

            # output the error message
            return render_template('submit.html', error = True)

# tell what URL should trigger our function
@app.route('/view/', methods = ['POST', 'GET'])
def view():
    # generate 5 random messages
    results = random_message(5)
    try:
        # pass the message to the template
        return render_template('view.html', results = results)
    except:
        return render_template('view.html')
        

def get_message_db():
    # create a database if does not exist
    if 'message_db' not in g:
        g.message_db = sqlite3.connect("messages_db.sqlite")
   
    # cmd line to create the table
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

    # return the connection
    return g.message_db

def insert_message(request):
    # retrieve user input
    message = request.form['message']
    handle = request.form['handle']

    # create a connection and cursor
    db = get_message_db()
    c = db.cursor()

    # generate ID
    current_row_number = (c.execute("SELECT COUNT(*) FROM messages")).fetchone()[0]
    current_row_number += 1

    # insert entry into the database
    c.execute(f"INSERT INTO messages VALUES ({current_row_number},'{handle}','{message}')")

    # save the insertion
    db.commit()

    # close the connection
    db.close()

def random_message(n):
    # get the connection and cursor
    db = get_message_db()
    c = db.cursor()

    # generate n random rows from the table
    c.execute(f"SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT {n}")
    results = c.fetchall()

    # close the connection
    db.close()
    return results

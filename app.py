from flask import Flask, session, request, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
# set app secret key to encrypt session key - value
app.secret_key = 'secret'

# flask_uuid wrapper

# local db connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)



# Create a database if not exist
db.create_all()

# Main Dashboard
@app.route("/")
def main():
    user_id = session.get('user_id')

    if user_id:
        return render_template('index.html')
    else:
        return redirect(url_for('login'), code=302)

# User enters his/her name and create a session from him
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        # Later, we will store the data into databse
        session['user_id'] = uuid.uuid4()
        session['name'] = username
        return redirect(url_for('main'))
    else:
        return render_template('login.html')

# User creates a wordset
@app.route("/create-wordset")
def create_wordset():
    return 'create-wordset'

if __name__ == "main":
    app.run(debug=True)
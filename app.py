import enum
from flask import Flask, session, request, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import uuid

# *Should think about the way to check if a user has a session and the user id in the session exists
# in the database, and if not, redirect him to '/login' like using a middleware*

app = Flask(__name__)
# set app secret key to encrypt session key - value
app.secret_key = 'secret'

# local db connection
if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
else: 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://u563uq13927pv8:p3a1695dab31bf5214b4ef8a5d0b8bc1c35515278df177964bee0bc0969a18eb6@ceu9lmqblp8t3q.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d4nven4jtj5jc5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models

# User model
class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    wordsets = db.relationship('Wordset', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.name}, id: {self.id}>"

# Wordset model
class Wordset(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    word = db.relationship('Word', backref='word', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Wordset {self.name}, id: {self.id}>"

# Word model
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    wordset_id = db.Column(db.String(100), db.ForeignKey('wordset.id'), nullable=False)

    def __repr__(self):
        return f"<Word {self.name}, id: {self.id}"

# Create a database if not exist
db.create_all()

# Main Dashboard
@app.route("/")
def main():
    user_id = session.get('user_id')

    if user_id:
        wordsets = Wordset.query.filter_by(user_id=user_id).all()
        return render_template('dashboard.html', wordsets=wordsets)
    else:
        return redirect(url_for('login'), code=302)

# User enters his/her name and create a session from him
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user_id = str(uuid.uuid4()) # Default type of uuid.uuid4() is a class so need to convert it to a string

        try: 
             # Create a user in the database
            new_user = User(id=user_id, name=username)
            db.session.add(new_user)
            db.session.commit()

            # When a user is successfully added to the database, create a session
            session['user_id'] = new_user.id
            session['name'] = new_user.name
            return redirect('/')
        except:
            return "Error: unable to create a user"        
    else:
        if session.get('user_id'):
            return redirect(url_for('main'), code=302)
        else:
            return render_template('login.html')

# When user logs out, delete a session data
@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    # Query a user associated with the user_id in the session
    try:
        user_to_delete = User.query.get_or_404(user_id)
    except:
        return f"Error: No user with id: {user_id}"

    # Delete the user with the user_id
    try:
        db.session.delete(user_to_delete)
        db.session.commit()

        # pop the user from the session
        session.pop("user_id", None)
        session.pop("name", None)   
        return redirect(url_for('main'))
    except:
        return "Error: Deleting a user"

# User creates a wordset
@app.route("/create_wordset", methods=['POST', 'GET'])
def create_wordset():
    if request.method == 'POST':
        # create a wordset
        wordset_id = uuid.uuid4()
        wordset_name = request.form['wordset_name']
        new_wordset = Wordset(id=str(wordset_id),user_id=str(session['user_id']),name=wordset_name)
        
        try: 
            db.session.add(new_wordset)
            db.session.commit()

        except:
            return "Error: adding wordset" 

        # receives form data
        words = request.form.getlist('word')
        descriptions = request.form.getlist('description')

        # create a word associtated with the created wordset
        for index, word in enumerate(words):
            new_word = Word(name=word, description=descriptions[index], wordset_id=new_wordset.id)

            try:
                db.session.add(new_word)
                db.session.commit()
            except:
                return "Error: failed to add word"
        return redirect(url_for('main'), code=302)
    else:       
        return render_template('create_wordset.html')

@app.route("/study/<id>")
def study(id):
    wordset = Wordset.query.filter_by(id=id).first()
    words = Word.query.with_parent(wordset).all()

    return render_template('study.html', wordset=wordset, words=words)

@app.route("/test/<id>")
def test(id):
    wordset = Wordset.query.filter_by(id=id).first()
    words = Word.query.with_parent(wordset).all()

    return render_template('test.html', wordset=wordset, words=words)

############################### this is where you should pick it up from ##############################

# Delete a wordset with id
@app.route("/delete_wordset/<id>", methods=['POST', 'GET'])
def delete(id):
    if request.method == 'POST':
        print("Received")
        try:
            wordset_to_delete = Wordset.query.get_or_404(id)
        except:
            return "Error: No user with id: %r" % id
        try:
            db.session.delete(wordset_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return "Error: deleteing wordset"
    else:
        return redirect(url_for('main'))

# Wordset helper functions
# get the first wordset in the database and can see the words associated with the set
@app.route("/wordset")
def wordset():
    wordset = Wordset.query.filter_by(user_id=session.get('user_id')).first()
    words = Word.query.filter_by(wordset_id=wordset.id).all()
    return render_template('wordsets.html', wordset=wordset, words=words)

# Test Result Page Route
@app.route("/result")
def result():
    return render_template('result.html')

if __name__ == "__main__":
    app.run(debug=True)

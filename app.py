from flask import Flask, session, request, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
# set app secret key to encrypt session key - value
app.secret_key = 'secret'

# flask_uuid wrapper

# local db connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



# Create a database if not exist
db.create_all()

# Models

# User model
class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    wordsets = db.relationship('Wordset', backref='user', lazy=True, cascade="all, delete, delete-orphan")

    def __repr__(self):
        return '<User(%r) %r>' % (self.name, self.id)

# Wordset model
class Wordset(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Wordset(%r) %r>' % (self.name, self.id)

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

        # Create uuid and save uuid and username in session
        session['user_id'] = uuid.uuid4()
        session['name'] = username
        
        return redirect('/create_user/'+ str(session['user_id']) + '/' + username)          
    else:
        return render_template('login.html')

# User creates a wordset
@app.route("/create_wordset", methods=['POST', 'GET'])
def create_wordset():
    wordset_id = uuid.uuid4()
    wordset_name = request.form['wordset_name']
    new_wordset = Wordset(id=str(wordset_id),user_id=str(session['user_id']),name=wordset_name)
    
    try: 
        db.session.add(new_wordset)
        db.session.commit()
        return redirect('/')
    except:
        return "Error: adding wordset"

# Delete a wordset with id
@app.route("/delete_wordset/<id>")
def delete(id):
    try:
        wordset_to_delete = Wordset.query.get_or_404(id)
    except:
        return "Error: No user with id: %r" % id
    try:
        db.session.delete(wordset_to_delete)
        db.session.commit()
        return redirect('/wordset')
    except:
        return "Error: deleteing wordset"

# When user logs out, delete a session data
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    id = session.pop("user_id", None)
    session.pop("name", None)
    return redirect("/delete_user/" + str(id))


# User helper functions
# Add a user
@app.route("/create_user/<id>/<name>")
def create_user(id, name):
    new_user = User(id=id, name=name)
    try: 
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    except:
        return "Error: creating user with id(%r), name(%r)", (id,name)

# delete user
@app.route("/delete_user/<id>")
def delete_user(id):
    try:
        user_to_delete = User.query.get_or_404(id)
    except:
        return "Error: No user with id: %r" % id
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for('main'))
    except:
        return "Error: Deleting a user"

# get users
@app.route("/user")
def user():
    users = User.query.all()
    return render_template('users.html', users=users)

# Wordset helper functions
# get Wordset
@app.route("/wordset")
def wordset():
    wordsets = Wordset.query.all()
    return render_template('wordsets.html', wordsets=wordsets)


if __name__ == "__main__":
    app.run(debug=True)
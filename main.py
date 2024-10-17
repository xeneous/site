from flask import Flask, Blueprint, request, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_bcrypt import bcrypt
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

from waitress import serve

app = Flask(__name__, template_folder='templates')
app.secret_key = "Cr0m0s0mat1c0"

vPort = 5000
#Configure SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), unique=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash( self.password_hash, password )

#ROutes
#root
@app.route('/')
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    
    return render_template('index.html')

#login
@app.route('/login', methods=["POST"])
def login():
    #collect info from the from
    postUsername=request.form['username']
    postPassword=request.form['password']
    user = User.query.filter_by(username=postUsername).first()

    if user and user.chech_password(postPassword):
        session['username'] = postUsername
        return redirect(url_for,'Dashboard')
    else:
        return render_template("index.html")
    
    #Check if user exists

    #if not return to home page

#Register
@app.route('/register', methods=["POST"])
def register():
    #collect info from the from
    postUsername=request.form['username']
    postPassword=request.form['password']
    user = User.query.filter_by(username=postUsername).first()

    if user:
        return render_template("index.html",error = "User already exists.")
    else:
        new_User = User(username=postUsername)
        new_User.set_password(postPassword)
        db.session.add(new_User)
        db.session.commit()
        session['username'] = postUsername
        return redirect(url_for,'Dashboard')
    
#Dashboard

#logout

mode = 'dev'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    if mode == 'dev':
        app.run(host='0.0.0.0', port=vPort, debug=True )
    else:
        serve(app,port=vPort, threads=2, url_prefix="/sao" )


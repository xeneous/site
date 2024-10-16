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

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model


#ROutes
@app.route('/')
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    
    return render_template('index.html')

mode = 'dev'

if __name__ == '__main__':
    with app.app_context():
        db.create_all

    if mode == 'dev':
        app.run(host='0.0.0.0', port=vPort, debug=True )
    else:
        serve(app,port=vPort, threads=2, url_prefix="/sao" )


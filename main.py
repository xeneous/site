from flask import Flask, Blueprint, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_bcrypt import bcrypt
from flask_migrate import Migrate

from waitress import serve

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./testdb'

    db.init_app(app)

    from routes import register_routes
    register_routes(app, db)

    migrate = Migrate(app, db)

    return app

app = Flask(__name__)
vPort = 5000

@app.route('/')
def index():
    return render_template('index.html')

mode = 'prod'

if __name__ == '__main__':
    if mode == 'dev':
        app.run(host='0.0.0.0', port=vPort, debug=True )
    else:
        serve(app,port=vPort, threads=2, url_prefix="/sao" )

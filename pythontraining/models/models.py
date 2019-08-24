from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ..config import application as ap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ap.database_name
# To supress the sqlalchemy warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(10), unique=False, nullable=False)

    def __repr__(self):
        return '<User %d, %r, %r, %r>' % (self.id, self.username, self.email, self.phone)

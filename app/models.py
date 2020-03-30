from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    about_me = db.Column(db.String(140))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f"<USER {self.username}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_key = db.Column(db.String(50), index=True, unique=True)
    edition = db.Column(db.String(25))
    email = db.Column(db.String(120), unique=True)
    order_number = db.Column(db.String(25), unique=True)
    country = db.Column(db.String(25))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    current_ip = db.Column(db.String(25))
    all_ips = db.Column(db.String())

    def __repr__(self):
        return f"<LICENSE {self.license_key}>"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(140))
    summary = db.Column(db.String(750))
    change_type = db.Column(db.String(25))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<POST {self.title}>"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
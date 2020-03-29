from datetime import datetime

from app import db


class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_key = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(120), unique=True)
    order_number = db.Column(db.String(25), unique=True)
    country = db.Column(db.String(25))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<LICENSE {self.license_key}>"

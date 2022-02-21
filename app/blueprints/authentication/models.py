from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import string, random

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    token = db.Column(db.String(255), default=''.join(random.choice(string.ascii_letters) for i in range (25)))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    character = db.relationship('Character', backref='user', lazy='dynamic')
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generate_password(self.password)
        # self.password = generate_password_hash(self.password)

    def check_password(self, password_to_check):
        return check_password_hash(self.password, password_to_check)

    def generate_password(self, password_create_salt_from):
        self.password = generate_password_hash(password_create_salt_from)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
        return data    

    def __repr__(self):
        return f'<User: {self.email}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
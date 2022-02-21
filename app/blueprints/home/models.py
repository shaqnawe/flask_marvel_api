from app import db
from datetime import datetime

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text(1024))
    comics_appeared_in = db.Column(db.Integer)
    super_power = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer)


    def to_dict(self):
        from app.blueprints.authentication.models import User
        data = {
            'id': self.id,
            'name' : self.name,
            'description': self.description,
            'comics_appeared_in' : self.comics_appeared_in,
            'super_power' : self.super_power,
            'date_created': self.date_created,
            'image': self.image,
            'user_id': User.query.get(self.user_id).to_dict()
        }
        return data


    def __repr__(self):
        return f'<Character: {self.name}, Owner: {self.user_id}>'
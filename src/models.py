from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    population=db.Column(db.Integer)
    weather=db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "weather": self.weather,
        }
    
class Character(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    age=db.Column(db.Integer)
    star_sign =db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "star_sign": self.star_sign,
        }

class Favourites(db.Model):

    id=db.Column(db.Integer, primary_key=True)

    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    user=db.relationship(User)

    character_id=db.Column(db.Integer, db.ForeignKey('character.id'))
    character=db.relationship(Character)

    planet_id=db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet=db.relationship(Planet)    

    def __repr__(self):
        return '<Favourites %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
        }

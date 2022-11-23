from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), unique=False, nullable=False)
    last_name = db.Column(db.String(200), unique=False, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(10), unique=False, nullable=False)

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    rotation_period = db.Column(db.Integer, unique=False, nullable=True)
    orbital_period = db.Column(db.Integer, unique=False, nullable=True)
    diameter = db.Column(db.Integer, unique=False, nullable=True)
    climate = db.Column(db.String, unique=False, nullable=True)
    gravity = db.Column(db.Integer, unique=False, nullable=True)
    terrain = db.Column(db.String, unique=False, nullable=True)
    surface_water = db.Column(db.Integer, unique=False, nullable=True)
    population = db.Column(db.Integer, unique=False, nullable=True)

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    birth_year = db.Column(db.String(200), unique=False, nullable=True)
    height = db.Column(db.Integer, unique=False, nullable=True)
    mass = db.Column(db.Integer, unique=False, nullable=True)
    hair_color = db.Column(db.String(200), unique=False, nullable=True)
    skin_color = db.Column(db.String(200), unique=False, nullable=True)
    eye_color = db.Column(db.String(200), unique=False, nullable=True)
    gender = db.Column(db.String(200), unique=False, nullable=True)

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, ForeignKey('user.id'))
    id_planet = db.Column(db.Integer, ForeignKey('planet.id'))
    id_people = db.Column(db.Integer, ForeignKey('people.id'))
    

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
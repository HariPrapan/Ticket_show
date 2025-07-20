from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Show(db.Model):
    show_id=db.Column(db.Integer,primary_key=True)
    show_name=db.Column(db.String,nullable=False)
    Rating=db.Column(db.Integer,nullable=False)
    Tags=db.Column(db.String,nullable=False)
    Price=db.Column(db.Integer,nullable=False)
    shift=db.Column(db.String,nullable=False)
    image_url=db.Column(db.String)
    venue=db.relationship("Venue",secondary="joint",back_populates="show")

class Venue(db.Model):
    venue_id=db.Column(db.Integer,primary_key=True)
    venue_name=db.Column(db.String,nullable=False)
    venue_loc=db.Column(db.String,nullable=False)
    capacity=db.Column(db.Integer,nullable=False)
    show=db.relationship("Show",secondary="joint",back_populates="venue")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.show_id'), nullable=False)
    show_name=db.Column(db.String,nullable=False)
    venue=db.Column(db.String,nullable=False)
    tickets = db.Column(db.Integer)

class Joint(db.Model):
    show_id=db.Column(db.Integer,db.ForeignKey("show.show_id"),primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.venue_id"), primary_key=True)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Rate(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String,nullable=False)
    show_id=db.Column(db.Integer,nullable=False)
    Rating=db.Column(db.Integer,nullable=False)



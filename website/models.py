#database model for uers and notes

from . import db

from flask_login import UserMixin
from sqlalchemy.sql import func

#all notes have to conform to this format, telling the database to look like this, so all information is consistent


class Note(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    #associating the note with the user

    #one user can have many relationships

    #one to many relationship (every time we have a note, we can have the user id)

    #reference the user's
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    #inherits
    #define a schema for object storing in database
    #object in databse = key = uniquely identifying the object
    id = db.Column(db.Integer, primary_key = True)
    #invalid to create a user whose email already exists in the database
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    #Every time we create a note, add the note
    notes = db.relationship('Note')






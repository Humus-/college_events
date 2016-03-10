from datetime import datetime
from flask import Flask
from config import db

admins = db.Table('admins',
    db.Column('eventid', db.Integer, db.ForeignKey('lobby.id'), primary_key = True ),
    db.Column('adminid', db.Integer, db.ForeignKey('users.id'), primary_key = True ),
#    db.Column('phno_visible',db.Boolean) 
    )

attends = db.Table('attends',
    db.Column('userid', db.Integer, db.ForeignKey('users.id'), primary_key = True ),
    db.Column('eventid', db.Integer, db.ForeignKey('lobby.id'), primary_key = True )
    )

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True,nullable=False)
    password = db.Column(db.String(256), nullable=False)
#    phno = db.Column(db.phone_number)
    authenticated = db.Column(db.Boolean, default=False)
    about_me = db.Column(db.Text())
    
    attends = db.relationship('Activity',secondary=attends,
        backref = db.backref('users',lazy = 'dynamic') )
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.authenticated = True

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
                
class Activity(db.Model):
    __tablename__ = "lobby"
    id = db.Column( db.Integer, primary_key=True)
    name = db.Column( db.String(20), unique=True, nullable=False)
    description = db.Column( db.Text(160) )
    type = db.Column(db.Enum(
                        'Game',
                        'Quiz',
                        'Exhibition',
                        'Concert',
                        name='Event_tags')
                   ,default=None)
    max_entries = db.Column( db.Integer )
    attending = db.Column( db.Integer )
    date = db.Column(db.DateTime)
    #the curr slot_no of the event as it can span over multiple timeslots/days 
    part = db.Column(db.SmallInteger, default = 1)
    #stores the id of the first part of the event lobby
    part_id = db.Column(db.Integer, default=id)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    
    admins = db.relationship('User',secondary=admins,
        backref = db.backref('lobby', lazy = 'dynamic') )
    
    attends = db.relationship('User',secondary=attends,
        backref = db.backref('lobby',lazy = 'dynamic') )
    
    def __init__(self,name,description,date,partno=None,part_id=None):
        """
    Initializes 
    *name- of the event
    *description- describes the details of the event
    *date- when the event is happening
    *attending- number of users attending the event.Atlest one user must attend for the lobby to exist (creator or admin can be included),therefore attending =1
    
    If a new slot of the event is being created then the function expects 2 more arguments
    *partno-the next slot number of the event
    *part_id - the event id of the first slot (this groups together all the different parts of the same event),in case there is only 1 part then the part_id is same as its event id
        """
        self.name = name
        self.description = description
        self.date = date
        self.attending=1
        if partno:
            if not part_id:
                raise Exception("part_id argument expected")
            self.part=partno
            self.part_id=partid
        elif part_id:
            raise Exception("part argument expected")
    
    def is_active(self):
        """True if event date is not yet over"""
        if(self.date < datetime.now() ):
            return False;
        return True;
    
    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return self.id
        
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.column( db.Text )
    start_date = db.Column( db.DateTime )
    end_date = db.Column( db.DateTime )
    
    activities = db.relationship('Activity', backref = 
            db.backref('event',lazy = 'dynamic') )
            


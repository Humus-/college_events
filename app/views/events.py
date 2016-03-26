from flask import Blueprint, render_template, redirect, url_for
from ..config import db
from ..models import User,Activity,Event,admins,attends
from flask.ext.login import current_user, login_required
from forms import LobbyCreateForm

events = Blueprint('events', __name__)

@events.route('/events')
def loadevents():
    events = Events.query.all()
    return render_temlate('event/view_events.html',events=events)
       
@events.route('/createlobby', methods=["GET", "POST"])
@login_required
def createlobby():
    """For GET requests, display the create lobby form. For POSTS, create the lobby
        by processing the form."""
    form = LobbyCreateForm()
    if form.validate_on_submit():
        lobby = Activity.query.filter_by(name = form.name.data).all()
        if not lobby:
            lobby = Activity(form.name.data,
                form.description.data,
                form.date.data)
            if form.max_entries.data: 
                lobby.max_entries=form.max_entries.data #create a setter function
                
            print "Inserting into lobby"
            
            lobby.admins.append(current_user)
            
            db.session.add(lobby)
            db.session.commit()
            
            lobbies = Activity.query.all()
            return redirect(url_for("events.lobby_details",id=lobby.get_id() ) )
        else:
            return "Lobby already exists"
    
    return render_template('event/create_lobby.html', form=form)
    
@events.route('/lobby/<id>')
def lobby_details(id):
    lobby = Activity.query.filter_by(id = id).first()
    current_user_id = current_user.get_id()
    if not lobby :
        return "Lobby does not Exist"
    print lobby.admins
    if current_user_id in lobby.admins:
        return render_template('event/lobby_details.html',lobby=lobby,admin=True)
    return render_template('event/lobby_details.html',lobby=lobby,admin=False)
    
#@events.route('/editlobby/<id>')
#def edit_lobby(id):
#    form=EditLobbyForm()

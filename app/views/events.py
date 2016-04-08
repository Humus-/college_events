from flask import Blueprint, render_template, redirect, url_for
from ..config import db
from ..models import User,Activity,Event,admins,attends
from flask.ext.login import current_user, login_required
from forms import LobbyCreateForm,EditLobbyForm

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
            lobby.type = form.lobby_type.data
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
    #debug info,will remove in next push
    print "asdf"
    print lobby.admins[0].username
    print "qwer"
    
    admin=False
    if current_user in lobby.admins:
        admin=True
    return render_template('event/lobby_details.html',lobby=lobby,admin=admin)
    
@events.route('/expandlobby/<id>', methods=["GET", "POST"])
@login_required
def expandlobby(id):
    """
    Checks if the lobby exists,
    if it exists ,checkif the user is allowed to change the loby details.
    For GET requests, display the create lobby form. For POSTS, create the lobby
    by processing the form."""
    lobby_last_part = Activity.query.filter_by(part_id = id).order_by(Activity.part_id).first()
    if lobby_last_part ==None:
        return "Lobby does not exist"
    if not current_user in lobby_last_part.admins:
        return "Sorry u need to be admin to edit this lobby :("
    return "haha"
    parent_lobby = Activity.query.filter_by(id=lobby_last_part.part_id).first()
    form = LobbyCreateForm()
    #dont allow changing of name
    form.name = parent_lobby.name
    form.description = lobby_last_part.description
#    form.lobby_type
    if form.validate_on_submit():
        lobby = Activity(
            parent_lobby.name+'@'+str(lobby_last_part.part+1),#name of new lobby part = name@partno
            form.description.data,
            form.description.date,
            partno=lobby_last_part.part,
            part_id=parent_lobby.id)
        if form.max_entries.data: 
            lobby.max_entries=form.max_entries.data #create a setter function
        lobby.type = form.lobby_type.data
            
        print "Inserting into lobby"
            
        lobby.admins.append(current_user)
        
        db.session.add(lobby)
        db.session.commit()
        
        return redirect(url_for("events.lobby_details",id=lobby.get_id() ) )
    
    return render_template('event/create_lobby.html', form=form)
    

@events.route('/editlobby/<id>')
@login_required
def edit_lobby(id):
    form=EditLobbyForm(id)
    lobby = Activity.query.filter_by(id=id).first()
    if lobby == None:
        return "Lobby doesn't exist "
    if not current_user in lobby.admins:
        return "Sorry u need to be admin to edit this lobby :("
    if form.validate_on_submit():
        if form.new_part:
            return "Stuff"
        elif 5==3:
            url_for("events.createlobby",part=1)
    return render_template('event/edit_lobby.html',form=form)


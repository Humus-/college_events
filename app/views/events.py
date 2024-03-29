from flask import Blueprint, render_template, redirect, url_for, jsonify, send_from_directory
from ..config import db
from ..models import User,Activity,Event,admins,attends
from flask.ext.login import current_user, login_required
from forms import LobbyCreateForm,EditLobbyForm
import os

static_folder = os.path.join(os.pardir, 'static')
events = Blueprint('events', __name__, static_folder=static_folder, static_url_path='/static')

@events.route('/events')
def loadevents():
    return render_template('event/view_events.html')

@events.route('/getevents')
def get_events():
    return jsonify(events=[event.serialize() for event in Event.query.all()])

"""
@events.route('/image/<path:path>')
def send_image(path):
        return send_from_directory('static/images', path)
"""

# Fake route to test
# FIXME: User send_image instead
@events.route('/abc')
def root():
        # return "<html>yes</html>"
        return events.send_static_file('images/dota2.jpg')

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
            #id is created only after commit
            db.session.commit()
            #changing part id to lobby id
            lobby.part_id = lobby.id
            db.session.commit()
            
            lobbies = Activity.query.all()
            return redirect(url_for("events.lobby_details",id=lobby.get_id() ) )
        else:
            return "Lobby already exists"
    
    return render_template('event/create_lobby.html', form=form)
    
@events.route('/lobby/<id>')
def lobby_details(id):
    lobby = Activity.query.filter_by(id = id).first()
    if not lobby :
        return "Lobby does not Exist"
    
    admin=False
    if current_user in lobby.admins:
        admin=True
    return render_template('event/lobby_details.html',lobby=lobby,admin=admin)
    
@events.route('/expandlobby/<id>', methods=["GET", "POST"])
@login_required
def expand_lobby(id):
    """
    Checks if the lobby exists,
    if it exists ,checkif the user is allowed to change the loby details.
    For GET requests, display the create lobby form. For POSTS, create the lobby
    by processing the form."""
    lobby_last_part = Activity.query.filter_by(part_id = id).order_by(Activity.part.desc()).first_or_404()
    if lobby_last_part ==None:
        return "Lobby does not exist"
    if not current_user in lobby_last_part.admins:
        return "Sorry u need to be admin to edit this lobby :("
    parent_lobby = Activity.query.filter_by(id=lobby_last_part.part_id).first()
    form = LobbyCreateForm()
    #dont allow changing of name
    form.name.data = parent_lobby.name + '_new_part'
    form.description.data = lobby_last_part.description
#    form.lobby_type
    if form.validate_on_submit():
        lobby = Activity(
            parent_lobby.name+'@'+str(lobby_last_part.part+1),#name of new lobby part = name@partno
            form.description.data,
            form.date.data,
            partno=lobby_last_part.part+1,
            part_id=parent_lobby.id)
        if form.max_entries.data: 
            lobby.max_entries = form.max_entries.data #create a setter function
        lobby.type = form.lobby_type.data
            
        print "Inserting into lobby"
            
        lobby.admins.append(current_user)
        
        db.session.add(lobby)
        db.session.commit()
        
        return redirect(url_for("events.lobby_details",id=lobby.get_id() ) )
    
    return render_template('event/create_lobby.html', form=form)
    

@events.route('/editlobby/<id>', methods=["GET", "POST"])
@login_required
def edit_lobby(id):
    lobby = Activity.query.filter_by(id=id).first()
    if lobby == None:
        return "Lobby doesn't exist "
    if not current_user in lobby.admins:
        return "Sorry u need to be admin to edit this lobby :("
    
    form=EditLobbyForm(id)
    
    if form.validate_on_submit():
        if form.new_part.data:
            return redirect(url_for("events.expand_lobby",id=lobby.part_id ) )
        elif form.Add_admin_button.data and not form.Add_admin.data == None:
            user = User.query.filter_by(username = form.Add_admin.data).first()
            if user != None:
                lobby.admins.append(user)
                db.session.commit()
        else:
            lobby.name = form.name.data
            lobby.description = form.description.data
            lobby.max_entries = form.max_entries.data
            lobby.date = form.date.data
            lobby.type = form.lobby_type.data
            db.session.commit()
    return render_template('event/edit_lobby.html',form=form,lobby=lobby)


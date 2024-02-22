from re import A
from flask import Blueprint
from flask import request, render_template, flash, redirect, url_for, session

import music.adapters.repository as repo
import music.playlists.services as services

from music.authentication.authentication import login_required


playlists_blueprint = Blueprint(
    'playlists_bp', __name__)


@playlists_blueprint.route('/playlist/<string:user_name>')
@login_required
def view_playlist(user_name):
    user = services.get_user(user_name, repo.repo_instance)
    if user != None:
        playlist = services.get_users_playlist(user_name, repo.repo_instance)
        favourite = services.get_users_favourite(user_name, repo.repo_instance)

        if not playlist:
            flash('No songs in playlist')
            return render_template('home.html')
        return render_template('playlist.html', playlist=playlist, favourite = favourite, user=user)
    else:
        return redirect(url_for('authentication_bp.login'))


@playlists_blueprint.route('/playlist/add/<int:track_id>')
@login_required
def add_to_playlist(track_id):
    user_name = session['user_name']
    user = services.get_user(user_name, repo.repo_instance)
    track = services.get_track(track_id, repo.repo_instance)
    if user != None:

        if services.add_to_playlist(track, user, repo.repo_instance):
            flash('Successfully added to playlist')
            return redirect(request.referrer)
        else:
            flash('Song already in playlist')
            return redirect(request.referrer)
    else:
        return redirect(url_for('authentication_bp.login'))

# -- When add to playlist is called from friends playlist, return to friends playlist pgae
@playlists_blueprint.route('/playlist/add/<friend_name>/<int:track_id>')
@login_required
def add_to_playlist_from_friend(track_id, friend_name):  
    user_name = session['user_name']
    user = services.get_user(user_name, repo.repo_instance)
    track = services.get_track(track_id, repo.repo_instance)

    friend = services.get_user(friend_name, repo.repo_instance)

    if services.add_to_playlist(track, user, repo.repo_instance):
        flash('Successfully added to playlist')
        return render_template('user.html', user=friend)
    else:
        flash('Song already in playlist')
        return render_template('user.html', user=friend)

@playlists_blueprint.route('/playlist/remove/<int:track_id>')
@login_required
def remove_from_playlist(track_id):
    user_name = session['user_name']
    user = services.get_user(user_name, repo.repo_instance)
    track = services.get_track(track_id, repo.repo_instance)

    services.remove_from_playlist(track, user, repo.repo_instance)
    services.remove_from_favourite(track, user, repo.repo_instance)
    flash('Successfully removed from playlist')
    return redirect(url_for("playlists_bp.view_playlist", user_name=user_name))


@playlists_blueprint.route('/playlist/add_favourite/<int:track_id>')
@login_required
def add_to_favourite(track_id):
    user_name = session['user_name']
    user = services.get_user(user_name, repo.repo_instance)
    track = services.get_track(track_id, repo.repo_instance)
    if user != None:

        services.add_to_favourite(track, user, repo.repo_instance)
        return redirect(request.referrer)
    else:
        return redirect(url_for('authentication_bp.login'))


@playlists_blueprint.route('/playlist/remove_favourite/<int:track_id>/<int:view>')
@login_required
def remove_from_favourite(track_id, view):
    user_name = session['user_name']
    user = services.get_user(user_name, repo.repo_instance)
    track = services.get_track(track_id, repo.repo_instance)


    services.remove_from_favourite(track, user, repo.repo_instance)

    # the following code refresh and redirect user to the same page
    if view == 1:      #if user click from playlist url view = 1
        return redirect(url_for("playlists_bp.view_favourite", user_name=user_name))
    else:
        return redirect(url_for("playlists_bp.view_playlist", user_name=user_name))



@playlists_blueprint.route('/favourite/<string:user_name>')
@login_required
def view_favourite(user_name):
    user = services.get_user(user_name, repo.repo_instance)
    if user != None:
        playlist = services.get_users_playlist(user_name, repo.repo_instance)
        favourite = services.get_users_favourite(user_name, repo.repo_instance)

        if len(favourite) == 0:
            flash('No songs in favourites')
            return render_template('home.html')
        return render_template('favourite.html', playlist=playlist, favourite = favourite)
    else:
        return redirect(url_for('authentication_bp.login'))


from flask import Blueprint
from flask import request, render_template, flash, url_for, session
from werkzeug.utils import redirect

import music.adapters.repository as repo
import music.tracks.services as services

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import datetime


tracks_blueprint = Blueprint(
    'tracks_bp', __name__)

@tracks_blueprint.route('/all_tracks', methods=['GET'])
def tracks_list():
    tracks_per_page = 20
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    first_track_url = None
    last_track_url = None
    next_track_url = None
    prev_track_url = None

    track_ids = services.get_all_tracks(repo.repo_instance)

    if cursor > 0:
        prev_track_url = url_for('tracks_bp.tracks_list', cursor=cursor - tracks_per_page)
        first_track_url = url_for('tracks_bp.tracks_list')
    if cursor + tracks_per_page < len(track_ids):
        next_track_url = url_for('tracks_bp.tracks_list', cursor=cursor + tracks_per_page)

        last_cursor = tracks_per_page * int(len(track_ids) / tracks_per_page)
        if len(track_ids) % tracks_per_page == 0:
            last_cursor -= tracks_per_page
        last_track_url = url_for('tracks_bp.tracks_list', cursor=last_cursor)

    #all_tracks = services.get_all_tracks(repo.repo_instance)
    tracks = track_ids[cursor:cursor + tracks_per_page]


    return render_template('tracks_list.html',
                           tracks = tracks,
                           first_track_url=first_track_url,
                            last_track_url = last_track_url,
                            next_track_url = next_track_url,
                            prev_track_url = prev_track_url
                           )


@tracks_blueprint.route('/track/<int:track_id>')
def view_track(track_id):
    current_user = None
    track = services.get_track(track_id, repo.repo_instance)
    track_to_show_reviews = request.args.get('view_comments_for')


    all_reviews = services.get_all_reviews(repo.repo_instance)
    track_review = []
    user_review = {}
    for review in all_reviews:
        if review.track.track_id == track_id:
            track_review.append(review)
    all_users = services.get_all_users(repo.repo_instance)

    for user in all_users:
        for review in track_review:
            if review in user.reviews:
                user_review[track_id] = user.user_name

    if 'user_name' in session:
        user_name = session['user_name']
        current_user = services.get_user(user_name, repo.repo_instance)
    if track is not None:
        # -- convert track_duration from seconds into hrs:min:sec format
        duration = datetime.timedelta(seconds=track.track_duration)
        
        return render_template('view_track.html',
                                    current_user = current_user,
                                    track = track,
                                    track_id = track.track_id,
                                    title=track.title, 
                                    artist=(track.artist).full_name, 
                                    track_duration=duration, 
                                    genres=track.genres, 
                                    album=(track.album).title, 
                                    url=track.track_url,
                                    all_reviews = track_review,
                                    user_review = user_review
                                    )


@tracks_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    interests = []

    if 'user_name' in session:
        user_name = session['user_name']
        user = services.get_user(user_name, repo.repo_instance)

        if user != None:
            interests = services.get_user_interests(user, repo.repo_instance)


    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for('tracks_bp.search_result', key = form.search.data, chose = form.select.data))
    return render_template('search.html', form=form, handler_url=url_for('tracks_bp.search'), interests = interests)

@tracks_blueprint.route('/search_result', methods=['GET'])
def search_result():
    key = request.args.get('key')
    chose = request.args.get('chose')
    cursor = request.args.get('cursor')
    results = []

    if chose == 'Artist':
        results = services.get_tracks_by_artist(key, repo.repo_instance)
    elif chose == 'Album':
        results = services.get_tracks_by_album(key, repo.repo_instance)
    else:
        results = services.get_tracks_by_genre(key, repo.repo_instance)

    if len(results) == 0:
        flash('No results found')
        #flash(key)
        # return render_template('tracks_list.html', tracks=services.get_all_tracks(repo.repo_instance))
        return redirect(url_for('tracks_bp.search'))
    else:
        tracks_per_page = 20
        cursor = request.args.get('cursor')

        if cursor is None:
            cursor = 0
        else:
            cursor = int(cursor)

        first_track_url = None
        last_track_url = None
        next_track_url = None
        prev_track_url = None

        track_ids = results

        if cursor > 0:
            prev_track_url = url_for('tracks_bp.search_result', cursor=cursor - tracks_per_page, key = key, chose = chose)
            first_track_url = url_for('tracks_bp.search_result', key = key, chose = chose)
        if cursor + tracks_per_page < len(track_ids):
            next_track_url = url_for('tracks_bp.search_result', cursor=cursor + tracks_per_page, key = key, chose = chose)

            last_cursor = tracks_per_page * int(len(track_ids) / tracks_per_page)
            if len(track_ids) % tracks_per_page == 0:
                last_cursor -= tracks_per_page
            last_track_url = url_for('tracks_bp.search_result', cursor=last_cursor, key = key, chose = chose)

        tracks = track_ids[cursor:cursor + tracks_per_page]

        return render_template('tracks_list.html',
                               tracks=tracks,
                               first_track_url=first_track_url,
                               last_track_url=last_track_url,
                               next_track_url=next_track_url,
                               prev_track_url=prev_track_url)


class SearchForm(FlaskForm):
    select = SelectField('Search by: ', choices=[('Artist', 'Artist'), ('Album', 'Album'), ('Genre', 'Genre')])
    search = StringField('search', [DataRequired('Search key must not be empty')])
    submit = SubmitField('Search')


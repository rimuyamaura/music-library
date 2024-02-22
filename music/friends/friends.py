from flask import Blueprint
from flask import request, render_template, flash, redirect, url_for, session

import music.adapters.repository as repo
import music.friends.services as services

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError


friends_blueprint = Blueprint(
    'friends_bp', __name__)


@friends_blueprint.route('/search_user', methods=['GET', 'POST'])
def search_user():
    form = UserForm()

    if form.validate_on_submit():
        results = []
        key = form.search.data

        if form.select.data == 'User name':
            results = services.get_user(key, repo.repo_instance)
        else:
            try:
                results = services.get_user_by_id(int(key), repo.repo_instance)
                if int(key) < 0:
                    flash('input user id contains invalid character')
            except:
                flash('user id contains plain numbers')


        if not results:
            flash('No results found')
        else:
            return render_template('user.html', user=results)
    return render_template('search.html', form=form, handler_url=url_for('friends_bp.search_user'))

@friends_blueprint.route('/search_user/like/<int:friend_id>')
def like(friend_id):
    try:
        user_name = session['user_name']
        print(user_name)
    except:
        return redirect(url_for('authentication_bp.login'))

    friend = services.get_user_by_id(friend_id, repo.repo_instance)
    if services.like_playlist(friend, user_name, repo.repo_instance):
        return render_template('user.html', user=friend)
    else:
        services.unlike_playlist(friend, user_name, repo.repo_instance)
        return render_template('user.html', user=friend)

class UserForm(FlaskForm):
    select = SelectField('Search by: ', choices=[('User name', 'User name'), ('Id', 'Id')])
    search = StringField('search', [DataRequired('Search key must not be empty')])
    submit = SubmitField('Search')


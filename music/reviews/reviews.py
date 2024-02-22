from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField, validators
from wtforms.validators import DataRequired, Length, ValidationError

import music.adapters.repository as repo
import music.reviews.services as services

from music.authentication.authentication import login_required

# Configure Blueprint.
reviews_blueprint = Blueprint(
    'reviews_bp', __name__)




@reviews_blueprint.route('/review/<int:track_id>', methods=['GET', 'POST'])
@login_required
def review_on_track(track_id):
    user_name = session['user_name']

    #user = services.get_user(user_name, repo.repo_instance)

    form = ReviewForm()
    track = services.get_track(track_id, repo.repo_instance)


    if form.validate_on_submit():

        services.add_review(track, form.review_text.data, user_name, int(form.rating.data), repo.repo_instance)
        return redirect(url_for('tracks_bp.view_track', track_id = track.track_id))

    '''
    if request.method == 'GET':
        track_id = int(request.args.get('track_id'))

        form.track_id.data = track_id
    else:
        track_id = int(form.track_id.data)'''

    track = services.get_track(track_id, repo.repo_instance)
    return render_template(
        'reviews/review_on_track.html',
        title='Edit track',
        track=track,
        form=form,
        handler_url=url_for('reviews_bp.review_on_track', track_id = track_id),
    )

class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review_text = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    rating = IntegerField('Rating', [
        validators.NumberRange(min=1, max=5)
    ])
    track_id = HiddenField("Track id")
    submit = SubmitField('Submit')


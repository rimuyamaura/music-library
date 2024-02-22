import pytest

from flask import session

def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == '/authentication/login'



@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message, in_memory_repo):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data



def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    response = client.post(
        '/authentication/login',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )


    assert response.headers['Location'] == '/'


    # Check that a session has been created for the logged-in user.


    auth.logout()
    auth.register()
    auth.login()
    with client:
        client.get('/')
        assert session['user_name'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Music Library' in response.data


def test_login_required_to_add_review(client, auth):
    auth.register()
    response = client.post('/review/2',
            data={'review_text': 'nice', 'rating': 5})
    assert response.headers['Location'] == '/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.register()
    auth.login()

    # Check that we can retrieve the comment page.
    response = client.get('/review/2')

    response = client.post(
        '/review/2',
        data={'review_text': 'nice', 'rating': 5}
    )
    assert response.headers['Location'] == '/track/2'



@pytest.mark.parametrize(('comment', 'messages'), (
        ('Who thinks Trump is a f***wit?', (b'Your comment must not contain profanity')),
        ('Hey', (b'Your comment is too short')),
        ('ass', (b'Your comment is too short', b'Your comment must not contain profanity')),
))
def test_review_with_invalid_input(client, auth, comment, messages):
    # Login a user.
    auth.register()
    auth.login()

    # Attempt to comment on an article.
    response = client.post(
        '/review/2',
        data={'review_text': comment, 'rating': 1}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_search(client):
    # Check that we can retrieve the articles page.
    response = client.get('/search')
    assert response.status_code == 200


def test_without_login_to_add_to_playlist(client, auth):
    auth.register()
    response = client.get('/playlist/add/2')
    assert response.headers['Location'] == '/authentication/login'


def test_login_required_to_add_to_playlist(client, auth):
    auth.register()
    auth.login()
    response = client.get('/playlist/add/2')
    assert response.headers['Location'] == 'None'


def test_greeting(client, auth):
    auth.register()
    auth.login()
    response = client.get('/')
    assert response.status_code == 200
    assert b'thorke' in response.data


def test_greeting_without_login(client, auth):
    auth.logout()
    response = client.get('/')
    assert response.status_code == 200
    assert b'thorke' not in response.data


def test_view_empty_play_list(client, auth):
    auth.register()
    auth.login()
    response = client.get('/playlist/thorke')
    assert b'No songs in playlist' in response.data


def test_add_song_to_play_list(client, auth):
    auth.register()
    auth.login()
    client.get('/playlist/add/2')
    response = client.get('/all_tracks')
    assert b'Successfully added to playlist' in response.data


def test_add_same_song_to_play_list(client, auth):
    auth.register()
    auth.login()
    client.get('/playlist/add/2')
    client.get('/playlist/add/2')
    response = client.get('/all_tracks')
    assert b'Song already in playlist' in response.data


def test_search_a_non_existing_or_invalid_user(client):
    client.get('/search_user')
    response = client.post('/search_user',
                           data={'select': 'User name', 'search': 'thorke'})
    assert b'No results found' in response.data

    response = client.post('/search_user',
                           data={'select': 'Id', 'search': 'thorke'})
    assert b'user id contains plain numbers' in response.data

    response = client.post('/search_user',
                           data={'select': 'Id', 'search': '-1'})
    assert b'input user id contains invalid character' in response.data







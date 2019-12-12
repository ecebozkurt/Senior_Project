'''
    This code was modified from the template provided by
     https://github.com/mari-linhares/spotify-flask

'''

from flask import Flask, request, redirect, g, render_template, session
from spotify_requests import spotify
import os
import find_recordings


app = Flask(__name__)
app.secret_key = os.urandom(24)

# ----------------------- AUTH API PROCEDURE -------------------------


@app.route("/auth")
def auth():
    return redirect(spotify.AUTH_URL)


@app.route("/callback/")
def callback():

    auth_token = request.args['code']
    auth_header = spotify.authorize(auth_token)
    session['auth_header'] = auth_header

    return profile()


def valid_token(resp):
    return resp is not None and not 'error' in resp

# -------------------------- API REQUESTS ----------------------------


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/search/')
def search():
    if 'auth_header' in session:
        auth_header = session['auth_header']
    try:
        search_type = 'track'
        name = request.args['name']
        sorted_performers = find_recordings.find_main(name)
        print(sorted_performers)
        return make_search(search_type, name, auth_header, sorted_performers)
    except:
        return render_template('search.html')


@app.route('/search/<search_type>/<name>')
def search_item(search_type, name):
    if 'auth_header' in session:
        auth_header = session['auth_header']
    return make_search(search_type, name, auth_header)


def make_search(search_type, name, auth_header, sorted_performers):
    item_list = []
    for performer in sorted_performers:
        data = spotify.search(search_type, name, auth_header, performer)
        api_url = data[search_type + 's']['href']
        items = data[search_type + 's']['items']
        item_list.append(items[0])

    return render_template('search.html',
                           name=name,
                           results=item_list,
                           api_url=api_url,
                           search_type=search_type)


@app.route('/artist/<id>')
def artist(id):
    try:
        artist = spotify.get_artist(id)
        image_url = 'http://bit.ly/2nXRRfX'

        tracksdata = spotify.get_artist_top_tracks(id)
        tracks = tracksdata['tracks']

        related = spotify.get_related_artists(id)
        related = related['artists']

        return render_template('artist.html',
                               artist=artist,
                               related_artists=related,
                               image_url=image_url,
                               tracks=tracks)
    except:
        return render_template('search.html')


@app.route('/profile')
def profile():
    if 'auth_header' in session:
        auth_header = session['auth_header']
        # get profile data
        profile_data = spotify.get_users_profile(auth_header)

        # get user playlist data
        playlist_data = spotify.get_users_playlists(auth_header)

        # get user recently played tracks
        recently_played = spotify.get_users_recently_played(auth_header)

        if valid_token(recently_played):
            return render_template("profile.html",
                                   user=profile_data,
                                   playlists=playlist_data["items"],
                                   recently_played=recently_played["items"])

    return render_template('profile.html')


@app.route('/featured_playlists')
def featured_playlists():
    if 'auth_header' in session:
        auth_header = session['auth_header']
        hot = spotify.get_featured_playlists(auth_header)
        if valid_token(hot):
            return render_template('featured_playlists.html', hot=hot)

    return render_template('profile.html')


if __name__ == "__main__":
    app.run(debug=True, port=spotify.PORT)

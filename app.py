from flask import Flask,jsonify,request,redirect,json
from flask_cors import CORS
import spotipy
from spotipy import oauth2
import os

#DEBUG = True

ENV = os.environ.get("SPOTIFY_SETTINGS")
app = Flask(__name__)
app.config.from_object(ENV) 

CORS(app)

DEBUG = app.config['DEBUG']
SPOTIPY_CLIENT_ID = app.config['SPOTIPY_CLIENT_ID']
SPOTIPY_CLIENT_SECRET = app.config['SPOTIPY_CLIENT_SECRET']
SPOTIPY_REDIRECT_URI = app.config['SPOTIPY_REDIRECT_URI']
CLIENT_REDIRECT_URL = app.config['CLIENT_REDIRECT_URL']
SCOPE = 'user-library-read user-library-modify user-read-private user-top-read playlist-modify-public playlist-modify-private playlist-read-private'
CACHE = '.spotipyoauthcache'

print(SPOTIPY_CLIENT_ID)
sp_oauth = spotipy.oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE, cache_path=CACHE)

@app.route('/', methods=['GET'])
def login():
    access_token = ""
    refresh_token = ""
    token_info = sp_oauth.get_cached_token()
    if token_info:
        access_token = token_info['access_token']
        refresh_token = token_info['refresh_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']
            refresh_token = token_info['refresh_token']

    if access_token:
        return redirect(CLIENT_REDIRECT_URL + access_token + '&refresh_token=' + refresh_token)      
    else:
        return redirect(sp_oauth.get_authorize_url())

@app.route('/refresh', methods=['GET'])
def refresh():
    refresh_token_in = request.form.get('refresh_token')
    token_info = sp_oauth.refresh_access_token(refresh_token)
    access_token = token_info['access_token']
    refresh_token = token_info['refresh_token']
    #TODO - pass back new access token and figure out the refresh workflow 
    return 0 

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

if __name__ == "__main__":
    app.run()

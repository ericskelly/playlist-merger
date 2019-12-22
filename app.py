from flask import Flask,jsonify,request,redirect,json
from flask_cors import CORS
import spotipy
from spotipy import oauth2

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

SPOTIPY_CLIENT_ID='eda0f7945ae544ebad38c981ace7d987'
SPOTIPY_CLIENT_SECRET='60a9212acff644afbe79e56eaa0b7164'
#SPOTIPY_REDIRECT_URI='http://ericwebserver.eastus.cloudapp.azure.com:8080/'
SPOTIPY_REDIRECT_URI='http://127.0.0.1:5000/'
SCOPE = 'user-library-read user-library-modify user-read-private user-top-read playlist-modify-public playlist-modify-private'
CACHE = '.spotipyoauthcache'

sp_oauth = spotipy.oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE, cache_path=CACHE)

@app.route('/', methods=['GET'])
def login():
    access_token = ""
    
    token_info = sp_oauth.get_cached_token()

    if token_info:
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        #return redirect('http://ericwebserver.eastus.cloudapp.azure.com:8008/login/#access_token=' + access_token)
        return redirect('http://localhost:8080/login/#access_token=' + access_token)
    else:
        return htmlForLoginButton()

def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

if __name__ == "__main__":
    app.run()

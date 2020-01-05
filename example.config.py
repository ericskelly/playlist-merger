class Base():
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Base):
    DEBUG = True
    DEVELOPMENT = True
    SPOTIPY_CLIENT_ID=''
    SPOTIPY_CLIENT_SECRET=''
    SPOTIPY_REDIRECT_URI=''

class ProductionConfig(Base):
    DEBUG = False
    TESTING = False
    SPOTIPY_CLIENT_ID=''
    SPOTIPY_CLIENT_SECRET=''
    SPOTIPY_REDIRECT_URI=''
from flask import Flask
from flask_restful import Api, Resource, reqparse
import os

app = Flask(__name__)
api = Api(app)

PAUSED=False

class SpotifyLiked(Resource):
    def get(self):
	if not PAUSED:
	    os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "Spotify Play Liked"'""")

class SpotifyJazz(Resource):
    def get(self):
	if not PAUSED:
	    os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "Spotify Play Jazz"'""")

class SpotifyAmbient(Resource):
    def get(self):
	if not PAUSED:
	    os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "Spotify Play Ambient"'""")

class SpotifyPause(Resource):
    def get(self):
	if not PAUSED:
	    os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "Pause Spotify"'""")

class ReverbOn(Resource):
    def get(self):
	if not PAUSED:
	    os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "Start AULab"'""")

class ReverbOff(Resource):
    def get(self):
	if not PAUSED:
	    os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "Stop AULab"'""")

class BackgroundCrickets(Resource):
    def get(self):
	if not PAUSED:
	    os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "Play Crickets"'""")

class BackgroundRain(Resource):
    def get(self):
	if not PAUSED:
	    os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "Play Rain"'""")

class BackgroundOff(Resource):
    def get(self):
	if not PAUSED:
	    os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "Stop Background Loop"'""")

class PauseSystem(Resource):
    def get(self):
        global PAUSED
	PAUSED = True

class ResumeSystem(Resource):
    def get(self):
        global PAUSED
	PAUSED = False

api.add_resource(SpotifyLiked, '/spotify/liked')
api.add_resource(SpotifyJazz, '/spotify/jazz')
api.add_resource(SpotifyAmbient, '/spotify/ambient')
api.add_resource(SpotifyPause, '/spotify/pause')

api.add_resource(ReverbOn, '/reverb/on')
api.add_resource(ReverbOff, '/reverb/off')

api.add_resource(BackgroundCrickets, '/background/crickets')
api.add_resource(BackgroundRain, '/background/rain')
api.add_resource(BackgroundOff, '/background/off')

api.add_resource(PauseSystem, '/pause')
api.add_resource(ResumeSystem, '/resume')

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

from flask import Flask
from flask_restful import Api, Resource, reqparse
import glob
import vlc

video_folder = '/videos/youtube_scenes/'
video_type = 'm4v'


vlc_inst = vlc.Instance(
		'--aout=alsa', 
		'--alsa-samplerate=44100', 
		'--input-repeat=999999', 
		'--loop',
		'--repeat',
		'--no-video-title-show', 
		'--video-on-top', 
		'--fullscreen', 
		'--mouse-hide-timeout=0')

videos = glob.glob(video_folder + '*.' + video_type)
media = [vlc_inst.media_new_path(v) for v in videos]

for v in videos: print v
playing = 'nothing'

p = vlc_inst.media_player_new()
p.set_fullscreen(True)

app = Flask(__name__)
api = Api(app)


class Playing(Resource):
	def get(self):
		return playing, 200

class Videos(Resource):
	def get(self):
		return videos

class Play(Resource):
	def get(self, video):
		for i,v in enumerate(videos):
			if video in v:
				global playing
				global p

				p.set_media(media[i])
				p.play()

				playing = v
				return 'switched to ' + v, 200

		return 'no such video', 400

api.add_resource(Playing, '/playing')
api.add_resource(Videos, '/videos')
api.add_resource(Play, '/play/<string:video>')

if __name__=='__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)

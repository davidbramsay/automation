
from flask import Flask
from flask_restful import Api, Resource, reqparse
import glob
import vlc
import os


video_folder = '/videos/youtube_scenes/'
video_type = 'webm'


app = Flask(__name__)
api = Api(app)

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
playing = 'nothing'

p = vlc_inst.media_player_new()
p.set_fullscreen(True)

start_video = 'black'

for i,v in enumerate(videos):
    if start_video in v:
        global playing
        global p

        p.set_media(media[i])
        p.play()
        playing = v

class Playing(Resource):
	def get(self):
		return playing, 200

class Videos(Resource):
	def get(self):
		return videos

class Play(Resource):
	def get(self, video):
        if not PAUSED:
            for i,v in enumerate(videos):
                if video in v:
                    global playing
                    global p

                    p.set_media(media[i])
                    p.play()

                    playing = v
                    return 'switched to ' + v, 200

            return 'no such video', 400
        return 'system paused', 400


class PauseSystem(Resource):
    def get(self):
        global PAUSED
        PAUSED = True

class ResumeSystem(Resource):
    def get(self):
        global PAUSED
        PAUSED = False


api.add_resource(Playing, '/playing')
api.add_resource(Videos, '/videos')
api.add_resource(Play, '/play/<string:video>')

api.add_resource(PauseSystem, '/pause')
api.add_resource(ResumeSystem, '/resume')

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

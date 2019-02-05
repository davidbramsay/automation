from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

videos = ['a','b','c']
playing = 'nothing'

class Playing(Resource):
	def get(self):
		return playing, 200

class Videos(Resource):
	def get(self):
		return videos

class Play(Resource):
	def get(self, video):
		for v in videos:
			if video in v:
				global playing
				playing = v
				return 'switched to ' + v, 200
		return 'no such video', 400

api.add_resource(Playing, '/playing')
api.add_resource(Videos, '/videos')
api.add_resource(Play, '/play/<string:video>')

if __name__=='__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)

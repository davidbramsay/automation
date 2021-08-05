
import helpers2
from flask import Flask
from flask_restful import Api, Resource, reqparse
import glob
import vlc
import os



video_folder = '/videos/youtube_scenes/'
video_type = 'webm'

class LightHandler(object):
    def __init__(self):
        self.oc = helpers2.OutletNetworkController("192.168.2.*")
        self.dmx = helpers2.UKingController(8)
        self.colors = { 'white' : (255, 255, 255),
                        'yellow': (255, 255, 102),
                        'orange': (255, 178, 102),
                        'purple': (153, 153, 153),
			'red' : (255, 0, 0),
			'green' : (0, 255, 0),
			'blue' : (0, 0, 255),
			'black' : (0, 0, 0)
            }

    def set_light(self, dmxch, color='white', dim=False):
        # color can be text or (r,g,b), dim can be True/False or brightness value 0/255

        if type(color) is unicode: color = color.encode('ascii', 'ignore')
        if type(dim) is bool and dim: dim = 10
        if type(dim) is bool and not dim: dim = 255
        if isinstance(color, str):
            try:
                color = self.colors[color]
            except:
                return 'not a valid color, ignoring', 404

        #assert (type(color) is tuple), 'color must be (r,g,b) tuple'
        #assert (type(dim) is int), 'dim must be an int'

        value = [dim] + list(color)

        print dmxch
        print value
        print [type(v) for v in value]
        self.dmx.update_channel(dmxch, value)


    def fade_light(self, dmxch, fadein=True):
        if fadein:
            self.dmx.fade_in(dmxch)
        else:
            self.dmx.fade_out(dmxch)


    def light_power(self, dmxch, on=True):
        if on:
            self.dmx.update_channel(dmxch, [255])
        else:
            self.dmx.update_channel(dmxch, [0])


    def all_lights_power(self, on=True):
        if on:
            self.dmx.update_channel([255])
        else:
            self.dmx.update_channel(values=[0])


    def fade_all_lights(self, fadein=True):
        if fadein:
            self.dmx.fade_in()
        else:
            self.dmx.fade_out()


    def outlet_power(self, outletnum, on=True):
        if on:
            self.oc.set_outlet_state(outletnum, True)
        else:
           	self.oc.set_outlet_state(outletnum, False)


    def outlet_toggle(self, outletnum):
        self.oc.toggle_outlet(outletnum)


    def all_outlets_power(self, on=True):
        if on:
            self.oc.set_outlet_state(state=True)
        else:
            self.oc.set_outlet_state(state=False)


    def all_outlets_toggle(self):
        self.oc.toggle_outlet()


app = Flask(__name__)
api = Api(app)

lightcontrol = LightHandler()

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

        p.set_media(media[i])
        p.play()
        playing = v

PAUSED = False

class SetLightColorString(Resource):
    def get(self, dmxch, color):
        lightcontrol.set_light(int(dmxch), color)

class SetLightColorInt(Resource):
    def get(self, dmxch, r, g, b):
        lightcontrol.set_light(int(dmxch), (r, g, b))

class SetLightColorStringDim(Resource):
    def get(self, dmxch, color):
        lightcontrol.set_light(int(dmxch), str(color), dim=True)

class SetLightColorIntDim(Resource):
    def get(self, dmxch, r, g, b):
        lightcontrol.set_light(int(dmxch), (r, g, b), dim=True)

class SetLightColorStringDimInt(Resource):
    def get(self, dmxch, color, dim):
        lightcontrol.set_light(int(dmxch), str(color), dim)

class SetLightColorIntDimInt(Resource):
    def get(self, dmxch, r, g, b):
        lightcontrol.set_light(int(dmxch), (r, g, b), dim)


class FadeLightIn(Resource):
    def get(self, dmxch):
        lightcontrol.fade_light(int(dmxch), fadein=True)

class FadeLightOut(Resource):
    def get(self, dmxch):
        lightcontrol.fade_light(int(dmxch), fadein=False)

class FadeLightsIn(Resource):
    def get(self):
        lightcontrol.fade_all_lights(fadein=True)

class FadeLightsOut(Resource):
    def get(self):
        lightcontrol.fade_all_lights(fadein=False)


class LightOn(Resource):
    def get(self, dmxch):
        lightcontrol.light_power(int(dmxch), on=True)

class LightsOn(Resource):
    def get(self):
        lightcontrol.all_lights_power(on=True)

class LightOff(Resource):
    def get(self, dmxch):
        lightcontrol.light_power(int(dmxch), on=False)

class LightsOff(Resource):
    def get(self):
        lightcontrol.all_lights_power(on=False)


class OutletOn(Resource):
    def get(self, outletnum):
        lightcontrol.outlet_power(outletnum, on=True)

class OutletOff(Resource):
    def get(self, outletnum):
        lightcontrol.outlet_power(outletnum, on=False)

class OutletToggle(Resource):
    def get(self, outletnum):
        lightcontrol.outlet_toggle(outletnum)

class OutletsOn(Resource):
    def get(self):
        lightcontrol.all_outlets_power(on=True)

class OutletsOff(Resource):
    def get(self):
        lightcontrol.all_outlets_power(on=False)

class OutletsToggle(Resource):
    def get(self):
        lightcontrol.all_outlets_toggle()

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


class PauseSystem(Resource):
    def get(self):
        global PAUSED
        PAUSED = True

class ResumeSystem(Resource):
    def get(self):
        global PAUSED
        PAUSED = False

class SystemState(Resource):
    def get(self):
        return PAUSED, 200


api.add_resource(Playing, '/playing')
api.add_resource(Videos, '/videos')
api.add_resource(Play, '/play/<string:video>')

api.add_resource(SetLightColorString, '/setlight/<int:dmxch>/color/<string:color>')
api.add_resource(SetLightColorStringDim, '/setlight/<int:dmxch>/color/<string:color>/dim')
api.add_resource(SetLightColorStringDimInt, '/setlight/<int:dmxch>/color/<string:color>/dim/<int:dim>')

api.add_resource(SetLightColorInt, '/setlight/<int:dmxch>/rgb/<int:r>/<int:g>/<int:b>')
api.add_resource(SetLightColorIntDim, '/setlight/<int:dmxch>/rgb/<int:r>/<int:g>/<int:b>/dim')
api.add_resource(SetLightColorIntDimInt, '/setlight/<int:dmxch>/rgb/<int:r>/<int:g>/<int:b>/dim/<int:dim>')

api.add_resource(FadeLightsIn, '/fadein')
api.add_resource(FadeLightsOut, '/fadeout')
api.add_resource(FadeLightIn, '/fadein/<int:dmxch>')
api.add_resource(FadeLightOut, '/fadeout/<int:dmxch>')

api.add_resource(LightsOn, '/lighton')
api.add_resource(LightsOff, '/lightoff')
api.add_resource(LightOn, '/lighton/<int:dmxch>')
api.add_resource(LightOff, '/lightoff/<int:dmxch>')

api.add_resource(OutletOn, '/outlet/<int:outletnum>/on')
api.add_resource(OutletOff, '/outlet/<int:outletnum>/off')
api.add_resource(OutletToggle, '/outlet/<int:outletnum>/toggle')

api.add_resource(OutletsOn, '/outlets/on')
api.add_resource(OutletsOff, '/outlets/off')
api.add_resource(OutletsToggle, '/outlets/toggle')

api.add_resource(PauseSystem, '/pause')
api.add_resource(ResumeSystem, '/resume')
api.add_resource(SystemState, '/paused')

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

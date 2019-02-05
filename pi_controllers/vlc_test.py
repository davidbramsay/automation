import glob
import vlc
import os

os.environ['XDG_RUNTIME_DIR'] = '/run/user/1000'

video_folder = '/videos/youtube_scenes/'
video_type = 'mp4'

videos = glob.glob(video_folder + '*.' + video_type)

for v in videos: print v

vlc_inst = vlc.Instance('--aout=alsa', '--alsa-samplerate=44100', '--input-repeat=-1', '--no-video-title-show', '--video-on-top', '--fullscreen', '--mouse-hide-timeout=0')
media = [vlc_inst.media_new_path(v) for v in videos]

p = vlc_inst.media_player_new()
p.set_media(media[0])
p.set_fullscreen(True)
p.play()

while(1): continue

#make the video folder
sudo mkdir /videos
sudo mkdir /videos/youtube_scenes
sudo chown pi /videos
sudo chown pi /videos/youtube_scenes

#install youtube-dl
sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl

#pick a video and run this (will download an mp4, or other if not available, and
#save it in the folder we just made
youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' -o '/videos/youtube_scenes/nameyouwant' <youtube-id-val>

#should probably limit it to 480
youtube-dl -f 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]/best' -o '/videos/youtube_scenes/nameyouwant' <youtube-id-val>

#chop it down
ffmpeg -i /videos/youtube_scenes/fog.mp4 -ss 00:00:00 -to 00:00:10 -c copy /videos/youtube_scenes/fog_short.mp4


vlc doesn't like the repeat mode set to -1 for infinite repeat, need to set it to a large number like 9999999

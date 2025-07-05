```sh
ffmpeg -y -i offset_crankslider_with_speed-YTShort.mp4 -stream_loop -1 -i afilador_101.mp3 \
  -c:v copy -c:a aac -shortest -map 0:v:0 -map 1:a:0 \
  ./offset_crankslider_with_speed-YTShort_audio_looped.mp4

#scp jalcocert@192.168.1.11:/home/jalcocert/mechanism/animations/offset_crankslider_with_speed-YTShort_audio_looped.mp4 ./
```
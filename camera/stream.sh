#!/bin/sh

PORT="8080"
ID="pi"
PW="1qazxcvb"
SIZE="640x480"
FRAMERATE="20"
export LD_LIBRARY_PATH=/usr/local/lib

/usr/local/bin/mjpg_streamer \
    -i "input_uvc.so -f $FRAMERATE -r $SIZE -d /dev/video0 -y -n" \
    -o "output_http.so -w /usr/local/www -p $PORT -c $ID:$PW"

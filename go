#!/bin/bash

FLOWDIR="flows"
PORT=8118

if [ "$1" == "-c" ]; then
  CMD="mitmproxy"
else
  echo "* Starting proxy server on port $PORT..."
  CMD="mitmdump"
fi

# TODO: parse args properly (position-independant)
if [ "$1" == "-d" ]; then

  if [ ! -d "$FLOWDIR" ]; then
    mkdir "$FLOWDIR"
  fi

  DUMPFILE="$FLOWDIR/log-`date +%s`.flows"
  echo "* Dumping data to $DUMPFILE..."

  $CMD -s adblock.py -p $PORT -w "$DUMPFILE" --set stream_large_bodies=100k

else

  $CMD -s adblock.py -p $PORT --set stream_large_bodies=100k

fi


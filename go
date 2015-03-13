#!/bin/bash

FLOWDIR="flows"
PORT=8118
DUMPFILE="$FLOWDIR/log-`date +%s`.flows"

if [ ! -d "$FLOWDIR" ]; then
  mkdir "$FLOWDIR"
fi

if [ "$1" == "-c" ]; then
  CMD="mitmproxy"
else
  echo "* Starting proxy server on port $PORT..."
  CMD="mitmdump"
fi

$CMD -s adblock.py -p $PORT -w "$DUMPFILE" --stream 100k

# MITM Adblock

An adblocker that runs as a proxy server! (And works on HTTPS connections.)

Use this to block ads on your mobile device, or just monitor its traffic.

## Installation

 1. Install [mitmproxy](http://mitmproxy.org/)
 2. Install required python modules:

```
$ pip install re2 adblockparser
```

 3. Run `./update-blocklists` to download some blocklists
 4. Run `./go` to start the proxy server on port 8118 (or run `./go -c` for a curses interface, which lets you inspect the requests/responses)
 5. Setup your browser/phone to use `localhost:8118` or `lan-ip-address:8118` as an HTTP proxy server; then, visit http://mitm.it on that device to install the MITM SSL certificate so that your machine won't throw security warnings whenever the proxy server intercepts your secure connections.

If you'd like to change any of the mitmproxy settings (like port, and where/whether it logs your connections), edit the `go` script.
# MITM Adblocker

An adblocker running as a proxy server! (Works on HTTPS connections.)

## Installation

 1. Install [http://mitmproxy.org/](mitmproxy)
 2. Install required python modules:

      $ pip install re2 adblockparser

 3. Run `./update-blocklists` to download some blocklists
 4. Run `./go` to start the proxy server on port 8118 (or run `./go -c` for a curses interface, which lets you inspect the requests/responses)
 5. Setup your browser/phone to use <your-ip>:8118 as an HTTP proxy server. then visit http://mitm.it to install the MITM SSL certificate on your device so it can MITM all your secure connections.

If you'd like to change any of the mitmproxy settings, edit the `go` script.
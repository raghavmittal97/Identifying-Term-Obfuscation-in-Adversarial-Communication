import SimpleHTTPServer
import SocketServer
# from Integrate_test import ProcessContent
# from http.server import BaseHTTPRequestHandler, HTTPServer
#from url.parse import urlparse, parse_qs #for reading query parameters
# from urllib.parse import urlparse, parse_qs #for reading query parameters
import traceback
import os
import sys
import urllib
import urllib2

def new():
    print('hello')
    response = urllib2.urlopen('http://localhost:8081?message=Pen will be delivered to you to shoot the president.')
    html = response.read()
    print(html)
def run():
    PORT = 8080

    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    Handler.extensions_map.update({
        '.webapp': 'application/x-web-app-manifest+json',
    });
    httpd = SocketServer.TCPServer(("", PORT), Handler)

    print "Serving at port", PORT

    # new()
    httpd.serve_forever()

run()



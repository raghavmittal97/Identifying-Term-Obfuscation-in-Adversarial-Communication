from http.server import BaseHTTPRequestHandler, HTTPServer
#from url.parse import urlparse, parse_qs #for reading query parameters 
from urllib.parse import urlparse, parse_qs #for reading query parameters 
import traceback

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET
  def do_GET(self):
        try:
          #reading query parameters		
          #query_components = parse_qs(urlparse(self.path).query)
          #imsi = query_components["imsi"] 
          qs = {}
          path = self.path
          message=""
          if '?' in path:
             path, tmp = path.split('?', 1)
             #qs = parse_qs(urlparse(tmp))
             message = tmp.split('=',1)[1]
			 #format = url.com?message='here we get message'
          # Send response status code
          self.send_response(200)
 
          # Send headers
          self.send_header('Content-type','text/html')
          self.end_headers()
 
          # Send message back to client
          #message = "hello"
          #print(message)
          # Write content as utf-8 data
          self.wfile.write(bytes(message, "utf8"))
          return
        except:
          traceback.print_exc()		
          pass
def run():
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()
 
 
run()
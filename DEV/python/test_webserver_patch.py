from http.server import HTTPServer, BaseHTTPRequestHandler
import datetime

def do_GET(self):
    if self.path == '/time':
        do_time(self)
    elif self.path == '/date':
        do_date(self)

def do_time(self):
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()
    # Send the html message
    self.wfile.write("<b> Hello World !</b>" + "<br><br>Current time: " + str(datetime.datetime.now()))
    
def do_date(self):
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()
    # Send the html message
    self.wfile.write("<b> A Date</b>")
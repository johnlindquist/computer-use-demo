import os
import socket
import base64
from http.server import HTTPServer, SimpleHTTPRequestHandler
from functools import partial


class AuthHandler(SimpleHTTPRequestHandler):
    KEY = "admin"  # Default password, can be overridden by environment variable
    
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Login Required"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        auth_header = self.headers.get('Authorization')
        if auth_header is None:
            self.do_AUTHHEAD()
            return
        
        try:
            auth_decoded = base64.b64decode(auth_header.split()[1]).decode()
            username, password = auth_decoded.split(':')
            if password == os.getenv('COMPUTER_USE_PASSWORD', self.KEY):
                return super().do_GET()
        except Exception:
            pass
            
        self.do_AUTHHEAD()


class HTTPServerV6(HTTPServer):
    address_family = socket.AF_INET6


def run_server():
    os.chdir(os.path.dirname(__file__) + "/static_content")
    server_address = ("::", 8080)
    handler = AuthHandler
    httpd = HTTPServerV6(server_address, handler)
    print("Starting HTTP server on port 8080...")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()

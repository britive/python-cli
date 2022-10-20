import http.server
import ssl

httpd = http.server.HTTPServer(('127.0.0.1', 8043), http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./server.pem', server_side=True)
httpd.serve_forever()
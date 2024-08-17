# from http.server import BaseHTTPRequestHandler, HTTPServer
# import urllib.parse
# import json

# # Define the port you want to run the server on
# PORT = 8000

# world = [[0, 0, 0, "stone.png"]]

# players = {}


# # Custom HTTPRequestHandler class
# class MyHandler(BaseHTTPRequestHandler):

#     def do_GET(self):
#         if self.path == '/get_players':
#             # print(self.rfile.read())
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             # Send the response content
#             self.wfile.write(json.dump(players))
#             # self.wfile.write(b"<html><body><h1>GET Request Received!</h1></body></html>")
#             # val = self.rfile.read()
#             # self.wfile.write(val)
#         elif self.path == '/get_world':
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(json.dump(world))
#         else:
#             self.send_response(404)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")
#             # pass

#     def do_POST(self):
#         if self.path == '/post_endpoint':
#             content_length = int(self.headers['Content-Length'])
#             post_data = self.rfile.read(content_length)
#             parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             # Send the response content
#             # self.wfile.write(b"<html><body><h1>POST Request Received!</h1>")
#             # self.wfile.write(b"<p>Posted data:</p>")
#             # self.wfile.write(b"<pre>")
#             self.wfile.write(post_data)
#             if post_data.startswith("trans"):
#                 pd2 = post_data.replace("trans", "")
#                 pdd = json.load(pd2)
#                 players[str(pdd.name)] = [pdd.name, pdd.position, pdd.rotation]
#             if post_data.startswith("block"):
#                 pd2 = post_data.replace("block", "")
#                 pdd = json.load(pd2)
#                 world.append(pdd.position[0], pdd.position[1], pdd.position[2], pdd.texture)
#             # self.wfile.write(b"</pre></body></html>")
#         else:
#             self.send_response(404)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")

# # Create an HTTP server instance
# httpd = HTTPServer(('localhost', PORT), MyHandler)

# # Output server start message
# print(f"Server started at localhost:{PORT}")

# # Start the HTTP server
# httpd.serve_forever()

if __name__ == '__main__':
    import sqlite_server

    sqlite_server.app.run(host='0.0.0.0', port=input("Run on port: "))
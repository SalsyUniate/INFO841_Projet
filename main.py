from simple_websocket_server import WebSocketServer, WebSocket 
import simple_http_server
import http.server
import urllib 
import socket as sk
PORT_website = 80
PORT_firefox = 5454


#création socket 

web_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
# reuse socket after crash (don't wait 1 min)
web_socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

url = "info.cern.ch"
req = f"GET / HTTP/1.1\r\nHost:{url}\r\n\r\n"
web_socket.connect((url, PORT_website))
print("connected")
web_socket.send(bytes(req, 'utf-8')) 
#pour send il faut obligatoirement mettre des bytes en argment dont soit 
#on encode comme ça soit on met direct une chaîne de charaactères en bytes
print("sent")
result = web_socket.recv(99999)
print(result)



# création socket du navigateur 

browser_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
# reuse socket after crash (don't wait 1 min)
browser_socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

browser_socket.bind(('', PORT_firefox))
browser_socket.listen() # TODO il faut attendre qu'il y ait une connction et l'accepter avant de recv
result2 = browser_socket.recv(9999)
print(result2)

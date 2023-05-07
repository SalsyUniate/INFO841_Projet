"""
Launch the web proxy server
"""

from classServer.web_server import WebServer

PORT_OUT = 5656
PORT_WEB = 80
PORT_RSA = 5555

#launching server
myProxyOut = WebServer(PORT_OUT, PORT_WEB, PORT_RSA)

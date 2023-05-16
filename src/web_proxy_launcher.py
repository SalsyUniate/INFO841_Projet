"""
Launch the web proxy server
"""

from classes.web_server import WebServer
from constants import SOCKET_OUT, SOCKET_WEB, SOCKET_RSA

#launching server
myWebProxyServer = WebServer(SOCKET_OUT, SOCKET_WEB, SOCKET_RSA)

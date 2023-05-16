"""
Launch the client proxy server
"""

from classServer.client_server import ClientServer
from constants import SOCKET_IN, SOCKET_OUT, SOCKET_RSA

#launching server
myClientProxyServer = ClientServer(SOCKET_IN, SOCKET_OUT, SOCKET_RSA)

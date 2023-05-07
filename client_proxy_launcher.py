"""
Launch the client proxy server
"""

from classServer.client_server import ClientServer

PORT_IN = 5454
PORT_OUT = 5656
PORT_RSA = 5555

#launching server
myProxyIn = ClientServer(PORT_IN, PORT_OUT, PORT_RSA)

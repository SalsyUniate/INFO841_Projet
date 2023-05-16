"""
Implementing client proxy
"""

import signal
import socket
import threading
from time import sleep
import rsa


class ClientServer:
    """
    Implementing a client proxy server with RSA algorithm
    """


    def __init__(self, socket_in, socket_out, socket_rsa):
        """
        Start client server : initialize secured connection and waiting for connection

        Parameters :
            socket_in (int) : port number of this server
            socket_out (int) : port number of web proxy server
            socket_rsa (int) : port number to share rsa keys

        No returns
        """

        print("Starting client proxy server...")

        # can stop the server with Ctl+C in shell
        self.shutdown = 0
        signal.signal(signal.SIGINT, self.shutdown)

        # creating socket and making it reusable
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binding socket to host and port
        self.server_socket.bind(('localhost', socket_in))

        # waiting queue for requests
        self.server_socket.listen(10)

        # initialize secured connection
        self.secure_connection(socket_rsa)

        print("Server up !\n")

        id_thread = 1
        while True :
            (client_socket, _) = self.server_socket.accept()
            # making thread correspondig to the request
            thread = threading.Thread(target=self.proxy_thread,
                                      args = (client_socket,
                                              socket_out,
                                              id_thread))
            id_thread += 1
            thread.daemon = True
            thread.start()


    def secure_connection(self, socket_rsa):
        """
        Initialize the rsa key to scure the connection

        Parameters :
            socket_rsa (int): socket number to connect

        No returns
        """

        print("Initializing secured connection...")

        # generating encryption keys
        (self.public_key, self.private_key) = rsa.newkeys(512)

        # get public key in bytes to send it
        str_public_key = str(self.public_key)[10:-1].split(", ")
        bytes_public_key = [str.encode(str_public_key[0]),
                            str.encode(str_public_key[1])]


        # binding socket to host and port
        self.rsa_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rsa_socket.connect(('localhost', socket_rsa))

        # send public key to web proxy
        sleep(1)
        self.rsa_socket.send(bytes_public_key[0])
        sleep(1)
        self.rsa_socket.send(bytes_public_key[1])

        # receiving web proxy public key
        bytes_out_key = [self.rsa_socket.recv(4096)]
        bytes_out_key.append(self.rsa_socket.recv(4096))

        # convert web proxy public key in rsa.PublicKey
        int_out_key = [int(str(bytes_out_key[0])[2:-1]),
                    int(str(bytes_out_key[1])[2:-1])]
        self.web_proxy_key = rsa.PublicKey(int_out_key[0], int_out_key[1])

        # closing rsa socket
        self.rsa_socket.close()


    def proxy_thread(self, client_socket, socket_out, id_thread):
        """
        Handle a request from the client

        Parameters :
            client_socket (socket): socket to communicate with the client
            socket_out (int): socket number of the web proxy
            id_thread (int): the id of the thread

        No returns
        """

        print(f"New connection (id : {id_thread})!")
        request = str(client_socket.recv(4096))
        print(f"  Thread {id_thread}: Request received")

        # parse the first line
        first_line = request.split('\n', maxsplit=1)[0]
        url = first_line.split(' ')[1].replace('http://', '')[:-1]

        # creation of the thread socket
        thread_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        thread_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        thread_socket.connect(('localhost', socket_out))

        # encrypt request and send it to the web proxy
        masqued_url = rsa.encrypt(url.encode('ascii'), self.web_proxy_key)
        thread_socket.send(masqued_url)
        print(f"  Thread {id_thread}: Request sent to web proxy")

        # receiving response from web proxy
        masqued_result = []
        end_bool = False
        while not end_bool:
            new = thread_socket.recv(4096)
            if new == b'END':
                # stop listening when receiving 'END'
                end_bool = True
            else : masqued_result.append(new)

        # decrypt response from web proxy
        clear_result = ''
        for part in enumerate(masqued_result):
            clear_result += str(rsa.decrypt(masqued_result[part[0]], self.private_key))[2:-1]

        # remove '\\' in the response
        clear_result = clear_result.replace("\\n", "\n")
        clear_result = clear_result.replace("\\r", "\r")

        # sending answer to client
        client_socket.send(bytes(clear_result, 'utf-8'))

        # ending thread
        print(f"  Thread {id_thread}: Response sent to client")
        print(f"Closing thread {id_thread}")

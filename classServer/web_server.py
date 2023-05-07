"""
# TODO: write documentation
"""

import signal
import socket
import threading
from time import sleep
import rsa



class WebServer :
    """
    # TODO: xrite docstring
    """
    def __init__(self, port_out, port_web, port_rsa):

        print("Starting web proxy server...")


        self.shutdown = 0
        signal.signal(signal.SIGINT, self.shutdown)

        # creating socket and making it reusable
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binding socket to host and port
        self.server_socket.bind(('localhost', port_out))

        # waiting queue for requests
        self.server_socket.listen(10)


        self.secure_connection(port_rsa)


        print("Server up !\n")
        id_thread = 1
        while True :
            (client_socket, _) = self.server_socket.accept()
            # making thread correspondig to the request
            thread = threading.Thread(target=self.proxy_thread,
                                      args = (client_socket,
                                              port_web,
                                              id_thread))
            id_thread += 1
            thread.daemon = True
            thread.start()

    def secure_connection(self, port_rsa) :
        """
        # TODO: write documentation
        """
        print("Initializing secured connection...")


        # generating encryption keys
        self.public_key, self.private_key = rsa.newkeys(512)

        # creating socket and making it reusable
        self.rsa_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rsa_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.rsa_socket.bind(('localhost', port_rsa))
        self.rsa_socket.listen()

        (self.rsa_connected, _) = self.rsa_socket.accept()


        bytes_in_key = []
        while len(bytes_in_key) < 2 :
            bytes_in_key.append(self.rsa_connected.recv(4096))

        str_public_key = str(self.public_key)[10:-1].split(", ")
        bytes_public_key = [str.encode(str_public_key[0]),
                            str.encode(str_public_key[1])]

        self.rsa_connected.send(bytes_public_key[0])
        sleep(2)
        self.rsa_connected.send(bytes_public_key[1])


        int_in_key = [int(str(bytes_in_key[0])[2:-1]),
                    int(str(bytes_in_key[1])[2:-1])]
        self.client_proxy_key = rsa.PublicKey(int_in_key[0], int_in_key[1])

        self.rsa_socket.close()


    def proxy_thread(self, client_socket, port_web, id_thread):
        """
        # TODO: write documentation
        """
        print(f"New connection (id : {id_thread})!")
        request = client_socket.recv(4096)
        print(f"  Thread {id_thread}: Request received")
        request = str(rsa.decrypt(request, self.private_key))
        request = request.replace("b'", "")
        request = request.replace("'", "")


        ### creation of the thread socket

        thread_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        thread_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        thread_socket.connect((request, port_web))
        req = f"GET / HTTP/1.1\r\nHost:{request}\r\n\r\n"
        thread_socket.send(bytes(req, 'utf-8'))
        print(f"  Thread {id_thread}: Request sent to web server")
        result = thread_socket.recv(4096)


        masqued_result = []
        for index in range(0, len(result), 53):
            part = result[index:index+53]
            masqued_result.append(rsa.encrypt(part, self.client_proxy_key))


        # sending answer to client
        for part in enumerate(masqued_result):
            client_socket.send(masqued_result[part[0]])
            sleep(0.0005)

        client_socket.send(b'END')
        print(f"  Thread {id_thread}: Response sent to client proxy")
        print(f"Closing thread {id_thread}")
        
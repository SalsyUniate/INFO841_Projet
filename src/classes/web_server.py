"""
Implementing web proxy
"""

import signal
import socket
import threading
from time import sleep
from time import time
import rsa


class WebServer :
    """
    Implementing a web proxy server with RSA algorithm
    """


    def __init__(self, port_out, port_web, port_rsa):
        """
        Start web server : initialize secured connection and waiting for connection

        Parameters :
            socket_out (int) : port number of this server
            socket_web (int) : port number of web servers
            socket_rsa (int) : port number to share rsa keys

        No returns
        """

        print("Starting web proxy server...")

        # can stop the server with Ctl+C in shell
        self.shutdown = 0
        signal.signal(signal.SIGINT, self.shutdown)

        # creating socket and making it reusable
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binding socket to host and port
        self.server_socket.bind(('localhost', port_out))

        # waiting queue for requests
        self.server_socket.listen(10)

        # initialize secured connection
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
        Initialize the rsa key to scure the connection

        Parameters :
            socket_rsa (int): socket number to connect

        No returns
        """

        print("Initializing secured connection...")

        # generating encryption keys
        self.public_key, self.private_key = rsa.newkeys(512)

        # creating socket and making it reusable
        self.rsa_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rsa_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binding socket and listening
        self.rsa_socket.bind(('localhost', port_rsa))
        self.rsa_socket.listen()

        # accepting the connection
        (self.rsa_connected, _) = self.rsa_socket.accept()

        # receiving client proxy publi key
        bytes_in_key = []
        while len(bytes_in_key) < 2 :
            bytes_in_key.append(self.rsa_connected.recv(4096))

        # get public key in bytes to send it
        str_public_key = str(self.public_key)[10:-1].split(", ")
        bytes_public_key = [str.encode(str_public_key[0]),
                            str.encode(str_public_key[1])]

        # send public key to client proxy
        self.rsa_connected.send(bytes_public_key[0])
        sleep(0.05)
        self.rsa_connected.send(bytes_public_key[1])

        # convert web proxy public key in rsa.PublicKey
        int_in_key = [int(str(bytes_in_key[0])[2:-1]),
                    int(str(bytes_in_key[1])[2:-1])]
        self.client_proxy_key = rsa.PublicKey(int_in_key[0], int_in_key[1])

        # closing rsa socket
        self.rsa_socket.close()


    def proxy_thread(self, client_socket, port_web, id_thread):
        """
        Handle a request from the client

        Parameters :
            client_socket (socket): socket to communicate with the client proxy
            socket_out (int): socket number of the web server
            id_thread (int): the id of the thread

        No returns
        """

        t_request_received = time()

        print(f"New connection (id : {id_thread})!")
        request = client_socket.recv(4096)
        print(f"  Thread {id_thread}: Request received")

        # decrypt request from client proxy
        t_decryption_starting = time()
        request = str(rsa.decrypt(request, self.private_key))
        request = request.replace("b'", "")
        request = request.replace("'", "")
        t_decryption_ended = time()
        t_decryption = round(1000*(t_decryption_ended - t_decryption_starting))

        host_name, req_list = request.split('/', maxsplit=1)[0], request.split('/')[1:]
        req = host_name
        for i in req_list :
            req = req + i

        # creation of the thread socket
        thread_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        thread_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        thread_socket.connect((host_name, port_web))

        # build a new request for web server and send it
        req = f"GET / HTTP/1.1\r\nHost:{req}\r\n\r\n"
        thread_socket.send(bytes(req, 'utf-8'))
        print(f"  Thread {id_thread}: Request sent to web server")

        # get response from web server
        result = thread_socket.recv(4096)

        # encrypt response from web server
        t_encyption_starting = time()
        masqued_result = []
        for index in range(0, len(result), 53):
            part = result[index:index+53]
            # doing by step because size is limited in rsa.encrypt
            masqued_result.append(rsa.encrypt(part, self.client_proxy_key))
        t_encryption_ended = time()
        t_encryption = round(1000*(t_encryption_ended - t_encyption_starting))

        # sending answer to client proxy
        for part in enumerate(masqued_result):
            client_socket.send(masqued_result[part[0]])
            sleep(0.0005)

        # alert client proxy all the data where sent
        client_socket.send(b'END')

        # ending thread
        t_request_handled = time()
        t_request = round(1000*(t_request_handled - t_request_received))
        print(f"  Thread {id_thread}: Response sent to client proxy")
        print(f"  Thread {id_thread}: Writing time logs")
        with open("logs/web_logs.txt", "a", encoding="utf-8") as file :
            file.write(f"Thread {id_thread} time logs\n")
            file.write(f"   Total time : {t_request} ms\n")
            file.write(f"   Encryption time : {t_encryption} ms\n")
            file.write(f"   Decryption time : {t_decryption} ms\n\n")
        print(f"Closing thread {id_thread}")

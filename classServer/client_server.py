"""
# TODO: write documentation
"""

import signal
import socket
import threading
from time import sleep
import rsa


class ClientServer:
    """
    TODO: write documentation

    """

    def __init__(self, port_in, port_out, port_rsa):

        print("Starting client proxy server...")

        self.shutdown = 0
        signal.signal(signal.SIGINT, self.shutdown)

        # creating socket and making it reusable
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binding socket to host and port
        self.server_socket.bind(('localhost', port_in))

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
                                              port_out,
                                              id_thread))

            id_thread += 1
            thread.daemon = True
            thread.start()



    def secure_connection(self, port_rsa):
        """
        Initialize the rsa key to scure the connection
        Args:
            port_rsa (int): port numver to connect
        """
        print("Initializing secured connection...")
        # generating encryption keys
        (self.public_key, self.private_key) = rsa.newkeys(512)


        str_public_key = str(self.public_key)[10:-1].split(", ")
        bytes_public_key = [str.encode(str_public_key[0]),
                            str.encode(str_public_key[1])]


        # binding socket to host and port
        self.rsa_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rsa_socket.connect(('localhost', port_rsa))

        sleep(1)
        self.rsa_socket.send(bytes_public_key[0])
        sleep(1)
        self.rsa_socket.send(bytes_public_key[1])
        bytes_out_key = [self.rsa_socket.recv(4096)]
        bytes_out_key.append(self.rsa_socket.recv(4096))

        int_out_key = [int(str(bytes_out_key[0])[2:-1]),
                    int(str(bytes_out_key[1])[2:-1])]
        self.web_proxy_key = rsa.PublicKey(int_out_key[0], int_out_key[1])

        self.rsa_socket.close()

    def proxy_thread(self, client_socket, port_out, id_thread):
        """
        Handle a request from the client

        Args:
            client_socket (_type_): _description_
            port_out (_type_): _description_
            id_thread (_type_): _description_
            server_keys (_type_): _description_
            web_proxy_key (_type_): _description_
        """


        print(f"New connection (id : {id_thread})!")
        request = str(client_socket.recv(4096))
        print(f"  Thread {id_thread}: Request received")

        # parse the first line
        first_line = request.split('\n', maxsplit=1)[0]
        url = first_line.split(' ')[1].replace('http://', '')[:-1]
        # print(url)


        ### creation of the thread socket
        thread_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        thread_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        thread_socket.connect(('localhost', port_out))

        masqued_url = rsa.encrypt(url.encode('ascii'), self.web_proxy_key)
        thread_socket.send(masqued_url)
        print(f"  Thread {id_thread}: Request sent to web proxy")

        masqued_result = []
        end_bool = False
        while not end_bool:
            new = thread_socket.recv(4096)
            if new == b'END':
                end_bool = True
            else : masqued_result.append(new)


        clear_result = ''
        for part in enumerate(masqued_result):
            clear_result += str(rsa.decrypt(masqued_result[part[0]], self.private_key))[2:-1]

        clear_result = clear_result.replace("\\n", "\n")
        clear_result = clear_result.replace("\\r", "\r")

        # sending answer to client
        client_socket.send(bytes(clear_result, 'utf-8'))


        print(f"  Thread {id_thread}: Response sent to client")
        print(f"Closing thread {id_thread}")

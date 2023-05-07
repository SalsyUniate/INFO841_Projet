import signal
import socket
import threading
import rsa
from time import sleep

      

class ServerOut : 
    def __init__(self, port_out, port_web, port_rsa):
        
        print("\nStarting web proxy server...")

        
        self.shutdown = 0
        signal.signal(signal.SIGINT, self.shutdown)
        
        # creating socket and making it reusable
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # binding socket to host and port 
        self.serverSocket.bind(('localhost', port_out))
        
        # waiting queue for requests 
        self.serverSocket.listen(10)
        
        print("Initializing secured connection...")
        
        
        # generating encryption keys 
        (public_key, private_key) = rsa.newkeys(512)
        server_keys = (public_key, private_key)
        
        # creating socket and making it reusable
        self.rsaSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rsaSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.rsaSocket.bind(('localhost', port_rsa))
        self.rsaSocket.listen()

        (self.rsaIn, _) = self.rsaSocket.accept()


        bytes_in_key = []
        while len(bytes_in_key) < 2 :
            bytes_in_key.append(self.rsaIn.recv(4096))
        
        str_public_key = str(public_key)[10:-1].split(", ")
        bytes_public_key = [str.encode(str_public_key[0]),
                            str.encode(str_public_key[1])]
        
        self.rsaIn.send(bytes_public_key[0])
        sleep(2)
        self.rsaIn.send(bytes_public_key[1])
        
        
        
        int_in_key = [int(str(bytes_in_key[0])[2:-1]),
                      int(str(bytes_in_key[1])[2:-1])]
        in_key = rsa.PublicKey(int_in_key[0], int_in_key[1])
        
        self.rsaSocket.close()
        
        
        
        
        
        
        ### accepting clients 
        print("Server up !\n")
        id_thread = 1
        while True :
            (clientSocket, _) = self.serverSocket.accept()
            # making thread correspondig to the request 
            thread = threading.Thread(target=self.proxy_thread, 
                                      args = (clientSocket,
                                              port_web,
                                              id_thread, 
                                              server_keys,
                                              in_key))
            id_thread += 1
            thread.setDaemon(True)
            thread.start()
            




    ### execution of the thread
    
    def proxy_thread(self, clientSocket, port_web, id, server_keys, in_key):
        print("New connection (id : {})!".format(id))
        request = clientSocket.recv(4096)
        print("  Thread {}: Request received".format(id))
        request = str(rsa.decrypt(request, server_keys[1]))
        request = request.replace("b'", "")
        request = request.replace("'", "")
        
    
        ### creation of the thread socket 
        
        self.threadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.threadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.threadSocket.connect((request, port_web)) # connecting socket with web port
        req = f"GET / HTTP/1.1\r\nHost:{request}\r\n\r\n" # creating new request 
        self.threadSocket.send(bytes(req, 'utf-8')) # sending new request 
        print("  Thread {}: Request sent to web server".format(id))
        result = self.threadSocket.recv(4096) # recieving answer from web server
        # print(result) 
        print(len(str(result)) - 3)
        # masqued_result = rsa.encrypt(result, in_key)
        # print(result)  
        
        masqued_result = []
        for n in range(0, len(result), 53):
            part = result[n:n+53]
            masqued_result.append(rsa.encrypt(part, in_key))
            
        # print(len(masqued_result))
        
        # sending answer to client 
        for n in range (len(masqued_result)):
            clientSocket.send(masqued_result[n])
            sleep(0.05)
        # sleep(1.7)
        clientSocket.send(b'END')
        print("  Thread {}: Response sent to client proxy".format(id))
        print("Closing thread {}".format(id))
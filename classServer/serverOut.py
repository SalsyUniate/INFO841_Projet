import signal
import socket
import threading
import rsa 
from time import sleep

      

class ServerOut : 
    def __init__(self, port_in, port_out, port_web):

        
        self.shutdown = 0
        signal.signal(signal.SIGINT, self.shutdown)
        
        # creating socket and making it reusable
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # binding socket to host and port 
        self.serverSocket.bind(('localhost', port_out))
        
        # waiting queue for requests 
        self.serverSocket.listen(10)
        
        
        # # generating encryption keys 
        # (public_key, private_key) = rsa.newkeys(512)
        # print('public out :')
        # print(public_key)
        # #print(private_key) 
        
        # self.rsaSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.rsaSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sleep(3)
        # self.rsaSocket.connect(('localhost', port_in))
        # in_key = self.rsaSocket.recv(4096)
        # self.rsaSocket.send(public_key, 'utf-8')
        # print('public in :')
        # print(in_key)
        
        
        
        
        
        
        ### accepting clients 
        
        print("OUT : Waiting connection...")
        id_thread = 1
        while True :
            (clientSocket, client_address) = self.serverSocket.accept()
            # making thread correspondig to the request 
            thread = threading.Thread(target=self.proxy_thread, 
                                      args = (clientSocket,
                                              client_address,
                                              port_web,
                                              id_thread))
            id_thread += 1
            thread.setDaemon(True)
            thread.start()
            




    ### execution of the thread
    
    def proxy_thread(self, clientSocket, client_address, port_web, id):
        print("OUT : New connection (id : {})!".format(id))
        request = str(clientSocket.recv(4096))
        request = request.replace("b'", "")
        request = request.replace("'", "")
        # request = request[2:-1]
        # request = request.replace("\r", "").split("\n")
        # temp = request[0].split(" ")
        # request = temp[1].replace("https://", "").split("/")[0]
        

    
        ### creation of the thread socket 
        
        self.threadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.threadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.threadSocket.connect((request, port_web)) # connecting socket with web port
        req = f"GET / HTTP/1.1\r\nHost:{request}\r\n\r\n" # creating new request 
        self.threadSocket.send(bytes(req, 'utf-8')) # sending new request 
        print("OUT : Request sent")
        result = self.threadSocket.recv(4096) # recieving answer from web server 
        # print(result)  
        
        # sending answer to client 
        clientSocket.send(result)
        print("OUT : END THREAD")
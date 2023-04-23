import signal
import socket
import threading

      

class ServerOut : 
    def __init__(self, port_out, port_web):
        
        self.shutdown = 0
        signal.signal(signal.SIGINT, self.shutdown)
        
        # creating socket and making it reusable
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # binding socket to host and port 
        self.serverSocket.bind(('localhost', port_out))
        
        # waiting queue for requests 
        self.serverSocket.listen(10)
        
        
        
        
        
        ### accepting clients 
        
        print("OUT : Waiting connection...")
        while True :
            (clientSocket, client_address) = self.serverSocket.accept()
            # making thread correspondig to the request 
            thread = threading.Thread(target=self.proxy_thread, 
                                      args = (clientSocket, client_address, port_web))
            thread.setDaemon(True)
            thread.start()
            




    ### execution of the thread
    
    def proxy_thread(self, clientSocket, client_address, port_web):
        print("OUT : New connection!")
        request = str(clientSocket.recv(4096))
        request = request[2:-1]

    
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
        
        
        
  
import signal
import socket
import threading


class ServerIn : 
    def __init__(self, port_in, port_out):
        
        self.shutdown = 0
        signal.signal(signal.SIGINT, self.shutdown)
        
        # creating socket and making it reusable
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # binding socket to host and port 
        self.serverSocket.bind(('localhost', port_in))
        
        # waiting queue for requests 
        self.serverSocket.listen(10)
        
        
        
        
        
        ### accepting clients 
        
        print("IN : Waiting connection...")
        while True :
            (clientSocket, client_address) = self.serverSocket.accept()
            # making thread correspondig to the request 
            thread = threading.Thread(target=self.proxy_thread, 
                                      args = (clientSocket, client_address, port_out))
            thread.setDaemon(True)
            thread.start()
            




    ### execution of the thread
    
    def proxy_thread(self, clientSocket, client_address, port_out):
        print("IN : New connection!")
        request = str(clientSocket.recv(4096))
        
        # parse the first line
        first_line = request.split('\n')[0]
        temp = first_line.split(' ')[1]
        
        # deletion of http:// and the last / in the url
        url = temp.replace('http://', '')
        url = url[:-1]
        print(url)
    
    
        ### creation of the thread socket 
        
        self.threadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.threadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.threadSocket.connect(('localhost', port_out)) # connecting socket with web port
        print("IN : connected")
        
        # req = f"GET / HTTP/1.1\r\nHost:{url}\r\n\r\n" # creating new request 
        self.threadSocket.send(bytes(url, 'utf-8')) # sending new request 
        print("IN : Request sent")
        result = self.threadSocket.recv(4096) # recieving answer from web server 
        # print(result)  
        
        # sending answer to client 
        clientSocket.send(result)
        print("IN : END THREAD")
        
        
    
  
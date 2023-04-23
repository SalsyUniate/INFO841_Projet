import signal
import socket
import threading

port = 5454


class Server : 
    def __init__(self, config = None):
        
        self.shutdown = 0
        signal.signal(signal.SIGINT, self.shutdown)
        # creating the socket 
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #making the socket reusdown able 
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #binding socket to host and port 
        #self.serverSocket.bind((config['localhost'], config[port]))
        self.serverSocket.bind(('localhost', port))
        
        self.serverSocket.listen(10)
        self.__clients = {}
        
        
        
        
        
        
        
        # accepting client 
        
        print("Waiting connection...")
        while True :
            (clientSocket, client_address) = self.serverSocket.accept()
            thread = threading.Thread(#name=self._getClientName(client_address), 
                                      target=self.proxy_thread, 
                                      args = (clientSocket, client_address))
            thread.setDaemon(True)
            thread.start()
            


    def proxy_thread(self, clientSocket, client_address):
        print("New connection !")
        
        #redirection of the request 

        request = str(clientSocket.recv(4096))
        # print(request)
        # print(type(request))
        #request = bytes(request, 'utf-8')
                
        # parse the first line
        first_line = request.split('\n')[0]
        # print(first_line)
        # get url
        url = first_line.split(' ')[1]
        #url2 = 'info.cern.ch'
        url2 = url.replace('http://', '')
        url2 = url2[:-1]
        
    
        self.threadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.threadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.threadSocket.connect((url2, 80))
        req = f"GET / HTTP/1.1\r\nHost:{url2}\r\n\r\n"
        self.threadSocket.send(bytes(req, 'utf-8'))
        print("Request sent")
        result = self.threadSocket.recv(4096)
        # print(result)  
        
        clientSocket.send(result)
        print("FIN THREAD")
              

        
        
myServer = Server()
        
        
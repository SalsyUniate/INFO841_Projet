import signal
import socket
import threading
import rsa 
from time import sleep

class ServerIn : 
    def __init__(self, port_in, port_out, port_rsa): 
        
        print("\nStarting client proxy server...")  
        
        self.shutdown = 0
        signal.signal(signal.SIGINT, self.shutdown)
        
        
        # creating socket and making it reusable
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # binding socket to host and port 
        self.serverSocket.bind(('localhost', port_in))
        
        # waiting queue for requests 
        self.serverSocket.listen(10)
    
        
        
        print("Initializing secured connection...")
        # generating encryption keys 
        (public_key, private_key) = rsa.newkeys(512)
        server_keys = (public_key, private_key)
        
        
        
        str_public_key = str(public_key)[10:-1].split(", ")
        bytes_public_key = [str.encode(str_public_key[0]),
                            str.encode(str_public_key[1])]

        
        # binding socket to host and port 
        self.rsaSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rsaSocket.connect(('localhost', port_rsa))
        
        sleep(2)
        self.rsaSocket.send(bytes_public_key[0])
        sleep(2)
        self.rsaSocket.send(bytes_public_key[1])
        bytes_out_key = [self.rsaSocket.recv(4096)]
        bytes_out_key.append(self.rsaSocket.recv(4096))
        
        int_out_key = [int(str(bytes_out_key[0])[2:-1]),
                      int(str(bytes_out_key[1])[2:-1])]
        out_key = rsa.PublicKey(int_out_key[0], int_out_key[1])
        # print('out_key :')
        # print(out_key)
        
        self.rsaSocket.close()
        
        
        

        
        ### accepting clients 
        
        print("Server up !\n")
        id_thread = 1
        while True :
            (clientSocket, _) = self.serverSocket.accept()
            # making thread correspondig to the request 
            thread = threading.Thread(target=self.proxy_thread, 
                                      args = (clientSocket,
                                              port_out,
                                              id_thread, 
                                              server_keys,
                                              out_key))
            id_thread += 1
            thread.setDaemon(True)
            thread.start()
            # if id_thread > 1 :
            #     self.serverSocket.close()
            




    ### execution of the thread
    
    def proxy_thread(self, clientSocket, port_out, id, server_keys, out_key):
        
        print("New connection (id : {})!".format(id))
        request = str(clientSocket.recv(4096))
        print("  Thread {}: Request received".format(id))
        
        # parse the first line
        first_line = request.split('\n')[0]
        temp = first_line.split(' ')[1]
        
        # deletion of http:// and the last / in the url
        url = temp.replace('http://', '')
        url = url[:-1]
        # print(url)
    
    
        ### creation of the thread socket 
        
        self.threadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.threadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.threadSocket.connect(('localhost', port_out)) # connecting socket with web port
        
        masqued_url = rsa.encrypt(url.encode('ascii'), out_key)
        # self.threadSocket.send(bytes(url, 'utf-8')) # sending new request 
        self.threadSocket.send(masqued_url)
        print("  Thread {}: Request sent to web proxy".format(id))
        
        masqued_result = []
        end_bool = False
        print("debut while")
        while not end_bool:
            new = self.threadSocket.recv(4096) 
            # print(new)
            if new == b'END':
                end_bool = True
            else : masqued_result.append(new)
        # masqued_result = self.threadSocket.recv(4096) # recieving answer from web server 
        # print(result) 
        
        print("fin while")
        print(len(masqued_result))
        # print('\n')
        # print(masqued_result) 
        
        clear_result = ''
        for n in range(len(masqued_result)):
            # print(str(rsa.decrypt(masqued_result[n], server_keys[1])))
            clear_result += str(rsa.decrypt(masqued_result[n], server_keys[1]))[2:-1]
            
        # print('\n\n\n' + clear_result)
        print("decrypté")
        print(len(clear_result))
        # sending answer to client 
        # clientSocket.send(bytes(clear_result, 'utf-8'))
        clientSocket.send(bytes(clear_result, 'utf-8'))
        print("  Thread {}: Response sent to client".format(id))
        print("Closing thread {}".format(id))
        
        
    
  
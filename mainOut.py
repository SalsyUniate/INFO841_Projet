from classServer.serverOut import ServerOut

port_in = 5454
port_out = 5656
port_web = 80

        
#launching server  
myProxyOut = ServerOut(port_in, port_out, port_web)


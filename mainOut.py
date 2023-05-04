from classServer.serverOut import ServerOut

port_in = 5454
port_out = 5656
port_web = 80
port_rsa = 5555

        
#launching server  
myProxyOut = ServerOut(port_out, port_web, port_rsa)


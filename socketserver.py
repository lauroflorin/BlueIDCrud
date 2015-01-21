###################################################################
# Socket Server
###################################################################
import SocketServer
import json
import blueid

# socket declaration
HOST, PORT = "192.168.0.100", 9999


class socketHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        #self.request.sendall("connection initiated \r\n" + '\n')
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        #self.request.sendall(self.data + '\n')
        print "Message succesfully sent !"
        # print "{} wrote:".format(self.client_address[0])
        print self.data
        
        # get message and decode
        message = json.loads(self.data)
        command = message["command"]
        params = message["params"]
        username = params["username"]
        if command == "login":
            password = params["password"]
        else:
            password = "none"

        db = blueid.crud()
        if command == "login":
            isLoggedin = db.login(username,password)
            #self.request.sendall(self.data + '\n')
            self.request.sendall(isLoggedin +'\n')
            print "testing login " + isLoggedin
        else: #todo add logout
            if command == "logout":
                 isLoggedOut = db.logout(username)
                 self.request.sendall(isLoggedOut+'\n')
        #self.request.sendall(self.data + '\n')         

        #self.request.sendall(self.data.upper())


if __name__ == "__main__":
    db = blueid.crud()
    db.initial_setup();

    # Create the server on localhost port 9999
    server = SocketServer.TCPServer((HOST, PORT), socketHandler)
    server.serve_forever()
    print "::::::::::::::: server running :::::::::::::::"

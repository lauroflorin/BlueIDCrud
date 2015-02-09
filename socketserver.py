###################################################################
# Socket Server
###################################################################
import SocketServer
import json
import blueid

# socket declaration
HOST, PORT = "192.168.43.104", 9999


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
        db = blueid.crud()

        if command == "login":
            username = params["username"]
            password = params["password"]
            isLoggedin = db.login(username,password)
            #self.request.sendall(self.data + '\n')
            #TODO changed goku
            self.request.sendall(str(isLoggedin) +'\n')
            print "testing login " + str(isLoggedin)

        if command == "authorize":
            uid = params["uid"]
            did = params["did"]
            gid = params["gid"]
            cha = params["cha"]
            skey = params["skey"]
            ServerResponse = db.authorize(uid,did,gid,cha,skey)
            #self.request.sendall(self.data + '\n')
            #TODO changed goku
            self.request.sendall(str(ServerResponse) +'\n')

        if command == "writelog":
            entry = params["entry"]
            db.write_log(entry)

        if command == "logout":
            username = params["username"]
            isLoggedOut = db.logout(username)
            self.request.sendall(isLoggedOut+'\n')

if __name__ == "__main__":
    db = blueid.crud()
    db.initial_setup();

    # Create the server on localhost port 9999
    server = SocketServer.TCPServer((HOST, PORT), socketHandler)
    server.serve_forever()
    print "::::::::::::::: server running :::::::::::::::"


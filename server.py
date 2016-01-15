#  coding: utf-8 
import SocketServer, os.path, mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall("OK")
        #self.request.sendall(self.data)
        self.dataList = self.data.split()
        self.type = self.dataList[0]
        if (self.type == "GET"):
            self.dataString = self.dataList[1]
            self.httpType = self.dataList[2]
            print("data: %s\n" % self.dataString)
            self.serve()

    def serve(self):
        self.dir = "./www"
        self.filepath = self.dir+self.dataString
        print("filepath: "+self.filepath)
        #http://stackoverflow.com/questions/8933237/how-to-find-if-directory-exists-in-python by phihag
        print ("exists?",os.path.exists(self.filepath))
        if (os.path.exists(self.filepath)):
            if (self.filepath.endswith(".css")):
                f = open(self.filepath,"r")
                self.request.sendall('HTTP/1.1 200\r\n Content-Type: text/css\n\n')
                #self.request.sendall('HTTP/1.1 200 '+f.read()+'\n\n')
                self.request.sendall(f.read())
                f.close()
            else:
                if (not self.filepath.endswith("/") and not self.dataString.endswith(".html")):
                    self.request.sendall('HTTP/1.1 301 Moved Permanently\r\n')
                    self.dataString = self.dataString+'/'
                    print ("filepath fixed: "+self.dataString)
                    self.request.sendall('Location: '+self.dataString+'\r\n')
                #print ("got a request of: %s\n" % self.filepath)
                if (not self.filepath.endswith(".html")):
                    self.filepath = self.filepath+"/index.html"
                f = open(self.filepath,"r")
                self.request.sendall('HTTP/1.1 200\r\n Content-Type: text/html\n\n')
                #self.request.sendall('HTTP/1.1 200 '+f.read()+'\n\n')
                self.request.sendall(f.read())
                f.close()
        else:
            #send 404
            print('404')
            self.request.sendall('HTTP/1.1 404 Not Found\r\n')
            self.request.sendall('Content-Type: text/html\n\n')
            self.request.sendall('404 Page Not Found')

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

######################################################################

# Copyright 2023 Marafi Mergani

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


import sys
import socket
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = int(data.split()[1])
        return code

    def get_headers(self,data):
        return None

    def get_body(self, data):
        body = data.split("\r\n\r\n")[1]
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""
        parsedUrl = urllib.parse.urlparse(url)
        path = parsedUrl.path
        if path == "":
            path = "/"
        host = parsedUrl.hostname
        port = parsedUrl.port
        if port == None:
            port = 80
        self.connect(host, port)
        if args != None:
            args = urllib.parse.urlencode(args)
            path += "?" + args
        request = "GET " + path + " HTTP/1.1\r\n" 
        request += "Host: " + host + "\r\n"
        request += "Connection: close\r\n"
        request += "\r\n"
        self.sendall(request)
        buffer = self.recvall(self.socket)
        code = self.get_code(buffer)
        body = self.get_body(buffer)
        self.close()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        parsedUrl = urllib.parse.urlparse(url)
        path = parsedUrl.path
        host = parsedUrl.hostname
        self.connect(host, parsedUrl.port)
        if args == None:
            args = ""
        else:
            args = urllib.parse.urlencode(args)
        request = "POST " + path + " HTTP/1.1\r\n" 
        request += "Host: " + host + "\r\n"
        request += f"Content-Type: application/x-www-form-urlencoded\r\n"
        request += "Content-Length: " + str(len(args)) + "\r\n"
        request += "Connection: close\r\n"
        request += "\r\n"
        request += args
        self.sendall(request)
        buffer = self.recvall(self.socket)
        code = self.get_code(buffer)
        body = self.get_body(buffer)
        self.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))

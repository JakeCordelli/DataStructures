__author__ = 'rosienej'
import threading
import mimetypes
from socket import *


class ProcessRequest (threading.Thread):
    def __init__(self, connectionSocket):
        threading.Thread.__init__(self)
        self.connectionSocket = connectionSocket
    def run(self):
        print ( self.connectionSocket)

        try:
            request = self.connectionSocket.recv(1024)
        except IOError:
            print ( "Server Socket Recv Error")

        if request:
            # https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html
            try:
                [Method,Request_URI,HHTP_Version] = request.split(" ",2)
                print ( Method)
                print ( Request_URI)
                print ( HHTP_Version)
            except ValueError:
                print ( "Request Parse Error:" + request)

            try:
            # https://www.ietf.org/rfc/rfc2396.txt
                [scheme,hier_part]=Request_URI.split(":",1)
                print ( scheme)
                print ( hier_part)
            except ValueError:
                print ( "No Scheme")
                scheme = None
                hier_part = Request_URI

            # more parsing is required but assuming the Request_URI is a path
            print ( "Request URI is: "+hier_part)

            if hier_part == "/":
                hier_part = "/index.html"

            # see if the file is present
            if hier_part != "/":
                try:
                    print ( "Request File is: "+hier_part)
                    fo = open('.'+hier_part,"rb")
                except IOError:
                    # here need to send a 404 error
                    http_status = 'HTTP/1.1 404 Not Found\n'
                    http_content = 'Content-Type: text/html charset=utf-8\n\n'
                    outputdata = 'Bad File'
                else:
                    # right now only file we have is the icon
                    outputdata = fo.read()
                    fo.close()
                    http_status = 'HTTP/1.1 200 OK\n'
                    #here need to guess mime type
                    # https://docs.python.org/2/library/mimetypes.html
                    #http_content = 'Content-Type: image/x-icon\n\n'
                    mimeString,_ = mimetypes.guess_type('.' + hier_part)
                    http_content = 'Content-Type: ' + mimeString +'\n\n'
            else:
                # here we would the contents of index.html
                outputdata = '<!DOCTYPE html><head><meta charset="utf-8">' \
                             +'<title> test </title></head><body><h1>Index File</h1><p>Should be index</p></body></html>'
                http_status = 'HTTP/1.1 200 OK\n'
                http_content = 'Content-Type: text/html charset=utf-8\n\n'

            # send the response header

            self.connectionSocket.send(http_status)
            self.connectionSocket.send('Connection: close\n')
            # https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html Should
            LengthString = 'Content-Length: '+str(len(outputdata))+'\n'
            #connectionSocket.send('Transfer-Encoding: identity\n')
            self.connectionSocket.send(LengthString)
            self.connectionSocket.send(http_content)

            self.connectionSocket.send(outputdata)

           # connectionSocket.shutdown(SHUT_RDWR)
            self.connectionSocket.close()
        else:
            print ( "No Request")




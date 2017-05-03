#-------------------------------------------------------------------------------
# Name:        Hello World Server
# Purpose:
#
# Author:      rosienej
#
# Created:     20/09/2013
# Copyright:   (c) rosienej 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import WebServer

def main():

    myWebServer = WebServer.WebServer(8082)
    myWebServer.start()
    myWebServer = WebServer.WebServer(8081)
    myWebServer.start()

    pass

if __name__ == '__main__':
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-


import BaseHTTPServer
import SimpleHTTPServer
import socket
import mimetypes
import sys
import os
import re
import codecs
import json
import urllib2
import urllib

import parser

PATH = ''
PORT = 8150
baseDir = None
encoding = 'utf-8'

class PrHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    """
    def sendResponseWithOutput(self, response, contentType, body):
        """
        handles both str and unicode types
        """
        self.send_response(response)
        self.send_header("Content-Type", contentType)
        self.send_header("Content-Length", len(body))
        if response == 301:
            self.send_header("Location", body)
        self.end_headers()
        if response != 301:
            self.wfile.write(body)

    def getServerConfig(self , encoding , baseDir):
        path = baseDir + 'server.json'
        if os.path.exists(path):
            f = codecs.open(path , 'r' , encoding)
            serverConfig = f.read()
            f.close()
            return json.loads(serverConfig)
            

    def urlProxy(self , url):
        response = urllib2.urlopen(url)
        contentType = response.info()['Content-Type']
        body = response.read()
        return (contentType,body)

    def pluginsProxy(self , plugins , params):
        print plugins
        try:
            exec("from " + plugins+" import main")
            return main(params)
        except:
            return ('text/html;charset=utf-8' , "Unexpected error:"+ str(sys.exc_info()))
        

    
    def do_GET(self):
        """
        
        Arguments:
        - `self`:
        """
        global encoding
        global baseDir
        truncate_path = self.path.split('?')[0].split('#')[0]
        path_items = self.path.split('?')
        response = 200


        serverConfig = self.getServerConfig(encoding , baseDir)

        isInServerConfig = False
        for reg,target in serverConfig.items():
            if re.search(reg , truncate_path):
                isInServerConfig = True
                if target.startswith('http'):#http url
                    contentType,body =self.urlProxy(target)
                elif target.startswith('plugins'):#local plugins
                    path = ''
                    if( len(path_items) >1 ):
                        path = path_items[1]
                    contentType , body = self.pluginsProxy(target , path)

        if not isInServerConfig:
            if truncate_path.endswith('.pr'):
                contentType = 'application/javascript; charset='+encoding
                package = re.search('\/(\w+?)\.pr' , truncate_path)
                package = package.group(1)
                
                
                p = parser.Parser(baseDir , package , 'local')
                
                body = p.getFile(package).encode(encoding)
            else:
                response, contentType, body = self.server_static(truncate_path) 
        self.sendResponseWithOutput(response , contentType , body)
           
        

    def server_static(self,file_path):
        file_path = '.' + file_path
        if not os.path.exists(file_path):
            return (404, 'text/html', 'no such file, may be your forget add /doc/, for example "/doc/' + file_path + '"')
    
        if os.path.isfile(file_path):
            stat_result = os.stat(file_path)    
            mime_type, encoding = mimetypes.guess_type(file_path)

            file = open(file_path, "rb")
            try:
                return (200, mime_type, file.read())
            finally:
                file.close()
            
        elif os.path.isdir(file_path):
            if file_path.endswith('/'):
                index_file = os.path.join(file_path, 'index.html')
                if os.path.exists(index_file):
                    return (200, 'text/html', open(index_file).read())
                else:
                    return (200 , 'text/html; charset=utf-8' , self.list_directory(os.path.abspath(file_path)).read().encode('utf-8')[150:])
            else:
                return (301, 'text/html', file_path + '/')
        else:
            pass





def setpath(path):
    if os.path.exists(path):
        PATH = path

def setBaseDir(m):
    global baseDir
    baseDir = m


def run(handler_class = PrHandler):
    try:
        httpd = BaseHTTPServer.HTTPServer((PATH, PORT), handler_class)
        print 'server in http://localhost:' + str(PORT) 
        httpd.serve_forever()
    except socket.error:
        print 'may be address already in use'
        print 'you can try another port by use "python localServer.py xxx"'
        sys.exit(1)
        


if __name__ == '__main__':
    if (len(sys.argv) > 1):
        PORT = int(sys.argv[1])
    run()
        


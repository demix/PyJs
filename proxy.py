#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import json
import pprint
import sys
import re
import codecs

import proxy


manifest= None

def getManifest():
    """
    """
    global manifest
    f = codecs.open('manifest.json' , 'r' , 'utf-8')
    manifest = f.read()
    f.close()
    manifest = json.loads(manifest)




if __name__ == '__main__':
    args = sys.argv

    getManifest()

    target = None
    
    if len(args) == 1:
        target = 'build'
        p = proxy.parser.Parser(manifest)
    elif len(args) == 2:
        if args[1] != '*':
            raise Exception('A source must specify build file')
        target = 'build'
        p = proxy.parser.Parser(manifest ,  args[1])
    elif len(args) == 3:
        target = args[2]
        p = proxy.parser.Parser(manifest , args[1] )
    elif len(args) == 4:
        target = args[2]
        p = proxy.parser.Parser(manifest , args[1] , args[3])

        
    p.write(target)

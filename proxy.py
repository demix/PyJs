#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import json
import pprint
import sys
import re
import codecs
import os


import proxy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  + os.sep



if __name__ == '__main__':
    args = sys.argv


    target = None

    
    if len(args) >1 and args[1] == 'runserver':
        proxy.localserver.setpath(BASE_DIR)
        proxy.localserver.setBaseDir(BASE_DIR)
        proxy.localserver.run()
    else:
        if len(args) == 1:
            target = 'build'
            p = proxy.parser.Parser(BASE_DIR )
        elif len(args) == 2:
            if args[1] != '*':
                raise Exception('A source must specify build file')
            target = 'build'
            p = proxy.parser.Parser(BASE_DIR  ,  args[1])
        elif len(args) == 3:
            target = args[2]
            p = proxy.parser.Parser(BASE_DIR , args[1] )
        elif len(args) == 4:
            target = args[2]
            p = proxy.parser.Parser(BASE_DIR , args[1] , args[3])
        p.write(target)

        

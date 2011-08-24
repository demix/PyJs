#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import json
import pprint
import sys
import re
import codecs
import os


import pyjs

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  + os.sep



if __name__ == '__main__':
    args = sys.argv


    target = None

    
    if len(args) >1 and args[1] == 'runserver':
        pyjs.localserver.setpath(BASE_DIR)
        pyjs.localserver.setBaseDir(BASE_DIR)
        pyjs.localserver.run()
    else:
        if len(args) == 1:
            target = 'build'
            p = pyjs.parser.Parser(BASE_DIR )
        elif len(args) == 2:
            target = 'build'
            p = pyjs.parser.Parser(BASE_DIR , '*'  ,  args[1])
        p.write(target)

#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import re
import codecs
import utils
import os
import json


class Parser():
    REPLACE_TOKEN = re.compile('%#(\w+)#%')
    """
    """
    
    def __init__(self , manifest , package = '*' ,  replace='online' ):
        """
        """
        self._encoding = 'utf-8'
        self._manifest = manifest
        self._package = package
        self._replace = replace
        self._getManifest()


        self._js = {}
        self._css = {}

        self.parseJs(self._package)
        self.replace()

        

    def _getManifest(self):
        """
        """
        if 'charset' in self._manifest:
            self._encoding = self._manifest['charset']
        

    def parseJs(self , package):
        """
        """
        if( package == '*' ):
            for i in self._manifest['sources']:
                self.parseJs(i)
        else:
            files = self._manifest['sources'][package]
            for i in files:
                f = codecs.open(i , 'r' , self._encoding)

                if not package in self._js:
                    self._js[package] = ''
                
                self._js[package] = self._js[package] + f.read()
                f.close()
            self.parseCss(package)

    def parseCss(self , package):
        if package in self._manifest['css']:
            files = self._manifest['css'][package]
            for i in files:
                f = codecs.open(i , 'r' , self._encoding)
                if not package in self._css:
                    self._css[package] = ''
                self._css[package] = self._css[package] + f.read()

            if len(self._css[package]) and 'method' in self._manifest['css']:
                self._css[package]= self._manifest['css']['method'] + '(' + json.dumps(self._css[package]) + ", ['" + package + "']);"
                
    def replace(self,):
        """
        """
        replace_targets = self._manifest['replace'][self._replace]

        def _replace(match):
            """
            """
            return replace_targets[match.group(1)]

        for i in self._js:
            self._js[i] = Parser.REPLACE_TOKEN.sub(_replace , self._js[i])



    def getFiles(self):
        return ''

    def getFile(self , package):
        """
        
        Arguments:
        - `self`:
        """
        code = ''
        if package in self._js:
            code = code + self._js[package]
        if package in self._css:
            code = code + self._css[package]
        return code


    def write(self , tfile , package=None):
        """
        
        Arguments:
        - `self`:
        """
        if package == None:
            package = self._package
            
        if package == '*':
            utils.rm(tfile)
            os.mkdir(tfile)
            
            for i in self._js:
                self.write(os.path.basename(tfile) + os.sep + i + '.js' , i)
                

            
        else:
            f = codecs.open(tfile , 'w' , self._encoding)
            f.write(self.getFile(package))
            f.close()



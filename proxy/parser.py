#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import re
import codecs
import utils
import os


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
        return self._js

    def getFile(self , package):
        """
        
        Arguments:
        - `self`:
        """
        if package in self._js:
            return self._js[package]


    def write(self , file , package=None):
        """
        
        Arguments:
        - `self`:
        """
        if package == None:
            package = self._package
            
        if package == '*':
            utils.rm(file)
            os.mkdir(file)
            
            for i in self._js:
                self.write(os.path.basename(file) + os.sep + i + '.js' , i)
                

            
        else:
            f = codecs.open(file , 'w' , self._encoding)
            f.write(self._js[package])
            f.close()



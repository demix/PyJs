#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import re
import codecs


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


        self._js = ''
        self._css = ''

        self.parseJs()
        self.replace()

        

    def _getManifest(self):
        """
        """
        if 'charset' in self._manifest:
            self._encoding = self._manifest['charset']
        

    def parseJs(self):
        """
        """
        if( self._package == '*' ):
            print 1
        else:
            package = self._manifest['sources'][self._package]
            for i in package:
                f = codecs.open(i , 'r' , self._encoding)
                self._js = self._js + f.read()
                f.close()
                
    def replace(self,):
        """
        """
        replace_targets = self._manifest['replace'][self._replace]

        def _replace(match):
            """
            """
            return replace_targets[match.group(1)]

        self._js = Parser.REPLACE_TOKEN.sub(_replace , self._js)



    def getFile(self):
        return self._js

    def write(self , file):
        """
        
        Arguments:
        - `self`:
        """
        f = codecs.open(file , 'w' , self._encoding)
        f.write(self._js)
        f.close()



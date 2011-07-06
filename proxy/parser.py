#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import re
import codecs
import utils
import os
import json


class Parser():
    REPLACE_TOKEN = re.compile('%#(\w+)#%')
    INJECT_TOKEN = re.compile('#%(\w+)%#')
    PARENT_TOKEN = re.compile('@template')
    DEF_TARGET_TOKEN = re.compile('##(\w+)##')
    DEF_TOKEN = re.compile('@define\s+(\w+)\s*(\w+)\s*[\s\r\n]')
    FILE_TOKEN = re.compile('##file##')
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
        self.inject()

        

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

                file_content = f.read();
                f.close()

                if 'parent' in self._manifest and Parser.PARENT_TOKEN.search(file_content):
                    parent_file  = codecs.open(self._manifest['parent'] , 'r' , self._encoding)
                    parent = parent_file.read()
                    parent_file.close()
                    file_content = self.parseParent(parent , file_content)
                
                self._js[package] = self._js[package] + file_content
            self.parseCss(package)

    def parseParent(self , parent , child):
        child = Parser.FILE_TOKEN.sub(child , parent)
        
        defs = Parser.DEF_TOKEN.findall(child)

        def _replace(match):
            for item in defs:
                if item[0] == match.group(1):
                    return item[1]
        
        child = Parser.DEF_TARGET_TOKEN.sub(_replace , child)
            
        return child
        

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

    def inject(self , ):
        if not 'file_inject' in self._manifest:
            return

        def _replace(match):
            target = match.group(1)
            if target in self._manifest['file_inject']:
                tfile = self._manifest['file_inject'][target]
                f = codecs.open(tfile , 'r' , self._encoding)
                return f.read()


        for i in self._js:
            self._js[i] = Parser.INJECT_TOKEN.sub(_replace , self._js[i])


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



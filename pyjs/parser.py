#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import re
import codecs
import utils
import os
import json
import time


class Parser():
    REPLACE_TOKEN = re.compile('%#(\w+)#%')
    INJECT_TOKEN = re.compile('#%(\w+)%#')
    DEF_TARGET_TOKEN = re.compile('##(\w+)##')
    FILE_TOKEN = re.compile('##file##')
    PACKAGE_FILE = "__init__.js"
    BOOT_FILE = "boot.js"
    REQUIRE_TOKEN = re.compile("require\([\'\"](\w+)[\'\"]\)")
    """
    """
    
    def __init__(self , baseDir  , package = '*' ,  replace='online' ):
        """
        """
        self._baseDir = baseDir
        self._encoding = 'utf-8'
        self._package = package
        self._replace = replace
        self._manifest = None
        self._getManifest()


        self._js = {}
        self._css = {}

        self.parseJs(self._package)
        self.replace()
        self.inject()

        

    def _getManifest(self):
        """
        """
        f = codecs.open(self._baseDir + 'manifest.json' , 'r' , self._encoding)
        manifest = f.read()
        f.close()
        manifest = json.loads(manifest)

        self._manifest = manifest
        
        if 'charset' in manifest:
            self._encoding = manifest['charset']

        if 'pyjsdir' in manifest:
            self._srcDir = manifest['pyjsdir'] + os.sep
        else:
            self._srcDir = 'src/'
        

    def parseJs(self , package):
        """
        """
        targetDir = self._baseDir + self._srcDir 
        if( package == '*' ):
            nlist = os.listdir(targetDir)

            for name in nlist:
                if os.path.isdir(targetDir + name):
                    self.parseJs(name)
                elif os.path.isfile( targetDir + name ):
                    name = name.replace('.js' , '')
                    self.parseJs(name)
            
        else:
            file_content = ''
            if not package in self._js:
                self._js[package] = ''
                
            if os.path.isfile(targetDir+package + '.js'):
                f = codecs.open(targetDir + package + '.js')
                file_content = file_content + '\n' + f.read()
                f.close()
                file_content = self.parseParent( file_content , package )

            else:
                targetDir = targetDir + package + os.sep

                if( not os.path.exists(targetDir + Parser.PACKAGE_FILE) ):
                    print 'no package file found.'
                    return

                
                initFile = codecs.open(targetDir + Parser.PACKAGE_FILE)
                initFileSource = initFile.read();
                initFile.close();

                exec(initFileSource)

                for i in __all__:
                    f = codecs.open(targetDir + i + '.js')
                    file_content = file_content + '\n' + f.read()
                    f.close()

                if not '__unextends__' in locals().keys() or  not __unextends__:  #继承
                    defs = locals()
                    file_content = self.parseParent( file_content ,  package , defs)
                        
            self._js[package] = self._js[package] + file_content


    def parseParent(self  , child , package , defs = {} ):
        if not 'parent' in self._manifest:
            return child
        
        parent_file  = codecs.open( self._baseDir + self._manifest['parent'] , 'r' , self._encoding)
        parent = parent_file.read()
        parent_file.close()
        #保留字
        defs['package'] = package
        
        child = Parser.FILE_TOKEN.sub(child , parent)

        def _replace(match):
            for item,value in defs.items():
                if item == match.group(1):
                    return value
        
        child = Parser.DEF_TARGET_TOKEN.sub(_replace , child)
            
        return child
        

    def parseCss(self , package):
        if 'css' in self._manifest and package in self._manifest['css']:
            files = self._manifest['css'][package]
            for i in files:
                f = codecs.open(self._baseDir + i , 'r' , self._encoding)
                if not package in self._css:
                    self._css[package] = ''
                self._css[package] = self._css[package] + f.read()

            if len(self._css[package]) and 'method' in self._manifest['css']:
                self._css[package]= self._manifest['css']['method'] + '(' + json.dumps(self._css[package]) + ", ['" + package + "']);"
                
    def replace(self,f=''):
        """
        """
        if not 'replace' in self._manifest:
            return
        
        replace_targets = self._manifest['replace'][self._replace]

        def _replace(match):
            """
            """
            return replace_targets[match.group(1)]

        if len(f):
            return Parser.REPLACE_TOKEN.sub(_replace , f)
        else:
            for i in self._js:
                self._js[i] = Parser.REPLACE_TOKEN.sub(_replace , self._js[i])

    def inject(self , ):
        if not 'file_inject' in self._manifest:
            return

        def _replace(match):
            target = match.group(1)
            if target in self._manifest['file_inject']:
                tfile = self._manifest['file_inject'][target]
                f = codecs.open(self._baseDir + tfile , 'r' , self._encoding)
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
                

            self.jsdoc( tfile )
            self.addboot( tfile )
        else:
            f = codecs.open(tfile , 'w' , self._encoding)
            f.write(self.getFile(package))
            f.close()
            self.lint(tfile)

    def addboot(self , tdir):
        dependency = {}
        for package,js in self._js.items():
            dependency[package] = self._analyse(js)
            dependency[package] = list(set(dependency[package]))

        f = codecs.open(self._baseDir + 'lib/dep_tpl.js' , 'r' , self._encoding)
        dep_tpl = f.read()
        f.close()

        boot = ''
        for item,value in dependency.items():
            temp_str = re.sub( '##package##' , item , dep_tpl  )
            temp_str = re.sub( '##dependence##' , ','.join(value) , temp_str )
            boot = boot + temp_str

        f = codecs.open(self._baseDir + 'lib/pyjs.js' , 'r' , self._encoding)
        boot = f.read() + '\n' + boot
        f.close()

        #替换build
        boot = re.sub('##build##' ,  time.strftime('%Y%m%d') , boot);

        #替换combourl
        combo_url = ''
        if 'combo' in self._manifest:
            combo_url = self._manifest['combo']['combo_url']
            
        boot = re.sub('##combo_url##' ,  combo_url , boot);
        boot = re.sub('##version##' ,  self._manifest['version'] , boot);
        boot = self.replace(boot)

        f = codecs.open(tdir + os.sep + 'boot.js' , 'w' , self._encoding)
        f.write(boot)
        f.close()



    def _analyse(self , js):
        deps = Parser.REQUIRE_TOKEN.findall(js)
        return deps
        

    def lint(self , file):
        print 'jslint ing...'
        #os.system('python '+ self._baseDir +'tools/closure_linter/gjslint.py --nojsdoc '  + file);


    def jsdoc(self , dir):
        print 'jsdoc ing...'
        #os.system('java -jar '+ self._baseDir +'tools/jsdoc/jsrun.jar '+ self._baseDir +'tools/jsdoc/app/run.js -a -t='+ self._baseDir +'tools/jsdoc/templates/jsdoc -d=doc ' + dir)

/*
 * package.js
 * A js toolkit for PyJsDoc
 * @author demixcn@gmail.com
 */


(function(ns){
    
    var page_modules = {};
    
    var existing_modules = {};
    
    
    var getXHR = function(){
        if (window.ActiveXObject) {
            try {
                return new ActiveXObject("Msxml2.XMLHTTP");
            } catch (e) {
                try {
                    return new ActiveXObject("Microsoft.XMLHTTP");
                } catch (e) {}
            }
        }
        if (window.XMLHttpRequest) {
            return new XMLHttpRequest();
        }
    };
    
    var getScript = function(url , cb){
        var xhr = getXHR();
        xhr.open('GET' , url , false);
        
        xhr.send();
        if(xhr.readyState == 4 && xhr.status == 200){
            eval(xhr.responseText);
        }
    };

    var define = function(module , declare){
        page_modules[module] = declare;
    };

    var require = function(md){
        if( !existing_modules[md] ){
            getScript('/' + md + '.js');
        }
        


        var declare = page_modules[md];
        var exports = {};
        var module = '';
        
        declare(require , exports , module );
        
        return exports;
    };




    ns.define = define;
    ns.require = require;

})(this);


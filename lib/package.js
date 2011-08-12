/*
 * package.js
 * A js toolkit for PyJsDoc
 * @author demixcn@gmail.com
 */


(function(ns){
    
    var BUILD = '##build##';
    var COMBO_URL = "##combo_url##";
    var VERSION = '##version##';
    
    var isIE = /*@cc_on!@*/false;
    
    var page_modules = {};
    
    var dependencies = {};
    
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
    
    var getXdScript = function(src, cb){
        var scrElement;
        var scrElements = document.getElementsByTagName('script');
        if( scrElements ){
            scrElement = document.createElement('script');

            scrElement.onload = scrElement.onreadystatechange = function(){
                var readyState = scrElement.readyState;
                if ('undefined' == typeof readyState
                    || readyState == "loaded"
                    || readyState == "complete") {
                    try {
                        cb && cb();
                    } finally {
                        scrElement.onload = scrElement.onreadystatechange = null;
                    }
                }                
            };

            scrElement.async = true;
            scrElement.src = src;
            scrElement.charset = 'utf-8';
            scrElements[0].parentNode.appendChild(scrElement);
        }
        
    };
    
    
    var prefetchScript = function(urls , cb){
        var current_deps = [].slice.call(urls);
        urls = [].slice.call(urls);
        var callback = function(url){
            if( current_deps.indexOf(url) != -1 ){
                current_deps.splice(current_deps.indexOf(url) , 1);
            }
            if(current_deps.length == 0){
                cb && cb();
            }
        };

        for( var i=0,l=urls.length; i<l; i++ ){
            var elTrigger = null;
            if (isIE) {
                elTrigger = new Image();
                elTrigger.onload = (function(url , elTrigger){
                    return function(){
                        callback(url);
                        elTrigger.onload = null;
                        elTrigger = null;
                    };
                })(urls[i] , elTrigger);
                elTrigger.src = urls[i];
                return;
            }
            elTrigger = document.createElement('object');
            elTrigger.data = urls[i]; 
            
            elTrigger.width  = 0;
            elTrigger.height = 0;
            
            elTrigger.onload = (function(url , elTrigger){
                return function(){
                    callback(url);
                    elTrigger.onload = null;
                    elTrigger.parentNode.removeChild(elTrigger);
                    elTrigger = null;
                };
            })(urls[i] , elTrigger);
            
            document.body.appendChild(elTrigger);
        }
    };

    var define = function(module , declare){
        page_modules[module] = declare;
    };
    
    var use = function(md , cb){
        var deps = getDependence(md);
        if( +BUILD > 0 ){//编译之后
            if( COMBO_URL.length ){//有combo的情况
                for( var i =0, l= deps.length ; i<l ; i++ ){
                    deps[i] = VERSION + '/' + deps[i] + '.js';
                }
                var js = deps.join('&');
                getXdScript( COMBO_URL + js  , function(){
                    cb && cb(require(md));
                });
            }else{
                for( var i =0, l= deps.length ; i<l ; i++ ){
                    deps[i] = '%#js_url#%'  + deps[i] + '.js';
                }
                
                var getAllScript = function(){
                    if( deps.length ){
                        var url = deps.shift();
                        getXdScript(url , function(){
                            getAllScript();
                        });
                    }else{
                        cb && cb(require(md));
                    }
                };

                prefetchScript(deps , function(){
                    getAllScript();
                });
            }
        }
    };

    var require = function(md){
        if( !page_modules[md] ){
            getScript('/' + md + '.js');
        }

        var declare = page_modules[md];
        var exports = {};
        var module = '';
        
        declare(require , exports , module );
        
        return exports;
    };
    
    var addDependence = function(pkg  ,deps){
        dependencies[pkg] = deps.split(',');
    };
    
    var getDependence = function(pkg){
        var deps = dependencies[pkg] || [];
        var final_deps = [].slice.call(deps);
        for( var i=0 , l=deps.length ; i<l; i++ ){
            var rs = getDependence(deps[i]);
            for ( var j=0,k=rs.length ; j<k; j++ ){
                if( final_deps.indexOf(rs[j]) == -1 && rs[j].length){
                    final_deps.unshift(rs[j]);
                }
            }
        }
        final_deps.push(pkg);
        return final_deps;
    };


    ns.define = define;
    ns.require = require;
    ns.addDependence = addDependence;
    ns.getDependence = getDependence;
    ns.use = use;

})(this);


var baidu = baidu || {};
baidu.more = baidu.more || {};

/**
 * 使用 style 标签添加一段stylesheet
 * @function
 * @name baidu.more.addCssRules
 * @param styles {string} 样式
 * @param names {array} 样式的name值
 */
baidu.more.addCssRules = function(styles, names) {
    if (!baidu.more.addCssRules._cssRules) {
        baidu.more.addCssRules._cssRules = {};
    }

    // note, we potentially re-include CSS if it comes with other CSS that we
    // have previously not included.
    var allIncluded = true;
    baidu.each(names, function(id) {
        if (!(id in baidu.more.addCssRules._cssRules)) {
            allIncluded = false;
            baidu.more.addCssRules._cssRules[id] = true;
        }
    });

    if (allIncluded) {
        return;
    }

    if (!baidu.browser.ie) {
        var style = document.createElement('style');
        style.type = 'text/css';
        style.textContent = styles;
        document.getElementsByTagName('HEAD')[0].appendChild(style);
    } else {
        try {
            document.createStyleSheet().cssText = styles;
        } catch (exc) {
            // major problem on IE : You can only create 31 stylesheet objects with
            // this method. We will have to add the styles into an existing
            // stylesheet.
            if (document.styleSheets[0]) {
                document.styleSheets[0].cssText += styles;
            }
        }
    }
};


// **********************
// This is a modified version of the NYT code.
// **********************

// only want one resizer on the page
if (document.documentElement.className.indexOf("g-resizer-v3-init") > -1) {
    console.error('TOO MANY')
} else {
    document.documentElement.className += " g-resizer-v3-init";
}
// require IE9+
// if (!("querySelector" in document)) return;

function resizer() {
    console.log('resizer triggered');
    var elements = Array.prototype.slice.call(document.querySelectorAll(".g-artboard[data-min-width]")),
        widthById = {};
    elements.forEach(function(el) {
        var parent = el.parentNode,
            width = widthById[parent.id] || parent.getBoundingClientRect().width,
            minwidth = el.getAttribute("data-min-width"),
            maxwidth = el.getAttribute("data-max-width");
        widthById[parent.id] = width;
        if (+minwidth <= width && (+maxwidth >= width || maxwidth === null)) {
            el.style.display = "block";
        } else {
            el.style.display = "none";
        }
    });
    // pymChild.sendHeight();
}
 


function throttle(func, wait) {
    // from underscore.js
    var _now = Date.now || function() { return new Date().getTime(); },
        context, args, result, timeout = null, previous = 0;
    var later = function() {
        previous = _now();
        timeout = null;
        result = func.apply(context, args);
        if (!timeout) context = args = null;
    };
    return function() {
        var now = _now(), remaining = wait - (now - previous);
        context = this;
        args = arguments;
        if (remaining <= 0 || remaining > wait) {
            if (timeout) {
                clearTimeout(timeout);
                timeout = null;
            }
            previous = now;
            result = func.apply(context, args);
            if (!timeout) context = args = null;
        } else if (!timeout && options.trailing !== false) {
            timeout = setTimeout(later, remaining);
        }
        return result;
    };
}
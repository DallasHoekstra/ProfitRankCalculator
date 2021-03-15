window.onload = highlightData("red", "green");

MutationObserver = window.MutationObserver || window.WebKitMutationObserver;

var observer = new MutationObserver(function(mutations, observer) {
    highlightData("yellow", "blue");
    collectAndCleanData();

    // console.log(mutations, observer);
});

// define what element should be observed by the observer
// and what types of mutations trigger the callback
observer.observe(document, {
  subtree: true,
  childList: true
});

function highlightData(color1, color2) {
    var firstHref = $("span").css("background-color", color1);
    firstHref.children().css("background-color", color2);
    
}

function collectAndCleanData() {
    statsBar = document.getElementById("xt-info");
    
    // console.log(statsBar != null)
    if (statsBar != null) {
        console.log(statsBar)
    }
}
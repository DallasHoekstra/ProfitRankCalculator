// window.onload = highlightData("red", "green");

MutationObserver = window.MutationObserver || window.WebKitMutationObserver;

var observer = new MutationObserver(function(mutations, observer) {
    // highlightData("yellow", "blue");
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

        extractedStats = extractStatsBar(statsBar);
        processedStats = processStats(extractedStats);
    }
}

function extractStatsBar(statsBar) {
    statsStringObject = {}
    $.extend(statsStringObject, statsBar);
    return statsStringObject.innerText;
}

function processStats(extractedStats) {
        
    categories = extractedStats.split("|")

    avgMonthlyVolume = categories[0].split(":"); // "Volume: [number]/month"
    avgMonthlyVolume = avgMonthlyVolume[1].split("/"); // [number]/month
    avgMonthlyVolume = avgMonthlyVolume[0]; // [number]

    cpc = categories[1].split(":") // "CPC: [dollars.cents]"
    cpc = cpc[1] // "[dollars.cents]"
    
    competition = categories[2].split(":"); // "Competition: [decimal]"
    competition = competition[1] // [decimal]

    processedData = {
        "Volume": avgMonthlyVolume,
        "cpc": cpc,
        "Competition": competition 
    };

    return processedData;
}
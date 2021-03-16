MutationObserver = window.MutationObserver || window.WebKitMutationObserver;

var observer = new MutationObserver(function(mutations, observer) {
    keywordVolumeByRank = clicksAtRank();
    keyword = retrieveKeywords();
    if (keywordVolumeByRank && keyword) {
        // localStorage.setItem(keyword, keywordVolumeByRank);
        dataObject = {
            "keyword": keyword,
            "keywordVolumeByRank": keywordVolumeByRank
        };
        // prepend filename with KWP- to separate from other files for easy automated processing
        filename = "KWP-" + keyword;

        downloadKeywordAndRankData(dataObject, filename);
    }

});

observer.observe(document, {
  subtree: true,
  childList: true
});

function retrieveKeywords() {
    keywordTag = document.getElementsByTagName("input")[0];
    if (keywordTag.value !== '') {
        return keywordTag.value;
    } 
}

function clicksAtRank() {
    cleanedData = collectAndCleanData();

    if (cleanedData != false) {
        avgMonthlyVolume = parseInt(cleanedData.Volume, 10);

        percentAtRank = [.3802, .1246, .0767, .0506, .0144, .0163, .0145, .0106, .01, .0113];
        volumeAtRank = [];
        for (i = 0; i < percentAtRank.length; i++) {
            volumeAtRank.push(Math.trunc(avgMonthlyVolume*percentAtRank[i]));
        }
        return volumeAtRank;
    }

    return false;
}

function collectAndCleanData() {
    statsBar = document.getElementById("xt-info");
    
    if (statsBar != null) {
        extractedStats = extractStatsBar(statsBar);
        processedData = processStats(extractedStats);
        return processedData;
    }
    else {
        return false;
    }
}

function extractStatsBar(statsBar) {
    statsStringObject = {}
    $.extend(statsStringObject, statsBar);
    return statsStringObject.innerText;
}

function processStats(extractedStats) {
        
    categories = extractedStats.split("|")

    avgMonthlyVolume = categories[0].split(":"); // "Volume: [number,number]/month"
    avgMonthlyVolume = avgMonthlyVolume[1].split("/"); // [number,number]/month
    avgMonthlyVolume = avgMonthlyVolume[0]; // [number,number]
    avgMonthlyVolume = avgMonthlyVolume.split(",");
    avgMonthlyVolume[0] = parseInt(avgMonthlyVolume[0]);
    while (avgMonthlyVolume.length > 1) {
        avgMonthlyVolume[0] = avgMonthlyVolume[0]*1000;
        avgMonthlyVolume.pop();
    }

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


function highlightData(color1, color2) {
    var firstHref = $("span").css("background-color", color1);
    firstHref.children().css("background-color", color2);
    
}

function downloadKeywordAndRankData(data, filename){
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));
    var autoDownloadLink = document.createElement('a');
    autoDownloadLink.setAttribute("href", dataStr);
    autoDownloadLink.setAttribute("download", filename + ".json");
    document.body.appendChild(autoDownloadLink); // required for firefox
    autoDownloadLink.click();
    autoDownloadLink.remove();
}
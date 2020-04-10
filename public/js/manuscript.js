
/* Controls flipping through the manuscript exhibit page. */

var currPage = 10;
var currLetter = 'R'

window.onload = function() { currPage -= 0.5; currLetter = (currLetter == 'R' ? 'V' : 'R');  this.nextPage() };

function nextPage() {
    currPage += 0.5
    currLetter = (currLetter == 'R' ? 'V' : 'R')
    reqFile = 'ARC_manuscript_1_'+String(Math.floor(currPage))+ currLetter 
    console.log(reqFile)
    replaceContent(reqFile)
}
function prevPage() {
    currPage -= 0.5
    currLetter = (currLetter == 'R' ? 'V' : 'R')
    reqFile = 'ARC_manuscript_1_'+String(Math.floor(currPage))+ currLetter
    console.log(reqFile)
    replaceContent(reqFile)
}

//ARC_manuscript_1_11R.JPG

function replaceContent(reqFile) {
    // I'im sticking to the basic swap for now. Might implement carousel
    $('#manu-img').attr('src', '/img/script-imgs/' + reqFile + '.jpg');
    $('#transc-cont').load('/transcriptions/' + reqFile + '.html', function() {
        // Set up the tooltips for incoming abbreviations
        $('[data-toggle="tooltip"]').tooltip();
    });

    // Trying a fancy fade in and out
    /*$("#manu-img").fadeOut("slow",function(){
        console.log('faded out')
        $("#manu-img").on('load', function () { //avoiding blinking, wait until loaded
            $("#manu-img").fadeIn();
        });
        $("#manu-img").attr("src","/img/script-imgs/" + reqFile);
    });*/
}


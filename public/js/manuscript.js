
/* Controls flipping through the manuscript exhibit page. */

var currPage = 1;
var currLetter = 'V';

window.onload = function() { 
    currPage -= 0.5;
    currLetter = (currLetter == 'R' ? 'V' : 'R');
    this.nextPage();

    // Open introduction modal immediately
    $('#intro-modal').modal('show');

    $('#help-button').click(function() {
        $('#intro-modal').modal('show');
    });

    // Open modal when manuscript image is clicked
    $("#img-cont").on("click", function() {
        console.log('clicked');
        $('#imagepreview').attr('src', $('#manu-img').attr('src')); // here asign the image to the modal when the user click the enlarge link
        $('#imagemodal').modal('show'); // imagemodal is the id attribute assigned to the bootstrap modal, then i use the show function
     });

};

function nextPage() {
    currPage += 0.5;
    currLetter = (currLetter == 'R' ? 'V' : 'R');
    reqFile = 'ARC_manuscript_1_'+String(Math.floor(currPage))+ currLetter;
    console.log(reqFile);
    replaceContent(reqFile);
}
function prevPage() {
    currPage -= 0.5;
    currLetter = (currLetter == 'R' ? 'V' : 'R');
    reqFile = 'ARC_manuscript_1_'+String(Math.floor(currPage))+ currLetter;
    console.log(reqFile);
    replaceContent(reqFile);
}

function replaceContent(reqFile) {
    // I'im sticking to the basic swap for now. Might implement carousel
    $('#manu-img').attr('src', '/img/script-imgs/' + reqFile + '.jpg');
    $('#transc-cont').load('/transcriptions/' + reqFile + '.html', function() {
        // Set up the tooltips for incoming abbreviations
        $('[data-toggle="tooltip"]').tooltip();
    });
    $('#page-number').html('Page '+ reqFile.replace('ARC_manuscript_1_',''));

    // Fancy fade in and out
    /*$("#manu-img").fadeOut("slow",function(){
        console.log('faded out')
        $("#manu-img").on('load', function () { //avoiding blinking, wait until loaded
            $("#manu-img").fadeIn();
        });
        $("#manu-img").attr("src","/img/script-imgs/" + reqFile);
    });*/
}

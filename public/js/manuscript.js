/* This script controls flipping through the manuscript exhibit page. */

var currPage = 1;
var currLetter = 'R';
const pageMax = 65;
const pageMin = 1;

window.onload = function () {
    currPage -= 0.5;
    currLetter = (currLetter == 'R' ? 'V' : 'R');
    this.nextPage();

    // Open introduction modal immediately
    $('#intro-modal').modal('show');

    $('#help-button').click(function () {
        $('#intro-modal').modal('show');
    });

    // Open modal when manuscript image is clicked
    $("#img-cont").on("click", function () {
        $('#imagepreview').attr('src', $('#manu-img').attr('src'));
        $('#imagemodal').modal('show');
    });

    populatePageSelector();

    $('#page-selector-dropdown a').click(function (e) {
        var sVal = e.currentTarget.text;
        console.log(sVal);
        sVal.includes('V') ? currLetter = 'V' : currLetter = 'R';
        currPage = Number(sVal.replace('V', '').replace('R', ''));
        reqFile = 'ARC_manuscript_1_' + String(currPage) + currLetter;
        replaceContent(reqFile);
    });
};

/* Hide prev/next button on first/last page */
function checkEdges() {
    if (currPage == pageMin) {
        $('#prev-button').hide();
    } else if (currPage >= pageMax) {
        $("#next-button").hide();
    } else {
        $("#prev-button").show();
        $("#next-button").show();
    }
}

function nextPage() {
    currPage += 0.5;
    checkEdges();
    if (currPage > pageMax) {
        currPage = pageMax;
        return;
    }
    currLetter = (currLetter == 'R' ? 'V' : 'R');
    reqFile = 'ARC_manuscript_1_' + String(Math.floor(currPage)) + currLetter;
    replaceContent(reqFile);
}
function prevPage() {
    currPage -= 0.5;
    checkEdges();
    if (currPage < pageMin) {
        currPage = pageMin;
        return;
    }
    currLetter = (currLetter == 'R' ? 'V' : 'R');
    reqFile = 'ARC_manuscript_1_' + String(Math.floor(currPage)) + currLetter;
    replaceContent(reqFile);
}

function replaceContent(reqFile) {
    $('#manu-img').attr('src', '/img/script-imgs/' + reqFile + '.jpg');
    $('#transc-cont').load('/transcriptions/' + reqFile + '.html', function () {
        // Set up the tooltips for incoming abbreviations
        $('[data-toggle="tooltip"]').tooltip();
    });
    $('#page-number').text('Folio ' + reqFile.replace('ARC_manuscript_1_', ''));
}

function populatePageSelector() {
    pageNum = 0.5;
    pageLetter = 'V'; // Immediately flips to R on first iteration
    pageSel = ''
    while (pageNum <= 65.5) {
        pageLetter = (pageLetter == 'V' ? 'R' : 'V');
        pageNum += 0.5;
        pageName = String(Math.floor(pageNum)) + pageLetter;
        pageSel += '<a class="dropdown-item">' + pageName + '</a>';
    }
    $('#page-selector-dropdown').html(pageSel);
}

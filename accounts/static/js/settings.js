var mobileNavOpen = false;

$('#mobileNavOpenButton').click(function(event) {
    event.stopPropagation(); // Stop event propagation
    openSideNavbar();
    mobileNavOpen = true;
    //console.log("mobileNavOpen: " + mobileNavOpen);
});

$(document).on('click', function(event) {
    if (!$(event.target).closest('#sideNavbar').length && !$(event.target).is('#mobileNavOpenButton') && mobileNavOpen) {
        closeSideNavbar();
        mobileNavOpen = false;
        //console.log("mobileNavOpen: " + mobileNavOpen);
    }
});

$(window).on('resize', function() {
    if ($(window).width() > 991) {
        closeSideNavbar();
        $('#sideNavbar').show();
        $('#mobileNavOpenButton').hide();
        mobileNavOpen = false;
        //console.log("mobileNavOpen: " + mobileNavOpen);
    } else {
        $('#mobileNavOpenButton').show();
        $('#sideNavbar').hide();
    }
});

function openSideNavbar() {
    $('#mobileNavOpenButton').hide();
    $('#sideNavbar').css('z-index', '1000');
    $('#sideNavbar').show().animate({left:'0'}, 500);
    $('#pageContent').css('background-color', 'rgba(0,0,0,0.4)');
}

function closeSideNavbar() {
    $('#sideNavbar').hide();
    $('#pageContent').css('background-color', 'transparent');
    $('#mobileNavOpenButton').show();
}

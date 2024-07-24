$(document).ready(function() {
    $('.sidebar-toggle').on('click', function() {
        $('.overlay').toggle();
        $('.side-navbar-mobile-list-container').toggle();
        $('.side-navbar-mobile-list-container').animate({
            'width': '60%'
        }, {
            duration: 340, 
        });
    });

    $('.overlay').on('click', function(e) {
        //$('.side-navbar-mobile-list-container').toggle();
        if (!$(e.target).is('.side-navbar-mobile-list-container')) {
            $('.side-navbar-mobile-list-container').animate({
                'width': '0%'
            }, {
                duration: 340, 
                complete: function() {
                    $('.overlay').toggle(); 
                    $('.side-navbar-mobile-list-container').toggle();
                }
            });
        }
    });
});


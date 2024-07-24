
function dropdownAuto() {
    
}


$(document).ready(function() {
    $('.switch-form-link').on('click', function() {
        if ( $('.login-form').css('display') == 'none') {
            $('.signup-form').fadeOut(100, 'linear', function() {
                $('.login-form').fadeIn();
            });
        } else {
            $('.login-form').fadeOut(100, 'linear', function() {
                $('.signup-form').fadeIn();
            });
        }
    })
})
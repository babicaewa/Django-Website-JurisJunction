function renderCaptchas() {
    var params = {
        "sitekey": "ea26674e-0527-405c-90d4-fecd46e24062",
        "theme": "light"
    }
    reviewWidgetId = hcaptcha.render('reviewCaptcha', params);
}

$(document).ready(function() {
    renderCaptchas();
})
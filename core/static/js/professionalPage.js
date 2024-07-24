var contactWidgetId, reviewWidgetId, starValue, professional_pk;

var dateFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    hour12: true,
  };

professional_pk = $('#professional').data('pk');

//console.log(professional_pk);

reviewsStarsInit('.rating-star');
reviewsStarsInit('.review-star');


fetchReviews(false);

function fetchReviews(new_review) {
    var professional_pk = $('#professional').data('pk');
    var delay = 0;

    $.ajax({
        type: 'GET',
        url: '/get_reviews/',
        data: {
            professional_pk: professional_pk
        },
        success: function(response) {
            //console.log("it worked");
            //console.log(response);
            // Clear existing reviews
            $('#reviews-container').empty();

            if (response.reviews.length > 0) {
                // Hide existing reviews before appending new ones
                $('#reviews-container .review-card').hide();
            
                if (new_review) {
                    response.reviews.forEach(function(review, index) {
                        var reviewHtml = generateReviewHtml(review);
                        if (index == 0) {
                            var $reviewCard = $(reviewHtml).appendTo('#reviews-container').css('opacity', 0);
                        } else {
                            var $reviewCard = $(reviewHtml).appendTo('#reviews-container');
                        }
                    });
                    var $firstReviewCard = $('#reviews-container .review-card:first');
                    // Now you can perform operations on the first review card, such as fading it in
                    $firstReviewCard.animate({ opacity: 1 }, 1000);
                } else {
                    response.reviews.forEach(function(review, index) {
                        var reviewHtml = generateReviewHtml(review);
                        var $reviewCard = $(reviewHtml).appendTo('#reviews-container').css('opacity', 0); // Set initial opacity to 0
                    });
                    
                    // Fade in each review card sequentially
                    $('#reviews-container .review-card').each(function(index) {
                        $(this).delay(80 * index).animate({ opacity: 1 }, 1000); // Delay fading in each review card by 500 milliseconds * index
                    });
                }
                

                /*
                response.reviews.forEach(function(review, index) {
                    var reviewHtml = generateReviewHtml(review);
                    var $reviewCard = $(reviewHtml).appendTo('#reviews-container');
                    $reviewCard.fadeIn(1000);
                    $reviewCard.css('opacity', 0);
                })
                */

                //for (var i = response.reviews.length() - 1; i > 0; i++) {
                    //$reviewCard.slideDown().animate({ opacity: 1 }, 1000);
                //}
                /*
                response.reviews.forEach(function(review, index) {
                    var reviewHtml = generateReviewHtml(review);
                    var $reviewCard = $(reviewHtml).prependTo('#reviews-container');
                    if (index === response.reviews.length - 1) {
                        $reviewCard.css('opacity', 0);
                            
                    } else {
                        delay += 500; // Increase the delay for each subsequent review
                        setTimeout(function() {
                            $reviewCard.css('opacity', 0);
                           // $reviewCard.fadeIn(1000);
                        }, delay);
                    }
                });
                */
            } else {
                $('#reviews-container').html('<p>No reviews yet.</p>');
            }   
        },
        error: function(xhr, status, error) {
            //console.error('Error fetching reviews:', error);
        }
    });
}

function renderCaptchas() {
    var params = {
        "sitekey": "ea26674e-0527-405c-90d4-fecd46e24062",
        "theme": "light",
        "difficulty": "easy"
    }
    reviewWidgetId = hcaptcha.render('reviewCaptcha', params);
}

function reviewsStarsInit(className) {
    starClass = $(className);
    var rating = parseFloat($('.rating').text());
    //console.log("rating" + rating)

    starClass.each(function() {
        if (rating >= 0.8) $(this).removeClass('bi-star').addClass('bi-star-fill');
        else if (rating >= 0.4) $(this).removeClass('bi-star').addClass('bi-star-half');
        rating -= 1;
    });
    //console.log("rating" + rating)
}

function initCaptcha() {
    renderCaptchas();
    //console.log("youre only once");
}

$(document).ready(function () {
    const formContainer = $('#formContainer');
    const showReviewForm = $('#reviewButton');
    const reviewFormContainer = $('#reviewFormContainer');
    const overlay = $('#overlay');
    const closeContactFormButton = $('#contactFormCloseButton');

    overlay.on("click", function() {
        formContainer.css('display', 'none');
        overlay.css('display', 'none');
    });

    showReviewForm.on("click", function() {
        reviewFormContainer.slideDown();
        //reviewFormContainer.css('display', 'block')
    });

    closeContactFormButton.on("click", function() {
        reviewFormContainer.slideUp();
    });

});


$(document).ready(function() {
    var starArr = [0, 0, 0, 0, 0]
    $('.bi-star').hover(
        function() {
            var starIndex = $(this).data('value');
            highlightStars(starIndex);
        },
        function() {
            resetStars();
        }
    );

    $('.bi-star').click(function() {
        var starIndex = $(this).data('value');
        // Toggle between empty and filled star on click
        //$(this).removeClass('bi-star').addClass('bi-star-fill');
        // Highlight stars up to the clicked one
        highlightStarsStay(starIndex);

        // Update the value or send it to the server if needed
        starValue = $(this).data('value');
        //console.log('Selected value: ' + starValue);
    });

    function highlightStarsStay(starIndex) {
        for (var i = 0; i < 5; i++) {
            if (i < starIndex) starArr[i] = 1;
            else starArr[i] = 0;
        }

        //console.log(starArr);
    }

    function highlightStars(starIndex) {
        $('.star-id').each(function(index) { //highlights stars
            if (index < starIndex) {
                $(this).removeClass('bi-star').addClass('bi-star-fill');
            } else $(this).removeClass('bi-star-fill').addClass('bi-star');
        });
    }

    function resetStars() { //removes highlighted stars
        $('.star-id').each(function(index) {
            if (starArr[index] == 0) $(this).removeClass('bi-star-fill').addClass('bi-star');
            else $(this).removeClass('bi-star').addClass('bi-star-fill');
        });
    }
});

document.getElementById("reviewForm").addEventListener("submit", function(event) {

    // Prevent the default form submission behavior
    event.preventDefault();

    // Verify hCaptcha
    var captchaResponse = window.hcaptcha.getResponse(reviewWidgetId);


    if (captchaResponse) {
        $.ajax({
            type: 'POST',
            url: '/create_review',
            data: {
                inputNameReview: $('#inputNameReview').val(),
                inputEmail: $('#inputEmail').val(),
                starRating: starValue,
                inputReview: $('#inputReview').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                professional: professional_pk
            },
            success: function(data) {
                //console.log("worked");
                // Assuming the AJAX call to add a new review is successful
                // Retrieve the updated list of reviews from the server
                $.ajax({
                    type: 'GET',
                    url: '/get_reviews/',
                    data: {
                        professional_pk: professional_pk
                    },
                    success: function(response) {
                        fetchReviews();
                    }
                });

                // Optionally, you can hide the form or perform other actions
                document.getElementById("reviewFormContainer").style.display = "none";

                // Show the Bootstrap alert for successful submission
                var successAlert = $("#successAlertReview");
                successAlert.css('display', 'flex');
                successAlert.hide();
                successAlert.fadeIn();

                // Add an event listener to close the alert when the button is clicked
                document.getElementById("closeSuccessAlert").addEventListener("click", function() {
                    successAlert.fadeOut();
                });
            },
            error: function(data) {
                //console.log("failfail");
                document.getElementById("reviewFormContainer").style.display = "none";


                try {
                    var response = JSON.parse(data.responseText);
                    var message = response.message || 'Unexpected error occurred. Please try again later.';
                } catch (e) {
                    var message = 'Unexpected error occurred. Please try again later.';
                }
        
                console.log("response: " + message);

                if (message == "You have already reviewed this professional.") {
                    var successAlert = $("#repeatAlertReview");
                    successAlert.css('display', 'flex');
                    successAlert.hide();
                    successAlert.fadeIn();
    
                    // Add an event listener to close the alert when the button is clicked
                    document.getElementById("closeSuccessAlert").addEventListener("click", function() {
                        successAlert.fadeOut();
                    });
                } else {
                    var successAlert = $("#failAlertReview");
                    successAlert.css('display', 'flex');
                    successAlert.hide();
                    successAlert.fadeIn();
    
                    // Add an event listener to close the alert when the button is clicked
                    document.getElementById("closeSuccessAlert").addEventListener("click", function() {
                        successAlert.fadeOut();
                    });
                }

            }
        })

    } else {
        // Handle the case where hCaptcha verification failed
        alert("hCaptcha verification failed. Please try again.");
        //console.log("fail");
    }
});

// Function to generate HTML for a single review
function generateReviewHtml(review) {
    var reviewHtml = '<div class="card review-card">';
    var reviewDate = new Date(review.created_at).toLocaleDateString('en-US', dateFormatOptions);
    reviewHtml += '<h5><strong>' + review.reviewer_name + '</strong></h5>';
    var starsHtml = '<div class="stars">';
    for (var i = 1; i < 6; i++) {
        if (i <= review.rating) starsHtml += '<i class="bi bi-star-fill review-star"></i>';
        else starsHtml += '<i class="bi bi-star review-star"></i>';
    }
    starsHtml += '</div>';
    reviewHtml += starsHtml;
    reviewHtml += '<small>Created On: ' + reviewDate + '</small>';
    reviewHtml += '<hr>';
    reviewHtml += '<p class="overflow-auto">' + review.comment + '</p>';
    reviewHtml += '</div>';
    return reviewHtml;
}

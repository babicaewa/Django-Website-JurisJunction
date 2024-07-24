$(document).ready(function() {
    const advancedSearch = $('#advancedSearch');
    const advancedSearchButton = $('#advancedSearchButton');

    advancedSearchButton.click(function() {
        if (advancedSearch.is(':hidden')) {
            advancedSearch.slideDown();
            advancedSearch.css('style', 'flex');
        } else advancedSearch.slideUp();
    });

    const $slider = $('.radius-slider');

    const updateSliderStyle = () => {
        const value = ($slider.val() - $slider.attr('min')) / ($slider.attr('max') - $slider.attr('min')) * 100;
        $slider.css('background', `linear-gradient(to right, #022140 0%, #022140 ${value}%, #dddddd ${value}%, #dddddd 100%)`);
    };

    // Update slider style on page load
    updateSliderStyle();

    $slider.on('input', updateSliderStyle);
    //for url trimming

    var autocompleteField = document.getElementById('autocomplete');
    var languagesField = document.getElementById('spokenLanguagesInput');      //search form fields
    var specialtyField = document.getElementById('specialty'); 
    var professionalField = document.getElementById('professional');
    var slider = document.getElementById('radiusSlider')
    var experienceField = document.getElementById('yearsExperience')
    var searchForm = document.getElementById("searchForm");

    var searchFields = [autocompleteField, languagesField, specialtyField, 
        professionalField, slider, experienceField]

/*
    // Add an event listener to listen for form submission
    searchForm.addEventListener('submit', function(event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Get the value of the input field
        for (var i = 0; i < searchFields.length; i++) {
            if (searchFields[i] != null) {
                var value = searchFields[i].value.trim();
                if (value == '' || value == 200 || value == '0') {
                    searchFields[i].removeAttribute('name');  //cleaning url if empty fields
                }
            }
        }
        searchForm.submit();
    });
*/

$('.specialty-container').on('click', function () {
    if ($('.specialty-dropdown').css('display') == 'none') {
        $('.specialty-dropdown').css('display', 'block');
    }
})

$('#languageInput').on('click', function(event) {
    if ($('#languageDropdown').css('display') == 'none') {
            //console.log("hallooo!!")
        $('#languageDropdown').css('display', 'block');
    }
})

$('.specialty-bullet').on('click', function() {
    var selectedBullet = $(this).text().trim();
    $('#specialtyInput').val(selectedBullet);
    $('.specialty-dropdown').css('display', 'none');
})

$('.language-bullet').on('click', function() {
    var selectedBullet = $(this).text().trim();
    $('#languageInput').val(selectedBullet);
    //console.log("sadsada");
    $('#languageDropdown').css('display', 'none');
})

$('#ratingDropdownContainer').on('click', function() {
    if ($('.dropdown-list-container').css('display') == 'none') {
        $('.dropdown-list-container').show();
        $('.rating-placeholder-text').animate({
            'margin-top': '-38px',
            'font-size': '0.8rem'
        }, 100);
    }
})

$('.avg-rating-select').on('click', function(event) {
    event.stopPropagation();
    var selectedRatingImg = $(this).find('img').prop('outerHTML');
    var selectedRatingText = $(this).find('p').prop('outerHTML');

    var newDiv = $("<div>" + selectedRatingImg + selectedRatingText + "</div>");
    newDiv.addClass("rating-selected-container");

    if ($('.rating-selected-container').length) {
        $('.rating-selected-container').replaceWith(newDiv);
    } else {
        $('.rating-dropdown-inner-text').append(newDiv);
        $('rating-dropdown-inner-text').css('justify-content', 'flex-end');
    }
    $('.dropdown-list-container').hide();
})

$(document).on('click', function(event) {
    if (!$(event.target).is('.specialty-dropdown') && 
    !$(event.target).is('.specialty-container') &&
    !$(event.target).is('.specialty-input') &&
    $('.specialty-dropdown').css('display') == 'block') {
        $('.specialty-dropdown').css('display', 'none');
    }

    if (!$(event.target).is('.language-dropdown') && !$(event.target).closest('.language-container').length && $('.language-dropdown').css('display') == 'block') {
        $('.language-dropdown').hide();
    }

    if (!$(event.target).is('.dropdown-list-container') && !$(event.target).closest('.rating-dropdown-container').length && $('.dropdown-list-container').css('display') == 'block') {
        $('.dropdown-list-container').hide();
    }
    
})

$('.filter-button').on('click', function () {
    if ($('.form-col').css('margin-top') === '24px') {
        $('.form-col').animate({
            'margin-top': '0px'
        },100);
    } else {
        $('.form-col').animate({
            'margin-top': '24px'
        },400);
    }
    $('.extra-filters').slideToggle();
})

var locationPlaceholder = $('#locationPlaceholder');
var specialtyPlaceholder = $('#specialtyPlaceholder');
var languagePlaceholder = $('#languagePlaceholder');
var keywordPlaceholder = $('#keywordPlaceholder');
var ratingPlaceholder = $('#ratingPlaceholder')

function shiftPlaceholderUp(placeholderId) {
    placeholderId.animate({
        'margin-top': '-10px',
        'font-size': '0.8rem'
    }, 100);
}

$(document).on('click', function(event) {
    if ($(event.target).is('#autocomplete')) {
        shiftPlaceholderUp(locationPlaceholder)
    }
    if ($(event.target).is('#specialtyInput')) {
        shiftPlaceholderUp(specialtyPlaceholder)
    }
    if ($(event.target).is('#languageInput')) {
        shiftPlaceholderUp(languagePlaceholder)
    }
    if ($(event.target).is('#keywordInput')) {
        shiftPlaceholderUp(keywordPlaceholder)
    }

    if(!$(event.target).is(locationPlaceholder) &&
    parseInt((locationPlaceholder).css('margin-top')) === -10 && !$('#autocomplete').val()) {
        $(locationPlaceholder).animate({
            'margin-top': '8px',
            'font-size': '1rem'
        }, 100);
    }
    if(!$(event.target).is(specialtyPlaceholder) &&
    parseInt((specialtyPlaceholder).css('margin-top')) === -10 && !$('#specialtyInput').val()) {
        $(specialtyPlaceholder).animate({
            'margin-top': '8px',
            'font-size': '1rem'
        }, 100);
    }
    if(!$(event.target).is(languagePlaceholder) &&
    parseInt((languagePlaceholder).css('margin-top')) === -10 && !$('#languageInput').val()) {
        $(languagePlaceholder).animate({
            'margin-top': '8px',
            'font-size': '1rem'
        }, 100);
    }

    if(!$(event.target).is($('#ratingDropdownContainer')) &&
        parseInt((ratingPlaceholder).css('margin-top')) === -38 &&
     !$('.rating-selected-container').length) {
        $(ratingPlaceholder).animate({
            'margin-top': '0px',
            'font-size': '1rem'
        }, 100);
    }

    if(!$(event.target).is(keywordPlaceholder) &&
    parseInt((keywordPlaceholder).css('margin-top')) === -10 && !$('#keywordInput').val()) {
        $(keywordPlaceholder).animate({
            'margin-top': '8px',
            'font-size': '1rem'
        }, 100);
    }
})

specialtyArr = []

function filterList(searchTerm, specialtyArr, dropdownClass) {
    const listItems = document.querySelectorAll(dropdownClass);

    listItems.forEach(function (item) {
        let index = specialtyArr.indexOf(item.textContent);
        const itemText = item.textContent.toLowerCase();

        if (itemText.includes(searchTerm) && index === -1) {
            item.style.display = 'list-item';
        } else {
            item.style.display = 'none';
        }
    });
}

$('#specialtyInput').on('input', function (event) {
    const searchTerm = event.target.value.toLowerCase();
    filterList(searchTerm, specialtyArr, ".specialty-dropdown li");
    });

$('#languageInput').on('input', function (event) {
        const searchTerm = event.target.value.toLowerCase();
        filterList(searchTerm, specialtyArr, ".language-dropdown li");
        });
    

    // Function to initialize Google Maps autocomplete
function initAutocomplete() {
    var autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('autocomplete'), {
           // types: ['geocode', '(cities)'],
            types: ['(cities)'],
            ComponentRestrictions: { country: 'CA' }
        });
        //console.log(document.getElementById('autocomplete'));
}

    // Call the initAutocomplete function when the page loads
    window.onload = function() {
        initAutocomplete();
        $('#searchForm').trigger('reset');
    };

    var radiusSlider = document.getElementById('radiusSlider');

$('#radiusSlider').on('input', function() {
        $('#radiusInput').val($(this).val());
})

// Function to update pseudo-element border-radius based on input value
$('#radiusInput').on('input', function() {
    $('#radiusSlider').val($(this).val());
})
});


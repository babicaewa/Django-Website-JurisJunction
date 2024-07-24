var specialtyInput = $('#specialtyInput');
var languageInput = $('#languageInput');
var designationInput = $('#designationInput');

var specialtiesSelectedArr, languagesSelectedArr, designationsSelectedArr;

var specialtiesArrayInput= $('#specialtiesArrayInput');
var languagesArrayInput = $('#languagesArrayInput');
var designationsArrayInput = $('#designationsArrayInput');



// Function to initially hide already selected items and update the autocomplete dropdown
function initializeAutocompleteDropdown(alreadySelected, dropdown, selectedArr, arrayInput) {
    selectedArr = $(alreadySelected + ' p').map(function() {
        return $(this).text();
    }).get();

    $(dropdown +' li').each(function() {
        var listItem = $(this);
        var listItemText = listItem.text();

        // Hide the list item if it's already selected
        if (selectedArr.indexOf(listItemText) !== -1) {
            listItem.hide();
        }
    });
    //console.log(selectedArr);
    $(arrayInput).val(JSON.stringify(selectedArr));
}

// Function to filter out already selected items and update the autocomplete dropdown
function updateAutocompleteDropdown(searchTerm, dropdown, selectedItem) {
    selectedArr = $(selectedItem + ' p').map(function() {
        return $(this).text();
    }).get();

    $(dropdown + ' li').each(function() {
        var listItem = $(this);
        var listItemText = listItem.text();

        // Check if the listItemText contains the searchTerm and is not already selected
        if (listItemText.toLowerCase().includes(searchTerm.toLowerCase()) && selectedArr.indexOf(listItemText) === -1) {
            listItem.show(); // Show the list item if it matches the search term and is not already selected
        } else {
            listItem.hide(); // Hide the list item if it doesn't match the search term or is already selected
        }
    });
}

function addNewSelection(selectedItem, selectedContainerName, selectedClassName) {
   var newDiv = '<div class="selected-dropdown-item ' + selectedClassName + '"> <p>' + selectedItem + '</p></div>';

   $(selectedContainerName).append(newDiv);
}

function getBackgroundImagePreview(event) {
    $('body').css('overflow', 'hidden');
    $('#imgCropBackground').fadeIn();
    $('#imgCropBackground').css('display', 'flex');
    var image = URL.createObjectURL(event.target.files[0]);
    $('#backgroundCroppedImg').attr('src', image);
    $('#backgroundCroppedImg').croppie({
            url: image, 
            enableExif: true, // Enable EXIF orientation support
            viewport: {
                width: 400, // Width of the viewport
                height: 200, // Height of the viewport
                type: 'square' // Crop type: 'square' or 'circle'
            },
            boundary: {
                width: 400, // Width of the outer boundary
                height: 300 // Height of the outer boundary
            }
    });
    var zoomDiv = $('<div class="zoom-text-container"><p>Zoom</p><i class="bi bi-plus-slash-minus"></i></div>');
    $('.cr-boundary').after(zoomDiv);
    var buttonDiv = $('<div class="photo-submit-crop-container"><div class="submit-button" onclick="getCroppedImgBackground()"><p>Confirm</p></div></div>');
    $('.cr-slider-wrap').after(buttonDiv);

}

function getImagePreviewPfp(event) {
    $('body').css('overflow', 'hidden');
    $('#imgCrop').fadeIn();
    $('#imgCrop').css('display', 'flex');
    var image = URL.createObjectURL(event.target.files[0]);
    $('#pfpCroppedImg').attr('src', image);
    $('#pfpCroppedImg').croppie({
            url: image, 
            enableExif: true, // Enable EXIF orientation support
            viewport: {
                width: 200, // Width of the viewport
                height: 200, // Height of the viewport
                type: 'circle' // Crop type: 'square' or 'circle'
            },
            boundary: {
                width: 300, // Width of the outer boundary
                height: 300 // Height of the outer boundary
            }
    });
    var zoomDiv = $('<div class="zoom-text-container"><p>Zoom</p><i class="bi bi-plus-slash-minus"></i></div>');
    $('.cr-boundary').after(zoomDiv);
    var buttonDiv = $('<div class="photo-submit-crop-container"><div class="submit-button" onclick="getCroppedImgPfp()"><p>Confirm</p></div></div>');
    $('.cr-slider-wrap').after(buttonDiv);

}

function getCroppedImgBackground() {
    $('#backgroundCroppedImg').croppie('result', {
        type: 'blob', 
        size: { width: 400, height: 200 } 
    }).then(function (blob) {
        // Handle the base64 encoded data URL here
        //console.log(blob);
        var objectURL = URL.createObjectURL(blob);
        $('#backgroundShowImg').attr('src', objectURL);

        var newBackgroundFile = new File([blob], "background_photo.jpg", { type: 'image/jpeg' });

        // Create a DataTransfer object
        var dataTransfer = new DataTransfer();

        // Add the new File object to the DataTransfer object
        dataTransfer.items.add(newBackgroundFile);

        // Get the file input element
        var fileInput = $('#id_background_picture').get(0);

        // Set the files property of the file input to the DataTransfer object's files property
        fileInput.files = dataTransfer.files;

    });
    exitBackgroundChange();
}

function getCroppedImgPfp() {
    $('#pfpCroppedImg').croppie('result', {
        type: 'blob', 
        size: { width: 200, height: 200 } 
    }).then(function (blob) {
        // Handle the base64 encoded data URL here
        //console.log(blob);
        var objectURL = URL.createObjectURL(blob);
        $('#pfpShowImg').attr('src', objectURL);

        var newPfpFile = new File([blob], "profile_photo.jpg", { type: 'image/jpeg' });

        // Create a DataTransfer object
        var dataTransfer = new DataTransfer();

        // Add the new File object to the DataTransfer object
        dataTransfer.items.add(newPfpFile);

        // Get the file input element
        var fileInput = $('#id_profile_picture').get(0);

        // Set the files property of the file input to the DataTransfer object's files property
        fileInput.files = dataTransfer.files;
    });
    exitPfpChange();
}

function exitPfpChange() {
    $('#imgCrop').fadeOut('slow', function() {
        $('.croppie-container').remove();
        $('body').css('overflow', '');
    });

    var newImgElement = $('<img src="" alt="" class="cropped-img" id="pfpCroppedImg"></img>');
    $('.crop-img-card').append(newImgElement)

    //$('.cropped-img').src = '';
}

function exitBackgroundChange() {
    $('#imgCropBackground').fadeOut('slow', function() {
        $('.croppie-container').remove();
        $('body').css('overflow', '');
    });

    var newImgElement = $('<img src="" alt="" class="cropped-img" id="backgroundCroppedImg"></img>');
    $('.background-crop-img-card').append(newImgElement)

    //$('.cropped-img').src = '';
}

$(document).ready(function() {

    $(document).on('input', '.cr-slider', function() {
        const $slider = $(this);
        const updateSliderStyle = () => {
            const value = ($slider.val() - $slider.attr('min')) / ($slider.attr('max') - $slider.attr('min')) * 100;
            $slider.css('background', `linear-gradient(to right, #022140 0%, #022140 ${value}%, #dddddd ${value}%, #dddddd 100%)`);
        };
    
        updateSliderStyle();
    });

        // Add event listener for profile picture file input
        $('#id_profile_picture').on('change', function(event) {
            getImagePreviewPfp(event);
        });
    
        // Add event listener for background picture file input (if needed)
        $('#id_background_picture').on('change', function(event) {
            getBackgroundImagePreview(event);
        });
    
    
    initializeAutocompleteDropdown('.selected-specialty', '#specialtyDropdown', specialtiesSelectedArr, specialtiesArrayInput);
    initializeAutocompleteDropdown('.selected-language', '#languageDropdown', languagesSelectedArr, languagesArrayInput);
    initializeAutocompleteDropdown('.selected-designation', '#designationDropdown', designationsSelectedArr, designationsArrayInput);

    $('#pfpImgContainer').on('mouseenter', function() {
        $('#editProfilePencil').css('display', 'block');
    }).on('mouseleave', function() {
        $('#editProfilePencil').css('display', 'none');
    });
    

    $('#pfpImgContainer').on('click', function() {
        $('#id_profile_picture').click();
    })

    $('#backgroundImgContainer').on('mouseenter', function() {
        $('#editBackgroundPencil').css('display', 'block');
    }).on('mouseleave', function() {
        $('#editBackgroundPencil').css('display', 'none');
    });
    

    $('#backgroundImgContainer').on('click', function() {
        $('#id_background_picture').click();
    })

    designationInput.on('click', function() {
        $('#designationDropdown').show();
    })

    designationInput.on('input', function(event) {
        var searchTerm = $(this).val();
        updateAutocompleteDropdown(searchTerm, '#designationDropdown','.selected-designation');
    })

    $('.designation-bullet').on('click', function() {
        var newItem = $(this).text();
        //console.log(newItem);
        addNewSelection(newItem, '.all-selected-designations', 'selected-designation');
        initializeAutocompleteDropdown('.selected-designation', '#designationDropdown', designationsSelectedArr, designationsArrayInput);
        $('#designationDropdown').hide();
        $('#designationInput').val("");
    })

    $(document).on('click', '.selected-designation', function() {
        $(this).remove();
        initializeAutocompleteDropdown('.selected-designation', '#designationDropdown', designationsSelectedArr, designationsArrayInput);
    })


    specialtyInput.on('click', function() {
        $('#specialtyDropdown').show();
    })

    specialtyInput.on('input', function(event) {
        var searchTerm = $(this).val();
        updateAutocompleteDropdown(searchTerm, '#specialtyDropdown','.selected-specialty');
    })

    $('.specialty-bullet').on('click', function() {
        var newItem = $(this).text();
        //console.log(newItem);
        addNewSelection(newItem, '.all-selected-specialties', 'selected-specialty');
        initializeAutocompleteDropdown('.selected-specialty', '#specialtyDropdown', specialtiesSelectedArr, specialtiesArrayInput);
        $('#specialtyDropdown').hide();
        $('#specialtyInput').val("");
    })

    $(document).on('click', '.selected-specialty', function() {
        $(this).remove();
        initializeAutocompleteDropdown('.selected-specialty', '#specialtyDropdown', specialtiesSelectedArr, specialtiesArrayInput);
    })


    languageInput.on('click', function() {
        $('#languageDropdown').show();
    })

    languageInput.on('input', function(event) {
        var searchTerm = $(this).val();
        updateAutocompleteDropdown(searchTerm, '#languageDropdown','.selected-language');
    })

    $('.language-bullet').on('click', function() {
        var newItem = $(this).text();
        //console.log(newItem);
        addNewSelection(newItem, '.all-selected-languages', 'selected-language');
        initializeAutocompleteDropdown('.selected-language', '#languageDropdown', languagesSelectedArr, languagesArrayInput);
        $('#languageDropdown').hide();
        $('#languageInput').val("");
    })

    $(document).on('click', '.selected-language', function() {
        $(this).remove();
        initializeAutocompleteDropdown('.selected-language', '#languageDropdown', languagesSelectedArr, languagesArrayInput);
    });
    

    $(document).click(function(e) {
        if (!$(e.target).is(specialtyInput) && $(specialtyInput).css('display') == 'block') {
            $('#specialtyDropdown').hide();
        }
        if (!$(e.target).is(languageInput) && $(languageInput).css('display') == 'block') {
            $('#languageDropdown').hide();
        }
        if (!$(e.target).is(designationInput) && $(designationInput).css('display') == 'block') {
            $('#designationDropdown').hide();
        }
    })



})
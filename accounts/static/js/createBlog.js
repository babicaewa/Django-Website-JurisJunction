var mobileNavOpen = false;

$(document).ready(function() {
        const quill = new Quill('#editor', {
            theme: 'snow'
        });



    $('#topicButton').click(function(event) {
        if ($("#inputTopicList").css('display') == 'block') $("#inputTopicList").css('display', 'none') ;
        else $("#inputTopicList").css('display', 'block');

    })

    $('#topicInput').on('input', function() {
        var inputValue = $(this).val().toLowerCase(); 
        $('#topicList li').each(function() {
            var listItemText = $(this).text().toLowerCase();
            if (listItemText.indexOf(inputValue) > -1) {
                $(this).show();
            } else {
                $(this).hide(); 
            }
        });
    });

    $('#topicList').on('click', 'li', function() {
        var selectedTopic = $(this).text();
        $('#inputTopicList').css('display', 'none');
        if ($('#topicAdded')) $('#topicAdded').remove(); 
        var topicDiv = $('<div>').addClass('tag-added');
        topicDiv.attr('id', 'topicAdded');
        var topicPTag = $('<p>').text(selectedTopic);
        topicDiv.append(topicPTag);
        $('#topicButton p').text("Change Topic");
        topicDiv.insertBefore('#topicButton');
    });

    $(document).on('click', '#topicAdded', function(event) {
        $(this).remove();
        $('#topicButton p').text("Add A Topic Tag");
    });



    $('#provinceButton').click(function(event) {
        if ($("#inputProvinceList").css('display') == 'block') $("#inputProvinceList").css('display', 'none') ;
        else $("#inputProvinceList").css('display', 'block');

    })

    $('#provinceInput').on('input', function() {
        var inputValue = $(this).val().toLowerCase(); 
        $('#provinceList li').each(function() {
            var listItemText = $(this).text().toLowerCase();
            if (listItemText.indexOf(inputValue) > -1) {
                $(this).show();
            } else {
                $(this).hide(); 
            }
        });
    });

    $('#provinceInput').on('input', function() {
        var inputValue = $(this).val().toLowerCase(); 
        $('#provinceList li').each(function() {
            var listItemText = $(this).text().toLowerCase();
            if (listItemText.indexOf(inputValue) > -1) {
                $(this).show();
            } else {
                $(this).hide(); 
            }
        });
    });

    $('#provinceList').on('click', 'li', function() {
        var selectedTopic = $(this).text();
        $('#inputProvinceList').css('display', 'none');
        if ($('#provinceAdded')) $('#provinceAdded').remove(); 
        var topicDiv = $('<div>').addClass('tag-added');
        topicDiv.attr('id', 'provinceAdded')
        var topicPTag = $('<p>').text(selectedTopic);
        topicDiv.append(topicPTag);
        $('#provinceButton p').text("Change Province");
        topicDiv.insertBefore('#provinceButton');
    });

    $(document).on('click', '#provinceAdded', function(event) {
        $(this).remove();
        $('#provinceButton p').text("Add A Province");
    });

    $('#blogForm').submit(function (event) {
        event.preventDefault();

        if (!$('#topicAdded p').text()){
            recreateAlertMessage();
        } else if (!$('#provinceAdded p').text()) {
            recreateAlertMessage();
        }

        else {
            $.ajax({
                type:'POST',
                url:'/user_blogs/post_blog/',
                data: {
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    blog_title: $('#blogTitle').val(),
                    blog_text: quill.root.innerHTML,
                    topic_tag: $('#topicAdded p').text(),
                    province_tag: $('#provinceAdded p').text()
                },
                success: function(response) {
                    if (response.status === 'success') {
                        window.location.href = '/user_blogs/';
                    } else {
                       // console.log("NOT WORK");
                        recreateErrorMessage();
                    }
                },
                error: function(xhr, status, error) {
                    //console.error('AJAX request failed:', error);
                }
            })  
        }
    })

    function recreateAlertMessage() {
        // Check if the alert message div already exists
        if ($('#alertMessage').length) {
            $('#alertMessage').remove();
        }
        // Recreate the alert message div and append it to the body
        var alertMessage = '<div id="alertMessage" class="alert alert-danger alert-dismissible fade show fixed-alert alert-message" role="alert">';
        alertMessage += 'You must fill out one topic and one province.';
        alertMessage += '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
        alertMessage += '</div>';

        var navAndContent = $('#navAndContent');
        var parentDiv = navAndContent.parent();

        parentDiv.before(alertMessage);
    }

    function recreateErrorMessage() {
        // Check if the alert message div already exists
        if ($('#alertMessage').length) {
            $('#alertMessage').remove();
        }
        // Recreate the alert message div and append it to the body
        var alertMessage = '<div id="alertMessage" class="alert alert-danger alert-dismissible fade show fixed-alert alert-message" role="alert">';
        alertMessage += 'There was an error creating your blog post.';
        alertMessage += '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
        alertMessage += '</div>';
        $('#navAndContent').prepend(alertMessage);
    }
});







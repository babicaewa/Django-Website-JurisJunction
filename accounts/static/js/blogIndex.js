var overlayDiv = $('.overlay-delete-container')
var blogId;
var blogToDelete;

$(document).ready(function() {
    $('.blogs-created-container').on('click', '.delete-blog-button', function() {
        blogId = $(this).closest('.blog-card').data('id');
        blogToDelete = $(this).closest('.blog-card');
        //console.log(blogId);
        overlayDiv.css('display', 'flex');
        $('html').css('overflow', 'hidden');
    })

    $('.cancel-button').on('click', function() {
        overlayDiv.css('display', 'none');
        $('html').css('overflow', '');
    })

    $('.btn-close').on('click', function() {
        overlayDiv.css('display', 'none');
        $('html').css('overflow', '');
    })

    $('.confirm-delete-button').on('click', function(event) {
        event.preventDefault();
        overlayDiv.css('display', 'none');
        $('html').css('overflow', '');
        var csrfToken = $('#delete-blog-form input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: 'POST',
            url: 'delete_blog_post/',
            headers: {'X-CSRFToken': csrfToken},
            data: {'blogId' : blogId},
            success: function(response) {
                $('#successAlert').fadeIn();
                blogToDelete.fadeOut('slow', function() {
                    $(this).remove();
                })
            },
            error: function(response) {
                $('#failAlert').fadeIn();
            }
        })

    })
})
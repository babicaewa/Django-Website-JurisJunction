function checkLiked(blogId, csrftoken) {
    $.ajax({
        type:'POST',
        url: '/check_blog_liked',
        data: {
            blog_id: blogId,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function(response) {
            if (response.message == "Already Liked") {
                $('#liked').css('display', 'block');
                $('#notLiked').css('display', 'none');
            } else {
                $('#liked').css('display', 'none');
                $('#notLiked').css('display', 'block');
            }
        },

    })
}

$(document).ready(function () { 
    const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    var likeCount = $('#totalLikes').html();
    const blogId = $('.blog-container').data('blog-id');
    checkLiked(blogId, csrftoken);
    
    $('.like-button-container').on('click', function() {
        if($('#liked').css('display') === 'none') {
            $('#liked').css('display', 'block');
            $('#notLiked').css('display', 'none');
            likeCount++;
            $('#totalLikes').html(likeCount);

            $.ajax({
                type:'POST',
                url: '/update_blog_likes',
                data: {
                    blog_id: blogId,
                    csrfmiddlewaretoken: csrftoken,
                    like_status: true,
                }

            })
        } else {
            $('#liked').css('display', 'none');
            $('#notLiked').css('display', 'block');
            likeCount--;
            $('#totalLikes').html(likeCount);
            $.ajax({
                type:'POST',
                url: '/update_blog_likes',
                data: {
                    blog_id: blogId,
                    csrfmiddlewaretoken: csrftoken,
                    like_status: false,
                }

            })
        }
    });
});
$('#answerForm').submit(function (event) {
    event.preventDefault();

    $.ajax({
        type:'POST',
        url:'/create_forum_answer/',
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            pk: $("#question").data("pk"),
            answer_text: $('#answerCardText').val()
        },
        success: function(response) {
            if (response.status === 'success') {
                location.reload();
            } else {
                //console.log("NOT WORK");
                recreateAlertMessage();
            }

        },
        error: function(xhr, status, error) {
            //console.error('Error fetching reviews:', error);
        }
    });
});
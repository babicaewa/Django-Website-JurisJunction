document.addEventListener('DOMContentLoaded', function() {
var topicButton = document.getElementById("topicButton")
var topicDropdown = document.getElementById("topicsSelectsContainer")
var provinceSearchCard = document.getElementById('provinceSearchCard')
var provinceDropdown = document.getElementById('provinceSearchCard');
var provinceSearch = document.getElementById('provinceSearch')

var topicsArr = [];

function filterList(searchTerm, topicsArr) {
    const listItems = document.querySelectorAll('#topicList li');

    listItems.forEach(function (item) {
        let index = topicsArr.indexOf(item.textContent);
        const itemText = item.textContent.toLowerCase();

        if (itemText.includes(searchTerm) && index === -1) {
            item.style.display = 'list-item';
        } else {
            item.style.display = 'none';
        }
    });
}

topicButton.addEventListener("click", function () {
    if (topicDropdown.style.display == "block") topicDropdown.style.display = "none";
    else topicDropdown.style.display = "block";
})

document.getElementById('topicInput').addEventListener('input', function (event) {
    const searchTerm = event.target.value.toLowerCase();
    filterList(searchTerm, topicsArr);
    });

document.getElementById("topicList").addEventListener('click', function(event) {
    if (event.target.tagName === 'LI') {
        var topicName = event.target.textContent;
        var topicKeyword = document.createElement("div");
        var topicKeywordText = document.createElement("p");
        var topicParent = document.getElementById("topicsContainer");
        var topicButtonAndDropdown = document.getElementById('topicButtonAndDropdown');
        var topicInputBox = document.getElementById('topicInput');

        
        topicKeyword.classList.add('keyword-added');
        topicKeyword.id = "keywordAdded";
        topicKeyword.appendChild(topicKeywordText);

        topicKeywordText.innerHTML += topicName;

        topicDropdown.style.display = "none";

        topicsArr.push(topicName);
        //console.log(topicsArr);

        topicParent.insertBefore(topicKeyword, topicButtonAndDropdown);

        topicInputBox.value = "";
        filterList("", topicsArr);
        

        topicKeyword.addEventListener('click', function() {
            topicKeyword.remove();
            let index = topicsArr.indexOf(topicKeyword.querySelector('p').textContent);
            if (index != -1) topicsArr.splice(index, 1);
            //console.log(topicsArr);
        });
    }
});

document.addEventListener('click', function(event) {
    if (!topicButton.contains(event.target) && !topicDropdown.contains(event.target) && topicDropdown.style.display === 'block') {
        topicDropdown.style.display = 'none';
    } 

    if (!provinceButton.contains(event.target) && !provinceSearchCard.contains(event.target) && provinceSearchCard.style.display === 'block') {
        provinceSearchCard.style.display = 'none';
    } 

});

document.getElementById('provinceButton').addEventListener('click', function() {
    if (provinceSearchCard.style.display == 'block') provinceSearchCard.style.display = 'none';
    else provinceSearchCard.style.display = 'block';
});

document.getElementById('provinceInput').addEventListener('input', function (event) {
    const searchTerm = event.target.value.toLowerCase();
    const listItems = document.querySelectorAll('#provinceList li');

    listItems.forEach(function (item) {
        const itemText = item.textContent.toLowerCase();

        if (itemText.includes(searchTerm)) {
            item.style.display = 'list-item';
        } else {
            item.style.display = 'none';
        }
    });
});

var provinceKeyword = document.createElement("div");
var provinceButton = document.getElementById('provinceButton');
var provinceButtonText = document.getElementById('provinceButtonText');

document.getElementById("provinceList").addEventListener('click', function(event) {
    if (event.target.tagName === 'LI') {

        if (provinceKeyword) provinceKeyword.remove(); 

            var provinceName = event.target.textContent;
            provinceKeyword = document.createElement("div");
            var provinceKeywordText = document.createElement("p");
            var provinceParent = document.getElementById("provinceSelectAndButton");

            
            provinceKeyword.classList.add('province-added');
            provinceKeyword.id = "provinceAdded";
            provinceKeyword.appendChild(provinceKeywordText);

            provinceKeywordText.innerHTML += provinceName;

            provinceDropdown.style.display = "none";

            provinceParent.insertBefore(provinceKeyword, provinceButton);
            provinceKeyword.appendChild(provinceKeywordText);

            provinceButtonText.innerHTML = "<p>Change Province</p>";

        provinceKeyword.addEventListener('click', function() {
            provinceKeyword.remove();
            provinceButtonText.innerHTML = `<p>Select Province</p>
            <i class="bi bi-plus-circle-fill"></i>`;
        });
    }
});

$('#askForm').submit(function (event) {
    event.preventDefault();

    //console.log(topicsArr.length);
    //console.log($('#provinceAdded').length);

    $.ajax({
        type:'POST',
        url:'/create_forum_question/',
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            email: $('#emailInput').val(),
            question_title: $('#questionTitleInput').val(),
            question_text: $('#questionTextInput').val(),
            topics_arr: JSON.stringify(topicsArr),
            province: $('#provinceAdded p').first().text()
        },
        success: function(response) {
            if (response.status === 'success') {
                window.location.href = '/forum/';
            } else {
                //console.log("NOT WORK");
                recreateAlertMessage();
            }
        },
        error: function(xhr, status, error) {
            //console.error('AJAX request failed:', error);
        }
    })  
})

function recreateAlertMessage() {
    // Check if the alert message div already exists
    if ($('#alertMessage').length) {
        $('#alertMessage').remove();
    }
    // Recreate the alert message div and append it to the body
    var alertMessage = '<div id="alertMessage" class="alert alert-danger alert-dismissible fade show fixed-alert" role="alert">';
    alertMessage += 'You must fill out at least one topic and a province.';
    alertMessage += '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
    alertMessage += '</div>';
    $('#navMain').prepend(alertMessage);
}

});

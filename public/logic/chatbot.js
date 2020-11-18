$(function () {
    //register inputsearch, enter triggers button click
    $("#user-input").keyup(function (event) {
        if (event.keyCode == 13) {
            $("#send-button").click();
        }
    });
});

function sendMessage() {
    //get user's input from the html
    var userInput = $("#user-input").val();
    //send the user input to the screen
    displayMessage(getPrefix('user') + userInput);
    //clear the textbox
    $("#user-input").val("");
    //send the user input to the backend conversation engine
    spinDiv('cba-forSpinningDiv');

    //prepare parameters for backend engine
    var params = {
        user_input: userInput,
        chatID: 'LindsayChat', //not in use
        sessionID: 'aamas2021' //not in use
    }

    $.post('/give_response', params, function (result) {
        //stop spinning when getting the response from the server
        stopSpinDiv('cba-forSpinningDiv');
        //show plain text - response from data
        displayMessage(getPrefix('agent') + result);

    }).fail(function (response) {
        console.log(response);
        stopSpinDiv('cba-forSpinningDiv');
    });

}

function displayMessage(text) {
    var returnHTML = '';
    returnHTML += `<div>`;
    returnHTML += `<p> ${text}<p>`;
    returnHTML += '</div>';

    $('#conversation-div').prepend(returnHTML);
    // $(`#vd_${data.id}`).show('slow');
}

function getPrefix(prefixType) {
    let timeElapsed = Date.now();
    let today = new Date(timeElapsed);
    let timeFlag = today.toISOString(); // "2020-06-13T18:30:00.000Z"
    if (prefixType == 'user')
        return timeFlag + ' USER: ';
    else if (prefixType == 'agent')
        return timeFlag + ' AGENT: ';
    else
        return '';
}
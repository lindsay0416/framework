$(function () {
    //register inputsearch, enter triggers button click
    $("#user-input").keyup(function (event) {
        if (event.keyCode == 13) {
            $("#send-button").click();
        }
    });
});

var username = "Lindsay";

function sendMessage() {
    //get user's input from the html
    var userInput = $("#user-input").val();
    //send the user input to the screen
    displayMessage(getPrefix(username) + userInput);
    uiList = userInput.split(" ");
    if(uiList.length == 2 && uiList[0] == "select"){
        username = uiList[1];
    }
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
        //show plain text - response from data
        console.log(result["Text"])
        if(result["Text"] == null){
            displayMessage(getPrefix('agent') + result);
            stopSpinDiv('cba-forSpinningDiv');
        }else{
            displayMessage(getPrefix('agent') + result["Text"]);
            updateData(result);
            //stop spinning when getting the response from the server
            stopSpinDiv('cba-forSpinningDiv');
            console.log(result);
        }
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
        // return '';
        return timeFlag + ' ' + prefixType + ': ';
}

document.addEventListener("DOMContentLoaded", function(){
    spinDiv('cba-forSpinningDiv');
    var params = {
        user_input: "init",
        chatID: 'LindsayChat', //not in use
        sessionID: 'aamas2021' //not in use
    }
    //alert("hello"); //test 牛皮
    $.post('/give_response', params, function (result) {
        displayMessage(getPrefix('agent') + "Welcome "+result["namespace"]+" !");
        username = result["namespace"];
        updateData(result);
        stopSpinDiv('cba-forSpinningDiv');
    }).fail(function (response) {
        console.log(response);
        stopSpinDiv('cba-forSpinningDiv');
    });
});
/*
The DOMContentLoaded event is fired when the initial HTML document
has been completely loaded and parsed, without waiting for stylesheets,
images, and subframes to finish loading. A very different event load
should be used only to detect a fully-loaded page. It is an
incredibly popular mistake to use load where DOMContentLoaded would
be much more appropriate, so be cautious.
*/

document.addEventListener('DOMContentLoaded', function () {

    // References to all the element we will need.
    var video = document.querySelector('#camera-stream');



    // The getUserMedia interface is used for handling camera input.
    // Some browsers need a prefix so here we're covering all the options
    navigator.getMedia = (
        navigator.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia ||
        navigator.msGetUserMedia
    );


    if(!navigator.getMedia){
        displayErrorMessage("Your browser doesn't have support for the navigator.getUserMedia interface.");
    }
    else{
        // Request the camera.
        navigator.getMedia(
            {
                video: true
            },
            // Success Callback
            function(stream) {

                // Create an object URL for the video stream and
                // set it as src of our HTLM video element.
                video.src = window.URL.createObjectURL(stream);

                // Play the video element to start the stream.
                video.play();
            

            },
            // Error Callback
            function(err) {
                displayErrorMessage("There was an error with accessing the camera stream: " + err.name, err);
            }
        );
    }









});

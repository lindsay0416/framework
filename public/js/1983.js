$(document).ready(function(){
  // const socket = new WebSocket('ws://localhost:9090');
  var host = location.origin.replace(/^http/, 'ws')
  // console.log(host);
  var socket = new WebSocket(host);

  // const socket = new WebSocket('ws://caito-demo.mybluemix.net:443');
  // const socket = new WebSocket('wss://192.168.1.169:9090');
  // $("#left").css("height", function() { return $(window).height() - 100 });
  // $("#right").css("height", function() { return $(window).height() - 100 });
  var infos = ["#r2","#r3","#r4","#r5","#r6","#r7","#r8","#r9","#r10"];
  var infoInterval;
  var pptInterval;
  var ks=[];
  ks.push('<br><p>Dualism</p><p>Descartes (1596-1650) </p><p>Animals as reflex; We also have material bodies But our minds are immaterial and nonphyscial</p>');
  ks.push('<br><p>Dualism</p><p>Argument 1: </p><p>The creativity and spontaneity of human action</p>');
  ks.push('<br><p>Dualism</p><p>Argument 2: </p><p>I think therefore I am</p>');
  ks.push('<br><p>Dualism seems right </p><p>1. Language </p><p>“my arm”, “my heart”, “my body”,“my brain” </p>');
  ks.push('<br><p>Dualism seems right </p><p>2. Personal identity </p><p>Same person after radical bodily changes </p>');
  ks.push('<br><p>Dualism seems right </p><p>2. Personal identity -- Many people, one body  </p>');
  ks.push('<br><p>Dualism seems right </p><p>3. The survival of the self after the destruction of the body  </p>');
  ks.push('<br><p>Current view: Dualism is wrong Mind = Brain  </p><p>1. We know have a better understanding of what physical things can do (computers & robots)  </p><p>2. Strong evidence for the role of the brain </p>');
  ks.push('<br><p>How does the brain work? </p>');
  ks.push('<br><p>Neurons </p><p>1. About 1,000,000,000,000 </p><p>2. Sensory neurons, motor neurons, interneurons </p><p>3. All-or-nothing</p>');
  ks.push('<br><p>Neurons </p><p>1. Communication over synapses; axons release neurotransmitters  </p><p>2. Drugs: agonists vs. antagonists </p>');


  socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);

    $('#transcription').html(event.data);

  });

  /**Transcription******/
  setInterval(function(){
    $('#transcription').scrollTop($('#transcription')[0].scrollHeight);
  }, 200);

  /**Information********/
  $('video').bind('play', function (e) {
    console.log("PLAY");
    startRecording();

    infoInterval = setInterval(function(){
      if(Math.random()>0.85){
        //add news
        $(infos.shift()).fadeIn('slow');
        $('#right').scrollTop($('#right')[0].scrollHeight);
      }
    }, 2500);

    pptInterval = setInterval(function(){
        $('#knwoledge').html(ks.shift());
    }, 18000);
  });

  $('video').bind('pause', function (e) {
    console.log("PAUSE");
    stopRecording();
    clearInterval(infoInterval);
    clearInterval(pptInterval);
  });

});

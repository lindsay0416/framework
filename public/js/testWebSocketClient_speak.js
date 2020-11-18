// var connection = new WebSocket('ws://localhost:9090');
// const connection = new WebSocket('ws://caito-demo.mybluemix.net:443');
var host = location.origin.replace(/^http/, 'ws');
// var host = `ws://cba-wbc-demo.au-syd.mybluemix.net`;
var connection = new WebSocket(host);
console.log(host);

// const connection = new WebSocket('wss://192.168.1.169:9090');
connection.onopen = onopen;
connection.onmessage = onmessage;
connection.onclose = onclose;
connection.onerror = onerror;



(function (window) {

})(this);


/*
$(window).bind('resize', function() {
  console.log("resize is triggered");
  $('#left').css({
    'height': '100%',
    'padding': '0px',
    'resize': 'both'
  });

  $('#right').css({
    'height': '100%',
    'padding': '60px',
    'overflow-y':'scroll',
    'resize': 'both'
  });
});
*/



function downsampleBuffer(buffer, rate) {
  if (rate == sampleRate) {
    return buffer;
  }
  if (rate > sampleRate) {
    throw "downsampling rate show be smaller than original sample rate";
  }
  var sampleRateRatio = sampleRate / rate;
  var newLength = Math.round(buffer.length / sampleRateRatio);
  var result = new Float32Array(newLength);
  var offsetResult = 0;
  var offsetBuffer = 0;
  while (offsetResult < result.length) {
    var nextOffsetBuffer = Math.round((offsetResult + 1) * sampleRateRatio);
    var accum = 0, count = 0;
    for (var i = offsetBuffer; i < nextOffsetBuffer && i < buffer.length; i++) {
      accum += buffer[i];
      count++;
    }
    result[offsetResult] = accum / count;
    offsetResult++;
    offsetBuffer = nextOffsetBuffer;
  }
  return result;
}

function convertoFloat32ToInt16(buffer) {
  var l = buffer.length;
  var buf = new Int16Array(l)

  while (l--) {

    buf[l] = buffer[l] * 0xFFFF;    //convert to 16 bit
  }
  return buf.buffer
}


var sampleRate = 48000;


function onopen(e) {
  console.log("Websocket Open");
  connection.send("hello from client!");

  if (!navigator.getUserMedia)
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia ||
      navigator.mozGetUserMedia || navigator.msGetUserMedia;

  if (navigator.getUserMedia) {
    navigator.getUserMedia({ audio: true }, success, function (e) {
      alert('Error capturing audio.');
    });
  } else alert('getUserMedia not supported in this browser.');

  var recording = false;

  window.startRecording = function () {
    recording = true;
    console.log("startRecording is triggered!!!");
  }

  window.stopRecording = function () {
    recording = false;
    // window.Stream.end();
  }


  function success(e) {
    audioContext = window.AudioContext || window.webkitAudioContext;
    context = new audioContext();
    console.log(`Context: ====  ${context.sampleRate}`);

    // the sample rate is in context.sampleRate
    audioInput = context.createMediaStreamSource(e);

    var bufferSize = 2048;
    recorder = context.createScriptProcessor(bufferSize, 1, 1);

    // var resampler = new Resampler(context.sampleRate, 16000, 1);
    recorder.onaudioprocess = function (e) {
      if (!recording) return;
      console.log('recording...');
      var left = e.inputBuffer.getChannelData(0);
      // var convertedBuffer = convertoFloat32ToInt16(left);

      // var resampled = resampler.resampler(left);
      // console.log(resampled);
      var resampled = downsampleBuffer(left, 16000);
      connection.send(convertoFloat32ToInt16(resampled));

      //keep the original sample rate
      // connection.send(convertoFloat32ToInt16(left));

      // window.Stream.write(convertoFloat32ToInt16(resampled));

      // console.log(window.Stream.readable);

      // window.Stream.on('data', function(data){
      //   console.log(data);
      // });

    }
    audioInput.connect(recorder)
    recorder.connect(context.destination);
  }

}

function onmessage(e) {
  var message = JSON.parse(e.data);
  // console.log(message.code);
 
  $('#transcription').html(message.text);

  if (message.code == 2000) {
    console.log(message);
    $('#transcript').append(`<p>${message.text}</p>`);
    //scroll down -> For Caito Normal Version
    window.scrollTo(0,document.body.scrollHeight);

    //preprocessing ... (if needed)

    //=============================================
    // send the transcript back to the site to grab knowledge
    // $.get('/nluquery', {text: e.data.substring(2)}, function(data){
    //   // console.log(data);
    //   displayKeywords(data);
    // });

    //==============================================
    //send the transcript back to the site to translate
    if (translationFlag) {
      $.get('/translate', {
        text: message.text,
        source: 'en-US',
        target: 'ja-JP'
      }, function (data) {
        console.log(data);
        displayTranslation(data);
      });
    }

  }
}

//=====================================
//capture the slidebar changing actions
var translationFlag = false;
/*
$('#translation_tag').change(function() {
    // console.log("translation_tag has changed");
    if(translationFlag){
      $('#translated_transcription').html('');
      translationFlag = false;
    }
    else
    {
      $('#translated_transcription').html('');
      translationFlag = true;
    }
    console.log(`Is translation: ${translationFlag}`);
});
*/

//=====================================

function onerror(e) {
  console.log("ERROR");
  console.log(e);
}

// function scrollToElement(ele) {
//   $('html,body').animate({
//         scrollTop: $(ele).offset().top},
//         'slow');
// }

function TapOnStart() {

}

//======================================

function displayTranslation(data) {
  // $('#right').append(`<div><p class="p1">${data.text}</p> <p class="p2">${data.translation}</p> </div>`);
  // $('#right').scrollTop($('#right')[0].scrollHeight);
  // $('#translated_transcription').html(data.translation);
}


function displayKeywords(data) {
  var keywords = obtainKeywords(data);
  $.each(keywords, function (i, item) {
    $.get('/queryKeyword', { keyword: item.text }, function (description) {
      $('#right').append(`<div><p class="p1">${item.text}</p> <p class="p2">${description}</p> </div>`);
      $('#right').scrollTop($('#right')[0].scrollHeight);
      //  text(`${item.text} : ${item.relevance}`).appendTo('body>dl');
      //  if(description != null) $('<dd>').text(description).appendTo('body>dl');
      // console.log(data);
    });
    //  $('<dd>').text(JSON.stringify(item.relevance)).appendTo('body>dl');
  });
}

function displayEntities(data) {
  var entities = obtainEntities(data);

  $.each(entities, function (i, item) {
    $('<dt>').text(item.type).appendTo('body>dl');
    $('<dd>').text(JSON.stringify(item.emotion)).appendTo('body>dl');
  });
}

//=======================================

function obtainEntities(data) {
  var entities = [];
  $.each(data.entities, function (i, item) {
    var sentiment = new Sentiment(item.sentiment.score);
    var emotion = new Emotion(item.emotion.sadness, item.emotion.joy, item.emotion.fear, item.emotion.disgust, item.emotion.anger);
    entities.push(new Entity(item.type, item.text, sentiment, emotion));
  });
  return entities;
}


function Entity(type, text, sentiment, emotion) {
  this.type = type;
  this.text = text;
  this.sentiment = sentiment;
  this.emotion = emotion;
}


function Sentiment(score) {
  this.score = score;
}


function Emotion(sadness, joy, fear, disgust, anger) {
  this.sadness = sadness;
  this.joy = joy;
  this.fear = fear;
  this.disgust = disgust;
  this.anger = anger;
}


//=========================================

function obtainCategories(data) {
  var categories = [];
  $.each(data.categories, function (i, item) {
    categories.push(new Category(item.score, item.label));
  });
  return categories;
}


function Category(score, label) {
  var categoryLevels = label.split("/");
  categoryLevels.shift(); //remove the first element
  this.score = score;
  this.categoryLevels = categoryLevels;
  this.label = label;
}


//==========================================


function obtainKeywords(data) {
  var keywords = [];
  $.each(data.keywords, function (i, item) {
    keywords.push(new Keyword(item.text, item.relevance));
  });
  return keywords;
}

function Keyword(text, relevance) {
  this.text = text;
  this.relevance = relevance;
}


//=============================================================
function obtainRelations(data) {
  var relations = [];
  $.each(data.relations, function (i, itemRelation) {
    var relationArguments = [];
    $.each(itemRelation.arguments, function (j, itemArgument) {
      var relationEntities = [];
      $.each(itemArgument.entities, function (k, itemEntity) {
        relationEntities.push(new RelationshipArgumentEntity(itemEntity.type, itemEntity.text))
      });
      relationArguments.push(new RelationArugment(itemArgument.text, relationEntities));
    });
    relations.push(new Relation(itemRelation.type, itemRelation.sentence, itemRelation.score, relationArguments));
  });
  return relations;
}



function Relation(type, sentence, score, relationArguments) {
  this.type = type;
  this.sentence = sentence;
  this.score = score;
  this.arguments = relationArguments; //array
}


function RelationArugment(text, entities) {
  this.text = text;
  this.entities = entities; //array
}


function RelationshipArgumentEntity(type, text) {
  this.type = type;
  this.text = text;
}

//================================================
function obtainConcepts(data) {
  var concepts = [];
  $.each(data.concepts, function (i, item) {
    concepts.push(new Concept(item.text, item.relevance, item.dbpedia_resource));
  });
  return concepts;
}

//for concept object
function Concept(text, relevance, dbpedia_resource) {
  this.text = text;
  this.relevance = relevance;
  this.dbpedia_resource = dbpedia_resource;
}

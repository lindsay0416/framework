$(document).ready(function() {
  // $.getJSON('/dictionary-api', printTerms);
  $('form').submit(function(e) {
    console.log('form is submitting...');
    console.log($('#text_analyse').val());
    e.preventDefault();
    // $.post('/dictionary-api', {term: $('#term').val(), defined: $('#defined').val()}, printTerms);
    $.post('/QueryDocByNaturalLanguage', {
      text: $('#text_analyse').val(),
      docid: $('#text_analyse').val(),
      agg: true, //future should be sentiments:true...
      who: 'Leo'
    }, function(data) {
      // $('#displayjson').html(JSON.stringify(data, null, 4));
      //encapsulation....
      $('#displayjson').html(data.aggregations[0].field);
      // console.log(data);
      // console.log(data.aggregations[0].field);
    });

    /*
    $.get('/queryget', {
      text: $('#text').val()
    }, function(data) {
      console.log(data);
    });
    */
    // this.reset();
  });
});

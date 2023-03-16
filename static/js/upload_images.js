$('form').submit(function(event) {
      event.preventDefault();
      var formData = new FormData(this);
      $.ajax({
        url: '{% url "image_upload" %}',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
          var results = response.results;
          var html = '';
          for (var i = 0; i < results.length; i++) {
            var result = results[i];
            html += '<div class="row">';
            html += '<div class="col">' + '<img src="' + result.step1 + '">' + '</div>';
            //html += '<div class="col">' + '<img src="' + result.step2 + '">' + '</div>';
            //html += '<div class="col">' + '<img src="' + result.step3 + '">' + '</div>';
            html += '</div>';
          }
          $('#results').html(html);
        },
        error: function(xhr, status, error) {
          console.error(xhr.responseText);
        }
      });
    });
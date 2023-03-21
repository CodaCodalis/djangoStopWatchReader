
$('form').submit(function (event) {
    event.preventDefault();
    var formData = new FormData(this);
    $.ajax({
        url: '/yolo/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        dataType: 'json',
        success: function (response) {
            var results = response.results;
            let resultsDiv = document.getElementById('results-container-yolo');
            for (var i = 0; i < results.length; i++) {
                var result = results[i];
                let originalImage = document.createElement('img')
                let originalImageId = 'img' + i + '_original';
                originalImage.setAttribute('id', originalImageId);
                originalImage.src = 'data:image/jpeg;base64,' + result.original;
                resultsDiv.appendChild(originalImage);

                let recognized = result.recognized;
                let recImage = document.createElement('img')
                let recImageId = 'img' + i + '_rec';
                recImage.setAttribute('id', recImageId);
                recImage.src = 'data:image/jpeg;base64,' + recognized;
                resultsDiv.appendChild(recImage);
            }
        },
        error: function (xhr, status, error) {
            console.error(xhr.responseText);
        }
    });
});


$('form').submit(function (event) {
    event.preventDefault();
    var formData = new FormData(this);
    $.ajax({
        url: '/upload_images/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            var results = response.results;
            let resultsDiv = document.getElementById('results-container');
            for (var i = 0; i < results.length; i++) {
                var result = results[i];
                let originalImage = document.createElement('img')
                let originalImageId = 'img' + i + '_original';
                originalImage.setAttribute('id', originalImageId);
                originalImage.src = 'data:image/jpeg;base64,' + result.original;
                resultsDiv.appendChild(originalImage);

                let stepDataList = result.steps;
                for (var j = 0; j < stepDataList.length; j++) {
                    let stepImage = document.createElement('img')
                    let stepImageId = 'img' + i + '_step' + (j + 1);
                    stepImage.setAttribute('id', stepImageId);
                    stepImage.src = 'data:image/jpeg;base64,' + stepDataList[j];
                    resultsDiv.appendChild(stepImage);
                }
            }
        },
        error: function (xhr, status, error) {
            console.error(xhr.responseText);
        }
    });
});

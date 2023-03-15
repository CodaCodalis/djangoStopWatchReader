const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const roi = document.getElementById('roi');
const startWebcamBtn = document.getElementById('start-webcam');
const captureImageBtn = document.getElementById('capture-image');
const stopWebcamBtn = document.getElementById('stop-webcam');
const homeBtn = document.getElementById('home');

startWebcamBtn.addEventListener('click', function () {
    navigator.mediaDevices.getUserMedia({video: true, audio: false})
        .then(function (stream) {
            video.srcObject = stream;
            window.stream = stream;
            video.play();
        })
        .catch(function (err) {
            console.log("An error occurred: " + err);
        });
    startWebcamBtn.style.display = 'none';
    captureImageBtn.style.display = 'block';
    stopWebcamBtn.style.display = 'block';
    roi.style.display = 'block';
    homeBtn.style.display = 'none';
});

captureImageBtn.addEventListener('click', function () {
    let image = canvas.getContext('2d');
    image.drawImage(video, 0, 0, canvas.width, canvas.height);
    let imageData = canvas.toDataURL();

    let formData = new FormData();
    formData.append('image', dataURItoBlob(imageData));

    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload_image/', true);
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.onload = function () {
        if (xhr.status === 200) {
            // Display success message
            // alert('Upload successful!');
            // Parse JSON response
            let response = JSON.parse(xhr.responseText);
            let resultTXT = document.getElementById('result-text');
            resultTXT.innerHTML = response.result;
            let image = document.createElement('img');
            image.src = 'data:image/jpeg;base64,' + response.image;
            let resultIMG = document.getElementById('result-image');
            resultIMG.appendChild(image);
            let resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
        } else {
            // Display error message
            alert('Upload failed!');
        }
    };
    xhr.send(formData);
});
stopWebcamBtn.addEventListener('click', function () {
    window.location.reload();
});

homeBtn.addEventListener('click', function () {
    location.href = '/';
});

function dataURItoBlob(dataURI) {
    // convert base64/URLEncoded data component to raw binary data held in a string
    const byteString = atob(dataURI.split(',')[1]);
    // separate the MIME type from the actual data
    const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    // write the bytes of the string to an ArrayBuffer
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    // convert ArrayBuffer to Blob object
    const blob = new Blob([ab], {type: mimeString});
    return blob;
}
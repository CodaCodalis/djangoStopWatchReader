const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const image = document.getElementById('image');
const startWebcamBtn = document.getElementById('start-webcam');
const takePictureBtn = document.getElementById('take-picture');
const stopWebcamBtn = document.getElementById('stop-webcam');

let stream;

/*
startWebcamBtn.addEventListener('click', function () {
    navigator.mediaDevices.getUserMedia({video: true})
        .then(function (mediaStream) {
            stream = mediaStream;
            video.srcObject = stream;
            video.play();
            video.style.display = 'block';
            canvas.style.display = 'none';
            image.style.display = 'none';
        })
        .catch(function (err) {
            console.log('An error occurred: ' + err);
        });
});
*/

startWebcamBtn.addEventListener('click', function() {
  navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(function(stream) {
      video.srcObject = stream;
      window.stream = stream;
      video.play();
    })
    .catch(function(err) {
      console.log("An error occurred: " + err);
    });
  startWebcamBtn.style.display = 'none';
  stopWebcamBtn.style.display = 'block';
});

takePictureBtn.addEventListener('click', function () {
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    video.pause();
    stream.getTracks().forEach(track => track.stop());
    video.style.display = 'none';
    canvas.style.display = 'block';

    const existingImage = document.getElementById('captured-image');
    existingImage.remove();

    const newImage = new Image();
    newImage.setAttribute('id', 'captured-image');
    newImage.setAttribute('class', 'img-fluid');
    newImage.setAttribute('src', canvas.toDataURL('image/png'));
    document.getElementById('captured-image-container').appendChild(newImage);
});

stopWebcamBtn.addEventListener('click', function() {
    window.location.reload();
});
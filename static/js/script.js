document.getElementById('uploadForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('imageUpload');
    formData.append('image', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('result').style.display = 'block';
                document.getElementById('description').textContent = data.description || data.text;
                document.getElementById('audio').src = data.audio_path;
            }
        })
        .catch(error => {
            alert('An error occurred: ' + error.message);
        });
});

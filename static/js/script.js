document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    // Show the loader and add blur effect
    document.body.classList.add('loading');
    document.getElementById('loader').style.display = 'flex';

    const formData = new FormData(this);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Failed to process the image');
        }

        const data = await response.json();

        // Hide the loader and remove blur effect
        document.body.classList.remove('loading');
        document.getElementById('loader').style.display = 'none';

        // Display the result
        const resultSection = document.getElementById('result');
        resultSection.style.display = 'block';
        document.getElementById('description').innerText = data.text || data.description;
        const audio = document.getElementById('audio');
        audio.src = data.audio_path;
        audio.load();
    } catch (error) {
        console.error(error);

        // Hide the loader and remove blur effect in case of error
        document.body.classList.remove('loading');
        document.getElementById('loader').style.display = 'none';

        alert('An error occurred while processing the image.');
    }
});

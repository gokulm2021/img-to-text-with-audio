document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('uploadForm');
    const loader = document.getElementById('loader');
    const result = document.getElementById('result');
    const description = document.getElementById('description');
    const audioContainer = document.getElementById('audio');  // Container to hold the audio element

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show the loader while processing
        loader.style.display = 'flex';

        const formData = new FormData(form);

        try {
            // Sending the image to the Flask backend for processing
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            // Handle the JSON response from the backend
            const data = await response.json();

            // Hide loader and display result
            loader.style.display = 'none';
            result.style.display = 'block';

            if (data.error) {
                description.innerHTML = `<strong>Error:</strong> ${data.error}`;
                return;
            }

            // Display the description
            description.innerHTML = `<strong>Description:</strong> ${data.description || 'No description available'}`;

            // Clear previous audio and create new audio element if available
            if (data.audio_path && data.audio_path !== 'undefined') {
                const audioElement = document.createElement('audio');
                audioElement.controls = true;  // Add controls for play/pause
                audioElement.src = data.audio_path;  // Path to the generated audio
                audioContainer.innerHTML = '';  // Clear previous audio
                audioContainer.appendChild(audioElement);
                audioElement.play();  // Automatically play the audio
            } else {
                console.error('Invalid audio path:', data.audio_path);
            }

        } catch (error) {
            console.error('Error uploading image:', error);
            loader.style.display = 'none';
        }
    });
});

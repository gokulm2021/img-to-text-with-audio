document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('uploadForm');
    const loader = document.getElementById('loader');
    const result = document.getElementById('result');
    const description = document.getElementById('description');
    const audio = document.getElementById('audio');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        loader.style.display = 'block';
        result.style.display = 'none';

        const formData = new FormData(form);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            loader.style.display = 'none';

            if (data.error) {
                description.innerHTML = `<strong>Error:</strong> ${data.error}`;
                return;
            }

            description.innerHTML = `<strong>Result:</strong> ${data.text || data.description}`;
            if (data.audio_path) {
                audio.src = data.audio_path;
                audio.style.display = 'block';
                audio.play();
            }
            result.style.display = 'block';
        } catch (error) {
            loader.style.display = 'none';
            description.innerHTML = `<strong>Error:</strong> Failed to upload image.`;
        }
    });
});

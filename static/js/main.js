function uploadFile() {
    const fileInput = document.getElementById('audioFile');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a file first');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('File uploaded successfully');
            // Update audio player source
            const audioPlayer = document.getElementById('audioPlayer');
            audioPlayer.src = URL.createObjectURL(file);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading file');
    });
}

function processPitch() {
    const semitones = document.getElementById('semitones').value;
    processAudio('pitch_shift', { semitones: parseFloat(semitones) });
}

function processSpeed() {
    const speed = document.getElementById('speed').value;
    processAudio('change_speed', { factor: parseFloat(speed) });
}

function processAudio(operation, params) {
    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            operation: operation,
            params: params
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Audio processed successfully');
            // Update audio player with processed audio
            const audioPlayer = document.getElementById('audioPlayer');
            audioPlayer.src = '/download?' + new Date().getTime();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error processing audio');
    });
}

function downloadProcessed() {
    window.location.href = '/download';
}

// Volume control
document.getElementById('volume').addEventListener('input', function(e) {
    const audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.volume = e.target.value;
}); 
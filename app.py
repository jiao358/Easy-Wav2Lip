from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import librosa
import soundfile as sf
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class AudioProcessor:
    def __init__(self):
        self.audio_data = None
        self.sr = None
        self.current_file = None

    def load_audio(self, file_path):
        self.audio_data, self.sr = librosa.load(file_path)
        self.current_file = file_path

    def pitch_shift(self, semitones):
        if self.audio_data is not None:
            return librosa.effects.pitch_shift(self.audio_data, sr=self.sr, n_steps=semitones)
        return None

    def change_speed(self, factor):
        if self.audio_data is not None:
            return librosa.effects.time_stretch(self.audio_data, rate=factor)
        return None

audio_processor = AudioProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    audio_processor.load_audio(filepath)
    
    return jsonify({'message': 'File uploaded successfully'})

@app.route('/process', methods=['POST'])
def process_audio():
    data = request.json
    operation = data.get('operation')
    params = data.get('params', {})
    
    if operation == 'pitch_shift':
        processed = audio_processor.pitch_shift(params.get('semitones', 0))
    elif operation == 'change_speed':
        processed = audio_processor.change_speed(params.get('factor', 1.0))
    else:
        return jsonify({'error': 'Invalid operation'}), 400
    
    # 保存处理后的音频
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed.wav')
    sf.write(output_path, processed, audio_processor.sr)
    
    return jsonify({'message': 'Audio processed successfully'})

@app.route('/download')
def download_file():
    return send_file(
        os.path.join(app.config['UPLOAD_FOLDER'], 'processed.wav'),
        as_attachment=True,
        download_name='processed.wav'
    )

if __name__ == '__main__':
    app.run(debug=True) 
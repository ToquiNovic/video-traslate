import os
import pytube
import whisper

# Descargar el archivo de audio desde YouTube
youtubeVideoId = "https://www.youtube.com/watch?v=cz-DaqClllQ&ab_channel=midudev"
youtubeVideo = pytube.YouTube(youtubeVideoId)
audio = youtubeVideo.streams.get_audio_only()
audio.download(filename='tmp.mp4')

# Verificar si el archivo existe
file_path = os.path.join(os.getcwd(), 'tmp.mp4')
if os.path.isfile(file_path):
    # Cargar el modelo Whisper
    model = whisper.load_model('small')

    # Transcribir el archivo de audio
    result = model.transcribe(file_path)
    print(result["text"])
else:
    print('El archivo no existe.')
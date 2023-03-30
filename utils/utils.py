
import os
from PIL import Image

import librosa

# Fonction pour redimensionner une image
def resize_image(image_path, new_size=(256, 256)):
    with Image.open(image_path) as image:
        resized_image = image.resize(new_size)
    return resized_image

# Fonction pour sauvegarder une image sur le disque
def save_to_disk(image, directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    file_name = os.path.basename(image.filename)
    file_path = os.path.join(directory_path, file_name)
    image.save(file_path)


# Fonction pour couper une partie d'un fichier audio
def trim_audio(audio_path, start_time, end_time):
    y, sr = librosa.load(audio_path, sr=None, mono=True)
    start_frame = int(start_time * sr)
    end_frame = int(end_time * sr)
    trimmed_audio = y[start_frame:end_frame]
    return trimmed_audio

# Fonction pour sauvegarder un fichier audio sur le disque
def save_audio_to_disk(audio, directory_path, file_name):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    file_path = os.path.join(directory_path, file_name)
    librosa.output.write_wav(file_path, audio, sr=44100)

import os
from docx2pdf import convert

# Fonction pour convertir un fichier vers le format PDF
def convert_to_pdf(file_path):
    converted_file_path = os.path.splitext(file_path)[0] + '.pdf'
    convert(file_path, converted_file_path)
    return converted_file_path

# Fonction pour sauvegarder un fichier sur le disque
def save_file_to_disk(file_path, directory_path, file_name):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    new_file_path = os.path.join(directory_path, file_name)
    os.rename(file_path, new_file_path)

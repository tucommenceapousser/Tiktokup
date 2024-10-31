from flask import Flask, request, render_template
import openai
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
import os
import requests
import tempfile
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()
# Configuration OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Configuration des dossiers
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Dossier pour stocker les fichiers temporaires
if not os.path.exists("static"):
    os.makedirs("static")

# Fonction pour générer la voix à partir de texte avec Eleven Labs
def generate_voice_eleven_labs(text, filename="static/audio.mp3"):
    api_url = "https://api.elevenlabs.io/v1/text-to-speech"
    headers = {
        "Authorization": f"Bearer {os.getenv('ELEVEN_LABS_API_KEY')}",  # Remplacez par os.getenv('ELEVEN_LABS_API_KEY') si vous stockez la clé dans les variables d'environnement
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice": "elevenlabs-voice-id",  # Remplacez par l'ID de la voix souhaitée
        "model_id": "elevenlabs-model-id"  # Remplacez par l'ID de votre modèle, si nécessaire
    }

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print(f"Erreur lors de la génération de la voix: {response.status_code}, {response.text}")

    return filename

# Fonction pour créer la vidéo
def create_video(image_path, audio_path, text, output="static/output_video.mp4"):
    # Chargement de l'image de fond
    image_clip = ImageClip(image_path).set_duration(10)

    # Création du texte animé
    text_clip = TextClip(text, fontsize=24, color='white', font="Arial-Bold", bg_color="#ff005a")
    text_clip = text_clip.set_position("center").set_duration(10).crossfadein(1).crossfadeout(1)

    # Chargement de l'audio
    audio_clip = AudioFileClip(audio_path)

    # Composite des éléments
    video = CompositeVideoClip([image_clip, text_clip])
    video = video.set_audio(audio_clip)

    # Export de la vidéo
    video.write_videofile(output, fps=24)
    return output

# Fonction pour obtenir une image via DALL-E
def generate_image(prompt, filename="static/image.png"):
    response = openai.Image.create(prompt=prompt, n=1, size="512x512")
    image_url = response["data"][0]["url"]
    image_data = requests.get(image_url).content
    with open(filename, "wb") as f:
        f.write(image_data)
    return filename

# Route pour la page principale
@app.route('/')
def index():
    return render_template('index.html')

def transcribe_audio(audio_file_path):
    """Transcrit un fichier audio en utilisant Whisper API"""
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                language="fr"
            )
        return transcript.get('text', '')
    except Exception as e:
        print(f"Erreur de transcription: {str(e)}")
        return "Erreur lors de la transcription"

def process_video_file(video_file_path):
    """Extrait l'audio d'une vidéo et le transcrit"""
    try:
        # Créer un fichier audio temporaire
        temp_audio = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        video_clip = VideoFileClip(video_file_path)
        video_clip.audio.write_audiofile(temp_audio.name)
        video_clip.close()

        # Transcrire l'audio
        transcription = transcribe_audio(temp_audio.name)

        # Nettoyer
        os.unlink(temp_audio.name)
        return transcription
    except Exception as e:
        print(f"Erreur de traitement vidéo: {str(e)}")
        return "Erreur lors du traitement de la vidéo"

@app.route('/optimize', methods=['POST'])
def optimize_content():
    content = request.form['content']
    image_theme = request.form['image_theme']

    # Gestion du fichier audio/vidéo
    media_file = request.files['audio_file']
    transcription_text = ""

    if media_file:
        filename = secure_filename(media_file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        media_file.save(file_path)

        # Détecter si c'est un fichier audio ou vidéo
        if filename.lower().endswith(('.mp4', '.mov', '.avi')):
            transcription_text = process_video_file(file_path)
        else:  # fichier audio
            transcription_text = transcribe_audio(file_path)

    # Optimisation du contenu avec GPT
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Utiliser GPT-4 comme demandé
        messages=[
            {"role": "system", "content": "Tu es un expert en optimisation de contenu TikTok."},
            {"role": "user", "content": f"""Optimise cette description TikTok en te basant sur:
            - Description originale: {content}
            - Transcription: {transcription_text}

            Rends-la plus engageante et virale."""}
        ],
        max_tokens=100,
        temperature=0.7
    )
    suggestion = response['choices'][0]['message']['content'].strip()

    # Génération de l'image
    image_path = generate_image(image_theme)

    # Génération de la voix avec Eleven Labs
    audio_path = generate_voice_eleven_labs(suggestion)

    # Création de la vidéo
    video_path = create_video(image_path, audio_path, suggestion)

    return render_template(
        'result.html',
        original_content=content,
        suggestion=suggestion,
        transcription=transcription_text,
        image_url=image_path,
        video_url=video_path
    )

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
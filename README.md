# Projet Flask de Génération de Vidéos

## Description

Ce projet utilise Flask pour créer une application web permettant de générer des vidéos à partir de fichiers audio et d'images, en utilisant l'API OpenAI pour optimiser le contenu. Il utilise également l'API Eleven Labs pour la synthèse vocale.

## Fonctionnalités

- **Génération de Vidéos** : Créez des vidéos en combinant du texte, des images et des fichiers audio.
- **Transcription Audio** : Utilise l'API Whisper d'OpenAI pour transcrire des fichiers audio.
- **Optimisation de Contenu** : Améliorez vos descriptions TikTok avec GPT-4.
- **Synthèse Vocale** : Générez des voix de haute qualité à partir de texte avec Eleven Labs.

## Technologies Utilisées

- **Flask** : Framework web pour Python.
- **OpenAI** : API pour la génération de texte et la transcription audio.
- **Eleven Labs** : API pour la synthèse vocale.
- **MoviePy** : Bibliothèque pour la manipulation de vidéos.
- **Requests** : Pour effectuer des requêtes HTTP.
- **Python-dotenv** : Pour gérer les variables d'environnement.

## Prérequis

Assurez-vous d'avoir Python 3.7 ou supérieur installé. Installez également les bibliothèques nécessaires avec :

```bash
pip install -r requirements.txt
```

## Configuration

1. Clonez le dépôt :

    ```bash
    git clone https://votre-repo-url.git
    cd votre-dossier
    ```

2. Créez un fichier `.env` à la racine de votre projet et ajoutez vos clés API :

    ```plaintext
    OPENAI_API_KEY=your_openai_api_key
    ELEVEN_LABS_API_KEY=your_eleven_labs_api_key
    ```

## Utilisation

1. Démarrez l'application Flask :

    ```bash
    python app.py
    ```

2. Ouvrez votre navigateur et allez à `http://127.0.0.1:8080`.

3. Téléchargez votre fichier audio ou vidéo, ajoutez un thème d'image et une description, puis cliquez sur le bouton pour générer votre vidéo.

## Screenshots

Voici quelques captures d'écran de l'application :

## Contribuer

Si vous souhaitez contribuer à ce projet, n'hésitez pas à ouvrir une issue ou à soumettre une demande de tirage.

## Auteurs

Votre Nom - Votre Profil GitHub

## License

Ce projet est sous licence MIT. Pour plus de détails, consultez le fichier LICENSE.

# Transcribe++

![Transcribe++ Banner](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/SVG_Text_Font_Test_Ubuntu.svg/800px-SVG_Text_Font_Test_Ubuntu.svg.png)

## 🎙️ Overview

**Transcribe++** is a Python-based audio-to-text transcription tool that goes far beyond traditional speech recognition. It transcribes recorded audio clips, extracts relevant keywords using NLP, performs image searches for visual representation, and logs both keywords and errors. It’s built with education, automation, and smart assistance in mind — ideal for students, researchers, and hobbyists.

---

## 📁 Project Structure

```
├── Transcribe ++.py                 # Main application file
├── log.txt                          # Runtime log file (errors & keywords)
├── settings.txt                     # Configuration for frequency, duration, and API keys
├── saved_keywords_and_urls.txt     # Import/export keyword-URL database
├── transcribed_data.txt            # Logged transcriptions from audio input
├── keywords_database.db            # SQLite3 database storing keyword-URL pairs
```

---

## 🧠 Features

- 🎙️ Record audio clips (WAV format)
- 📝 Transcribe speech to text using Google's Speech Recognition API
- 🧠 Extract keywords using NLTK (nouns only)
- 🔍 Search for images related to keywords via Google Custom Search API
- 🌐 Automatically open top image result in the browser
- 🗂️ Save keyword-URL pairs in SQLite database
- 📥 Import/export keyword-URL mappings via `.txt` files
- 🧾 Timestamped error and keyword logging
- ⚙️ Adjustable settings for frequency, duration, API key, and CX
- 🖼️ Auto-generated visual explanations based on audio input
- 💬 Menu-driven console interface for ease of use

---

## 📦 Modules Used

| Module              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `sqlite3`           | Manages local database storage of keyword-image mappings                    |
| `sounddevice`       | Captures microphone input for audio recording                               |
| `soundfile`         | Saves and reads `.wav` audio files                                          |
| `speech_recognition`| Converts audio to text using Google API                                     |
| `nltk`              | Extracts keywords from transcribed text                                     |
| `google_images_search` | Performs image search using keywords (Google Custom Search API)        |
| `datetime`          | Generates timestamps for logging                                            |
| `webbrowser`        | Opens image URLs in default browser                                         |
| `os`                | File management and environment checks                                      |

---

## 🔧 Configuration

Settings can be changed manually in `settings.txt` or via the app menu.

```txt
api_key::YOUR_API_KEY_HERE
cx::YOUR_CUSTOM_SEARCH_ENGINE_ID
fs::44100
clip_duration::2
```

---

## 🚀 How to Run

### 🐍 Requirements

Install the required libraries (if not already):

```bash
pip install sounddevice soundfile SpeechRecognition nltk google_images_search
```

### ▶️ Run the script

```bash
python "Transcribe ++.py"
```

---

## 💡 Usage

1. Launch the program.
2. Choose from:
   - Record a clip
   - Manage keywords and URLs
   - Change settings
3. Record your voice. The app transcribes, extracts nouns, logs keywords, and opens relevant images.
4. All errors and keyword logs are saved with timestamps in `log.txt`.

---

## 🧪 Sample Outputs

**Log file (`log.txt`) snippet:**
```
[KEYWORDS - 2023-10-02 18:20:32] potatoes, potatoes, potato
[ERROR - 2023-10-03 10:42:03] 'NoneType' object has no attribute 'split'
```

**Keyword-image mapping (`saved_keywords_and_urls.txt`):**
```
potatoes::https://m.media-amazon.com/images/I/41OV379W9bL._AC_UF1000,1000_QL80_.jpg
```

**Transcribed text (`transcribed_data.txt`):**
```
[2023-09-18 16:02:06] potato food
```

---

## 📊 Database Schema

Table: `keywords`

| Field    | Type    | Description                    |
|----------|---------|--------------------------------|
| id       | INTEGER | Primary key, auto-increment    |
| keyword  | TEXT    | Unique keyword extracted        |
| url      | TEXT    | Associated image URL            |

---

## ❗ Known Issues

- API quota exceeded errors from Google Custom Search (`rateLimitExceeded`)
- Transcription errors may cause `'NoneType' object has no attribute 'split'`
- Some keywords may not yield valid images depending on search results

---

## 📚 Acknowledgements

This project was developed as part of the AISSCE practicals and serves as a comprehensive integration of speech recognition, natural language processing, image search automation, and database handling. Special thanks to mentors and peers for their support.

---

## 🧑‍💻 Author

**Dhasvanth Muthukumar Gokila**  
Grade 12 – AISSCE  
Python Enthusiast | Tech Explorer

---

## 🏁 Conclusion

Transcribe++ isn't just a speech-to-text tool — it’s a full-stack multimedia assistant for research, presentations, and information synthesis. With automation and accessibility at its core, it bridges voice, text, and visuals to make technology more intuitive and expressive.

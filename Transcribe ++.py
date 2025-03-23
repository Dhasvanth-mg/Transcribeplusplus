import os
import webbrowser
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import nltk
from google_images_search import GoogleImagesSearch
from datetime import datetime
import sqlite3

DATABASE_FILENAME = 'keywords_database.db'
LOG_FILENAME = 'log.txt'

ascii_art = """
████████╗██████╗░░█████╗░███╗░░██╗░██████╗░█████╗░██████╗░██╗██████╗░███████╗  ░░░░░░░░░░░░░░
╚══██╔══╝██╔══██╗██╔══██╗████╗░██║██╔════╝██╔══██╗██╔══██╗██║██╔══██╗██╔════╝  ░░██╗░░░░██╗░░
░░░██║░░░██████╔╝███████║██╔██╗██║╚█████╗░██║░░╚═╝██████╔╝██║██████╦╝█████╗░░  ██████╗██████╗
░░░██║░░░██╔══██╗██╔══██║██║╚████║░╚═══██╗██║░░██╗██╔══██╗██║██╔══██╗██╔══╝░░  ╚═██╔═╝╚═██╔═╝
░░░██║░░░██║░░██║██║░░██║██║░╚███║██████╔╝╚█████╔╝██║░░██║██║██████╦╝███████╗  ░░╚═╝░░░░╚═╝░░
░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝╚═════╝░╚══════╝  ░░░░░░░░░░░░░░
"""

def init_database():
    connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY,
            keyword TEXT UNIQUE,
            url TEXT
        )
    ''')
    connection.commit()
    connection.close()

def save_keyword_url_to_database(keyword, url):
    connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO keywords (keyword, url)
        VALUES (?, ?)
    ''', (keyword, url))
    connection.commit()
    connection.close()

def get_saved_keywords_and_urls_from_database():
    connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = connection.cursor()
    cursor.execute('SELECT keyword, url FROM keywords')
    rows = cursor.fetchall()
    connection.close()
    return {row[0]: row[1] for row in rows}

def log_error(error_message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILENAME, 'a') as log_file:
        log_file.write(f"[ERROR - {timestamp}] {error_message}\n")

def log_keywords(keywords):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILENAME, 'a') as log_file:
        log_file.write(f"[KEYWORDS - {timestamp}] {', '.join(keywords)}\n")

def convert_wav_to_text(wav_file):
    try:
        r = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text
    except Exception as e:
        log_error(str(e) + str(wav_file))
        return None  # Return None if transcription fails

def convert_text_to_keyword(text):
    lines = text.split("\n")
    sentences = nltk.sent_tokenize(" ".join(lines))
    nouns = []
    for sentence in sentences:
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                nouns.append(word)
    return nouns

def search_and_open_image(keyword):
    saved_keywords_and_urls = get_saved_keywords_and_urls_from_database()
    saved_url = saved_keywords_and_urls.get(keyword)
    if saved_url:
        webbrowser.open(saved_url)
        return
    api_key = 'AIzaSyAcXfKjFkZaN4p6Fc8iu5kKWBiaJBXUSzE'
    cx = 'c21816f5610004210'
    gis = GoogleImagesSearch(api_key, cx)
    search_params = {
        'q': keyword,
        'num': 1,
        'fileType': 'png',
        'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
        'safe': 'safeUndefined',
        'imgType': 'imgTypeUndefined',
        'imgSize': 'imgSizeUndefined',
        'imgDominantColor': 'imgDominantColorUndefined',
        'imgColorType': 'imgColorTypeUndefined'
    }
    gis.search(search_params=search_params, path_to_dir='')
    first_image_url = gis.results()[0].url
    webbrowser.open(first_image_url)
    save_keyword_url_to_database(keyword, first_image_url)

def record_clip():
    clip_counter = 1
    print("Recording... Press Ctrl+C to stop recording.")
    try:
        while True:
            print(f"Recording Clip {clip_counter}...")
            audio_data = sd.rec(int(5 * fs), samplerate=fs, channels=2, dtype='float64')
            sd.wait()
            clip_filename = f'clip_{clip_counter}.wav'
            sf.write(clip_filename, audio_data, fs)
            clip_text = convert_wav_to_text(clip_filename)
            clear_transcript_separator()
            keywords = convert_text_to_keyword(clip_text)
            log_keywords(keywords) 
            print(f"Clip {clip_counter} saved and transcribed")
            print("Keywords:", keywords)
            if len(keywords) > 0:
                search_and_open_image(keywords[0])
            clip_counter += 1
    except KeyboardInterrupt:
        print("Recording stopped.")
    except Exception as e:
        log_error(str(e))

def callback(indata, frames, time, status):
    clip_filename = f'clip_{clip_counter}.wav'
    sf.write(clip_filename, indata, fs)
    clip_text = convert_wav_to_text(clip_filename)
    clear_transcript_separator()
    keywords = convert_text_to_keyword(clip_text)
    print(f"Clip {clip_counter} saved and transcribed")
    print("Keywords:", keywords)
    if len(keywords) > 0:
        search_and_open_image(keywords[0])

def clear_transcript_separator():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILENAME, 'a') as log_file:
        log_file.write(f"\n=============================================\n\n")

def erase_all_values_from_database():
    connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM keywords')
    connection.commit()
    connection.close()
    print("All values erased from the database.")

def import_keywords_and_urls_from_txt(file_path):
    try:
        with open(file_path, 'r') as txt_file:
            lines = txt_file.readlines()
        for line in lines:
            parts = line.strip().split("::")
            if len(parts) == 2:
                keyword = parts[0].strip()
                url = parts[1].strip()
                saved_keywords_and_urls = get_saved_keywords_and_urls_from_database()
                if keyword in saved_keywords_and_urls:
                    save_keyword_url_to_database(keyword, url)
                else:
                    save_keyword_url_to_database(keyword, url)
        print("Keywords and URLs imported successfully.")
    except Exception as e:
        print("An error occurred while importing keywords and URLs.")
        print(str(e))

def manage_keywords_and_urls():
    while True:
        print(' ')
        print(ascii_art)
        print("Keyword and URL Management Menu:")
        print("1. Add Keyword and URL")
        print("2. View Saved Keywords and URLs")
        print("3. Edit Keyword URL")
        print("4. Erase All Values from Database")
        print("5. Import Keywords and URLs from .txt")
        print("6. Go Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            keyword = input("Enter a keyword: ")
            url = input("Enter the URL: ")
            save_keyword_url_to_database(keyword, url)
        elif choice == '2':
            saved_keywords_and_urls = get_saved_keywords_and_urls_from_database()
            if saved_keywords_and_urls:
                for keyword, url in saved_keywords_and_urls.items():
                    print(f"{keyword}: {url}")
            else:
                print("No keywords and URLs saved.")
        elif choice == '3':
            keyword = input("Enter the keyword to edit: ")
            new_url = input("Enter the new URL: ")
            save_keyword_url_to_database(keyword, new_url)
        elif choice == '4':
            erase_all_values_from_database()
        elif choice == '5':
            txt_filename = input("Enter the .txt file path: ")
            import_keywords_and_urls_from_txt(txt_filename)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")


def record_clip_menu():
    while True:
        print(' ')
        print(ascii_art)
        print("Recording Menu:")
        print("1. Record a Clip")
        print("2. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                record_clip()  # Adjusted here
            except KeyboardInterrupt:
                print("Recording stopped.")
            input("Press Enter to continue...")
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please try again.")

def change_settings():
    while True:
        global fs, clip_duration, api_key, cx
        print(ascii_art)
        print('1. Change Frequency')
        print('2. Change Clip Duration')
        print('3. Change Api Key')
        print('4. Change Cx')
        print('5. Return to Main Menu')
        ch = input('Enter Your Choice: ')
        try:
            if ch == '1':
                fs = int(input('Enter New Recording Frequency: '))
            elif ch == '2':
                clip_duration = int(input('Enter New Clip Duration in Seconds: '))
            elif ch == '3':
                api_key = input('Enter New Api Key: ')
            elif ch == '4':
                cx = input('Enter new cx: ')
            elif ch == '5':
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Create log and transcript files
if not os.path.exists(LOG_FILENAME):
    open(LOG_FILENAME, 'w').close()

# Initialize the SQLite database
init_database()

# Define recording settings
fs = 44100
clip_duration = 5 
clip_counter = 1

menu_options = {
    '1': record_clip_menu,
    '2': manage_keywords_and_urls,
}

while True:
    print(ascii_art)
    print(' ')
    print("MAIN MENU:")
    print("1. Record a Clip")
    print("2. Manage Keywords and URLs")
    print("3. Change Settings")
    print("4. Quit")
    choice = input("Enter your choice: ")

    if choice in menu_options:
        menu_options[choice]()
    elif choice == '3':
        change_settings()
    elif choice == '4':
        break
    else:
        print("Invalid choice. Please try again.")
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
LOUDME_COOKIE = os.getenv("LOUDME_COOKIE")
if not LOUDME_COOKIE:
    raise EnvironmentError("LOUDME_COOKIE is not set. Please set it in the .env file.")

BASE_URL = "https://loudme.ai/api/trpc/music.generateMusic?batch=1"
NANOGPT_MODEL = os.getenv("NANOGPT_MODEL")

# Load the song data from song.txt
def load_song_data(file_path='song.txt'):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"{file_path} not found. Please ensure the file exists.")

# Extract relevant parts from song data
def extract_song_parts(song_data):
    try:
        description = song_data.split("Description:")[1].split("Title:")[0].strip()[:200]
        title = song_data.split("Title:")[1].split("Lyrics:")[0].strip()[:(80-3-len(NANOGPT_MODEL))] + " - "+NANOGPT_MODEL
        lyrics = song_data.split("Lyrics:")[1].split("Style:")[0].strip()[:3000]
        style = song_data.split("Style:")[1].split("Negative Style:")[0].strip()[:120].replace("Negative","").strip()
        return description, title, lyrics, style
    except IndexError as e:
        raise ValueError("Song data is not in the expected format.") from e

# Create the JSON payload
def create_payload(description, title, lyrics, style):
    return {
        "0": {
            "json": {
                "description": description,
                "customMode": {
                    "lyric": {
                        "type": "custom",
                        "content": lyrics
                    },
                    "style": style,
                    "title": title
                },
                "extend": None
            },
            "meta": {
                "values": {
                    "extend": ["undefined"]
                }
            }
        }
    }

# Define headers
def get_headers():
    return {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.7',
        'content-type': 'application/json',
        'cookie': LOUDME_COOKIE,
        'origin': 'https://loudme.ai',
        'priority': 'u=1, i',
        'referer': 'https://loudme.ai/ai-music-generator',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Brave";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

# POST request to the API
def post_to_loudme(payload, headers):
    try:
        response = requests.post(
            BASE_URL,
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Response: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None

def main():
    # Load and process song data
    song_data = load_song_data()
    description, title, lyrics, style = extract_song_parts(song_data)
    
    # Create payload
    payload = create_payload(description, title, lyrics, style)
    
    # Get headers
    headers = get_headers()
    
    # Post to Loudme
    response = post_to_loudme(payload, headers)
    
    # Check the response
    if response:
        print("Success:", json.dumps(response, indent=2))
    else:
        print("Failed to generate music.")

if __name__ == "__main__":
    main()

import requests
import json
import re

# Read song.txt to extract relevant parts
with open('song.txt', 'r') as file:
    song_data = file.read()

# Use regex to extract different parts of the song.txt content
description_match = re.search(r'Description:\s*(.*?)(?=\nName:)', song_data, re.DOTALL)
title_match = re.search(r'Name:\s*(.*?)(?=\nLyrics:)', song_data, re.DOTALL)
lyrics_match = re.search(r'Lyrics:\s*(.*?)(?=\nStyle:)', song_data, re.DOTALL)
style_match = re.search(r'Style:\s*(.*?)(?=\nCost:)', song_data, re.DOTALL)

# Extracted data
description = description_match.group(1).strip() if description_match else "No description found"
title = title_match.group(1).strip() if title_match else "No title found"
lyrics = lyrics_match.group(1).strip() if lyrics_match else "No lyrics found"
style = style_match.group(1).strip() if style_match else "No style found"

# Prepare the payload using the extracted data
payload = {
    "prompt": lyrics,  # Using the extracted lyrics for the prompt
    "generation_type": "TEXT",
    "tags": style,  # Using the extracted style as tags
    "negative_tags": "",
    "mv": "chirp-v3-5",
    "title": title,  # Using the extracted title
    "continue_clip_id": None,
    "continue_at": None,
    "continued_aligned_prompt": None,
    "infill_start_s": None,
    "infill_end_s": None,
    "task": None,
    "cover_clip_id": None
}

url = "http://127.0.0.1:8000/generate"
# Perform the POST request 20 times
for i in range(1):

    response = requests.post(url, data=json.dumps(payload))
    
    if response.status_code == 200:
        print(f"Request {i+1}: Success!")
    else:
        print(f"Request {i+1}: Failed with status code {response.status_code} and message: {response.text}")


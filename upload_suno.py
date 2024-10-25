import requests
import json
import re
import os
from dotenv import load_dotenv
load_dotenv()

# Read song.txt to extract relevant parts
with open('song.txt', 'r') as file:
    song_data = file.read()

NANOGPT_MODEL = os.getenv("NANOGPT_MODEL")
# Use regex to extract different parts of the song.txt content
description_match = re.search(r'Description:\s*(.*?)\n\n', song_data, re.DOTALL)
title_match = re.search(r'Title:\s*(.*)', song_data, re.DOTALL)
lyrics_match = re.search(r'Lyrics:\s*(.*?)Style', song_data, re.DOTALL)
style_match = re.search(r'Style:\s*(.*?)\n\n', song_data, re.DOTALL)
negative_style_match = re.search(r'Negative Style:\s*(.*?)\n\n', song_data, re.DOTALL)

# Extracted data
description = description_match.group(1).strip() if description_match else "No description found"
title = title_match.group(1).strip()[:80] if title_match else "No title found"
if not lyrics_match:
    assert False, "No lyrics found"
lyrics = lyrics_match.group(1).strip()[:3000]
style = style_match.group(1).strip()[:120] if style_match else "No style found"
negative_style = negative_style_match.group(1).strip()[:120] if negative_style_match else ""

if NANOGPT_MODEL:
    title += "["+NANOGPT_MODEL+"]"

# Prepare the payload using the extracted data
payload = {
    "prompt": lyrics,  # Using the extracted lyrics for the prompt
    "generation_type": "TEXT",
    "tags": style,  # Using the extracted style as tags
    "negative_tags": negative_style,
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


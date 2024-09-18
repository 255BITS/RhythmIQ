import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Configuration
BASE_URL = "https://nano-gpt.com/api"
API_KEY = os.getenv("NANOGPT_API_KEY")
DEFAULT_MODEL = os.getenv("NANOGPT_MODEL", "o1-mini")

# Validate API_KEY
if not API_KEY:
    raise ValueError("NANOGPT_API_KEY is not set. Please set it in the environment variables.")

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def talk_to_gpt(prompt, model=DEFAULT_MODEL, messages=None):
    if messages is None:
        messages = []
    
    data = {
        "prompt": prompt,
        "model": model,
        "messages": messages
    }
    
    try:
        response = requests.post(f"{BASE_URL}/talk-to-gpt", headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None
    
    return response.text

prompt = open("prompt.txt", "r").read()

messages = []
response = talk_to_gpt(prompt, messages=messages)

if response:
    # Split the response to separate the text and NanoGPT info
    parts = response.split('<NanoGPT>')

    # Extract the text response (everything before <NanoGPT>)
    text_response = parts[0].strip()

    # Extract the NanoGPT info
    nano_info = json.loads(parts[1].split('</NanoGPT>')[0])

    print("NanoGPT Response:", text_response)
    print("Cost:", nano_info['nanoCost'])
else:
    print("Failed to get response from GPT")



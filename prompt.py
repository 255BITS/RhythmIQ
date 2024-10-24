import os
import requests
import json
from dotenv import load_dotenv
import random

# Load environment variables from a .env file if present
load_dotenv()

# Configuration
GPT_PROVIDER = os.getenv("GPT_PROVIDER", "nanogpt").lower()  # Default to 'nanogpt' if not set

N_SHOT = int(os.getenv("N_SHOT", "2"))  # Number of example songs to include

# Common settings for both providers (if any)
# Example: You can add common parameters here if needed

# Configuration for NanoGPT API
NANOGPT_BASE_URL = "https://nano-gpt.com/api"
NANOGPT_API_KEY = os.getenv("NANOGPT_API_KEY")
NANOGPT_DEFAULT_MODEL = os.getenv("NANOGPT_MODEL", "o1-mini")

# Configuration for Local Server
LOCAL_SERVER_ADDRESS = os.getenv("LOCAL_SERVER_ADDRESS", "127.0.0.1")
LOCAL_SERVER_PORT = os.getenv("LOCAL_SERVER_PORT", "5000")  # Ensure it's a string

print(f"Using GPT Provider: {GPT_PROVIDER.capitalize()}")

def validate_environment():
    """
    Validates that necessary environment variables are set based on the selected GPT provider.
    """
    if GPT_PROVIDER == "nanogpt":
        if not NANOGPT_API_KEY:
            raise ValueError("NANOGPT_API_KEY is not set. Please set it in the environment variables.")
    elif GPT_PROVIDER == "local":
        # Optionally, you can add validation for local server settings
        pass
    else:
        raise ValueError(f"Unsupported GPT_PROVIDER '{GPT_PROVIDER}'. Supported providers are 'nanogpt' and 'local'.")

def talk_to_gpt(prompt, model=NANOGPT_DEFAULT_MODEL, messages=None):
    """
    Sends a prompt to the NanoGPT API and returns the response.

    Args:
        prompt (str): The input prompt to send to the model.
        model (str): The model to use for generation.
        messages (list): Optional list of messages for context.

    Returns:
        dict: Parsed JSON response from NanoGPT API containing the generated text and additional info.
    """
    headers = {
        "x-api-key": NANOGPT_API_KEY,
        "Content-Type": "application/json"
    }

    if messages is None:
        messages = []

    data = {
        "prompt": prompt,
        "model": model,
        "messages": messages
    }

    endpoint = f"{NANOGPT_BASE_URL}/talk-to-gpt"

    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request to NanoGPT failed: {e}")
        return None

    # Assuming the response text contains JSON separated by <NanoGPT> tags
    try:
        parts = response.text.split('<NanoGPT>')
        if len(parts) < 2:
            print("Unexpected response format from NanoGPT API.")
            return None

        # Extract the text response (everything before <NanoGPT>)
        text_response = parts[0].strip()

        # Extract the NanoGPT info
        nano_info_str = parts[1].split('</NanoGPT>')[0]
        nano_info = json.loads(nano_info_str)

        return {
            "text_response": text_response,
            "nano_info": nano_info
        }
    except (IndexError, json.JSONDecodeError) as e:
        print(f"Error parsing NanoGPT response: {e}")
        return None

def send_payload(prompt, server=LOCAL_SERVER_ADDRESS, port=LOCAL_SERVER_PORT):
    """
    Sends a formatted prompt to a local server for text generation.

    Args:
        prompt (str): The input prompt to send to the local server.
        server (str): The server address. Defaults to LOCAL_SERVER_ADDRESS.
        port (str): The server port. Defaults to LOCAL_SERVER_PORT.

    Returns:
        str: The generated text from the local server.
    """
    # Define the generation parameters
    params = {
             "messages": [{"role": "user", "content": prompt}],
             "max_tokens": 4096
    }

    # Prepare the payload
    payload = params

    try:
        response = requests.post(
            f"http://{server}:{port}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request to local server failed: {e}")
        return None

    return response.json()["choices"][0]["message"]["content"]

def main():
    """
    Main function to handle user interaction with GPT models based on the selected provider.
    """
    # Validate environment variables
    try:
        validate_environment()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return

    # Get random song and instruction files
    try:
        # Get list of files in songs directory
        song_files = [f for f in os.listdir("songs") if f.endswith('.txt')]
        if not song_files:
            raise FileNotFoundError("No song files found in songs directory")
        
        # Get list of files in instructions directory
        instruction_files = [f for f in os.listdir("instructions") if f.endswith('.txt')]
        
        # Read the base prompt
        with open("base.txt", "r") as file:
            base_prompt = file.read().strip()
        with open("system.txt", "r") as file:
            system_prompt = file.read().strip()
        messages = [{"role": "system", "content": system_prompt}]
            
        if not instruction_files:
            raise FileNotFoundError("No instruction files found in instructions directory")
            
        # Select random instruction file
        random_instruction = random.choice(instruction_files)
        with open(f"instructions/{random_instruction}", "r") as instruction_f:
            instruction_content = instruction_f.read().strip()
        
        # Select and read multiple random examples
        examples = []
        # Use min to handle case where we have fewer files than N_SHOT
        num_examples = min(N_SHOT, len(song_files))
        
        # Randomly sample without replacement
        selected_songs = random.sample(song_files, num_examples)
        
        for song_file in selected_songs:
            with open(f"songs/{song_file}", "r") as song_f:
                song_content = song_f.read().strip()
            examples.append(f"\nExample {len(examples) + 1}:\nSong:\n{song_content}")
            
        user_prompt = f"{base_prompt}\n{''.join(examples)}\n\nInstructions:\n{instruction_content}"

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except IOError as e:
        print(f"Error reading files: {e}")
        return

    if GPT_PROVIDER == "nanogpt":
        print("\n--- Using NanoGPT API ---")
        nano_response = talk_to_gpt(user_prompt, messages=messages)
        if nano_response:
            print("NanoGPT "+NANOGPT_DEFAULT_MODEL)
            print(nano_response['text_response'])
        else:
            print("Failed to get response from NanoGPT API.")
    elif GPT_PROVIDER == "local":
        print("\n--- Using Local Server API ---")
        # Format the prompt with special tokens
        local_response = send_payload(user_prompt)
        if local_response:
            print("Local Server Response:", local_response)
        else:
            print("Failed to get response from the local server.")
    else:
        print(f"Unsupported GPT_PROVIDER '{GPT_PROVIDER}'. Please set it to 'nanogpt' or 'local'.")

if __name__ == "__main__":
    main()

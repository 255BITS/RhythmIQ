
# RhythmIQ

**RhythmIQ** generates lyrics and creates audio using advanced language models and text-to-audio services.

**Turn on the song stream!**

## 🚀 Getting Started

### 📋 Prerequisites

- **Python 3.8+**
- **Git**
- **nano-gpt Account:** Sign up at [nano-gpt.com](https://nano-gpt.com) for access to the pay-per-prompt service.

Choose one of the following for audio synthesis:

- **Suno-API Setup:** Follow the instructions at [SunoAI-API/Suno-API](https://github.com/SunoAI-API/Suno-API) to set up the Suno API.
- **LOUDME_COOKIE:** Obtain the `LOUDME_COOKIE` environment variable by extracting it from the inspect window in your browser's network tab.

### 🔧 Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/255labs/rhythmiq.git
   cd rhythmiq
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**

   Create a `.env` file in the root directory or set the environment variables in your shell.

   - **Required:**
     - **NANOGPT_API_KEY:** Your API key from nano-gpt.com
     
   - **Optional:**
     - **NANOGPT_MODEL:** Choose the desired nano-gpt model. Defaults to `o1-mini`.
     - **LOUDME_COOKIE:** Your Loudme cookie value.
   
   **Example `.env` file:**
   ```
   NANOGPT_API_KEY=your_api_key_here
   LOUDME_COOKIE=your_cookie_value_here
   NANOGPT_MODEL=o1-mini
   ```

   **Alternatively, set them in your shell:**
   ```bash
   export NANOGPT_API_KEY='your_api_key_here'
   export LOUDME_COOKIE='your_cookie_value_here'
   export NANOGPT_MODEL='your_preferred_model' # Optional
   ```

## 🛠️ Usage

1. **Customize Prompts:**
   - Open `prompt.txt` in your preferred text editor.
   - Modify the existing prompts to tailor the lyric generation to your desired style and themes. The default is `hermes-405b` going a bit nuts.

2. **Run the Application:**
   ```bash
   python3 prompt.py > song.txt
   python3 upload_suno.py
   python3 upload_loudme.py
   ```

3. **Generate Multiple Songs:**
   - Use the following loop to create multiple songs consecutively:
     ```bash
     for i in {1..16}; do
       python3 prompt.py > song.txt && python3 upload_suno.py
       sleep 1.5m
     done
     ```

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

## 📄 License

This project is licensed under the **MIT License**.


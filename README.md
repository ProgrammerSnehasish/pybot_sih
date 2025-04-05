# WhatsApp Chat Analyzer Bot

A Python-based bot that captures WhatsApp chats via screenshots, extracts text using Tesseract OCR, and detects unsafe words using a predefined word list.

## Features

Detects unsafe words in WhatsApp chats (app & web version)

Takes automatic screenshots when WhatsApp is active

Uses Tesseract OCR to extract text from images

Saves unsafe chats with highlighted words

Supports Windows, Linux, and macOS

## 🛠 Installation

1️⃣ Clone the Repository

git clone https://github.com/ProgrammerSnehasish/pybot_sih.git
cd pybot_sih

2️⃣ Create a Virtual Environment

### On Windows
python -m venv bot_env
bot_env\Scripts\activate

### On Linux/macOS
python3 -m venv bot_env
source bot_env/bin/activate

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Install Tesseract OCR

Windows:

Copy the tesseract folder inside the repository.

The script automatically sets the Tesseract path.

Linux/macOS:

sudo apt install tesseract-ocr  # Debian-based
brew install tesseract  # macOS (Homebrew)

## Usage

Run the Bot

python pybot.whatsapp.py

Modify the Unsafe Words List

Edit the unsafe_words.txt file and add words to be detected, including terms related to drug trafficking.

## 🏗 Project Structure

📂 whatsapp-chat-analyzer
├── 📁 tesseract            # Tesseract OCR (Windows)
├── 📁 saved_screenshots    # Stores captured screenshots
├── 📁 unsafe_chats_img     # Stores unsafe chats
├── 📝 unsafe_words.txt     # List of words to detect (e.g., violence, threats, drug trafficking)
├── 📜 pybot.whatsapp.py    # Main script
├── 📝 requirements.txt     # Dependencies
├── 📝 README.md            # Project documentation

 ## 🛠 Troubleshooting

Tesseract Not Found?

Ensure tesseract.exe is in the tesseract folder.

For Windows, manually set the path:

pytesseract.pytesseract.tesseract_cmd = r"C:\path\to\tesseract.exe"

Module Not Found?

pip install -r requirements.txt

 ## License

This project is licensed under the MIT License.

## Contributing

Pull requests are welcome! Open an issue for any feature requests or bug reports.


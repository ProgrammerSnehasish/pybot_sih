# Pybot for WhatsApp to extract chat form it and analyze.

# To activate virtual environment of the bot use the command in the shell: source bot_env/bin/activate
# To deactivate virtual environment of the bot use the command in the shell: deactivate

#imported modules.

import pyautogui  # type: ignore
import pytesseract  # type: ignore
import cv2  # type: ignore
import os
import platform
import psutil  # type: ignore
import subprocess
import time
from datetime import datetime

def configure_tesseract():
    os_type = platform.system()
    
    if os_type == "Windows":
        # Use relative path based on script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        tesseract_path = os.path.join(script_dir, "tesseract", "tesseract.exe")
        
        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        else:
            print("Error: Tesseract is not installed or not found at", tesseract_path)
    
    elif os_type in ["Linux", "Darwin"]:
        # Check if Tesseract is installed and accessible
        if subprocess.run(["which", "tesseract"], stdout=subprocess.PIPE).returncode == 0:
            pytesseract.pytesseract.tesseract_cmd = "tesseract"
        else:
            print("Error: Tesseract is not installed. Install it or specify the correct path.")
            pytesseract.pytesseract.tesseract_cmd = "./lib/tesseract"  # Fallback

configure_tesseract()

def load_unsafe_words(txt_file):
    if not os.path.exists(txt_file):
        print("Error: Unsafe words file not found!")
        return set()
    with open(txt_file, 'r') as file:
        return set(line.strip().lower() for line in file if line.strip())

def is_whatsapp_active():
    os_type = platform.system()
    
    if os_type == "Windows":
        import win32gui  # type: ignore
        window = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(window)
        return "WhatsApp" in title or "WhatsApp Web" in title
    
    elif os_type == "Linux":
        try:
            result = subprocess.run(["xdotool", "getactivewindow", "getwindowname"], stdout=subprocess.PIPE, text=True)
            return "WhatsApp" in result.stdout or "WhatsApp Web" in result.stdout
        except FileNotFoundError:
            print("Warning: xdotool is not installed. Install it to enable window detection on Linux.")
    
    return False

def take_screenshot_whatsapp():
    screenshot = pyautogui.screenshot()
    save_dir = "saved_screenshots"
    os.makedirs(save_dir, exist_ok=True)
    screenshot_path = os.path.join(save_dir, f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    screenshot.save(screenshot_path)
    return screenshot_path

def extract_text_from_image(image_path):
    if not os.path.exists(image_path):
        return ""
    img = cv2.imread(image_path)
    return pytesseract.image_to_string(img).lower()

def check_chat_safety(extracted_text, unsafe_words):
    lines = extracted_text.splitlines()
    unsafe_matches = {}
    for i, line in enumerate(lines):
        matches = set(line.split()).intersection(unsafe_words)
        if matches:
            unsafe_matches[i + 1] = (line, matches)
    return ("Unsafe Chat", unsafe_matches) if unsafe_matches else ("Safe Chat", {})

def save_unsafe_chat(extracted_text, matched_lines, screenshot_path, detection_count):
    save_dir = "unsafe_chats"
    os.makedirs(save_dir, exist_ok=True)
    
    chat_path = os.path.join(save_dir, f"unsafe_chat_{detection_count}.txt")
    with open(chat_path, "w") as file:
        file.write("Extracted Chat with Unsafe Content:\n")
        for line_num, (line, words) in matched_lines.items():
            file.write(f"Line {line_num}: '{line}' contains unsafe words: {', '.join(words)}\n")
    print(f"Unsafe chat text saved to: {chat_path}")
    
    screenshot_save_path = os.path.join(save_dir, f"unsafe_chat_screenshot_{detection_count}.png")
    os.rename(screenshot_path, screenshot_save_path)
    print(f"Screenshot saved to: {screenshot_save_path}")

def main(txt_file):
    unsafe_words = load_unsafe_words(txt_file)
    detection_count = len(os.listdir("unsafe_chats_img")) // 2 + 1 if os.path.exists("unsafe_chats_img") else 1
    print("Monitoring WhatsApp for unsafe chat content. Press Ctrl+C to stop.")
    
    try:
        while True:
            if is_whatsapp_active():
                screenshot_path = take_screenshot_whatsapp()
                if screenshot_path:
                    extracted_text = extract_text_from_image(screenshot_path)
                    status, matched_lines = check_chat_safety(extracted_text, unsafe_words)
                    print(f"Chat Status: {status}")
                    
                    if matched_lines:
                        for line_num, (line, words) in matched_lines.items():
                            print(f"Line {line_num}: '{line}' contains unsafe words: {', '.join(words)}")
                        save_unsafe_chat(extracted_text, matched_lines, screenshot_path, detection_count)
                        detection_count += 1
                    else:
                        print("No unsafe words detected.")
            else:
                print("WhatsApp is not active.")
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

main("unsafe_words.txt")

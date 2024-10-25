# Pybot for WhatsApp to extract chat form it and analyze.
import pyautogui
import pytesseract
import cv2
import os
from datetime import datetime
import time
import platform
import psutil
import subprocess

# Configure Tesseract executable path (for Linux, e.g., Kali)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Update path as necessary

# Load unsafe words from a text file
def load_unsafe_words(txt_file):
    with open(txt_file, 'r') as file:
        unsafe_words = set(line.strip().lower() for line in file if line.strip())
    return unsafe_words

# Check if WhatsApp or WhatsApp Web is running in a browser (cross-platform)
def is_whatsapp_active():
    os_type = platform.system()
    
    if os_type == "Windows":
        import win32gui
        window = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(window)
        return "WhatsApp" in title or "WhatsApp Web" in title
    
    elif os_type == "Darwin":  # macOS
        from AppKit import NSWorkspace
        active_app_name = NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()
        return "WhatsApp" in active_app_name or "WhatsApp Web" in active_app_name

    elif os_type == "Linux":
        # Use xdotool to check the active window title
        try:
            result = subprocess.run(["xdotool", "getactivewindow", "getwindowname"], stdout=subprocess.PIPE, text=True)
            title = result.stdout.strip()
            return "WhatsApp" in title or "WhatsApp Web" in title
        except FileNotFoundError:
            print("xdotool is not installed. Please install it to enable window detection on Linux.")
            return False

    return False

# Capture a screenshot of WhatsApp (either app or WhatsApp Web)
def take_screenshot_whatsapp():
    os_type = platform.system()
    
    if os_type == "Windows":
        import win32gui
        window = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(window)
        if "WhatsApp" in title or "WhatsApp Web" in title:
            rect = win32gui.GetWindowRect(window)
            screenshot = pyautogui.screenshot(region=(rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]))
        else:
            return None
    
    elif os_type == "Darwin" or os_type == "Linux":
        # Screenshot the whole screen and crop later (no direct access to window geometry in macOS/Linux)
        screenshot = pyautogui.screenshot()
    
    save_dir = "saved_screenshots"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    screenshot_path = os.path.join(save_dir, f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    screenshot.save(screenshot_path)
    return screenshot_path

# Extract text from image using OCR
def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img)
    return text.lower()

# Compare extracted words with unsafe words and find matching lines
def check_chat_safety(extracted_text, unsafe_words):
    lines = extracted_text.splitlines()
    unsafe_matches = {}
    for i, line in enumerate(lines):
        words_in_line = set(line.split())
        matches = words_in_line.intersection(unsafe_words)
        if matches:
            unsafe_matches[i + 1] = (line, matches)  # Line number starts from 1
    if unsafe_matches:
        return "Unsafe Chat", unsafe_matches
    else:
        return "Safe Chat", {}

# Save unsafe chat text in the unsafe_chats directory
def save_unsafe_chat(extracted_text, detection_count):
    save_dir = "unsafe_chats_img"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    chat_path = os.path.join(save_dir, f"unsafe_chat_{detection_count}.txt")
    with open(chat_path, "w") as file:
        file.write(extracted_text)
    print(f"Chat saved to: {chat_path}")

# Main function to run the entire flow continuously
def main(txt_file):
    unsafe_words = load_unsafe_words(txt_file)
    detection_count = len(os.listdir("unsafe_chats_img")) + 1
    
    print("Monitoring WhatsApp for unsafe chat content. Press Ctrl+C to stop.")
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
                    
                    save_unsafe_chat(extracted_text, detection_count)
                    detection_count += 1
                else:
                    print("No unsafe words detected.")
        else:
            print("WhatsApp is not active.")
        
        time.sleep(10)  # Check every 10 seconds

# Run with your .txt file path
main("unsafe_words.txt")

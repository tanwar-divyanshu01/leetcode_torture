# import os
# import time
# import requests
# import logging
# import pyautogui
# import keyboard
# import threading
# import re
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# pyautogui.FAILSAFE = False

# def resource_path(relative_path):
#     """Resolve path inside PyInstaller onefile or normal run."""
#     if hasattr(sys, '_MEIPASS'):
#         return os.path.join(sys._MEIPASS, relative_path)
#     return os.path.join(os.path.abspath("."), relative_path)

# # Paths
# driver_path = resource_path("chromedriver.exe")
# chrome_binary_path = resource_path("chrome-win64/chrome.exe") 

# chrome_options = Options()
# chrome_options.binary_location = chrome_binary_path
# chrome_options.add_argument("--start-maximized")  # optional
# # chrome_options.add_argument("--headless=new")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--window-size=1920,1200")

# service = Service(driver_path)
# driver = webdriver.Chrome(service=service, options=chrome_options)

#------------------------
import os
import time
import requests
import logging
import pyautogui
import threading
import json
import sys
import re
import subprocess
import win32gui
import win32con
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
pyautogui.FAILSAFE = False

def resource_path(relative_path):
    """Return path to resource, works for dev and PyInstaller onefile."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

driver_path = resource_path("chromedriver.exe")
chrome_binary_path = resource_path("chrome-win64/chrome.exe") 

chrome_options = Options()
chrome_options.binary_location = chrome_binary_path
chrome_options.add_argument("--start-maximized")  # optional
# chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1200")
profile_dir = os.path.join(os.getenv("APPDATA"), "leet_torture_profile")
os.makedirs(profile_dir, exist_ok=True)
chrome_options.add_argument(f"--user-data-dir={profile_dir}")

driver = None
# service = Service("chromedriver.exe")
# driver = webdriver.Chrome(service=service, options=chrome_options)

problems_path = resource_path("problems.json")
autohotkey_path = resource_path("AutoHotkey64.exe")
blockahk_path = resource_path("block_keys_leetcode.ahk")

#------------------------


with open(problems_path, 'r') as file:
    data = json.load(file)

def is_fullscreen():
    hwnd = win32gui.GetForegroundWindow()
    rect = win32gui.GetWindowRect(hwnd)
    screen = win32gui.GetDesktopWindow()
    screen_rect = win32gui.GetWindowRect(screen)
    return rect == screen_rect

def runfull(selected):
    thisurl = data[selected][0]

    driver = create_driver()
    driver.get(thisurl)
    driver.fullscreen_window()

    def block_f11():
        subprocess.Popen([autohotkey_path, blockahk_path])

    threading.Thread(target=block_f11, daemon=True).start()

    while True:
        if driver.find_elements(By.XPATH, "//div[contains(text(), 'Runtime')]"):
            os.system("taskkill /IM AutoHotkey64.exe /F")
            data[selected].pop(0)
            with open(problems_path, 'w') as f:
                json.dump(data, f, indent=2)
            sys.exit()
            break
        x, y = pyautogui.position()
        if y < 135:
            pyautogui.moveTo(x, 136)
        if(not is_fullscreen()):
            if driver: driver.fullscreen_window()


import tkinter as tk
from tkinter import messagebox
import webbrowser

def create_driver():
    options = uc.ChromeOptions()
    options.binary_location = chrome_binary_path
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1200")
    options.add_argument(f"--user-data-dir={profile_dir}")
    driver = uc.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver


def login():
    driver = create_driver()
    driver.get("https://leetcode.com/accounts/login/")
    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="navbar_user_avatar"]/img'))
        )
    finally:
        driver.quit()

def start_clicked():
    selected = choice.get()
    if selected:
        messagebox.showinfo("Please NOTE", "Use Ctrl + Enter to submit. (Ctrl + ') to run")
        runfull(selected)
        root.destroy()
    else:
        messagebox.showwarning("No selection", "Please choose an option before starting.")

# Create main window
root = tk.Tk()
root.title("Leetcode Torture")
root.geometry("300x260")

# Title label
label = tk.Label(root, text="Login first. Choose an option:")
label.pack(pady=10)

# Option selector (Radio buttons)
choice = tk.StringVar(value="")  # Holds selected value
options = ["Easy", "Med.", "Hard"]
for opt in options:
    tk.Radiobutton(root, text=opt, variable=choice, value=opt).pack(anchor='w')

# Buttons in one frame
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

start_button = tk.Button(button_frame, text="Start", command=start_clicked)
start_button.pack(side='left', padx=10)

loginbt = tk.Button(button_frame, text="Login", command=login)
loginbt.pack(side='left', padx=10)

# Link below buttons
def open_link(event):
    webbrowser.open("https://x.com/DivyanshuT61518")

link = tk.Label(root, text="Connect with me on X", fg="blue", cursor="hand2")
link.pack(pady=10)
link.bind("<Button-1>", open_link)

# Run the app
root.mainloop()

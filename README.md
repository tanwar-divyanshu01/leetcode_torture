# leetcode_torture
Leetcode Torture is a small app that keeps you on the LeetCode problem page until you submit a solution.

## Setup:

Download all files into one folder.

Make sure you have all the dependencies from requirements.txt

Download and unzip Chrome-win64 from:
https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.92/win64/chrome-win64.zip
(Keep the chrome-win64 folder in the same directory.)

## To run:

You can run main.py directly (after installing dependencies), 

OR

Create a one-file .exe using this PyInstaller command:

pyinstaller --noconfirm --onefile --windowed `
--add-data "chromedriver.exe:." `
--add-data "chrome-win64:chrome-win64" `
--add-data "AutoHotkey64.exe:." `
--add-data "block_keys_leetcode.ahk:." `
--add-data "problems.json:." `
main.py

### I have also provided an executale if someone wants to run the app directly (contains chrome-64 hence the file size):
https://drive.google.com/file/d/1QtCgdFWFcRR4OgkxNO5ydcw_-PWfHbK_/view?usp=drive_link

The app uses:

Python + Selenium

AutoHotkey (to block all shortcuts except cut, copy, paste, undo, redo)

A minimal tkinter UI

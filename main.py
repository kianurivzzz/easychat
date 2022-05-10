from flask import Flask, request, render_template
from datetime import datetime
import json

application = Flask(__name__)
DB_FILE = './data/db.json'

MIN_NAME_LEN = 3
MAX_NAME_LEN = 100

MIN_MESS_LEN = 1
MAX_MESS_LEN = 3000


def load_messages():
    json_file = open(DB_FILE, 'r')
    data = json.load(json_file)
    return data['messages']


all_messages = load_messages()


def save_messages():
    data = {
        'messages': all_messages
    }
    json_file = open(DB_FILE, 'w')
    json.dump(data, json_file)


@application.route('/')
def display_chat():
    return render_template('form.html')


@application.route('/get_messages')
def get_messages():
    return {'messages': all_messages}


@application.route('/send_message')
def send_message():
    sender = request.args['name']
    text = request.args['text']
    if len(sender) > MAX_NAME_LEN or len(sender) < MIN_NAME_LEN:
        sender = 'ERROR, MIN/MAX LENGTH'
        text = f'Имя должно быть длиннее, чем {MIN_NAME_LEN} и короче, чем {MAX_NAME_LEN}!'
    if len(text) > MAX_MESS_LEN or len(text) < MIN_MESS_LEN:
        sender = 'ERROR, MIN/MAX LENGTH'
        text = f'Сообщение должно быть длиннее, чем {MIN_MESS_LEN} и короче, чем {MAX_MESS_LEN}!'
    add_message(sender, text)
    save_messages()


def add_message(sender, text):
    new_message = {
        'sender': sender,
        'text': text,
        'time': datetime.now().strftime('%H:%M:%S, %d/%m/%Y'),
    }
    all_messages.append(new_message)


application.run(host='0.0.0.0', port=80)

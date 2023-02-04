from flask import Flask, request, render_template
from db import all_messages, add_message, save_messages

application = Flask(__name__, template_folder='chat_templates')


@application.route('/')
def display_chat():
    return render_template('index.html')


@application.route('/get_messages')
def get_messages():
    return {'messages': all_messages}


@application.route('/send_message')
def send_message():
    min_name_len = 3
    max_name_len = 100

    min_mess_len = 1
    max_mess_len = 3000

    sender = request.args['name']
    text = request.args['text']
    if len(sender) > max_name_len or len(sender) < min_name_len:
        sender = 'ERROR, MIN/MAX LENGTH'
        text = f'Имя должно быть длиннее, чем {min_name_len} и короче, чем {max_name_len}!'
    elif len(text) > max_mess_len or len(text) < min_mess_len:
        sender = 'ERROR, MIN/MAX LENGTH'
        text = f'Сообщение должно быть длиннее, чем {min_mess_len} и короче, чем {max_mess_len}!'
    add_message(sender, text)
    save_messages()


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=80)

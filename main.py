import logging
import os
from datetime import datetime
from functools import wraps

from flask import Flask, jsonify, render_template, request, abort
from werkzeug.exceptions import HTTPException

from db import add_message, all_messages, save_messages

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger('easychat')

# Инициализация приложения
application = Flask(__name__, template_folder='chat_templates')

# Константы
MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 100
MIN_MESSAGE_LENGTH = 1
MAX_MESSAGE_LENGTH = 3000

# Создание директории для логов, если она не существует
os.makedirs('logs', exist_ok=True)


def validate_request(f):
    """Декоратор для проверки наличия необходимых параметров в запросе."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if f.__name__ == 'send_message':
            if 'name' not in request.args or 'text' not in request.args:
                logger.warning(f"Отсутствуют обязательные параметры в запросе: {request.args}")
                return jsonify({
                    'success': False,
                    'error': 'Отсутствуют обязательные параметры'
                }), 400
        return f(*args, **kwargs)
    return decorated_function


@application.route('/')
def display_chat():
    """Отображение главной страницы чата."""
    logger.info("Запрос главной страницы")
    return render_template('index.html')


@application.route('/get_messages')
def get_messages():
    """Получение всех сообщений."""
    logger.info("Запрос на получение всех сообщений")
    return jsonify({'messages': all_messages})


@application.route('/get_message_count')
def get_message_count():
    """Получение количества сообщений."""
    logger.info("Запрос на получение количества сообщений")
    return jsonify({'count': len(all_messages)})


@application.route('/send_message')
@validate_request
def send_message():
    """
    Отправка нового сообщения.
    
    Параметры:
        name (str): Имя отправителя
        text (str): Текст сообщения
    
    Возвращает:
        JSON с результатом операции
    """
    sender = request.args.get('name', '').strip()
    text = request.args.get('text', '').strip()
    
    # Валидация имени
    if len(sender) > MAX_NAME_LENGTH or len(sender) < MIN_NAME_LENGTH:
        error_msg = f'Имя должно быть длиннее, чем {MIN_NAME_LENGTH} и короче, чем {MAX_NAME_LENGTH}!'
        logger.warning(f"Ошибка валидации имени: {sender}")
        return jsonify({
            'success': False,
            'error': error_msg
        }), 400
    
    # Валидация сообщения
    if len(text) > MAX_MESSAGE_LENGTH or len(text) < MIN_MESSAGE_LENGTH:
        error_msg = f'Сообщение должно быть длиннее, чем {MIN_MESSAGE_LENGTH} и короче, чем {MAX_MESSAGE_LENGTH}!'
        logger.warning(f"Ошибка валидации сообщения от {sender}")
        return jsonify({
            'success': False,
            'error': error_msg
        }), 400
    
    # Добавление сообщения
    try:
        add_message(sender, text)
        save_messages()
        logger.info(f"Новое сообщение от {sender}")
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Ошибка при сохранении сообщения: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ошибка при сохранении сообщения'
        }), 500


@application.errorhandler(Exception)
def handle_error(e):
    """Глобальный обработчик ошибок."""
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    
    logger.error(f"Ошибка: {str(e)}")
    return jsonify({
        'success': False,
        'error': str(e)
    }), code


if __name__ == '__main__':
    logger.info("Запуск сервера EasyChat")
    application.run(host='0.0.0.0', port=80, debug=True)

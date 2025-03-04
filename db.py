import json
import logging
import os
from datetime import datetime

# Настройка логирования
logger = logging.getLogger('easychat.db')

# Константы
DB_FILE = './data/db.json'
MAX_MESSAGES = 1000  # Максимальное количество сообщений для хранения


def ensure_data_dir():
    """Убедиться, что директория для данных существует."""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)


def load_messages():
    """
    Загрузка сообщений из файла базы данных.

    Возвращает:
        list: Список сообщений
    """
    ensure_data_dir()

    try:
        # Проверка существования файла
        if not os.path.exists(DB_FILE):
            logger.info(f"Файл базы данных не найден. Создаём новый: {DB_FILE}")
            return []

        with open(DB_FILE, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            logger.info(f"Загружено {len(data.get('messages', []))} сообщений из базы данных")
            return data.get('messages', [])
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле {DB_FILE}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при загрузке сообщений: {str(e)}")
        return []


# Глобальная переменная для хранения сообщений
all_messages = load_messages()


def save_messages():
    """
    Сохранение сообщений в файл базы данных.

    Возвращает:
        bool: True если сохранение успешно, иначе False
    """
    ensure_data_dir()

    try:
        # Ограничение количества сообщений
        global all_messages
        if len(all_messages) > MAX_MESSAGES:
            all_messages = all_messages[-MAX_MESSAGES:]
            logger.info(f"Количество сообщений превысило лимит. Обрезано до {MAX_MESSAGES}")

        data = {'messages': all_messages}

        with open(DB_FILE, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)

        logger.info(f"Сохранено {len(all_messages)} сообщений в базу данных")
        return True
    except Exception as e:
        logger.error(f"Ошибка при сохранении сообщений: {str(e)}")
        return False


def add_message(sender, text):
    """
    Добавление нового сообщения в список.

    Аргументы:
        sender (str): Имя отправителя
        text (str): Текст сообщения

    Возвращает:
        dict: Добавленное сообщение
    """
    timestamp = datetime.now()

    new_message = {
        'sender': sender,
        'text': text,
        'time': timestamp.strftime('%H:%M:%S, %d/%m/%Y'),
        'timestamp': timestamp.timestamp()  # Добавляем UNIX-timestamp для сортировки
    }

    all_messages.append(new_message)
    logger.info(f"Добавлено новое сообщение от {sender}")

    return new_message


def clear_messages():
    """
    Очистка всех сообщений.

    Возвращает:
        bool: True если очистка успешна, иначе False
    """
    try:
        global all_messages
        all_messages = []
        save_messages()
        logger.info("Все сообщения очищены")
        return True
    except Exception as e:
        logger.error(f"Ошибка при очистке сообщений: {str(e)}")
        return False

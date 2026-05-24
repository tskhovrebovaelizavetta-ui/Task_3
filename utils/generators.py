import random
import string


def generate_random_string(length=10):
    """Генерирует случайную строку для уникальных тестовых данных."""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_user_data():
    """Создаёт словарь с данными тестового пользователя."""
    suffix = generate_random_string()
    return {
        'email': f'test_{suffix}@yandex.ru',
        'password': f'Pass_{suffix}_123',
        'name': f'User_{suffix}'
    }

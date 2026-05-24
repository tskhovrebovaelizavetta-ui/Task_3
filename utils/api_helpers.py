import requests
from utils.constants import API_URL


class UserApi:
    """Хелпер для работы с API пользователя.

    Используем его в фикстурах, чтобы:
    1. создать пользователя перед тестом;
    2. удалить пользователя после теста.
    Это делает тесты независимыми друг от друга.
    """

    @staticmethod
    def create_user(user_data):
        return requests.post(f'{API_URL}/auth/register', json=user_data)

    @staticmethod
    def login_user(email, password):
        return requests.post(
            f'{API_URL}/auth/login',
            json={'email': email, 'password': password}
        )

    @staticmethod
    def delete_user(access_token):
        headers = {'Authorization': access_token}
        return requests.delete(f'{API_URL}/auth/user', headers=headers)

    @staticmethod
    def create_order(access_token, ingredients):
        """Создаёт заказ через API — используем для подготовки данных в тестах ленты."""
        headers = {'Authorization': access_token}
        return requests.post(
            f'{API_URL}/orders',
            json={'ingredients': ingredients},
            headers=headers
        )

    @staticmethod
    def get_ingredients():
        """Получает список доступных ингредиентов через API."""
        response = requests.get(f'{API_URL}/ingredients')
        if response.status_code == 200 and response.json().get('success'):
            return response.json().get('data', [])
        return []

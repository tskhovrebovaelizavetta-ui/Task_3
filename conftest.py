import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from pages.base_page import BasePage
from utils.constants import BASE_URL
from utils.generators import generate_user_data
from utils.api_helpers import UserApi


def pytest_addoption(parser):
    """Добавляет параметр командной строки --browser для выбора браузера."""
    parser.addoption(
        '--browser',
        action='store',
        default='chrome',
        help='Укажи браузер: chrome или firefox'
    )


@pytest.fixture
def driver(request):
    """Фикстура создаёт WebDriver, открывает BASE_URL и закрывает после теста."""
    browser = request.config.getoption('--browser')

    if browser == 'firefox':
        options = FirefoxOptions()
        web_driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
    else:
        options = ChromeOptions()
        web_driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

    web_driver.maximize_window()
    # Открываем главную страницу через BasePage — там уже встроено ожидание оверлея.
    BasePage(web_driver).open(BASE_URL)

    yield web_driver
    web_driver.quit()


@pytest.fixture
def created_user():
    """Создаёт тестового пользователя через API и удаляет после теста.
    Возвращает словарь с ключами: email, password, name.
    """
    user_data = generate_user_data()
    response = UserApi.create_user(user_data)
    access_token = None

    if response.status_code == 200 and response.json().get('success'):
        access_token = response.json().get('accessToken')

    yield user_data

    if access_token:
        UserApi.delete_user(access_token)

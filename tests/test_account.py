import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from locators.login_page_locators import LoginPageLocators
from utils.constants import BASE_URL


@allure.feature('Личный кабинет')
class TestAccount:

    @allure.title('Переход по клику на Личный кабинет')
    def test_open_personal_account(self, driver, created_user):
        """Проверяет, что залогиненный пользователь попадает в профиль
        при клике на «Личный Кабинет»."""
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        # Логинимся
        main_page.click_personal_account()
        login_page.login(created_user['email'], created_user['password'])

        # Ожидаем возврат на главную после логина, затем кликаем «Личный Кабинет»
        main_page.wait_for_url_contains('/')
        main_page.click_personal_account()

        main_page.wait_for_url_contains('account')
        assert 'account' in driver.current_url

    @allure.title('Переход в раздел История заказов')
    def test_open_order_history(self, driver, created_user):
        """Проверяет переход в раздел «История заказов» из личного кабинета."""
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        account_page = AccountPage(driver)

        main_page.click_personal_account()
        login_page.login(created_user['email'], created_user['password'])

        main_page.wait_for_url_contains('/')
        main_page.click_personal_account()
        account_page.wait_for_profile_loaded()
        account_page.click_order_history()

        account_page.wait_for_url_contains('order-history')
        assert 'order-history' in driver.current_url

    @allure.title('Выход из аккаунта')
    def test_logout(self, driver, created_user):
        """Проверяет, что пользователь может выйти из аккаунта
        и попадает на страницу логина."""
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        account_page = AccountPage(driver)

        main_page.click_personal_account()
        login_page.login(created_user['email'], created_user['password'])

        main_page.wait_for_url_contains('/')
        main_page.click_personal_account()
        account_page.wait_for_profile_loaded()
        account_page.click_logout()

        login_page.wait_for_url_contains('login')
        assert login_page.is_login_page_opened()

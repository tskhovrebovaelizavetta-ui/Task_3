import allure

from pages.login_page import LoginPage
from pages.reset_password_page import ResetPasswordPage
from utils.constants import BASE_URL


@allure.feature('Восстановление пароля')
class TestPasswordRecovery:

    @allure.title('Переход на страницу восстановления пароля')
    def test_open_reset_password_page(self, driver):
        """Со страницы логина по ссылке «Восстановить пароль»
        открывается страница восстановления."""
        login_page = LoginPage(driver)
        reset_page = ResetPasswordPage(driver)

        login_page.open(f'{BASE_URL}login')
        login_page.click_forgot_password()

        assert reset_page.is_reset_page_opened()

    @allure.title('Ввод почты и клик по «Восстановить»')
    def test_fill_email_and_click_restore(self, driver):
        """После ввода email и клика «Восстановить» открывается reset-password."""
        reset_page = ResetPasswordPage(driver)

        reset_page.open(f'{BASE_URL}forgot-password')
        reset_page.request_password_reset('test@yandex.ru')

        # Метод request_password_reset уже дождался поля пароля на reset-password.
        # Дополнительно проверяем URL — он точно должен содержать reset-password.
        assert reset_page.url_contains('reset-password')

    @allure.title('Клик по «показать/скрыть пароль» делает поле активным')
    def test_click_show_hide_password_makes_field_active(self, driver):
        """На странице reset-password клик по иконке глаза подсвечивает поле пароля."""
        reset_page = ResetPasswordPage(driver)

        reset_page.open(f'{BASE_URL}forgot-password')
        reset_page.request_password_reset('test@yandex.ru')

        reset_page.click_show_hide_password()

        assert reset_page.is_password_field_active()

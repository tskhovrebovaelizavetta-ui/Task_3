import allure
from pages.login_page import LoginPage
from pages.reset_password_page import ResetPasswordPage
from locators.reset_password_page_locators import ResetPasswordPageLocators
from utils.constants import BASE_URL


@allure.feature('Восстановление пароля')
class TestPasswordRecovery:

    @allure.title('Переход на страницу восстановления пароля по кнопке Восстановить пароль')
    def test_open_reset_password_page(self, driver):
        """Проверяет, что со страницы логина по ссылке «Восстановить пароль»
        открывается страница восстановления пароля."""
        login_page = LoginPage(driver)
        reset_page = ResetPasswordPage(driver)

        login_page.open(f'{BASE_URL}login')
        login_page.click_forgot_password()

        assert reset_page.is_element_visible(ResetPasswordPageLocators.RESET_HEADER)

    @allure.title('Ввод почты и клик по кнопке Восстановить')
    def test_fill_email_and_click_restore(self, driver):
        """Проверяет, что после ввода email и клика «Восстановить» происходит
        переход на страницу reset-password."""
        reset_page = ResetPasswordPage(driver)

        reset_page.open(f'{BASE_URL}forgot-password')
        reset_page.fill_email('test@yandex.ru')
        reset_page.click_restore_button()

        # После клика должен произойти переход на страницу reset-password
        reset_page.wait_for_url_contains('reset-password')
        assert 'reset-password' in driver.current_url

    @allure.title('Клик по кнопке показать/скрыть пароль делает поле активным')
    def test_click_show_hide_password_makes_field_active(self, driver):
        """Проверяет, что на странице reset-password клик по иконке глаза
        подсвечивает (активирует) поле пароля.

        ВАЖНО: на страницу reset-password нельзя просто перейти по URL —
        сайт перенаправит на forgot-password. Нужно сначала ввести email
        и нажать «Восстановить», чтобы попасть на reset-password.
        """
        reset_page = ResetPasswordPage(driver)

        # Проходим весь флоу: forgot-password -> вводим email -> кнопка Восстановить
        reset_page.open(f'{BASE_URL}forgot-password')
        reset_page.fill_email('test@yandex.ru')
        reset_page.click_restore_button()

        # Ожидаем переход на reset-password
        reset_page.wait_for_url_contains('reset-password')

        # Кликаем иконку показать/скрыть пароль
        reset_page.click_show_hide_password()

        # Проверяем, что поле стало активным (подсвечено)
        assert reset_page.is_password_field_active()

import allure

from pages.base_page import BasePage
from locators.reset_password_page_locators import ResetPasswordPageLocators


class ResetPasswordPage(BasePage):

    @allure.step('Ввести email: {email}')
    def fill_email(self, email):
        self.set_text(ResetPasswordPageLocators.EMAIL_INPUT, email)

    @allure.step('Нажать «Восстановить»')
    def click_restore_button(self):
        self.click_element(ResetPasswordPageLocators.RESET_BUTTON)

    @allure.step('Запросить восстановление пароля и перейти на reset-password: {email}')
    def request_password_reset(self, email):
        """Заполняет email, нажимает «Восстановить» и ожидает загрузки reset-password.

        Иногда первый клик не доходит до кнопки (оверлей-лоадер или React ещё не
        прицепил обработчик). Делаем повторную попытку, если URL не сменился.
        """
        self.fill_email(email)
        self.click_restore_button()

        # Если URL не сменился за 5 секунд — повторяем клик
        if not self.wait_for_url_contains_safe('reset-password', timeout=5):
            self.click_restore_button()
            self.wait_for_url_contains('reset-password')

        # Ждём появления поля пароля на новой странице
        self.wait_for_visible(ResetPasswordPageLocators.PASSWORD_INPUT)

    @allure.step('Нажать иконку «показать/скрыть пароль»')
    def click_show_hide_password(self):
        self.click_element(ResetPasswordPageLocators.SHOW_HIDE_PASSWORD_BUTTON)

    @allure.step('Проверить, что поле пароля активно (подсвечено)')
    def is_password_field_active(self):
        return self.is_element_visible(ResetPasswordPageLocators.ACTIVE_PASSWORD_FIELD)

    @allure.step('Проверить, что открыта страница восстановления пароля')
    def is_reset_page_opened(self):
        return self.is_element_visible(ResetPasswordPageLocators.RESET_HEADER)

import allure
from pages.base_page import BasePage
from locators.reset_password_page_locators import ResetPasswordPageLocators


class ResetPasswordPage(BasePage):

    @allure.step('Ввести email для восстановления')
    def fill_email(self, email):
        self.set_text(ResetPasswordPageLocators.EMAIL_INPUT, email)

    @allure.step('Нажать кнопку Восстановить')
    def click_restore_button(self):
        self.click_element(ResetPasswordPageLocators.RESET_BUTTON)

    @allure.step('Нажать показать/скрыть пароль')
    def click_show_hide_password(self):
        self.click_element(ResetPasswordPageLocators.SHOW_HIDE_PASSWORD_BUTTON)

    @allure.step('Проверить, что поле пароля активно (подсвечено)')
    def is_password_field_active(self):
        return self.is_element_visible(ResetPasswordPageLocators.ACTIVE_PASSWORD_FIELD)

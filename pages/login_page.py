import allure
from pages.base_page import BasePage
from locators.login_page_locators import LoginPageLocators


class LoginPage(BasePage):

    @allure.step('Нажать на ссылку Восстановить пароль')
    def click_forgot_password(self):
        self.click_element(LoginPageLocators.FORGOT_PASSWORD_LINK)

    @allure.step('Авторизоваться: email={email}')
    def login(self, email, password):
        self.set_text(LoginPageLocators.EMAIL_INPUT, email)
        self.set_text(LoginPageLocators.PASSWORD_INPUT, password)
        self.click_element(LoginPageLocators.LOGIN_BUTTON)

    @allure.step('Проверить, что открыта страница логина')
    def is_login_page_opened(self):
        return self.is_element_visible(LoginPageLocators.LOGIN_HEADER)

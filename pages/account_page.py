import allure

from pages.base_page import BasePage
from locators.account_page_locators import AccountPageLocators


class AccountPage(BasePage):

    @allure.step('Открыть раздел «История заказов»')
    def click_order_history(self):
        self.click_element(AccountPageLocators.ORDER_HISTORY_LINK)

    @allure.step('Нажать «Выход»')
    def click_logout(self):
        self.click_element(AccountPageLocators.LOGOUT_BUTTON)

    @allure.step('Дождаться загрузки страницы профиля')
    def wait_for_profile_loaded(self):
        self.wait_for_visible(AccountPageLocators.PROFILE_LINK)

    @allure.step('Дождаться загрузки истории заказов')
    def wait_for_order_history_loaded(self):
        """Ждём пока URL станет order-history (вместо фиксированного time.sleep)."""
        self.wait_for_url_contains('order-history')

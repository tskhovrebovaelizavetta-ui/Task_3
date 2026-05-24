import time
import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from locators.feed_page_locators import FeedPageLocators


class FeedPage(BasePage):

    @allure.step('Открыть первый заказ в ленте')
    def open_first_order(self):
        self.click_element(FeedPageLocators.ORDER_CARD)

    @allure.step('Получить счётчик Выполнено за всё время')
    def get_total_done_value(self):
        text = self.get_text(FeedPageLocators.TOTAL_DONE_COUNTER)
        return int(text)

    @allure.step('Получить счётчик Выполнено за сегодня')
    def get_today_done_value(self):
        text = self.get_text(FeedPageLocators.TODAY_DONE_COUNTER)
        return int(text)

    @allure.step('Получить номера заказов из истории пользователя')
    def get_order_history_numbers(self):
        elements = self.find_elements(FeedPageLocators.ORDER_HISTORY_NUMBERS)
        return [el.text.strip().lstrip('#0') for el in elements if el.text.strip()]

    @allure.step('Получить все номера заказов из ленты')
    def get_all_feed_order_numbers(self):
        """Собирает номера заказов с ленты, убирает # и лидирующие нули."""
        numbers = []
        try:
            order_items = self.driver.find_elements(
                By.XPATH,
                "//ul[contains(@class, 'OrderFeed')]//p[contains(@class, 'text_type_digits-default')]"
            )
            for item in order_items:
                text = item.text.strip().lstrip('#0')
                if text:
                    numbers.append(text)
        except Exception:
            pass
        return numbers

    @allure.step('Получить номера заказов из раздела В работе')
    def get_in_progress_order_numbers(self):
        """Возвращает список номеров заказов из раздела «В работе»."""
        try:
            elements = self.find_elements(FeedPageLocators.IN_PROGRESS_ORDER_NUMBER)
            return [el.text.strip().lstrip('0') for el in elements if el.text.strip()]
        except TimeoutException:
            return []

    @allure.step('Дождаться загрузки ленты заказов')
    def wait_for_feed_loaded(self):
        self.find_element(FeedPageLocators.FEED_HEADER)

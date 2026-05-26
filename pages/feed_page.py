import allure
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from locators.feed_page_locators import FeedPageLocators


class FeedPage(BasePage):

    @allure.step('Открыть первый заказ в ленте')
    def open_first_order(self):
        self.click_element(FeedPageLocators.ORDER_CARD)

    @allure.step('Получить счётчик «Выполнено за всё время»')
    def get_total_done_value(self):
        return int(self.get_text(FeedPageLocators.TOTAL_DONE_COUNTER))

    @allure.step('Получить счётчик «Выполнено за сегодня»')
    def get_today_done_value(self):
        return int(self.get_text(FeedPageLocators.TODAY_DONE_COUNTER))

    @allure.step('Дождаться изменения счётчика «Выполнено за всё время»')
    def wait_for_total_done_to_change(self, current_value):
        """Ждёт, пока значение счётчика «Выполнено за всё время» отличится от текущего."""
        self.wait_for_text_to_change(
            FeedPageLocators.TOTAL_DONE_COUNTER, str(current_value)
        )

    @allure.step('Дождаться изменения счётчика «Выполнено за сегодня»')
    def wait_for_today_done_to_change(self, current_value):
        """Ждёт, пока значение счётчика «Выполнено за сегодня» отличится от текущего."""
        self.wait_for_text_to_change(
            FeedPageLocators.TODAY_DONE_COUNTER, str(current_value)
        )

    @allure.step('Получить номера заказов из истории пользователя')
    def get_order_history_numbers(self):
        texts = self.get_texts(FeedPageLocators.ORDER_HISTORY_NUMBERS)
        return [t.strip().lstrip('#0') for t in texts if t.strip()]

    @allure.step('Получить все номера заказов из ленты')
    def get_all_feed_order_numbers(self):
        """Собирает номера заказов с ленты, убирает # и лидирующие нули."""
        try:
            texts = self.get_texts(FeedPageLocators.ALL_FEED_ORDER_NUMBERS)
            return [t.strip().lstrip('#0') for t in texts if t.strip()]
        except TimeoutException:
            return []

    @allure.step('Получить номера заказов из раздела «В работе»')
    def get_in_progress_order_numbers(self):
        try:
            texts = self.get_texts(FeedPageLocators.IN_PROGRESS_ORDER_NUMBER)
            return [t.strip().lstrip('0') for t in texts if t.strip()]
        except TimeoutException:
            return []

    @allure.step('Дождаться загрузки ленты заказов')
    def wait_for_feed_loaded(self):
        self.wait_for_visible(FeedPageLocators.FEED_HEADER)

    @allure.step('Проверить, что открыта модалка деталей заказа')
    def is_order_modal_visible(self):
        return self.is_element_visible(FeedPageLocators.ORDER_MODAL)

    @allure.step('Дождаться появления заказа {order_number} в разделе «В работе»')
    def wait_for_order_in_progress(self, order_number, attempts=5):
        """Проверяет несколько раз с обновлением страницы, появился ли заказ в «В работе»."""
        target = order_number.lstrip('0')
        for _ in range(attempts):
            in_progress = self.get_in_progress_order_numbers()
            if target in [n.lstrip('0') for n in in_progress]:
                return True
            self.refresh_page()
            self.wait_for_feed_loaded()
        return False

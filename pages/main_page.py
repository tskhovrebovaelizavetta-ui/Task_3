import time
import allure
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):

    @allure.step('Открыть личный кабинет')
    def click_personal_account(self):
        self.click_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)

    @allure.step('Открыть раздел Конструктор')
    def click_constructor(self):
        self.click_element(MainPageLocators.CONSTRUCTOR_BUTTON)

    @allure.step('Открыть раздел Лента заказов')
    def click_order_feed(self):
        self.click_element(MainPageLocators.ORDER_FEED_BUTTON)

    @allure.step('Кликнуть на ингредиент для просмотра деталей')
    def open_ingredient_details(self):
        self.click_element(MainPageLocators.INGREDIENT_CARD)

    @allure.step('Закрыть модальное окно')
    def close_modal(self):
        self.click_element(MainPageLocators.MODAL_CLOSE_BUTTON)

    @allure.step('Добавить ингредиент (булку) в конструктор перетаскиванием')
    def add_bun_to_constructor(self):
        self.drag_and_drop_element(
            MainPageLocators.BUN_INGREDIENT,
            MainPageLocators.BURGER_CONSTRUCTOR_DROP_AREA
        )

    @allure.step('Добавить начинку в конструктор перетаскиванием')
    def add_filling_to_constructor(self):
        self.drag_and_drop_element(
            MainPageLocators.FILLING_INGREDIENT,
            MainPageLocators.BURGER_CONSTRUCTOR_DROP_AREA
        )

    @allure.step('Нажать Оформить заказ')
    def click_place_order(self):
        self.click_element(MainPageLocators.PLACE_ORDER_BUTTON)

    @allure.step('Получить значение каунтера ингредиента')
    def get_bun_counter_value(self):
        """Получает значение счётчика на первом ингредиенте.
        Каунтер появляется после добавления ингредиента в конструктор.
        """
        bun_element = self.find_element(MainPageLocators.BUN_INGREDIENT)
        counter = bun_element.find_element(*MainPageLocators.INGREDIENT_COUNTER)
        return int(counter.text)

    @allure.step('Получить номер заказа из модального окна')
    def get_order_number_from_modal(self):
        """Ожидает, пока номер заказа появится (не «9999»), и возвращает его."""
        # Ждём пока номер заказа прогрузится (вместо 9999 появится реальный номер)
        for _ in range(30):
            text = self.get_text(MainPageLocators.ORDER_NUMBER_IN_MODAL)
            if text and text != '9999':
                return text
            time.sleep(1)
        return self.get_text(MainPageLocators.ORDER_NUMBER_IN_MODAL)

    @allure.step('Дождаться появления модалки заказа')
    def wait_for_order_modal(self):
        """Ожидает появления модалки с идентификатором заказа."""
        self.find_element(MainPageLocators.ORDER_ID_LABEL)

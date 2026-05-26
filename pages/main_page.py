import allure

from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):

    @allure.step('Открыть личный кабинет')
    def click_personal_account(self):
        self.click_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)

    @allure.step('Открыть раздел «Конструктор»')
    def click_constructor(self):
        self.click_element(MainPageLocators.CONSTRUCTOR_BUTTON)

    @allure.step('Открыть раздел «Лента Заказов»')
    def click_order_feed(self):
        self.click_element(MainPageLocators.ORDER_FEED_BUTTON)

    @allure.step('Кликнуть по ингредиенту')
    def open_ingredient_details(self):
        self.click_element(MainPageLocators.INGREDIENT_CARD)

    @allure.step('Закрыть модальное окно')
    def close_modal(self):
        self.click_element(MainPageLocators.MODAL_CLOSE_BUTTON)

    @allure.step('Перетащить булку в конструктор')
    def add_bun_to_constructor(self):
        self.drag_and_drop_element(
            MainPageLocators.BUN_INGREDIENT,
            MainPageLocators.BURGER_CONSTRUCTOR_DROP_AREA
        )

    @allure.step('Перетащить начинку в конструктор')
    def add_filling_to_constructor(self):
        self.drag_and_drop_element(
            MainPageLocators.FILLING_INGREDIENT,
            MainPageLocators.BURGER_CONSTRUCTOR_DROP_AREA
        )

    @allure.step('Нажать «Оформить заказ»')
    def click_place_order(self):
        self.click_element(MainPageLocators.PLACE_ORDER_BUTTON)

    @allure.step('Получить значение каунтера булки')
    def get_bun_counter_value(self):
        """Каунтер на карточке булки появляется после её добавления в конструктор."""
        bun = self.wait_for_visible(MainPageLocators.BUN_INGREDIENT)
        counter = bun.find_element(*MainPageLocators.INGREDIENT_COUNTER)
        return int(counter.text)

    @allure.step('Дождаться появления модалки заказа')
    def wait_for_order_modal(self):
        self.wait_for_visible(MainPageLocators.ORDER_ID_LABEL)

    @allure.step('Получить номер заказа из модального окна')
    def get_order_number_from_modal(self):
        """Дожидается реального номера заказа (вместо плейсхолдера 9999) и возвращает его."""
        self.wait_for_order_number_loaded(
            MainPageLocators.ORDER_NUMBER_IN_MODAL,
            placeholder='9999'
        )
        return self.get_text(MainPageLocators.ORDER_NUMBER_IN_MODAL)

    # ---------- Методы-проверки для тестов (чтобы тесты не работали с локаторами) ----------

    @allure.step('Проверить, что открыта модалка «Детали ингредиента»')
    def is_ingredient_modal_visible(self):
        return self.is_element_visible(MainPageLocators.INGREDIENT_DETAILS_MODAL)

    @allure.step('Дождаться закрытия модалки «Детали ингредиента»')
    def wait_for_ingredient_modal_closed(self):
        return self.wait_for_invisible(MainPageLocators.INGREDIENT_DETAILS_MODAL)

    @allure.step('Проверить, что модалка с номером заказа отображается')
    def is_order_number_modal_visible(self):
        return self.is_element_visible(MainPageLocators.ORDER_NUMBER_IN_MODAL)

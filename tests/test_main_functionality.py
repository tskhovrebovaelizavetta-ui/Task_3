import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from locators.main_page_locators import MainPageLocators
from utils.constants import BASE_URL


@allure.feature('Основной функционал')
class TestMainFunctionality:

    @allure.title('Переход по клику на Конструктор')
    def test_open_constructor(self, driver):
        """Проверяет, что клик по «Конструктор» возвращает на главную страницу."""
        main_page = MainPage(driver)

        # Сначала уходим со страницы конструктора
        main_page.click_order_feed()
        main_page.wait_for_url_contains('feed')

        # Нажимаем «Конструктор»
        main_page.click_constructor()

        # Проверяем, что вернулись на главную (URL не содержит «feed»)
        assert 'feed' not in driver.current_url

    @allure.title('Переход по клику на Лента заказов')
    def test_open_order_feed(self, driver):
        """Проверяет, что клик по «Лента Заказов» открывает страницу ленты."""
        main_page = MainPage(driver)

        main_page.click_order_feed()

        main_page.wait_for_url_contains('feed')
        assert 'feed' in driver.current_url

    @allure.title('Если кликнуть на ингредиент, появится всплывающее окно с деталями')
    def test_open_ingredient_details_modal(self, driver):
        """Проверяет, что клик по ингредиенту открывает модалку «Детали ингредиента»."""
        main_page = MainPage(driver)

        main_page.open_ingredient_details()

        assert main_page.is_element_visible(MainPageLocators.INGREDIENT_DETAILS_MODAL)

    @allure.title('Всплывающее окно закрывается кликом по крестику')
    def test_close_ingredient_details_modal(self, driver):
        """Проверяет, что модальное окно закрывается при клике на крестик."""
        main_page = MainPage(driver)

        main_page.open_ingredient_details()
        main_page.find_element(MainPageLocators.INGREDIENT_DETAILS_MODAL)
        main_page.close_modal()

        assert main_page.wait_for_element_invisible(MainPageLocators.INGREDIENT_DETAILS_MODAL)

    @allure.title('При добавлении ингредиента в заказ увеличивается каунтер')
    def test_counter_increases_after_add_ingredient(self, driver):
        """Проверяет, что после перетаскивания ингредиента в конструктор
        на его карточке появляется каунтер > 0."""
        main_page = MainPage(driver)

        main_page.add_bun_to_constructor()

        counter_value = main_page.get_bun_counter_value()
        assert counter_value > 0

    @allure.title('Залогиненный пользователь может оформить заказ')
    def test_authorized_user_can_place_order(self, driver, created_user):
        """Проверяет, что после логина пользователь может собрать бургер
        и оформить заказ — появится модалка с номером."""
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        # Логинимся
        main_page.click_personal_account()
        login_page.login(created_user['email'], created_user['password'])
        main_page.wait_for_url_contains('/')

        # Собираем бургер
        main_page.add_bun_to_constructor()
        main_page.add_filling_to_constructor()

        # Оформляем заказ
        main_page.click_place_order()

        # Проверяем, что появилась модалка с идентификатором заказа
        main_page.wait_for_order_modal()
        assert main_page.is_element_visible(MainPageLocators.ORDER_NUMBER_IN_MODAL)

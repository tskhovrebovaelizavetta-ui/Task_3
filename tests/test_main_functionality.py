import allure

from pages.main_page import MainPage
from pages.login_page import LoginPage


@allure.feature('Основной функционал')
class TestMainFunctionality:

    @allure.title('Переход по клику на «Конструктор»')
    def test_open_constructor(self, driver):
        """Проверяет, что клик по «Конструктор» возвращает на главную страницу."""
        main_page = MainPage(driver)

        main_page.click_order_feed()
        main_page.wait_for_url_contains('feed')

        main_page.click_constructor()

        assert not main_page.url_contains('feed')

    @allure.title('Переход по клику на «Лента Заказов»')
    def test_open_order_feed(self, driver):
        """Проверяет, что клик по «Лента Заказов» открывает страницу ленты."""
        main_page = MainPage(driver)

        main_page.click_order_feed()

        main_page.wait_for_url_contains('feed')
        assert main_page.url_contains('feed')

    @allure.title('Клик по ингредиенту открывает модалку с деталями')
    def test_open_ingredient_details_modal(self, driver):
        main_page = MainPage(driver)

        main_page.open_ingredient_details()

        assert main_page.is_ingredient_modal_visible()

    @allure.title('Модалка деталей ингредиента закрывается крестиком')
    def test_close_ingredient_details_modal(self, driver):
        main_page = MainPage(driver)

        main_page.open_ingredient_details()
        assert main_page.is_ingredient_modal_visible()
        main_page.close_modal()

        assert main_page.wait_for_ingredient_modal_closed()

    @allure.title('При добавлении ингредиента увеличивается каунтер')
    def test_counter_increases_after_add_ingredient(self, driver):
        main_page = MainPage(driver)

        main_page.add_bun_to_constructor()

        assert main_page.get_bun_counter_value() > 0

    @allure.title('Залогиненный пользователь может оформить заказ')
    def test_authorized_user_can_place_order(self, driver, created_user):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        main_page.click_personal_account()
        login_page.login(created_user['email'], created_user['password'])
        main_page.wait_for_url_contains('/')

        main_page.add_bun_to_constructor()
        main_page.add_filling_to_constructor()
        main_page.click_place_order()

        main_page.wait_for_order_modal()
        assert main_page.is_order_number_modal_visible()

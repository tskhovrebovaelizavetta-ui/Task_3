import time
import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from pages.feed_page import FeedPage
from locators.feed_page_locators import FeedPageLocators
from utils.constants import BASE_URL


@allure.feature('Лента заказов')
class TestOrderFeed:

    @allure.title('Если кликнуть на заказ, откроется всплывающее окно с деталями')
    def test_open_order_details_modal_from_feed(self, driver):
        """Проверяет, что клик по заказу в ленте открывает модалку с деталями."""
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)

        main_page.click_order_feed()
        feed_page.wait_for_feed_loaded()
        feed_page.open_first_order()

        assert feed_page.is_element_visible(FeedPageLocators.ORDER_MODAL)

    @allure.title('Заказы пользователя из История заказов отображаются в Ленте заказов')
    def test_order_from_history_displayed_in_feed(self, driver, created_user):
        """Проверяет, что после оформления заказа его номер виден
        и в «Истории заказов» пользователя, и в «Ленте заказов»."""
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        account_page = AccountPage(driver)
        feed_page = FeedPage(driver)

        # Логинимся
        main_page.click_personal_account()
        login_page.login(created_user['email'], created_user['password'])
        main_page.wait_for_url_contains('/')

        # Создаём заказ через UI
        main_page.add_bun_to_constructor()
        main_page.add_filling_to_constructor()
        main_page.click_place_order()

        # Получаем номер заказа из модалки
        main_page.wait_for_order_modal()
        order_number = main_page.get_order_number_from_modal()
        main_page.close_modal()

        # Идём в Историю заказов
        main_page.click_personal_account()
        account_page.wait_for_profile_loaded()
        account_page.click_order_history()
        account_page.wait_for_url_contains('order-history')

        # Даём время на подгрузку истории
        time.sleep(2)

        # Проверяем, что номер заказа есть в истории
        history_numbers = feed_page.get_order_history_numbers()
        assert order_number.lstrip('0') in [n.lstrip('0') for n in history_numbers], \
            f'Заказ {order_number} не найден в истории: {history_numbers}'

        # Переходим в Ленту заказов
        main_page.click_order_feed()
        feed_page.wait_for_feed_loaded()

        # Проверяем, что номер заказа есть в ленте
        feed_numbers = feed_page.get_all_feed_order_numbers()
        assert order_number.lstrip('0') in [n.lstrip('0') for n in feed_numbers], \
            f'Заказ {order_number} не найден в ленте: {feed_numbers}'

    @allure.title('При создании нового заказа счётчик Выполнено за всё время увеличивается')
    def test_total_done_counter_increases(self, driver, created_user):
        """Проверяет, что после оформления заказа счётчик «Выполнено за всё время»
        увеличился."""
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        feed_page = FeedPage(driver)

        # Запоминаем текущее значение счётчика
        main_page.click_order_feed()
        feed_page.wait_for_feed_loaded()
        before_total = feed_page.get_total_done_value()

        # Логинимся и создаём заказ
        main_page.click_constructor()
        main_page.click_personal_account()
        login_page.login(created_user['email'], created_user['password'])
        main_page.wait_for_url_contains('/')

        main_page.add_bun_to_constructor()
        main_page.add_filling_to_constructor()
        main_page.click_place_order()

        # Ждём оформление заказа
        main_page.wait_for_order_modal()
        main_page.get_order_number_from_modal()
        main_page.close_modal()

        # Проверяем счётчик
        main_page.click_order_feed()
        feed_page.wait_for_feed_loaded()
        after_total = feed_page.get_total_done_value()

        assert after_total > before_total, \
            f'Счётчик не увеличился: было {before_total}, стало {after_total}'

    @allure.title('При создании нового заказа счётчик Выполнено за сегодня увеличивается')
    def test_today_done_counter_increases(self, driver, created_user):
        """Проверяет, что после оформления заказа счётчик «Выполнено за сегодня»
        увеличился."""
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        feed_page = FeedPage(driver)

        # Запоминаем текущее значение счётчика
        main_page.click_order_feed()
        feed_page.wait_for_feed_loaded()
        before_today = feed_page.get_today_done_value()

        # Логинимся и создаём заказ
        main_page.click_constructor()
        main_page.click_personal_account()
        login_page.login(created_user['email'], created_user['password'])
        main_page.wait_for_url_contains('/')

        main_page.add_bun_to_constructor()
        main_page.add_filling_to_constructor()
        main_page.click_place_order()

        # Ждём оформление заказа
        main_page.wait_for_order_modal()
        main_page.get_order_number_from_modal()
        main_page.close_modal()

        # Проверяем счётчик
        main_page.click_order_feed()
        feed_page.wait_for_feed_loaded()
        after_today = feed_page.get_today_done_value()

        assert after_today > before_today, \
            f'Счётчик не увеличился: было {before_today}, стало {after_today}'

    @allure.title('После оформления заказа его номер появляется в разделе В работе')
    def test_new_order_appears_in_progress(self, driver, created_user):
        """Проверяет, что после оформления заказа его номер виден
        в разделе «В работе» на странице ленты."""
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        feed_page = FeedPage(driver)

        # Логинимся
        main_page.click_personal_account()
        login_page.login(created_user['email'], created_user['password'])
        main_page.wait_for_url_contains('/')

        # Создаём заказ
        main_page.add_bun_to_constructor()
        main_page.add_filling_to_constructor()
        main_page.click_place_order()

        # Получаем номер заказа
        main_page.wait_for_order_modal()
        order_number = main_page.get_order_number_from_modal()
        main_page.close_modal()

        # Переходим в ленту заказов
        main_page.click_order_feed()
        feed_page.wait_for_feed_loaded()

        # Ждём пока заказ появится «В работе» — сервер может обновлять с задержкой,
        # поэтому проверяем несколько раз с перезагрузкой страницы
        found = False
        for _ in range(5):
            time.sleep(3)
            in_progress = feed_page.get_in_progress_order_numbers()
            if order_number.lstrip('0') in [n.lstrip('0') for n in in_progress]:
                found = True
                break
            # Обновляем страницу, чтобы подтянулись свежие данные
            driver.refresh()
            feed_page.wait_for_feed_loaded()

        assert found, \
            f'Заказ {order_number} не найден в разделе «В работе»: {in_progress}'

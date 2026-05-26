import allure

from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from pages.feed_page import FeedPage


@allure.feature('Лента заказов')
class TestOrderFeed:

    @allure.title('Клик по заказу открывает модалку с деталями')
    def test_open_order_details_modal_from_feed(self, driver):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)

        main_page.click_order_feed()
        feed_page.wait_for_feed_loaded()
        feed_page.open_first_order()

        assert feed_page.is_order_modal_visible()

    @allure.title('Заказы пользователя из «История заказов» отображаются в «Ленте заказов»')
    def test_order_from_history_displayed_in_feed(self, driver, created_user):
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

        main_page.wait_for_order_modal()
        order_number = main_page.get_order_number_from_modal()
        main_page.close_modal()

        # Проверяем заказ в Истории
        main_page.click_personal_account()
        account_page.wait_for_profile_loaded()
        account_page.click_order_history()
        account_page.wait_for_order_history_loaded()

        history_numbers = feed_page.get_order_history_numbers()
        assert order_number.lstrip('0') in [n.lstrip('0') for n in history_numbers], \
            f'Заказ {order_number} не найден в истории: {history_numbers}'

        # Проверяем заказ в Ленте
        main_page.click_order_feed()
        feed_page.wait_for_feed_loaded()
        feed_numbers = feed_page.get_all_feed_order_numbers()
        assert order_number.lstrip('0') in [n.lstrip('0') for n in feed_numbers], \
            f'Заказ {order_number} не найден в ленте: {feed_numbers}'

    @allure.title('При создании заказа счётчик «Выполнено за всё время» увеличивается')
    def test_total_done_counter_increases(self, driver, created_user):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        feed_page = FeedPage(driver)

        main_page.click_order_feed()
        feed_page.wait_for_feed_loaded()
        before_total = feed_page.get_total_done_value()

        main_page.click_constructor()
        main_page.click_personal_account()
        login_page.login(created_user['email'], created_user['password'])
        main_page.wait_for_url_contains('/')

        main_page.add_bun_to_constructor()
        main_page.add_filling_to_constructor()
        main_page.click_place_order()

        main_page.wait_for_order_modal()
        main_page.get_order_number_from_modal()
        main_page.close_modal()

        main_page.click_order_feed()
        feed_page.wait_for_feed_loaded()
        # Ждём изменения через явное ожидание (без time.sleep)
        feed_page.wait_for_total_done_to_change(before_total)
        after_total = feed_page.get_total_done_value()

        assert after_total > before_total, \
            f'Счётчик не увеличился: было {before_total}, стало {after_total}'

    @allure.title('При создании заказа счётчик «Выполнено за сегодня» увеличивается')
    def test_today_done_counter_increases(self, driver, created_user):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        feed_page = FeedPage(driver)

        main_page.click_order_feed()
        feed_page.wait_for_feed_loaded()
        before_today = feed_page.get_today_done_value()

        main_page.click_constructor()
        main_page.click_personal_account()
        login_page.login(created_user['email'], created_user['password'])
        main_page.wait_for_url_contains('/')

        main_page.add_bun_to_constructor()
        main_page.add_filling_to_constructor()
        main_page.click_place_order()

        main_page.wait_for_order_modal()
        main_page.get_order_number_from_modal()
        main_page.close_modal()

        main_page.click_order_feed()
        feed_page.wait_for_feed_loaded()
        # Ждём изменения через явное ожидание (без time.sleep)
        feed_page.wait_for_today_done_to_change(before_today)
        after_today = feed_page.get_today_done_value()

        assert after_today > before_today, \
            f'Счётчик не увеличился: было {before_today}, стало {after_today}'

    @allure.title('После оформления заказ появляется в разделе «В работе»')
    def test_new_order_appears_in_progress(self, driver, created_user):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        feed_page = FeedPage(driver)

        main_page.click_personal_account()
        login_page.login(created_user['email'], created_user['password'])
        main_page.wait_for_url_contains('/')

        main_page.add_bun_to_constructor()
        main_page.add_filling_to_constructor()
        main_page.click_place_order()

        main_page.wait_for_order_modal()
        order_number = main_page.get_order_number_from_modal()
        main_page.close_modal()

        main_page.click_order_feed()
        feed_page.wait_for_feed_loaded()

        assert feed_page.wait_for_order_in_progress(order_number), \
            f'Заказ {order_number} не появился в разделе «В работе»'

import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

from locators.base_page_locators import BasePageLocators
from utils.constants import DEFAULT_TIMEOUT


class BasePage:
    """Базовый класс Page Object.

    Здесь сосредоточены все обращения к Selenium API (WebDriverWait, EC,
    ActionChains, JS-исполнение). Тесты и наследники работают только
    с этими методами и НЕ обращаются к driver напрямую.
    """

    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------- Базовые ожидания (обёртки над WebDriverWait) ----------

    @allure.step('Ожидать видимости элемента')
    def wait_for_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step('Ожидать присутствия элемента в DOM')
    def wait_for_present(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step('Ожидать кликабельности элемента')
    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    @allure.step('Ожидать всех элементов')
    def wait_for_all_present(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    @allure.step('Ожидать исчезновения элемента')
    def wait_for_invisible(self, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(EC.invisibility_of_element_located(locator))

    @allure.step('Ожидать URL, содержащий {url_part}')
    def wait_for_url_contains(self, url_part):
        self.wait.until(EC.url_contains(url_part))

    @allure.step('Безопасно подождать URL, содержащий {url_part}')
    def wait_for_url_contains_safe(self, url_part, timeout=5):
        """Ждёт изменения URL. Возвращает True если дождались, False — если таймаут.
        Не выбрасывает исключение, в отличие от wait_for_url_contains."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(url_part))
            return True
        except TimeoutException:
            return False

    @allure.step('Ожидать изменения текста элемента (текущий: {current_text})')
    def wait_for_text_to_change(self, locator, current_text):
        """Ждёт, пока текст элемента станет отличным от current_text."""
        self.wait.until(
            lambda d: self.wait_for_visible(locator).text != current_text
        )

    @allure.step('Ожидать появления нового номера заказа в модалке')
    def wait_for_order_number_loaded(self, locator, placeholder='9999'):
        """Ждёт пока в модалке заказа появится реальный номер (не плейсхолдер 9999)."""
        self.wait.until(
            lambda d: self.wait_for_visible(locator).text != placeholder
            and self.wait_for_visible(locator).text != ''
        )

    # ---------- Действия с элементами ----------

    def _wait_for_overlay_to_disappear(self):
        """Внутренний метод. Ждёт, пока модальный оверлей исчезнет
        (актуально для Firefox)."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(BasePageLocators.MODAL_OVERLAY)
            )
        except TimeoutException:
            # Запасной вариант: прячем оверлей через JS, если он завис
            self._hide_overlay_via_js()

    def _hide_overlay_via_js(self):
        """Внутренний метод. Принудительно прячет оверлей через JavaScript."""
        self.driver.execute_script(
            "document.querySelectorAll('[class*=\"Modal_modal_overlay\"]')"
            ".forEach(el => el.style.display = 'none');"
        )

    @allure.step('Открыть URL: {url}')
    def open(self, url):
        self.driver.get(url)
        self._wait_for_overlay_to_disappear()

    @allure.step('Кликнуть по элементу')
    def click_element(self, locator):
        self._wait_for_overlay_to_disappear()
        element = self.wait_for_clickable(locator)
        try:
            element.click()
        except Exception:
            # Если обычный клик перехвачен, делаем клик через JS
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step('Ввести текст: {text}')
    def set_text(self, locator, text):
        self._wait_for_overlay_to_disappear()
        element = self.wait_for_visible(locator)
        element.clear()
        element.send_keys(text)

    @allure.step('Получить текст элемента')
    def get_text(self, locator):
        return self.wait_for_visible(locator).text

    @allure.step('Получить тексты всех элементов по локатору')
    def get_texts(self, locator):
        elements = self.wait_for_all_present(locator)
        return [el.text for el in elements]

    def is_element_visible(self, locator):
        """Проверяет видимость элемента без выброса исключения."""
        try:
            self.wait_for_visible(locator)
            return True
        except TimeoutException:
            return False

    @allure.step('Перетащить элемент')
    def drag_and_drop_element(self, source_locator, target_locator):
        self._wait_for_overlay_to_disappear()
        source = self.wait_for_visible(source_locator)
        target = self.wait_for_visible(target_locator)
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    @allure.step('Прокрутить страницу к элементу')
    def scroll_to_element(self, locator):
        element = self.wait_for_present(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    @allure.step('Обновить страницу')
    def refresh_page(self):
        self.driver.refresh()
        self._wait_for_overlay_to_disappear()

    # ---------- Геттеры состояния страницы ----------

    def get_current_url(self):
        return self.driver.current_url

    def url_contains(self, url_part):
        """Возвращает True, если в текущем URL есть url_part."""
        return url_part in self.driver.current_url

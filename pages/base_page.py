import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from utils.constants import DEFAULT_TIMEOUT

# Локатор модального оверлея — он перекрывает элементы при загрузке страницы
MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]")


class BasePage:
    """Базовый класс Page Object со всеми общими действиями."""

    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _wait_for_overlay_to_disappear(self):
        """Ждёт, пока модальный оверлей исчезнет (актуально для Firefox)."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(MODAL_OVERLAY)
            )
        except TimeoutException:
            # Если оверлей не нашёлся или не исчез за 5 секунд — пробуем закрыть его через JS
            self.driver.execute_script(
                "document.querySelectorAll('.Modal_modal_overlay__x2ZCr')"
                ".forEach(el => el.style.display = 'none');"
            )

    @allure.step('Открыть URL: {url}')
    def open(self, url):
        self.driver.get(url)
        self._wait_for_overlay_to_disappear()

    @allure.step('Найти элемент')
    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step('Найти все элементы')
    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    @allure.step('Кликнуть по элементу')
    def click_element(self, locator):
        self._wait_for_overlay_to_disappear()
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except Exception:
            # Если обычный клик не сработал (оверлей всё ещё мешает) — кликаем через JS
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step('Ввести текст')
    def set_text(self, locator, text):
        self._wait_for_overlay_to_disappear()
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step('Получить текст элемента')
    def get_text(self, locator):
        return self.find_element(locator).text

    @allure.step('Ожидать URL, содержащий: {url_part}')
    def wait_for_url_contains(self, url_part):
        self.wait.until(EC.url_contains(url_part))

    @allure.step('Ожидать исчезновение элемента')
    def wait_for_element_invisible(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def is_element_visible(self, locator):
        """Проверяет видимость элемента без выброса исключения."""
        try:
            self.find_element(locator)
            return True
        except TimeoutException:
            return False

    @allure.step('Перетащить элемент')
    def drag_and_drop_element(self, source_locator, target_locator):
        self._wait_for_overlay_to_disappear()
        source = self.find_element(source_locator)
        target = self.find_element(target_locator)
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def get_current_url(self):
        return self.driver.current_url

    @allure.step('Ожидать загрузку элемента')
    def wait_for_element_present(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step('Прокрутить к элементу')
    def scroll_to_element(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

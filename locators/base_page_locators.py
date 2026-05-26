from selenium.webdriver.common.by import By


class BasePageLocators:
    # Модальный оверлей — перекрывает элементы при загрузке страницы (особенно актуально для Firefox)
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]")

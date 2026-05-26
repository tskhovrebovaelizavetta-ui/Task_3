from selenium.webdriver.common.by import By


class LoginPageLocators:
    # Заголовок страницы «Вход»
    LOGIN_HEADER = (By.XPATH, "//h2[text()='Вход']")
    # Поле ввода email
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/../input")
    # Поле ввода пароля
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    # Кнопка «Войти»
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    # Ссылка «Восстановить пароль»
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(@href, 'forgot-password')]")

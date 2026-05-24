from selenium.webdriver.common.by import By


class ResetPasswordPageLocators:
    # Заголовок «Восстановление пароля»
    RESET_HEADER = (By.XPATH, "//h2[text()='Восстановление пароля']")
    # Поле ввода email на странице forgot-password
    EMAIL_INPUT = (By.XPATH, "//input[@type='text']")
    # Кнопка «Восстановить»
    RESET_BUTTON = (By.XPATH, "//button[text()='Восстановить']")
    # Поле ввода пароля на странице reset-password
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    # Иконка показать/скрыть пароль
    SHOW_HIDE_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'input__icon')]")
    # Контейнер поля, когда оно активно (подсвечено)
    ACTIVE_PASSWORD_FIELD = (
        By.XPATH,
        "//div[contains(@class, 'input_status_active')]"
    )

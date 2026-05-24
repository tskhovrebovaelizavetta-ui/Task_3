from selenium.webdriver.common.by import By


class AccountPageLocators:
    # Ссылка «Профиль» в боковом меню
    PROFILE_LINK = (By.XPATH, "//a[contains(@href, '/account/profile')]")
    # Ссылка «История заказов» в боковом меню
    ORDER_HISTORY_LINK = (By.XPATH, "//a[contains(@href, '/account/order-history')]")
    # Кнопка «Выход» в боковом меню
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")
    # Описание под меню профиля (проверка что раздел загружен)
    ACCOUNT_DESCRIPTION = (By.XPATH, "//p[contains(text(), 'В этом разделе')]")

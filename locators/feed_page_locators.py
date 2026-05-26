from selenium.webdriver.common.by import By


class FeedPageLocators:
    # Заголовок «Лента заказов»
    FEED_HEADER = (By.XPATH, "//h1[text()='Лента заказов']")
    # Первый заказ в ленте
    ORDER_CARD = (By.XPATH, "(//ul[contains(@class, 'OrderFeed')]/li)[1]")
    # Модальное окно деталей заказа
    ORDER_MODAL = (By.XPATH, "//p[text()='Cостав' or text()='Состав']")
    # Счётчик «Выполнено за всё время» — первый элемент с классом OrderFeed_number
    TOTAL_DONE_COUNTER = (
        By.XPATH,
        "(//p[contains(@class, 'OrderFeed_number')])[1]"
    )
    # Счётчик «Выполнено за сегодня» — второй элемент с классом OrderFeed_number
    TODAY_DONE_COUNTER = (
        By.XPATH,
        "(//p[contains(@class, 'OrderFeed_number')])[2]"
    )
    # Раздел «В работе» — номера заказов
    IN_PROGRESS_ORDER_NUMBER = (
        By.XPATH,
        "//p[text()='В работе:']/following-sibling::ul//li[contains(@class, 'text_type_digits-default')]"
    )
    # Номера заказов в истории пользователя
    ORDER_HISTORY_NUMBERS = (
        By.XPATH,
        "//ul[contains(@class, 'OrderHistory')]/li//p[contains(@class, 'text_type_digits-default')]"
    )
    # Номера всех заказов в ленте
    ALL_FEED_ORDER_NUMBERS = (
        By.XPATH,
        "//ul[contains(@class, 'OrderFeed')]//p[contains(@class, 'text_type_digits-default')]"
    )

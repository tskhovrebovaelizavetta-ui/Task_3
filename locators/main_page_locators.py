from selenium.webdriver.common.by import By


class MainPageLocators:
    # Кнопка «Личный Кабинет» в хедере
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//p[contains(text(), 'Личный') and contains(text(), 'абинет')]/..")
    # Кнопка «Конструктор» в хедере
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']/..")
    # Кнопка «Лента Заказов» в хедере
    ORDER_FEED_BUTTON = (By.XPATH, "//p[contains(text(), 'Лента') and contains(text(), 'аказов')]/..")
    # Кнопка «Войти в аккаунт» на главной (для незалогиненного пользователя)
    LOGIN_TO_ACCOUNT_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")
    # Первый ингредиент в списке (для клика и просмотра деталей)
    INGREDIENT_CARD = (By.XPATH, "(//a[contains(@class, 'BurgerIngredient')])[1]")
    # Заголовок модального окна «Детали ингредиента»
    INGREDIENT_DETAILS_MODAL = (By.XPATH, "//h2[text()='Детали ингредиента']")
    # Кнопка закрытия модального окна (крестик)
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    # Оверлей модального окна
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]")
    # Первая булка в списке ингредиентов
    BUN_INGREDIENT = (
        By.XPATH,
        "(//a[contains(@class, 'BurgerIngredient')])[1]"
    )
    # Начинка (ингредиент не-булка) — берём вторую позицию из списка ингредиентов,
    # чтобы это был не дубликат булки; если булки идут первыми, начинки ниже
    FILLING_INGREDIENT = (
        By.XPATH,
        "(//a[contains(@class, 'BurgerIngredient')])[3]"
    )
    # Область конструктора для перетаскивания (drop zone)
    BURGER_CONSTRUCTOR_DROP_AREA = (
        By.XPATH,
        "//section[contains(@class, 'BurgerConstructor')]"
    )
    # Каунтер на карточке ингредиента
    INGREDIENT_COUNTER = (
        By.XPATH,
        ".//p[contains(@class, 'counter_counter__num')]"
    )
    # Кнопка «Оформить заказ»
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    # Номер заказа в модальном окне
    ORDER_NUMBER_IN_MODAL = (By.XPATH, "//h2[contains(@class, 'text_type_digits-large')]")
    # Текст идентификатор заказа (проверяем что модалка с заказом видна)
    ORDER_ID_LABEL = (By.XPATH, "//p[text()='идентификатор заказа']")

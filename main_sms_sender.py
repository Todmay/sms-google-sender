from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time

# Инициализируем драйвер
# путь указывается только в случаях когда драйвер не установлен или не включен по умолчанию, указывается пусть в скобка веб драйвера
# пример пути если драйвер находится в каталоге скрипта
# path = '.\chromedriver_win32'
# сейчас на случай отсутствия драйвера он принудительно устанавливается при первом запуске

driver = webdriver.Chrome(ChromeDriverManager().install())

# Открываем нужную вкладку
driver.get("https://messages.google.com/web/")

time.sleep(10)

# Находим и нажимаем кнопку "Начать чат"

start_menu = driver.find_element(By.CLASS_NAME, "start-chat")
start_chat_btn = start_menu.find_element(By.CLASS_NAME, "mat-mdc-button")
start_chat_btn.click()

time.sleep(2)


# Находим и заполняем номер телефона
#phone_input_class = driver.find_element(By.CLASS_NAME, "ng-star-inserted")
#phone_input = phone_input_class.find_element(By.CLASS_NAME, "input-container")
#phone_input.send_keys("+12345678910")
phone_path = '/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-new-conversation-container/mw-new-conversation-sub-header/div/div[2]/mw-contact-chips-input/div/mat-chip-listbox/span/input'

phone_input = driver.find_element(by=By.XPATH, value=phone_path)
#phone_input = driver.find_element_by_xpath(phone_path)
phone_input.send_keys("+79263296018")

time.sleep(2)

send_path = '/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-new-conversation-container/div/mw-contact-selector-button/button'
start_send = driver.find_element(by=By.XPATH, value=send_path)
start_send.click()

time.sleep(4)


# Находим и заполняем текст сообщения
text_path = '/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-conversation-container/div/div[1]/div/mws-message-compose/div/div[2]/div/mws-autosize-textarea/textarea'
text = driver.find_element(by=By.XPATH, value=text_path)
text.send_keys("Hello, this is a test message")

time.sleep(15)

# Находим и нажимаем кнопку "SMS"
sms_but_path = '/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-conversation-container/div/div[1]/div/mws-message-compose/div/mws-message-send-button/div/mw-message-send-button/button'
sms_but = driver.find_element(by=By.XPATH, value=sms_but_path)
sms_but.click()
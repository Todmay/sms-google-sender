from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time

###### некоторые настройки #######

base_delay = 1

###### некоторые настройки #######

def browser_open():

# Инициализируем драйвер
# путь указывается только в случаях когда драйвер не установлен или не включен по умолчанию, указывается пусть в скобка веб драйвера
# пример пути если драйвер находится в каталоге скрипта
# path = '.\chromedriver_win32'
# сейчас на случай отсутствия драйвера он принудительно устанавливается при первом запуске

    driver = webdriver.Chrome(ChromeDriverManager().install())

# Открываем нужную вкладку
    driver.get("https://messages.google.com/web/")

    return driver

def new_sms_start(driver):

# Находим и нажимаем кнопку "Начать чат"
# если не находит кнопку, то ждем еще немного и повторяем, рекурсия
    try:
    	# Кликаем на переход к отправке
        start_menu = driver.find_element(By.CLASS_NAME, "start-chat")
        start_chat_btn = start_menu.find_element(By.CLASS_NAME, "mat-mdc-button")
        start_chat_btn.click()
    except:    
    	print('Кнопка "Начать чат" недоступна, проводились дейстивия в браузере или штрихкод не отсканирован')
    	time.sleep(base_delay*2)
    	new_sms_start(driver)

    return None

def btn_send_click(driver):
# если не находит кнопку, то ждем еще немного и повторяем, рекурсия
    try:
    	# Кликаем на переход к отправке
        send_path = '/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-new-conversation-container/div/mw-contact-selector-button/button'
        start_send = driver.find_element(by=By.XPATH, value=send_path)
        start_send.click()
    except:    
    	print('Кнопка отправки не прогрузилась')
    	time.sleep(base_delay*2)
    	btn_send_click(driver)

    return None

def text_pull(driver, sms_text):
# если окно заполнения текста не успело повиться, ждем немного и повторяем, РЕКУРСИЯ
    try:
# Находим и заполняем текст сообщения
        text_path = '/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-conversation-container/div/div[1]/div/mws-message-compose/div/div[2]/div/mws-autosize-textarea/textarea'
        text = driver.find_element(by=By.XPATH, value=text_path)
        text.send_keys(sms_text)
    except:    
    	print('Кнопка отправки не прогрузилась')
    	time.sleep(base_delay*2)
    	text_pull(driver, sms_text)

    return None


def sms_send(driver, phone_num = "+79263296018", sms_text = "Hello, this is a test message"):
# Находим и заполняем номер телефона
    phone_path = '/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-new-conversation-container/mw-new-conversation-sub-header/div/div[2]/mw-contact-chips-input/div/mat-chip-listbox/span/input'
    phone_input = driver.find_element(by=By.XPATH, value=phone_path)
    phone_input.send_keys(phone_num)

# без задержки кнопка отправить не успевает появиться
    time.sleep(base_delay*2)

# Кликаем на переход к отправке
    btn_send_click(driver)

# Находим и заполняем текст сообщения
    text_pull(driver, sms_text)

# Находим и нажимаем кнопку "SMS"
    sms_but_path = '/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-conversation-container/div/div[1]/div/mws-message-compose/div/mws-message-send-button/div/mw-message-send-button/button'
    sms_but = driver.find_element(by=By.XPATH, value=sms_but_path)
    sms_but.click()

    return None


##### рабочий код начинается отсюда ######

driver = browser_open()
new_sms_start(driver)
sms_send(driver)

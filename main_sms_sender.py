from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

import time

#### файл прокет в каталоге
from file_input_parser import main_parser

###### некоторые настройки #######

base_delay = 1

###### используемые xpath
### кнопка отправить после введения номера
send_path = '/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-new-conversation-container/div/mw-contact-selector-button/button'
### расположение окошка с вводом смс
text_path = '/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-conversation-container/div/div[1]/div/mws-message-compose/div/div[2]/div/mws-autosize-textarea/textarea'
### кнопка отправить СМС
sms_but_path = '/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-conversation-container/div/div[1]/div/mws-message-compose/div/mws-message-send-button/div/mw-message-send-button/button'


###### некоторые настройки #######

#### параметры для сохранения сессии, сессию храним в файле
SELENIUM_SESSION_FILE = './selenium_session'
SELENIUM_PORT=5015


###### билдим драйвер так чтобы сохранялась сессия
def build_driver():
    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument("--enable-file-cookies")

# если ранее билдер запустил браузер, то начинаем работать в нём, иначе иф пропускает и создаем новый

    try: 
        if os.path.isfile(SELENIUM_SESSION_FILE):
            session_file = open(SELENIUM_SESSION_FILE)
            session_info = session_file.readlines()
            session_file.close()
            executor_url = session_info[0].strip()
            session_id = session_info[1].strip()
            capabilities = options.to_capabilities()
            driver = webdriver.Remote(command_executor=executor_url, desired_capabilities=capabilities)
        # предотвращение кучи пустых окон, но если окно закрывается то раскомментить
            driver.close()
            driver.quit() 

        #добавляем сессию из файла к драйверу
            driver.session_id = session_id
            return driver
    except:
        print('Файл настройки есть, но по указанной сессии нет доступа к браузеру, вероятно он не запущен, перезапустите билдер')
        print('Стартуем новую сессию')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options, port=SELENIUM_PORT)

    session_file = open(SELENIUM_SESSION_FILE, 'a+')
    session_file.writelines([
        driver.command_executor._url,
        "\n",
        driver.session_id,
        "\n",
    ])
    session_file.close()

    return driver

def browser_open():

# Инициализируем драйвер
# путь указывается только в случаях когда драйвер не установлен или не включен по умолчанию, указывается пусть в скобка веб драйвера
# пример пути если драйвер находится в каталоге скрипта
# path = '.\chromedriver_win32'
# сейчас на случай отсутствия драйвера он принудительно устанавливается при первом запуске

    driver = build_driver()
#    driver = webdriver.Chrome(ChromeDriverManager().install())

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
        start_send = driver.find_element(by=By.XPATH, value=send_path)
        start_send.click()
    except:    
    	print('Кнопка отправки не прогрузилась')
    	time.sleep(base_delay*2)
# если кнопки уже нет, а окно отправки уже открылось, то надо выйти из рекурсии
    	if (driver.find_elements_by_xpath(text_path)):
    		return None
    	else:
    		btn_send_click(driver)

    return None

def text_pull(driver, sms_text):
# если окно заполнения текста не успело повиться, ждем немного и повторяем, РЕКУРСИЯ
    try:
# Находим и заполняем текст сообщения
        text = driver.find_element(by=By.XPATH, value=text_path)
        text.send_keys(sms_text)
    except:    
    	print('Окошко для текста смс не прогрузилась')
    	time.sleep(base_delay*2)
    	text_pull(driver, sms_text)

    return None

def send_sms_click(driver):
# если кнопка не нажалась, то не знаем даже что делать
    try:
# Находим и заполняем текст сообщения
        sms_but = driver.find_element(by=By.XPATH, value=sms_but_path)
        sms_but.click()

    except:    
    	print('Беда с кнопкой отправки СМС')
    	time.sleep(base_delay*2)
# Сначала хотел тут рекурсию вставить, но оно и так работает

    return None


def sms_send(driver, phone_num, sms_text = "Hello, this is a test message"):
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
    send_sms_click(driver)

    return None
# Логирование и защита от повторной отправки
def logs_check(phone_num):
    # Создаем файл если его нет файл для записи
    log = open('logs.txt', 'a+')
    log.close()
    # Читаем весь файл
    log = open('logs.txt', 'r')
    data = log.read()
    log.close()
    is_not_send = True
    if phone_num not in data:
        log = open('logs.txt', 'w')
        log.write(phone_num)
        log.close()
    else:
        is_not_send = False
        print('Попытка повторной отправки на номер ' + phone_num)
    # Закрываем файл
    
    return is_not_send

##### рабочий код начинается отсюда ######

driver = browser_open()

df = main_parser()

for row in df.itertuples():
    if len(row[1]) > 9 and row[1][0] == '+' and len(row[2]) > 3:
        if logs_check(row[1]):    
            new_sms_start(driver)
            sms_send(driver, row[1], row[2])
    else:
        print(f'Номер телефона {row[1]} некорректный или сообщение пустое - {row[2]}')
    time.sleep(base_delay*10)

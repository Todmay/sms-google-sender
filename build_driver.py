
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os


#### параметры для сохранения сессии, сессию храним в файле
SELENIUM_SESSION_FILE = './selenium_session'
SELENIUM_PORT=5015

# функция открывает сессию в имеющемся окне драйвера
def add_to_driver():
    session_file = open(SELENIUM_SESSION_FILE)
    session_info = session_file.readlines()
    session_file.close()
    executor_url = session_info[0].strip()
    session_id = session_info[1].strip()
    capabilities = options.to_capabilities()
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities=capabilities)
    # предотвращение кучи пустых окон, но если окно закрывается то раскомментить
    #driver.close()
    #driver.quit() 
    #добавляем сессию из файла к драйверу
    driver.session_id = session_id
    return driver

def build_driver():
    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument("--enable-file-cookies")

# проверяем наличие файла сессии от предыдущих запусков, если он есть удаляем его
    if os.path.isfile(SELENIUM_SESSION_FILE):
# если в рамках дой сессии делаем несколько билдеров то запускать функцией ниже, при отдельном скрипте тут чистим файл
#    	driver = add_to_driver()
#        return driver


        os.remove(SELENIUM_SESSION_FILE)

    
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


#driver = build_driver()
driver = webdriver.Chrome(ChromeDriverManager().install())

# Открываем нужную вкладку авторизации, проходим её один раз
driver.get("https://messages.google.com/web/")

# цикл нужен при запуске не через консоль, иначе и так работает
#while True:
#   continue

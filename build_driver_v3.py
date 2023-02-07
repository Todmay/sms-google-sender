
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os


#### параметры для сохранения сессии, сессию храним в файле
SELENIUM_SESSION_FILE = './selenium_session'

def build_driver():
    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument("--enable-file-cookies")

# проверяем наличие файла сессии от предыдущих запусков, если он есть удаляем его
    if os.path.isfile(SELENIUM_SESSION_FILE):
        os.remove(SELENIUM_SESSION_FILE)

    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    session_file = open(SELENIUM_SESSION_FILE, 'a+')
    session_file.writelines([
        driver.command_executor._url,
        "\n",
        driver.session_id,
        "\n",
    ])
    session_file.close()

    return driver


driver = build_driver()

# Открываем нужную вкладку авторизации, проходим её один раз
driver.get("https://messages.google.com/web/")

# цикл нужен при запуске не через консоль, иначе и так работает
while True:
   continue

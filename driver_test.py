from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time

options = Options()
options.add_argument("--disable-infobars")
options.add_argument("--enable-file-cookies")

try: 
    driver1 = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver1.get("https://ya.ru/")
    print("первый драйвер открыт")
    print(driver1.session_id)
except:
    print("первый драйвер не работает")

time.sleep(2)
try: 
    driver2 = webdriver.Chrome(ChromeDriverManager().install())
    driver2.get("https://google.com/")
    print("второй драйвер открыт")
    print(driver2.session_id)
except:
    print("второй драйвер не работает")

time.sleep(2)
try: 
    driver3 = webdriver.Chrome()
    driver3.get("https://vk.com/")
    print("третий драйвер открыт")
    print(driver3.session_id)
except:
    print("третий драйвер не работает")

time.sleep(2)
try: 
    driver4 = webdriver.Chrome(options=options)
    driver4.get("https://github.com/")
    print("четвертый драйвер открыт")
    print(driver4.session_id)
except:
    print("четвертый драйвер не работает")

time.sleep(2)

while True:
   continue


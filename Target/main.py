from main_60139 import scrapper_60139
from main_60177 import scrapper_60177
from main_60430 import scrapper_60430
from main_60603 import scrapper_60603
from main_60630 import scrapper_60630
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
import concurrent.futures
import secrets
import urllib3
import random
import re

proxy_data = []
# url = "https://thesocialproxy.com/wp-json/lmfwc/v2/licenses/customer/user-licenses/?consumer_key=ck_bbb039af52f3d81ba36131ac924daf057232708f&consumer_secret=cs_0a7455b440391f80039fa715420095aedf7cb930&page=1&proxy_format={USERNAME:PASSWORD@HOST:PORT}"
 
# payload = {}
# headers = {
#     'Content-Type': 'application/json'
# }
 
# response = requests.request("GET", url, headers=headers, data=payload).json()
# for po in response['data']:
#     proxy_data.append(po['licenseKey'].replace('{', '').replace('}', '').strip())
 
coo = {
    # 'TealeafAkaSid': '_BQ57vSnTWetihQK4TQNdHOsQ4SxCJfY',
    'visitorId': '018B480FDCC1020182CE06752C5DEF66',
    # 'sapphire': '1',
    # '_gcl_au': '1.1.979185579.1697721173',
    # 'crl8.fpcuid': 'b606ef6d-7f89-4511-8f42-f850d9dfde6b',
    # 'UserLocation': '60430|41.55542439949306|-87.66399297449533|IL|US',
    # 'fiatsCookie': 'DSI_1460|DSN_Homewood|DSZ_60430',
    # 'sddStore': 'DSI_1460|DSN_Homewood|DSZ_60430',
    # 'ci_pixmgr': 'other',
    # 'egsSessionId': '741bb6e1-fdbf-416f-ac63-938846de7a51',
    'accessToken': 'eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI4ZmJmY2Q1Yy0xMTAyLTRjMGEtYjhiNC02NzNhOGNjZjJiMzciLCJpc3MiOiJNSTYiLCJleHAiOjE3MDE0MjU5MDIsImlhdCI6MTcwMTMzOTUwMiwianRpIjoiVEdULjc2MGIwNGQ5ZWJkMjQ1ZWZhOWM1ZTdmNDRiNmY5ZjYwLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImEwMjdmNWZhYTQ2NDgwMjRhOWJiZDIzYjY3YjFiMTRmYjgzZmIwMTY3Y2JlYTI1YjJiZGExYjc2NzJlYWNmMjEiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.gEL0bCKsH_lBvrdxV0ycqdVDlXenG1awqzx6dTSgUpK8tL7zVhRmI5JzTVBQc041dz_okXkRXEJCwtueMmAsPn776lumuGuh-1HjKswfNu11GCn9C5iL3I0YUWEqw2x9X4U7ZhMBoTPFQP-7IMISlcOOQIiKprvqwgpBbW6-qzRiEU5xrsY1k1MUhKTPO6p26139pzQgyhJ7HAm_0X_q8PhLoOzgAZ921FZFqQv8TNKhXjGCvFF6v2DbZQwPJRm4kieQwZDizSMqYgnYn5CFNwHl8o9CBX_l58DgKEUIZglQR6rIrTL2AwH1GyYcXnKvBwBfaJX3R8zs50XZtgAGVg',
    'idToken': 'eyJhbGciOiJub25lIn0.eyJzdWIiOiI4ZmJmY2Q1Yy0xMTAyLTRjMGEtYjhiNC02NzNhOGNjZjJiMzciLCJpc3MiOiJNSTYiLCJleHAiOjE3MDE0MjU5MDIsImlhdCI6MTcwMTMzOTUwMiwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.',
    # 'refreshToken': 'qJBCfB1afQ_xQTjf0G7cV9SmS9ft_AUQC_Daq7m-1n9BeZjDKpWq1m958EBJh9IDlrVIVreologv-IcwTgrGJA',
    # '__gads': 'ID=04521ce72c22e032:T=1697721085:RT=1701339503:S=ALNI_Mb_eM0GqRVI4YbevUQiLLIOHMGCFw',
    # '__gpi': 'UID=00000d9af0ee6fb1:T=1697721085:RT=1701339503:S=ALNI_Mb8focbaFTYFdc-33NL0iYm9ZxusA',
    # 'ffsession': '{%22sessionHash%22:%22aa1bac48dc9831701169204050%22%2C%22prevPageName%22:%22grocery:%20frozen%20foods:%20frozen%20breakfast%20food%22%2C%22prevPageType%22:%22level%203%22%2C%22prevPageUrl%22:%22https://www.target.com/c/frozen-breakfast-food-foods-grocery/-/N-5xsza%22%2C%22sessionHit%22:10%2C%22prevSearchTerm%22:%22non-search%22}',
    # '_mitata': 'ZGMwNTJiMzhiNWMyMWE5N2UxZjgwNzMzYzYxNGRlOTZjZjNlNGFiMjcwMzc2MzIwODU0ZDAzZDI4MzJiYjQzOQ==_/@#/1701339917_/@#/czrmMynYzv6QyCM3_/@#/ZDYxODRiYjhiYjdmMzEyMjhmNzVhMjBlZWFjNDAyZDJhZDlhOTNlYzY4Yzc1MGJiOTMxOTU4N2JkZTIwZTUyNA==_/@#/000',
}

 
# def pro():
#     # # Create a list of tuples from the data
#     # proxies = [tuple(proxy.split(':')) for proxy in proxy_data]
#     # Randomly select a proxy from the list
#     proxy_url = random.choice(proxy_li)
#     # Set up the proxy dictionary
#     proxy = {
#         'http': f'http://{proxy_url}',
#         'https': f'http://{proxy_url}',
#     }
#     return proxy

# proxy_data = [
#         'v8He8wy:CgDBOod7kP1tq50@lt.4g.iproyal.com:6077',
#         'jyothish_1822:e9700d-ec46f9-6317aa-e45cc5-34e1ac@residential.proxyomega.com:10000',
#         'jyothish_1822:e9700d-ec46f9-6317aa-e45cc5-34e1ac@residential.proxyomega.com:10001',
#         'jyothish_1822:e9700d-ec46f9-6317aa-e45cc5-34e1ac@residential.proxyomega.com:10002',
#         'jyothish_1822:e9700d-ec46f9-6317aa-e45cc5-34e1ac@residential.proxyomega.com:10003',
#         'jyothish_1822:e9700d-ec46f9-6317aa-e45cc5-34e1ac@residential.proxyomega.com:10004',
        
#     ]

def cat_links():
    dataset = []
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()))
    driver.get('https://www.target.com/c/grocery/-/N-5xt1a')
    # input(f'Change pincode to {pincode} and press enter: ')
    # time.sleep(10)
    # driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div/div[1]/div[1]/button/div/span').click()
    # time.sleep(5)
    # driver.find_element(By.XPATH,'/html/body/div[4]/div/div/div[2]/div/div[1]/div/div[1]/div/input').clear()
    # time.sleep(5)
    # driver.find_element(By.ID,'zip-code').send_keys(str(pincode))
    # time.sleep(5)
    # driver.find_element(By.XPATH,'/html/body/div[4]/div/div/div[2]/div/div[2]/button').click()
    # time.sleep(5)
    try:
        driver.find_element(
            By.XPATH, '/html/body/div[1]/div[2]/main/div/div[1]/div/div[2]/div/div/button').click()
    except:
        pass
    time.sleep(5)
    s = BeautifulSoup(driver.page_source, "html.parser")
    links = s.select_one(
        ".h-flex-direction-row.h-display-flex.h-flex-wrap.h-flex-justify-center").find_all("li")[1:]
    for i in links:
        driver.get("https://www.target.com" + i.find("a")["href"])
        try:
            time.sleep(5)
            driver.find_element(
                By.XPATH, '//*[@id="pageBodyContainer"]/div/div[1]/div/div[2]/div/div/button').click()
            time.sleep(3)
        except:
            pass
        s1 = BeautifulSoup(driver.page_source, "html.parser")
        try:
            gl = s1.find("ul").find_all("li")
        except:
            gl = []
        for q in gl:
            try:
                link = q.find("a")["href"]
            except:
                link = None
            if link:
                dataset.append([i.text, q.text, link])
    df = pd.DataFrame(dataset)
    df.to_excel(f"category_links_target.xlsx")
    driver.quit()

import threading
def main_scrapper_with_threads(proxy_data):
    # Create threads for each scrapper function
    thread_60630 = threading.Thread(target=scrapper_60630, args=(proxy_data,))
    thread_60139 = threading.Thread(target=scrapper_60139, args=(proxy_data,))
    thread_60177 = threading.Thread(target=scrapper_60177, args=(proxy_data,))
    thread_60603 = threading.Thread(target=scrapper_60603, args=(proxy_data,))
    thread_60430 = threading.Thread(target=scrapper_60430, args=(proxy_data,))

    # Start all threads
    thread_60630.start()
    thread_60177.start()

    # Wait for all threads to finish
    thread_60630.join()
    thread_60177.join()

    # thread_60139.start()
    # thread_60603.start()
    
    # thread_60139.join()
    # thread_60603.join()
    
    thread_60430.start()
    thread_60430.join()
# Call the main_scrapper_with_threads function
# cat_links()
main_scrapper_with_threads(proxy_data)
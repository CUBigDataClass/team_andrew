from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

collections =[]
driver = webdriver.Chrome("/opt/homebrew/bin/chromedriver")


def get_collection_names(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # table_dune = soup.find_all('table', class_='table_table__fuS_N')
    t_body = soup.find('tbody')
    for i in t_body:
        collections.append(str(i.text))
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="tabs--1--panel--0"]/div/ul/li[6]/button').click()
    if len(collections) < 8250:
        get_collection_names(driver)
    else:
        return collections


try:
    driver.get("https://dune.xyz/queries/357818")
    time.sleep(10)
    get_collection_names(driver)
    df = pd.DataFrame(collections, columns=['Collections'])
    df.to_csv("Opensea_collections.csv",index=False)
except:
    print("do it again")
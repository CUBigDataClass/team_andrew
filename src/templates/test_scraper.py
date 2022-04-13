import bs4
import requests
import selenium
from selenium import webdriver
from pymongo import MongoClient
import traceback
import os
import time
from selenium.webdriver.common.by import By


def imageScrapping():
    '''
    Install selenium and chromedriver (make sure chromedriver matches your version of chrome)
    '''
    # download chromedriver and place it somewhere
    option = webdriver.ChromeOptions()
    # Prevent some useless logs
    # option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    option.add_argument('--no-sandbox')
    option.add_argument('--headless')
    option.add_argument("start-maximized")
    option.add_argument("--window-size=1920,1080")
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--disable-gpu')
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=1920x1080")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")


    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=option)
    try:
        # Open the website
        driver.get('https://images.google.com/')
        # Find cam button
        cam_button = driver.find_elements(by=By.XPATH, value="//div[@aria-label=\"Search by image\" and @role=\"button\"]")[0]
        cam_button.click()

        # Find upload tab
        upload_tab = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Upload an image')]")[0]
        upload_tab.click()
        # Find image input
        upload_btn = driver.find_elements(by=By.NAME, value='encoded_image')[0]
        #Using the image that user uploaded which saved in "temp.jpg" from app.py
        upload_btn.send_keys(os.getcwd()+"/images/temp.jpg")
        # Click on "visually similar images"
        driver.find_elements(by=By.XPATH, value="""//*[@id="rso"]/div[2]/div/div[2]/g-section-with-header/div[1]/title-with-lhs-icon/a/div[2]/h3""")[0].click()
        time.sleep(2)
    except Exception as e:
        print(e)
    # If we want to search by term
    # search_URL = "https://www.google.com/search?q=cute+puppies&source=lnms&tbm=isch"
    # driver.get(search_URL)
    num_images = 5
    # scroll down until we have enough images
    while True:
        page_html = driver.page_source
        pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
        # containers = pageSoup.findAll('div', {'class': "isv-r PNCib MSM1fd BUooTd"})
        containers = pageSoup.findAll('div', {'class': "c7cjWc"}) #had to change class to get docker to work
        driver.execute_script("window.scrollBy(0,1000);")
        len_containers = len(containers)
        # once we have enough containers to scrape the # of images we want
        if len_containers > num_images:
            break
    # scrolling all the way up
    driver.execute_script("window.scrollTo(0,0);")
    print("found %s image containers"%(len(containers)))

    #create list of imageurl to use in app.py and html
    image_list = []

    for i in range(1,num_images + 1):
        # in google images every 25th images is 'related images', this will break if we click this
        if i % 25 == 0:
            continue
        xpath = """//*[@id="islrg"]/div[1]/div[%s]"""%(i)
        image_website_xpath = """//*[@id="islrg"]/div[1]/div[%s]/a[2]"""%(i)
        preview_image_xpath = """//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img"""%(i)
        image_website_element = driver.find_elements(by=By.XPATH, value=image_website_xpath)[0]
        preview_image_element = driver.find_elements(by=By.XPATH, value=preview_image_xpath)[0]
        preview_image_url = preview_image_element.get_attribute("src")
        driver.find_elements(by=By.XPATH, value=xpath)[0].click()
        timeStarted = time.time()
        while True:
            image_element1 = driver.find_elements(by=By.XPATH, value="""//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img""")[0]
            # gather image URL
            imageURL = image_element1.get_attribute("src")
            image_description = image_element1.get_attribute("alt")
            image_website = image_website_element.get_attribute("href")
            i= i+1
            # if the new high-res image has loaded
            if imageURL != preview_image_url:
                break
            # if we have not loaded the high res images in x seconds, break
            if time.time() - timeStarted > 3:
                break
        #MongoDB with PyMongo to insert Database directly
        my_client = MongoClient("mongodb+srv://team_andrew:Green@cluster1.jsqyd.mongodb.net/ImageSearch")
        db = my_client.ImageSearch #connect to "ImageSearch" Database
        collection = db.get_collection("ImageData") #connect to "ImageData" Collection
        image_element = {"imageLink": imageURL,"description": image_description,"websiteLink":image_website, "previewImageURL:":preview_image_url} #Create Element
        data = [image_element]
        result = collection.insert_many(data) #insert the saved data into the collection

        #append each imageURL
        image_list.append(imageURL)

        # print("image description:", image_description)
        # print("image URL", imageURL)
        # print("image website:", image_website)
    return image_list
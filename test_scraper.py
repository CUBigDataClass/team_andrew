import bs4
import requests
from pymongo import MongoClient
from selenium import webdriver
import os
import time
'''
Install selenium and chromedriver (make sure chromedriver matches your version of chrome)
'''

# download chromedriver and place it somewhere
chromeDriverPath = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chromeDriverPath)


try:
    # Open the website
    driver.get('https://images.google.com/')

    # Find cam button
    cam_button = driver.find_elements_by_xpath("//div[@aria-label=\"Search by image\" and @role=\"button\"]")[0]
    cam_button.click()

    # Find upload tab
    upload_tab = driver.find_elements_by_xpath("//*[contains(text(), 'Upload an image')]")[0]
    upload_tab.click()

    # Find image input
    upload_btn = driver.find_element_by_name('encoded_image')
    upload_btn.send_keys(os.getcwd()+"/test_image.jpg")

    # Click on "visually similar images"
    driver.find_element_by_xpath("""//*[@id="rso"]/div[2]/div/div[2]/g-section-with-header/div[1]/title-with-lhs-icon/a/div[2]/h3""").click()

    time.sleep(1)

except Exception as e:
    print(e)

# create folder to save images
image_path = "/Users/drewbeathard/Documents/big_data_files/image_scrape_testing"
if not os.path.isdir(image_path):
    os.mkdir(image_path)

# If we want to search by term
# search_URL = "https://www.google.com/search?q=cute+puppies&source=lnms&tbm=isch"
# driver.get(search_URL)

num_images = 20


# scroll down until we have enough images
while True:
    page_html = driver.page_source
    pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
    containers = pageSoup.findAll('div', {'class': "isv-r PNCib MSM1fd BUooTd"})
    driver.execute_script("window.scrollBy(0,1000);")
    len_containers = len(containers)
    # once we have enough containers to scrape the # of images we want
    if len_containers > num_images:
        break

# scrolling all the way up
driver.execute_script("window.scrollTo(0,0);")


print("found %s image containers"%(len(containers)))


for i in range(1,num_images + 1):
    # in google images every 25th images is 'related images', this will break if we click this
    if i % 25 == 0:
        continue

    xpath = """//*[@id="islrg"]/div[1]/div[%s]"""%(i)
    image_website_xpath = """//*[@id="islrg"]/div[1]/div[%s]/a[2]"""%(i)
    preview_image_xpath = """//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img"""%(i)


    image_website_element = driver.find_element_by_xpath(image_website_xpath)
    preview_image_element = driver.find_element_by_xpath(preview_image_xpath)
    preview_image_url = preview_image_element.get_attribute("src")

    driver.find_element_by_xpath(xpath).click()

    timeStarted = time.time()
    while True:
        image_element = driver.find_element_by_xpath("""//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img""")
        # gather image URL
        imageURL = image_element.get_attribute("src")
        image_description = image_element.get_attribute("alt")
        image_website = image_website_element.get_attribute("href")
        # if the new high-res image has loaded
        if imageURL != preview_image_url:
            break

        # if we have not loaded the high res images in x seconds, break
        if time.time() - timeStarted > 3:
            break
    #MongoDB with PyMongo to insert Database directly
    my_client = MongoClient("mongodb+srv://team_andrew:Green91%40%40@cluster1.jsqyd.mongodb.net/test")
    db = my_client.ImageSearch #connect to "ImageSearch" Database
    collection = db.get_collection("ImageData") #connect to "ImageData" Collection
    image_element = {"imageLink": imageURL,"description": image_description,"websiteLink":image_website} #Create Element
    data = [image_element]
    result = collection.insert_many(data) #insert the saved data into the collection

    print("image description:", image_description)
    print("image URL", imageURL)
    print("image website:", image_website)




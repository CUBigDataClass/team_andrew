import bs4
import requests
from selenium import webdriver
import os
import time
'''
Install selenium and chromedriver (make sure chromedriver matches your version of chrome)
'''


def download_image(url, folder_name, num):
    # write image to file
    response = requests.get(url)
    if response.status_code==200:
        with open(os.path.join(folder_name, str(num)+".jpg"),'wb') as file:
            file.write(response.content)

# download chromedriver and place it somewhere
chromeDriverPath = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chromeDriverPath)

# create folder to save images
image_path = "/Users/drewbeathard/Documents/big_data_files/image_scrape_testing"
if not os.path.isdir(image_path):
    os.mkdir(image_path)

search_URL = "https://www.google.com/search?q=cute+puppies&source=lnms&tbm=isch"
driver.get(search_URL)

num_images = 60


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

    preview_image_xpath = """//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img"""%(i)
    preview_image_element = driver.find_element_by_xpath(preview_image_xpath)
    preview_image_url = preview_image_element.get_attribute("src")    

    driver.find_element_by_xpath(xpath).click()

    timeStarted = time.time()
    while True:
        image_element = driver.find_element_by_xpath("""//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img""")
        imageURL = image_element.get_attribute("src")
        
        # if the new high-res image has loaded
        if imageURL != preview_image_url:
            break

        # if we have not loaded the high res images in x seconds, break
        if time.time() - timeStarted > 7:
            break

    try:
        download_image(imageURL, image_path, i) 
        print("Downloaded element %s out of %s total. URL: %s" % (i, num_images, imageURL))
    except:
            print("Couldn't download an image %s, continuing downloading the next one"%(i))
from urllib.request import urlretrieve
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import sys
import json

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100): 
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

if "settings.json" not in os.listdir():
    print("CANNOT FIND SETTING FILE: 'settings.json'")
    sys.exit(0)

with open("settings.json", "r") as jsonFile:
    settings = json.load(jsonFile)

# load setting file
number_of_files = settings["number_of_files"]
class_id = settings["class_id"]
items = settings["items"]

# chrome driver settings
option = Options()
option.add_argument('--headless')
driver = webdriver.Chrome(options=option)

for item in items:

    print("LOADING URL ...")

    url='https://www.google.com/search?tbm=isch&sxsrf=ALeKk023f2FKJ8_\
        dfvIYfZtSbQdXb-dZpw%3A1592214626728&source=hp&biw=2495&bih=935\
        &ei=YkTnXtW6KoPN-QakvayYBw&q={}&oq=&gs_lcp=CgNpbWcQAxgAMgcIIxDq\
        AhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAn\
        MgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnUABYAGD9FWgBcAB4\
        AIABAIgBAJIBAJgBAKoBC2d3cy13aXotaW1nsAEK&sclient=img'.format(quote_plus(item))

    driver.get(url)

    print("URL LOADED")

    for _ in range(500):
        driver.execute_script("window.scrollBy(0,10000)")

    html = driver.page_source
    soup = BeautifulSoup(html)

    img = soup.select('.rg_i.Q4LuWd')
    imgurl=[]

    for i in img:
        try:
            imgurl.append(i.attrs['src'])
        except KeyError:
            imgurl.append(i.attrs['data-src'])

    dirlist = os.listdir()
    if "crawlled_images" not in dirlist:
        os.mkdir("crawlled_images/")

    if str(settings["items"][item]) not in os.listdir("crawlled_images/"):
        os.mkdir("crawlled_images/"+str(settings["items"][item]))

    print("Downloading {}".format(item))

    iteration = 0

    for imageFile in imgurl:
        if iteration >= number_of_files:
            break
        
        savePath = os.path.join("./crawlled_images/"+str(settings["items"][item]), str(iteration)+".jpg")
        urlretrieve(imageFile, savePath)
        iteration+=1
        printProgress(iteration, number_of_files, "Downloading:", "Complete", 1, 50)

print("DOWNLOAD COMPLETE")

driver.close()
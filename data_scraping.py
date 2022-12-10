from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def review_scrape(url, StarRating):
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--log-level=3')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    laman_akhir = driver.find_element(By.XPATH, '//*[@id="zeus-root"]/div/main/div[2]/div[1]/div[2]/section/div[3]/nav/ul/li[10]/button').text
    data = {'reviews':[], 'star':[]}

    for i in range(int(laman_akhir)-1):
        soup = BeautifulSoup(driver.page_source, "html.parser")

        for item in soup.findAll('div', {'class':'css-1k41fl7'}):
            if item.find('div', {'aria-label':f"bintang {StarRating}"}):
                bintang = item.find('div', {'aria-label':f"bintang {StarRating}"}).attrs
                bintang = bintang['aria-label']
                bintang = bintang[-1]
            
                if item.find('span', {"data-testid":"lblItemUlasan"}) != None:
                    review = item.find('span', {"data-testid":"lblItemUlasan"}).text
                    data['reviews'].append(review)
                    data['star'].append(bintang)
                    
                else:
                    continue
                    
        


        driver.find_element(By.XPATH, '//*[@id="zeus-root"]/div/main/div[2]/div[1]/div[2]/section/div[3]/nav/ul/li[11]/button').click()
        time.sleep(.5)
    driver.close()

    data = pd.DataFrame(data)
    data.to_csv('data/data.csv')

    return None

# review_scrape('https://www.tokopedia.com/tvchanghongstore/changhong-40-inch-newest-android-11-smart-tv-digital-led-tv-fhd-l40g7n/review', '5')
# review_scrape('https://www.tokopedia.com/azarinecosmetics/azarine-toner-90ml-beginner-exfo/review', '5')






import re
#scraping
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


chrome_options = Options()
chrome_options.add_argument("--start-maximized")
#chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("detach",True)
def find_coups(driver):
    time.sleep(3)
    ## coups jouer
    reel_coups=[]
    coups=driver.find_elements(By.CSS_SELECTOR, "#live-game-tab-scroll-container > wc-mode-swap-move-list > wc-simple-move-list > div > div")
    for i,coup in enumerate(coups):
        coupdiv=coup.text.split("\n")
        if len(coupdiv)==3:
            reel_coups.append(coupdiv[1])
            reel_coups.append(coupdiv[2])
    driver.quit()
    return reel_coups

def find_party(name,number=1):
    driver=webdriver.Chrome( options=chrome_options)
    driver.get("https://www.chess.com/member/"+name)
    time.sleep(2.5)
    elem=driver.find_element(By.CSS_SELECTOR, "#profile-main > div.archive-component > div > div > table > tbody > tr:nth-child("+str(number)+")")
    #elem=driver.find_element(By.CSS_SELECTOR, "#view-profile > div.cc-section-clear > div.v5-section.v5-overflow-hidden > div > table > tbody > tr:nth-child("+str(number)+")")
    elem.location_once_scrolled_into_view
    white=elem.find_element(By.CSS_SELECTOR,"#profile-main > div.archive-component > div > div > table > tbody > tr:nth-child("+str(number)+") > td.archived-games-user-cell > div > div > div:nth-child(1)").text
    print("avava",white)
    black=elem.find_element(By.CSS_SELECTOR,"#profile-main > div.archive-component > div > div > table > tbody > tr:nth-child("+str(number)+") > td.archived-games-user-cell > div > div > div:nth-child(2)").text
    print("avava",black)
    href=elem.find_element(By.CSS_SELECTOR,"#profile-main > div.archive-component > div > div > table > tbody > tr:nth-child("+str(number)+") > td.archived-games-user-cell > a").get_attribute("href")
    # go to href
    driver.get(href)
    time.sleep(2.5)
    
    return find_coups(driver), white, black

if __name__=="__main__":
    print(find_party("frouty6"))
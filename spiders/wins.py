# IMPORT REQUIRED MODULES
import time
from random import uniform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Modules for transport to database
from items import Win 
from pipelines import WinPipeline


################
# START DRIVER #
################

# INITIALISE DRIVER
def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver,5*uniform(0,1))
    return driver 


##################
# DRIVER ACTIONS #
##################

# LOAD WEBSITE
def open_url(driver):
    driver.get("https://www.oddschecker.com/football/germany/bundesliga")

    # GET RID OF ADD THAT POPS UP
    try:
        try:
            button = driver.wait.until(EC.presence_of_element_located((By.XPATH,'html/body/div[4]/div[1]/div/span[@title="Close"]')))
        except:
            button = driver.wait.until(EC.presence_of_element_located((By.XPATH,'html/body/div[5]/div[1]/div/span[@title="Close"]')))
        button.click()
    except:
        pass

# RETRIEVE ITEMS
def retrieve_teams(driver):
    count = 1
    # game container
    game_table = driver.find_element_by_xpath('//*[@id="fixtures"]/div/table/tbody')

    # Loop through games
    for game in game_table.find_elements_by_xpath('.//tr[@class="match-on "]'):
        # Get team names
        item['home_team'] = game.find_element_by_xpath('.//td[2]/p/span[1]').get_attribute('data-name')
        time.sleep(0.5 * uniform(0,1))
        item['away_team'] = game.find_element_by_xpath('.//td[4]/p/span[1]').get_attribute('data-name')
        time.sleep(0.5 * uniform(0,1))
        # Get odds
        item['home_odds'] = game.find_element_by_xpath('.//td[2]').get_attribute('data-best-odds')
        time.sleep(0.5 * uniform(0,1))
        item['away_odds'] = game.find_element_by_xpath('.//td[4]').get_attribute('data-best-odds')
        time.sleep(0.5 * uniform(0,1))
        item['draw_odds'] = game.find_element_by_xpath('.//td[3]').get_attribute('data-best-odds')
        time.sleep(2 * uniform(0,1))
        # Add to datebase
        db.process_item(item)
        print('Game {} successfully fetched'.format(count))
        count = count + 1

##############
# RUN SCRIPT #
##############

if __name__ == "__main__":
    # Set up item
    item = Win()
    # Set up table
    db = WinPipeline()
    db.__init__()
    driver = init_driver()
    open_url(driver)
    retrieve_teams(driver)
    time.sleep(5 * uniform(0,1))
    driver.quit()
    print('Successful')

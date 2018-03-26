######################################
### Import Modules                 ###
######################################

import time
import datetime
import numpy as np
from random import uniform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

# Import items class
from items import Halftime

# Modules for proxy
#from browsermobproxy import Server

# Define Class
class HalftimeBrowser():
    
    def __init__(self,country):
        self.country = country

######################################
### Main function                  ###
######################################

    # RETRIEVE ITEMS
    def retrieve_teams(self,driver,database,timestamp):
        count = 1
        # game container
        game_path = '//*[@id="fixtures"]/div/table/tbody//tr[@class="match-on "]'
        game_table = self.wait_pl(driver,game_path) 
        num_options = sum([1 for game in game_table])
        
        # Loop through games
        for i in range(num_options):
            self.reset_driver(driver)
     
            game = self.wait_pl(driver,game_path)[i]

            # Retrieve "ALL ODDS" button
            odds = self.wait(game,'.//td[5]/a')
            
            if self.check_in_play(odds) == 1 and odds is not None:
               
                odds.click()

                # Retrieve Halftime Button if existent
                options_count, code = self.retrieve_options_index(driver) 
                if code == 1:
                    game_info = self.extract_game_info(driver,timestamp) 
                    # ------> HALFTIME ODDS
                    self.wait(driver,'//*[@id="table-tabs-row"]/ul/li[{}]/a'.format(options_count)).click()
                    # Collect odds for the different providers and pass them on to the database
                    self.provider_odds(driver,database,game_info)
                    print('Game {} successfully fetched'.format(count))
                else:
                    print('There is no halftime/fulltime odds for game {} yet'.format(count))
                count = count + 1
            else:
                print('Element not found')
        driver.back()


######################################
### BUILDING BLOCKS                ###
######################################
    """
    # Set browser profile
    def set_profile(self,add_on):
        profile = webdriver.FirefoxProfile()
        profile._install_extension(add_on)
        return profile
    """

    # INITIALISE DRIVER
    def init_driver(self):
        # Start browser
        driver = webdriver.PhantomJS()
        driver.set_window_size(1280,1024)
        WebDriverWait(driver,0.5*uniform(0,1))
        return driver


    # LOAD WEBSITE
    def open_url(self,driver):
        url_stem = "https://www.oddschecker.com/football/"
        if self.country == "germany":
            driver.get(url_stem + "germany/bundesliga")
        elif self.country == "england":
            driver.get(url_stem + "english/premier-league")
        elif self.country == "spain":
            driver.get(url_stem + "spain/la-liga-primera")
        elif self.country == "italy":
            driver.get(url_stem + "italy/serie-a")
        elif self.country == "france":
            driver.get(url_stem + "france/league-1")

    def reset_driver(self,driver):
        url_stem = "https://www.oddschecker.com/football/"
        if self.country == "germany":
            driver.get(url_stem + "germany/bundesliga")
        elif self.country == "england":
            driver.get(url_stem + "english/premier-league")
        elif self.country == "spain":
            driver.get(url_stem + "spain/la-liga-primera")
        elif self.country == "italy":
            driver.get(url_stem + "italy/serie-a")
        elif self.country == "france":
            driver.get(url_stem + "france/league-1")
       
           
        # GET RID OF ADD THAT POPS UP
        try:
            try:
                button = self.wait(driver,'html/body/div[4]/div[1]/div/span[@title="Close"]')
            except:
                button = self.wait(driver,'html/body/div[5]/div[1]/div/span[@title="Close"]')
            button.click()
        except:
            pass


    # This break function runs through the toolbar to check whether halftime/fulltime odds exists/ and find their index
    def retrieve_options_index(self,driver):
        code = 0
        options_count = 1
        for option in self.wait_pl(driver,'//*[@id="table-tabs-row"]/ul/li'):
            if option.text != "Half Time/Full Time":
                options_count = options_count + 1
            elif option.text == "Half Time/Full Time":
                code = 1
                break
        return options_count, code


    # Extract team information
    def extract_game_info(self,driver,timestamp):
        # Messy splitting of team names. 
        teams = self.wait(driver,'//*[@id="betting-odds"]/div/section/div/header/h1').text
        home_team = teams.split(' v ')[0].replace(" ","")
        time.sleep(0.5 * uniform(0,1))
        container = teams.split(' v ')[1]
        away_team = container.split(' Winner')[0].replace(" ","")
        time.sleep(0.5 * uniform(0,1))
	# Messy splitting of date & time
        datetime = self.wait(driver,'//*[@id="betting-odds"]/div/section/div/div/div/div/span').text
        day = datetime.split(' / ')[0]
        clock = datetime.split(' / ')[1]
        # Build identifier variable
        day_ = day.split(' ')[1][:2]
        month = day.split(' ')[2][:3]
        h_team = home_team[:5]
        a_team = away_team[:5]
        identifier = h_team + '_' + a_team + '_' + day_ + '_' + month
        # save the info in list
        game_info = [home_team,away_team,day,clock,identifier,timestamp]
        return game_info
        

    # Extract the data by provider
    def provider_odds(self,driver,database,game_info):
        # Set up index for the different providers
        provider_indices = np.arange(2,31)
        provider_indices = np.delete(provider_indices,25)
        # Loop through each of the odds providers
        for i in provider_indices:
            # Quick nap
            time.sleep(0.5 * uniform(0,1))
            # Only include providers that have odds
            if self.wait(driver,'//*[@id="t1"]/tr[1]/td[{}]'.format(i)).get_attribute('data-odig') != "0":
                item = Halftime()
                item['home_team'] = game_info[0]  
                item['away_team'] = game_info[1]
                item['date'] = game_info[2]
                item['time'] = game_info[3]
                item['identifier'] = game_info[4]
                item['accessed']  = game_info[5]
                item['provider'] = self.wait(driver,'//*[@id="oddsTableContainer"]/table/thead/tr[4]/td[{}]/aside/a'.format(i)).get_attribute('title') 
                item['home_home'] = self.wait(driver,'//*[@id="t1"]/tr[1]/td[{}]'.format(i)).get_attribute('data-odig')  
                item['away_away'] = self.wait(driver,'//*[@id="t1"]/tr[2]/td[{}]'.format(i)).get_attribute('data-odig')
                item['draw_home'] = self.wait(driver,'//*[@id="t1"]/tr[3]/td[{}]'.format(i)).get_attribute('data-odig')
                item['draw_draw'] = self.wait(driver,'//*[@id="t1"]/tr[4]/td[{}]'.format(i)).get_attribute('data-odig')
                item['draw_away'] = self.wait(driver,'//*[@id="t1"]/tr[5]/td[{}]'.format(i)).get_attribute('data-odig')
                item['home_draw'] = self.wait(driver,'//*[@id="t1"]/tr[6]/td[{}]'.format(i)).get_attribute('data-odig')
                item['away_draw'] = self.wait(driver,'//*[@id="t1"]/tr[7]/td[{}]'.format(i)).get_attribute('data-odig')
                item['away_home'] = self.wait(driver,'//*[@id="t1"]/tr[8]/td[{}]'.format(i)).get_attribute('data-odig')
                item['home_away'] = self.wait(driver,'//*[@id="t1"]/tr[9]/td[{}]'.format(i)).get_attribute('data-odig')
                database.process_item(item)
   
    # Check whether game is in play
    def check_in_play(self,odds):
        button = odds.get_attribute('class')
        not_in_play = "button beta-callout btn-1-small"
        if button == not_in_play:
            code = 1
        else:
            code =  0
        return code

    # Wait for element
    def wait(self,driver,xpath):
        return WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,xpath)))

    # wait for handle
    def wait_pl(self,driver,xpath):
        return WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.XPATH,xpath)))

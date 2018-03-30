######################################
### BUILT LOGGER                   ###
######################################

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - [{}] - %(levelname)s : %(message)s'.format(__name__))
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

######################################
### Import Modules                 ###
######################################

import time
from bs4 import BeautifulSoup
import datetime
import numpy as np
from random import uniform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

# Import items class
from backend.items import Halftime

# Modules for proxy
from browsermobproxy import Server


######################################
### Main function                  ###
######################################

# Define Class
class HalftimeBrowser():

    def __init__(self,country):
        self.country = country

    # Set browser profile
    def set_profile(self,add_on):
        profile = webdriver.FirefoxProfile()
        profile._install_extension(add_on)
        return profile

    # INITIALISE DRIVER
    def init_driver(self,profile):
        # Start browser
        driver = webdriver.Firefox(firefox_profile=profile)
        WebDriverWait(driver, 5)
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

        # GET RID OF ADD THAT POPS UP
        self.remove_popup(driver, 0)

        # LOG
        logger.info('Starting Page Opened.')


    # RETRIEVE ITEMS
    def retrieve_teams(self, driver, database, timestamp):

        # Retrieve Page Type
        button_selector, page_type = self.retrieve_page_type(driver.page_source)

        # Set starting window
        start_window = driver.window_handles[0]

        count = 1

        # Loop through Different Games
        for game in self.wait_pl_pres(driver, 'tr.match-on '):

            # Move to Second Page
            self.move_to_game_page(game, driver, button_selector)

            self.remove_popup(driver, 1)
            #
            self.move_to_odds_page(driver, page_type)

            if count == 1:
                break

            # # Move to Half Time Odds
            # self.move_to_odds_page(driver, page_type)
            #
            # driver.close()
            # driver.switch_to_window(start_window)

            #
            #     # Retrieve Halftime Button if existent
            #     options_count, code = self.retrieve_options_index(driver)
            #     if code == 1:
            #         game_info = self.extract_game_info(driver,timestamp)
            #         # ------> HALFTIME ODDS
            #         self.wait(driver,'//*[@id="table-tabs-row"]/ul/li[{}]/a'.format(options_count)).click()
            #         # Collect odds for the different providers and pass them on to the database
            #         self.provider_odds(driver,database,game_info)
            #         print('Game {} successfully fetched'.format(count))
            #     else:
            #         print('There is no halftime/fulltime odds for game {} yet'.format(count))
            #     driver.close()
            #
            #     count = count + 1
            # else:
            #     print('Element not found')


######################################
### Action Function                ###
######################################

    def move_to_game_page(self, game, driver, button_selector):
        """ This function opens the next page and adjusts the window switch. """
        try:
            all_odds_button = self.wait_pres(game, button_selector.replace(' ', '.'))
            # Move on
            all_odds_button.send_keys(Keys.SHIFT, Keys.ALT, Keys.ENTER)
            logger.info('Moved On to Second Page.')
        except TimeoutException as ex:
            logger.error(ex)

        # Obtain and switch to new window handle
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        game_window = driver.window_handles[1]
        driver.switch_to_window(game_window)
        logger.info('Window Handle is switched.')

    def move_to_odds_page(self, driver, page_type):
        logger.info('Moving on to Odds Page.')
        if page_type == 'NEW':
            self.wait_pres(driver, 'div.market-dd.select-coupon-wrap > div.selected-coupon > div.market-item.selected.beta-caption1').click()
            additional_options = self.wait_pl_vis(driver, 'div.market-lists > ul.market-list.beta-3col-table > li > a.market-item.beta-caption1')
            for item in additional_options:
                option = item.get_property('title')
                print(option)
                if option == 'Half Time/Full Time':
                    item.click()
                    logger.info('Moved on to Odds Page.')
                    break
        else:
            logger.info('Not Moving on to Odds Page.')

    # Extract team information
    def extract_game_info(self, driver, timestamp):
        #  Messy splitting of team names.
        teams = self.wait_pres(driver, '//*[@id="betting-odds"]/div/section/div/header/h1').text
        home_team = teams.split(' v ')[0].replace(" ", "")
        time.sleep(0.5 * uniform(0, 1))
        container = teams.split(' v ')[1]
        away_team = container.split(' Winner')[0].replace(" ", "")
        time.sleep(0.5 * uniform(0, 1))
        # Messy splitting of date & time
        datetime = self.wait_pres(driver, '//*[@id="betting-odds"]/div/section/div/div/div/div/span').text
        day = datetime.split(' / ')[0]
        clock = datetime.split(' / ')[1]
        #  Build identifier variable
        day_ = day.split(' ')[1][:2]
        month = day.split(' ')[2][:3]
        h_team = home_team[:5]
        a_team = away_team[:5]
        identifier = h_team + '_' + a_team + '_' + day_ + '_' + month
        # save the info in list
        game_info = [home_team, away_team, day, clock, identifier, timestamp]
        return game_info

    # Extract the data by provider
    def provider_odds(self, driver, database, game_info):
        # Set up index for the different providers
        provider_indices = np.arange(2, 31)
        provider_indices = np.delete(provider_indices, 25)
        # Loop through each of the odds providers
        for i in provider_indices:
            # Quick nap
            time.sleep(0.5 * uniform(0, 1))
            # Only include providers that have odds
            if self.wait_pres(driver, '//*[@id="t1"]/tr[1]/td[{}]'.format(i)).get_attribute('data-odig') != "0":
                item = Halftime()
                item['home_team'] = game_info[0]
                item['away_team'] = game_info[1]
                item['date'] = game_info[2]
                item['time'] = game_info[3]
                item['identifier'] = game_info[4]
                item['accessed'] = game_info[5]
                item['provider'] = self.wait(driver,
                                             '//*[@id="oddsTableContainer"]/table/thead/tr[4]/td[{}]/aside/a'.format(
                                                 i)).get_attribute('title')
                item['home_home'] = self.wait(driver, '//*[@id="t1"]/tr[1]/td[{}]'.format(i)).get_attribute(
                    'data-odig')
                item['away_away'] = self.wait(driver, '//*[@id="t1"]/tr[2]/td[{}]'.format(i)).get_attribute(
                    'data-odig')
                item['draw_home'] = self.wait(driver, '//*[@id="t1"]/tr[3]/td[{}]'.format(i)).get_attribute(
                    'data-odig')
                item['draw_draw'] = self.wait(driver, '//*[@id="t1"]/tr[4]/td[{}]'.format(i)).get_attribute(
                    'data-odig')
                item['draw_away'] = self.wait(driver, '//*[@id="t1"]/tr[5]/td[{}]'.format(i)).get_attribute(
                    'data-odig')
                item['home_draw'] = self.wait(driver, '//*[@id="t1"]/tr[6]/td[{}]'.format(i)).get_attribute(
                    'data-odig')
                item['away_draw'] = self.wait(driver, '//*[@id="t1"]/tr[7]/td[{}]'.format(i)).get_attribute(
                    'data-odig')
                item['away_home'] = self.wait(driver, '//*[@id="t1"]/tr[8]/td[{}]'.format(i)).get_attribute(
                    'data-odig')
                item['home_away'] = self.wait(driver, '//*[@id="t1"]/tr[9]/td[{}]'.format(i)).get_attribute(
                    'data-odig')
                database.process_item(item)


######################################
### Auxiliary Function             ###
######################################

    # This break function runs through the toolbar to check whether halftime/fulltime odds exists/ and find their index
    def retrieve_options_index(self, driver):
        code = 0
        options_count = 1
        for option in self.wait_pl_pres(driver,'//*[@id="table-tabs-row"]/ul/li'):
            if option.text != "Half Time/Full Time":
                options_count = options_count + 1
            elif option.text == "Half Time/Full Time":
                code = 1
                break
        return options_count, code
   
    # Check whether game is in play
    def check_in_play(self, odds):
        button = odds.get_attribute('class')
        not_in_play = "button beta-callout btn-1-small"
        if button == not_in_play:
            code = 1
        else:
            code =  0
        return code

    # Wait for element
    def wait_vis(self, driver, css_selector):
        """ This function returns an element identified by via the given xpath. """
        return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    # Wait for element
    def wait_click(self, driver, css_selector):
        """ This function returns an element identified by via the given xpath. """
        return WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))

    # Wait for element
    def wait_pres(self, driver, css_selector):
        """ This function returns an element identified by via the given xpath. """
        return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

    # wait for handle
    def wait_pl_vis(self, driver, css_selector):
        """ This function assigns all elements identified by via the given xpath to a list. """
        return WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector)))

    # wait for handle
    def wait_pl_pres(self, driver, css_selector):
        """ This function assigns all elements identified by via the given xpath to a list. """
        return WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))


    def retrieve_page_type(self, driver_html):
        """ This function checks for the page type and retrieves the button class name."""
        try:
            if 'class="button beta-callout btn-1-small"' in driver_html:
                page_type = 'OLD'
                button_selector = 'a.button beta-callout btn-1-small'
            elif 'class="beta-callout"' in driver_html:
                page_type = 'NEW'
                button_selector = 'a.beta-callout'
            logger.info('Page Type: {}'.format(page_type))
        except TimeoutException:
            logger.error('No Button Found.')
        return button_selector, page_type

    def remove_popup(self, driver, button_type):
        """ This function removes popup adds. """
        # Identify type of Popup
        if button_type == 0:
            buttons = self.wait_pl_pres(driver, 'div.content-wrapper > span.inside-close-button.choose-uk')
        elif button_type == 1:
            buttons = self.wait_pl_pres(driver,'div#promo-modal.modal-dialog.active.offers-2 > '
                                               'div.modal-dialog-inner > div.content-wrapper > '
                                               'span.inside-close-button')
            time.sleep(2) # Otherwise the click does not work...
        # Remove Popup
        for button in buttons:
            try:
                button.click()
                logger.info('Popup Add Removed.')
            except BaseException as ex:
                logger.error(ex)
                pass
        del buttons


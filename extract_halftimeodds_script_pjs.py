######################################
### BUILT LOGGER                   ###
######################################

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

######################################
### MODULES                        ###
######################################

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

######################################
### MODULES                        ###
######################################))))))))



######################################
### Specify country                ###
######################################
import sys
country = sys.argv[1]

######################################
### Import Modules                 ###
######################################

# My own modules
from spiders.halftime_pjs import HalftimeBrowser
from items import Halftime
import time
from pipelines import GermanyPipeline, EnglandPipeline, SpainPipeline, FrancePipeline, ItalyPipeline
from germany_sql import ManageSQL
from germany_graph import GraphSQL

# Already installed modules
import psycopg2 as ps
from random import uniform
import pandas.io.sql as psql

######################################
### GENERAL DATA                   ###
######################################

# Retrieve time and date
hour = time.strftime("%H:%M").replace(":","_")
day = time.strftime("%Y/%m/%d").replace("/","_")
timestamp  = "d_" + day + "_h_" + hour

# Define parameters for database connection
params = {
    'database':'scrape',
    'user':'benglaser',
    'password':'',
    'host':'127.0.0.1',
    'port':'5432'
}


######################################
### FETCH THE DATA                 ###
######################################

if __name__ == "__main__":
    
    # Set up table and corresponding pipeline
    if country == "germany":
         db = GermanyPipeline()
    elif country == "england":
         db = EnglandPipeline()
    elif country == "spain":
         db = SpainPipeline()
    elif country == "france":
         db = FrancePipeline()
    elif country == "italy":
         db = ItalyPipeline()
    
    db.__init__()

    # Run the brower-spider
    phantomjs = HalftimeBrowser(country) 

    # Set up profile
    profile = firefox.set_profile('/Users/benglaser/ben/coding/python/anaconda/anaconda/envs/benglaeser/scraper/code/bundesliga/google_analytics/gaoptoutaddon_0.9.8.xpi')

    # Start Driver
    driver = phantomjs.init_driver()
    phantomjs.open_url(driver)

    # Get the odds
    phantomjs.retrieve_teams(driver,db,timestamp)
    time.sleep(5 * uniform(0,1))

    # Close the driver
    driver.quit()
    print('Data fully scraped')

######################################
### SEARCH FOR ARBITRAGE           ###
######################################

    # Create class instance
    sql = ManageSQL(country,timestamp)
    # Connect to database
    conn = sql.connect_to_database()
    # Define cursor
    cur = sql.define_cursor(conn)
    # If necessary, create max_odds table
    sql.create_max_odds(cur)
    # obtain unique game ids
    id_list = sql.obtain_unique_matches(cur)
    out_list = sql.obtain_outcomes(cur)
    # Obtain max odds for a game
    sql.insert_data(cur,id_list,out_list)
    sql.commit_changes(conn)

######################################
### GRAPH RESULTS                  ###
######################################
    
    # create connection instance
    sql = GraphSQL(country,timestamp)
    # connect to database and define cursor
    connection = sql.connect_to_database()
    cursor = sql.define_cursor(connection)
    # transfer psql data into pandas
    pf = sql.read_pandas(connection)
    sql.graph_odds(pf)

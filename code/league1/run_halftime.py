######################################
### Import Modules                 ###
######################################

# My own modules
from spiders.halftime import HalftimeBrowser
from items import Halftime
import time
from pipelines import HalftimePipeline
from france_sql import ManageSQL
from france_graph import GraphSQL

# Already installed modules
import psycopg2 as ps
from random import uniform
import pandas.io.sql as psql

######################################
### SQL COMMANDS                   ###
######################################

# Define country
country = "france"

# Retrieve time and date
hour = time.strftime("%H:%M").replace(":","_")
day = time.strftime("%d/%m/%Y").replace("/","_")
time_date_code = "d_" + day + "_h_" + hour

# Define parameters for database connection
params = {
    'database':'scrape',
    'user':'benglaser',
    'password':'',
    'host':'127.0.0.1',
    'port':'5432'
}

# Select distinct game ids
select_game_ids = "SELECT DISTINCT identifier from {}.halftime_all_odds".format(country)

# Select columnnames
select_columns = "SELECT * FROM {}.halftime_all_odds LIMIT 0".format(country)

# Select games to obtain max odds
select_all_odds = "SELECT identifier,home_home from halftime_premierleague".format(country)

# Select odds by game id
select_game_odds = "SELECT {out} from {country}.halftime_all_odds WHERE identifier = '{ident}'"

# Check table existence
table_exist = "select exists(select * from information_schema.tables where table_name=%s)"

# Define command for max_odds database
max_odds_table = (
    """
    CREATE TABLE {}.halftime_max_odds (
        ID SERIAL PRIMARY KEY NOT NULL,
        GAME_ID TEXT NOT NULL,
        HO_HO REAL NOT NULL,
        DR_HO REAL NOT NULL,
        DR_DR REAL NOT NULL,
        AW_AW REAL NOT NULL,
        DR_AW REAL NOT NULL,
        HO_DR REAL NOT NULL,
        AW_DR REAL NOT NULL,
        AW_HO REAL NOT NULL,
        HO_AW REAL NOT NULL,
        SUM REAL NOT NULL,
        ARBITRAGE TEXT NOT NULL
        )
    """.format(country))

# Define insert command
insert_command = (
    """
    INSERT INTO {}.halftime_max_odds (id,game_id, ho_ho, dr_ho, dr_dr, aw_aw, dr_aw, ho_dr, aw_dr, aw_ho,     ho_aw,sum,arbitrage) VALUES (DEFAULT,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """.format(country))

######################################
### FETCH THE DATA                 ###
######################################

if __name__ == "__main__":
    # Set up table and corresponding pipeline
    db = HalftimePipeline()
    db.__init__()

    # Run the brower-spider
    # Set up profile
    firefox = HalftimeBrowser()
    profile = firefox.set_profile('./google_analytics/gaoptoutaddon_0.9.8.xpi')
    # Start Driver
    driver = firefox.init_driver(profile)
    firefox.open_url(driver)
    # Get the odds
    firefox.retrieve_teams(driver,db)
    time.sleep(5 * uniform(0,1))
    driver.quit()
    print('Data fully scraped')

######################################
### SEARCH FOR ARBITRAGE           ###
######################################

    # Create sql connection instance
    sql = ManageSQL()
    connection = sql.connect_to_database()
    # Define the cursor
    cursor = sql.define_cursor(connection)
    # If necessary create the max_odds table
    cursor.execute(table_exist, ('{}.halftime_max_odds'.format(country),))
    if cursor.fetchone()[0] != True:
        sql.create_max_odds(cursor,max_odds_table)
        print('A new table has been created')
    else:
        print('The table already exists')
    # Obtain unique game ids and outcome lists
    id_list = sql.obtain_unique_matches(cursor)
    out_list = sql.obtain_outcomes(cursor)
    # Obtain max odds for a game
    sql.insert_data(cursor, id_list, out_list, insert_command)
    sql.commit_changes(connection)

######################################
### GRAPH RESULTS                  ###
######################################

    # Create connection instance
    gsql = GraphSQL()
    # connect to database and define cursor
    connection = gsql.connect_to_database()
    cursor = gsql.define_cursor(connection)
    # transfer psql data into pandas
    pf = gsql.read_pandas(connection)
    gsql.graph_odds(pf)





'''
* Thiss file builds and fills a new seperate table that will combine the best odds per game and determine whether there is any opportunity for arbitrage.

* Lesson: the order in which I apply quotes is crucial to the functioning cursor executions.
'''

######################################
### Import Modules                 ###
######################################

import psycopg2 as ps
import pandas.io.sql as psql
import matplotlib.pyplot as plt
import numpy as np
import time

######################################
### COMMAND DEFINITION             ###
######################################

# Define country
country = "italy"

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

read_pandas = "SELECT * FROM {}.halftime_max_odds".format(country)

######################################
### EXECUTION CLASS                ###
######################################

class GraphSQL():

    # Create connection
    def connect_to_database(self):
        connection = ps.connect(**params)
        print('Connection to Database successful')
        return connection

    # Define cursor
    def define_cursor(self,connection):
        cursor = connection.cursor()
        print('Cursor defined')
        return cursor

    # Read in data into pandas
    def read_pandas(self,connection):
        dataframe = psql.read_sql(read_pandas,connection)
        dt = dataframe.sort_values('sum')
        return dt


    # Graph best odd combination
    def graph_odds(self,dataframe):
        # Idenify data points
        data = dataframe['sum']
        game_ids = dataframe['game_id']
        index = np.arange(0,len(data))
        xlabels = [gid for gid in game_ids]
        fig, axes = plt.subplots(figsize=(12,6))
        axes.scatter(data,index)
        axes.set_yticks(np.arange(0, len(data), 1))
        axes.set_xticks(np.arange(0.85, max(data)+0.05,0.05))
        axes.set_yticklabels(xlabels)
        plt.axvline(x = 1)
        plt.axvspan(1,max(data)+0.05,facecolor='red',alpha=0.3)
        plt.axis([0.92,max(data)+0.05, -1,len(data)])
        plt.grid()
        # Save graph to dropbox
        g_name = '/Users/benglaser/Dropbox/scrape/{country}/{date}.png'.format(country=country,date=time_date_code)
        plt.savefig(g_name)


######################################
### EXECUTION SCRIPT               ###
######################################

if __name__ == "__main__":
    # create connection instance
    sql = GraphSQL()
    # connect to database and define cursor
    connection = sql.connect_to_database()
    cursor = sql.define_cursor(connection)
    # transfer psql data into pandas
    pf = sql.read_pandas(connection)
    sql.graph_odds(pf)

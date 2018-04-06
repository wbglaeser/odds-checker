'''
* This file builds and fills a new seperate table that will combine the best odds per game and determine whether there is any opportunity for arbitrage.

* Lesson: the order in which I apply quotes is crucial to the functioning cursor executions.
'''

######################################
### Import Modules                 ###
######################################

import psycopg2 as ps
import time
import sys

######################################
### GENERAL DATA                   ###
######################################

# Define country
#country = str(sys.argv[1])
#timestamp = str(sys.argv[2])

######################################
### SQL COMMANDS                   ###
######################################

# Select distinct game ids
select_game_ids = "SELECT DISTINCT identifier from {country}.halftime_all_odds WHERE accessed = '{timestamp}'"

# Select columnnames
select_columns = "SELECT * FROM {}.halftime_all_odds LIMIT 0"

# Select odds by game id
select_game_odds = "SELECT {out} from {country}.halftime_all_odds WHERE identifier = '{ident}' AND accessed = '{timestamp}'"

# Check table existence
table_exist = "select exists(select 1 from information_schema.tables WHERE table_schema = '{}' AND table_name = 'halftime_max_odds')"

# Define command for max_odds database
max_odds_table = """
        CREATE TABLE {}.halftime_max_odds (
        ID SERIAL PRIMARY KEY NOT NULL,
        ACCESSED TEXT NOT NULL,
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
                 """

# Define insert command
insert_command = """
    INSERT INTO {country}.halftime_max_odds (id,accessed,game_id, ho_ho, dr_ho, dr_dr, aw_aw, dr_aw, ho_dr, aw_dr, aw_ho,ho_aw,sum,arbitrage) VALUES (DEFAULT,'{timestamp}',%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                 """

#####################################
### EXECUTION CLASS                ###
######################################

class ManageSQL():
    
    # Initialise class
    def __init__(self,country,timestamp):

        ### GENERAL ###
        
        self.country = country
        self.timestamp = timestamp

        self.params =  {
            'database':'scrape',
            'user':'benglaser',
            'password':'',
            'host':'127.0.0.1',
            'port':'5432'
        }

        ### SQL COMMANDS ###
         
        # Obtain game ids
        self.select_game_ids = select_game_ids.format(country=country,timestamp=timestamp)

        # Select columns to retrieve outcomes
        self.select_columns = select_columns.format(country)
 
        # Select games odds
        self.select_game_odds = select_game_odds

        # Check for table existence
        self.table_exist = table_exist.format(country)

        # Build new table if necessary
        self.max_odds_table = (max_odds_table.format(country))

        # Define insert command
        self.insert_command = (insert_command.format(country=country,timestamp=timestamp))

    # Create connection
    def connect_to_database(self):
        connection = ps.connect(**self.params)
        print('Connection to Database successful')
        return connection

    # Define cursor
    def define_cursor(self,connection):
        cursor = connection.cursor()
        print('Cursor defined')
        return cursor

    # Define new table
    def create_max_odds(self,cursor):
        # Check for table
        cursor.execute(self.table_exist)
        if cursor.fetchone()[0] != True:
            cursor.execute(self.max_odds_table)
            print('A new table has been created')
        else:
            print('The table already exists')

    # Compute max odds by outcome
    def obtain_unique_matches(self,cursor):
        cursor.execute(self.select_game_ids)
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    # Obtain column names as list
    def obtain_outcomes(self,cursor):
        cursor.execute(self.select_columns)
        columnames = [desc[0] for desc in cursor.description]
        return columnames[8:17]

    # Obtain max_odds for a game
    def extract_max_odds(self,cursor,ident,out_list):
        max_odds = []
        for out in out_list:
            cursor.execute(self.select_game_odds.format(out=out,country=self.country,ident=ident,timestamp=self.timestamp))
            rows = cursor.fetchall()
            row_list = [row[0] for row in rows]
            max_odds.append(max(row_list))
        return max_odds

    # Insert data into table
    def insert_data(self,cursor,id_list,outlist):
        for ident in id_list:
            max_odds = self.extract_max_odds(cursor,ident,outlist)
            invert_odds = [1/i for i in max_odds]
            sum_odds = sum(invert_odds)
            if sum_odds < 1:
                arb = "YES"
            else:
                arb = "No"
            # insert command
            data = (ident, invert_odds[0], invert_odds[1], invert_odds[2], invert_odds[3], invert_odds[4], invert_odds[5], invert_odds[6], invert_odds[7], invert_odds[8],sum_odds,arb)
            cursor.execute(self.insert_command,data)

    # Commit changes to database
    def commit_changes(self,connection):
        connection.commit()

    
######################################
### EXECUTION SCRIPT               ###
######################################

if __name__ == '__main__':
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




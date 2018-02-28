'''
* This file builds and fills a new seperate table that will combine the best odds per game and determine whether there is any opportunity for arbitrage.

* Lesson: the order in which I apply quotes is crucial to the functioning cursor executions.
'''

######################################
### Import Modules                 ###
######################################

import psycopg2 as ps

######################################
### COMMAND DEFINITION             ###
######################################

# Define country
country = "france"

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
select_all_odds = "SELECT identifier,home_home from {}.halftime_all_odds".format(country)

# Select odds by game id
select_game_odds = "SELECT {out} from {country}.halftime_all_odds WHERE identifier = '{ident}'"

# Check table existence
table_exist = "select exists(select * from information_schema.tables where table_schema = '{}' and table_name= 'halftime_max_odds')".format(country)

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
    INSERT INTO {}.halftime_max_odds (id,game_id, ho_ho, dr_ho, dr_dr, aw_aw, dr_aw, ho_dr, aw_dr, aw_ho, ho_aw,sum,arbitrage) VALUES (DEFAULT,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """.format(country))
  
######################################
### EXECUTION CLASS                ###
######################################

class ManageSQL():

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

    # Define new table
    def create_max_odds(self,cursor,max_odds_table):
        # Define new table for max odds
        cursor.execute(max_odds_table)

    # Compute max odds by outcome
    def obtain_unique_matches(self,cursor):
        cursor.execute(select_game_ids)
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    # Obtain column names as list
    def obtain_outcomes(self,cursor):
        cursor.execute(select_columns)
        columnames = [desc[0] for desc in cursor.description]
        return columnames[7:16]

    # Obtain max_odds for a game
    def extract_max_odds(self,cursor,ident,out_list):
        cursor.execute(select_all_odds)
        rows = cursor.fetchall()
        max_odds = []
        for out in out_list:
            cursor.execute(select_game_odds.format(out=out,country=country,ident=ident))
            rows = cursor.fetchall()
            row_list = [row[0] for row in rows]
            max_odds.append(max(row_list))
        return max_odds

    # Insert data into table
    def insert_data(self,cursor,id_list,outlist,insert_command):
        for ident in id_list:
            max_odds = self.extract_max_odds(cursor,ident,outlist)
            invert_odds = [1/i for i in max_odds]
            sum_odds = sum(invert_odds)
            if sum_odds < 1:
                arb = "YES"
            else:
                arb = "NO"
            # insert command
            data = (ident, invert_odds[0], invert_odds[1], invert_odds[2], invert_odds[3], invert_odds[4], invert_odds[5], invert_odds[6], invert_odds[7], invert_odds[8],sum_odds,arb)
            cursor.execute(insert_command,data)

    # Commit changes to database
    def commit_changes(self,connection):
        connection.commit()

######################################
### EXECUTION SCRIPT               ###
######################################

if __name__ == '__main__':
    # Create class instance
    sql = ManageSQL()
    # Connect to database
    conn = sql.connect_to_database()
    # Define cursor
    cur = sql.define_cursor(conn)
    # If necessary, create max_odds table
    cur.execute(table_exist)
    if cur.fetchone()[0] != True:
        sql.create_max_odds(cur,max_odds_table)
        print('A new table has been created')
    else:
        print('The table already exists')
    # obtain unique game ids
    id_list = sql.obtain_unique_matches(cur)
    out_list = sql.obtain_outcomes(cur)
    # Obtain max odds for a game
    sql.insert_data(cur,id_list,out_list,insert_command)
    sql.commit_changes(conn)





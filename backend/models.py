from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import backend.settings as sets

DeclarativeBase_halftime = declarative_base()

#######################
# SHARED ENGINE       #
#######################

### HALFTIME CRAWLER ###
def db_halftime_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**sets.DATABASE))

def create_halftime_table(engine):
    DeclarativeBase_halftime.metadata.create_all(engine)

#######################
# COUNTRY MODELS      #
#######################

class Germany(DeclarativeBase_halftime):
    
    """ Sqlalchemy halftime model """
    __tablename__ = "halftime_all_odds"
    __table_args__ = {'schema':"germany"}

    id = Column(Integer, primary_key=True)
    # Identifier
    identifier = Column('identifier', String, nullable=True)
    accessed = Column('accessed', String, nullable=True)

    # Team names
    home_team = Column('home_team', String, nullable=True)
    away_team = Column('away_team', String, nullable=True)
    provider = Column('provider', String, nullable=True)

    # Time and date
    date = Column('date', String, nullable=True)
    time = Column('time', String, nullable=True)

    # Odds
    home_home = Column('home_home', Float, nullable=True)
    away_away = Column('away_away', Float, nullable=True)
    draw_home = Column('draw_home', Float, nullable=True)
    draw_draw = Column('draw_draw', Float, nullable=True)
    draw_away = Column('draw_away', Float, nullable=True)
    home_draw = Column('home_draw', Float, nullable=True)
    away_draw = Column('away_draw', Float, nullable=True)
    away_home = Column('away_home', Float, nullable=True)
    home_away = Column('home_away', Float, nullable=True)
    
class England(DeclarativeBase_halftime):
    
    """ Sqlalchemy halftime model """
    __tablename__ = "halftime_all_odds"
    __table_args__ = {'schema':"england"}

    id = Column(Integer, primary_key=True)
    # Identifier
    identifier = Column('identifier', String, nullable=True)
    accessed = Column('accessed', String, nullable=True)

    # Team names
    home_team = Column('home_team', String, nullable=True)
    away_team = Column('away_team', String, nullable=True)
    provider = Column('provider', String, nullable=True)

    # Time and date
    date = Column('date', String, nullable=True)
    time = Column('time', String, nullable=True)

    # Odds
    home_home = Column('home_home', Float, nullable=True)
    away_away = Column('away_away', Float, nullable=True)
    draw_home = Column('draw_home', Float, nullable=True)
    draw_draw = Column('draw_draw', Float, nullable=True)
    draw_away = Column('draw_away', Float, nullable=True)
    home_draw = Column('home_draw', Float, nullable=True)
    away_draw = Column('away_draw', Float, nullable=True)
    away_home = Column('away_home', Float, nullable=True)
    home_away = Column('home_away', Float, nullable=True)
    

class Spain(DeclarativeBase_halftime):
    
    """ Sqlalchemy halftime model """
    __tablename__ = "halftime_all_odds"
    __table_args__ = {'schema':"spain"}

    id = Column(Integer, primary_key=True)
    # Identifier
    identifier = Column('identifier', String, nullable=True)
    accessed = Column('accessed', String, nullable=True)

    # Team names
    home_team = Column('home_team', String, nullable=True)
    away_team = Column('away_team', String, nullable=True)
    provider = Column('provider', String, nullable=True)

    # Time and date
    date = Column('date', String, nullable=True)
    time = Column('time', String, nullable=True)

    # Odds
    home_home = Column('home_home', Float, nullable=True)
    away_away = Column('away_away', Float, nullable=True)
    draw_home = Column('draw_home', Float, nullable=True)
    draw_draw = Column('draw_draw', Float, nullable=True)
    draw_away = Column('draw_away', Float, nullable=True)
    home_draw = Column('home_draw', Float, nullable=True)
    away_draw = Column('away_draw', Float, nullable=True)
    away_home = Column('away_home', Float, nullable=True)
    home_away = Column('home_away', Float, nullable=True)
    

class France(DeclarativeBase_halftime):
    
    """ Sqlalchemy halftime model """
    __tablename__ = "halftime_all_odds"
    __table_args__ = {'schema':"france"}

    id = Column(Integer, primary_key=True)
    # Identifier
    identifier = Column('identifier', String, nullable=True)
    accessed = Column('accessed', String, nullable=True)

    # Team names
    home_team = Column('home_team', String, nullable=True)
    away_team = Column('away_team', String, nullable=True)
    provider = Column('provider', String, nullable=True)

    # Time and date
    date = Column('date', String, nullable=True)
    time = Column('time', String, nullable=True)

    # Odds
    home_home = Column('home_home', Float, nullable=True)
    away_away = Column('away_away', Float, nullable=True)
    draw_home = Column('draw_home', Float, nullable=True)
    draw_draw = Column('draw_draw', Float, nullable=True)
    draw_away = Column('draw_away', Float, nullable=True)
    home_draw = Column('home_draw', Float, nullable=True)
    away_draw = Column('away_draw', Float, nullable=True)
    away_home = Column('away_home', Float, nullable=True)
    home_away = Column('home_away', Float, nullable=True)
    

class Italy(DeclarativeBase_halftime):
    
    """ Sqlalchemy halftime model """
    __tablename__ = "halftime_all_odds"
    __table_args__ = {'schema':"italy"}

    id = Column(Integer, primary_key=True)
    # Identifier
    identifier = Column('identifier', String, nullable=True)
    accessed = Column('accessed', String, nullable=True)

    # Team names
    home_team = Column('home_team', String, nullable=True)
    away_team = Column('away_team', String, nullable=True)
    provider = Column('provider', String, nullable=True)

    # Time and date
    date = Column('date', String, nullable=True)
    time = Column('time', String, nullable=True)

    # Odds
    home_home = Column('home_home', Float, nullable=True)
    away_away = Column('away_away', Float, nullable=True)
    draw_home = Column('draw_home', Float, nullable=True)
    draw_draw = Column('draw_draw', Float, nullable=True)
    draw_away = Column('draw_away', Float, nullable=True)
    home_draw = Column('home_draw', Float, nullable=True)
    away_draw = Column('away_draw', Float, nullable=True)
    away_home = Column('away_home', Float, nullable=True)
    home_away = Column('home_away', Float, nullable=True)
    


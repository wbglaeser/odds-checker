from sqlalchemy.orm import sessionmaker
from models import Halftime, db_halftime_connect, create_halftime_table

class HalftimePipeline(object):
    """ Halftime Pipele for storing scraped items in the database """
    def __init__(self):
        """
        Initialise database connection and sessionsmaker.
        Creates halftime table
        """
        engine = db_halftime_connect()
        create_halftime_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self,item):
        """
        save matches in the database

        method is called for every item pipeline component.
        """
        session = self.Session()
        halftime = Halftime(**item)
        
        try:
            session.add(halftime)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        
        return item

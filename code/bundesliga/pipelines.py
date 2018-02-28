from sqlalchemy.orm import sessionmaker
from models import Germany,England,France,Spain,Italy, db_halftime_connect, create_halftime_table

class GermanyPipeline():
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
        halftime = Germany(**item)
        
        try:
            session.add(halftime)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        
        return item


class EnglandPipeline():
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
        halftime = England(**item)
        
        try:
            session.add(halftime)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        
        return item

class SpainPipeline():
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
        halftime = Spain(**item)
        
        try:
            session.add(halftime)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        
        return item

class ItalyPipeline():
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
        halftime = Italy(**item)
        
        try:
            session.add(halftime)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        
        return item

class FrancePipeline():
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
        halftime = France(**item)
        
        try:
            session.add(halftime)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        
        return item


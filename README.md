First things first, we need to create a config file. Unlike SQLAlchemy, PyMySQL doesn't support database URI strings out of the box. Because of this, we need to set variables for each part of a database connection such as username, password, etc.:



""" 
try : 
    db = Database(config)
except:
    print("Database could not be inizialized")

class Database:
    """Database connection class."""
    def open_connection(self):
        """Connect to MySQL Database."""
        try:
            if self.conn is None:
                self.conn = pymysql.connect(self.host,
                                            user=self.username,
                                            passwd=self.password,
                                            db=self.dbname,
                                            connect_timeout=5)
        except pymysql.MySQLError as e:
            logging.error(e)
            sys.exit()
        finally:
            logging.info('Connection opened successfully.') """
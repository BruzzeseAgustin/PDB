class Database:
    """Database connection class."""

    def __init__(self, config):
        self.host = config.db_host
        self.username = config.db_user
        self.password = config.db_password
        self.port = config.db_port
        self.dbname = config.db_name
        self.conn = None

# Initializing this class saves our database connection variables to the instance of the class, 
# as well as creates a self.conn variable for managing connections. 
# We create an instance of this class by passing our config object to Database:
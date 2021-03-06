"""Config values."""
from os import environ


class Config:

    # Database config
    db_user = environ.get('DATABASE_USERNAME')
    db_password = environ.get('DATABASE_PASSWORD')
    db_host = environ.get('DATABASE_HOST')
    db_port = environ.get('DATABASE_PORT')
    db_name = environ.get('DATABASE_NAME')

    #We're pulling the values for each of these from a .env file:
    #  a practice I highly recommend for security purposes.
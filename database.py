import sqlite3
import mysql.connector
import psycopg2
from urllib.parse import urlparse


class Database:
    def __init__(self, connection_url):
        self.connection_url = connection_url
        self.connection = None
        self.connect()

    def connect(self):
        # Urlparse parses the url as: 
        # ParseResult(scheme='postgresql', netloc='user:password@localhost:5432', path='/testdb', params='', query='', fragment='')
        url = urlparse(self.connection_url)
        if url.scheme == 'sqlite':
            self.connection = sqlite3.connect(url.path[1:])
        elif url.scheme == 'postgresql':
            self.connection = psycopg2.connect(
                dbname = url.path[1:],
                user = url.username,
                password = url.password,
                host = url.hostname,
                port = url.port
            )
        elif url.scheme == 'mysql':
            self.connect = mysql.connector.connect(
                database=url.path[1:],  # Remove leading '/'
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
        else:
            raise ValueError(f"Unsupported database scheme: {url.scheme}")
        
    def execute(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        self.connection.commit()
        return cursor
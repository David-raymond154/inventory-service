# ~/inventory_service/app/__init__.py
from flask import Flask
from flask_mysqldb import MySQL
from config import Config
from flask_cors import CORS # For frontend integration

import pymysql

#try:
    # Import pymysql's constants module directly
    #from pymysql import constants as pymysql_constants
    #import sys

    #if 'MySQLdb.constants' not in sys.modules or sys.modules['MySQLdb.constants'] is not pymysql_constants:
        #sys.modules['MySQLdb.constants'] = pymysql_constants
        #if not hasattr(sys.modules['MySQLdb.constants'], 'COMMAND'):
            #sys.modules['MySQLdb.constants'].COMMAND = pymysql_constants.COMMAND

#except ImportError:
    #pass

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for development (allowing all origins is okay for now)
    CORS(app)

    mysql.init_app(app)

    # Import and register the blueprint
    from .routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# app/models.py
import mysql.connector
import os
import logging

logging.basicConfig(level=logging.INFO)
model_logger = logging.getLogger(__name__)

class DBManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST'),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DATABASE')
            )
            self.cursor = self.connection.cursor(dictionary=True)
            model_logger.info("Database connection established.") # Use logger
        except mysql.connector.Error as err:
            model_logger.error(f"Error connecting to database: {err}") # Use logger
            self.connection = None
        except Exception as e: # Catch any other unexpected connection errors
            model_logger.error(f"An unexpected error occurred during database connection: {e}")
            self.connection = None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            model_logger.info("Database connection closed.") # Use logger

    def execute_query(self, query, params=None):
        result = None
        try:
            if not self.connection or not self.connection.is_connected():
                model_logger.info("Reconnecting to database...")
                self.connect() # Reconnect if not connected

            if not self.connection or not self.connection.is_connected():
                # If connect() failed, then we can't execute the query
                model_logger.error("Failed to establish database connection for query execution.")
                return None

            self.cursor.execute(query, params or ())
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                self.connection.commit()
                result = self.cursor.rowcount
                if query.strip().upper().startswith('INSERT'):
                    result = self.cursor.lastrowid
            else:
                result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            model_logger.error(f"MySQL Database error during query '{query}': {err}") # Use logger, add query for context
            self.connection.rollback()
            result = None
        except Exception as e: # CATCH ALL OTHER EXCEPTIONS
            model_logger.error(f"An unexpected error occurred during query '{query}': {e}", exc_info=True) # Log full traceback
            self.connection.rollback() # Still rollback for safety
            result = None
        finally:
            pass
        return result

db_manager = DBManager()

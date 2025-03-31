import pycouchdb
from ..core.config import settings

# Global variable to hold the CouchDB server instance (using pycouchdb)
# In a real application, consider connection pooling or managing the connection lifecycle
# perhaps tied to application startup/shutdown events or request scope.
server = None
db = None

def get_db():
    """
    Function to get the database instance.
    Initializes the connection if it doesn't exist.
    """
    global server, db
    if server is None:
        try:
            # Connect to CouchDB server using pycouchdb
            server = pycouchdb.Server(
                settings.COUCHDB_URL,
                username=settings.COUCHDB_USER if settings.COUCHDB_USER else None,
                password=settings.COUCHDB_PASSWORD if settings.COUCHDB_PASSWORD else None
            )

            # Select or create the database
            db_name = settings.COUCHDB_DB_NAME
            if server.exists(db_name):
                db = server.database(db_name)
                print(f"Connected to existing database '{db_name}'.")
            else:
                print(f"Database '{db_name}' not found. Creating...")
                db = server.create(db_name)
                print(f"Database '{db_name}' created successfully.")

        except Exception as e:
            print(f"Failed to connect to CouchDB or get/create database using pycouchdb: {e}")
            # Handle connection error appropriately
            db = None
            server = None # Reset server if connection failed
            # Consider raising an exception
            # raise ConnectionError(f"Failed to connect to CouchDB using pycouchdb: {e}") from e

    # In a more complex app, you might return a session or connection object
    # For pycouchdb, often the 'db' object (Database instance) itself is used directly.
    if db is None:
        # Handle the case where DB connection failed during initialization
        raise ConnectionError("CouchDB database connection is not available.")

    return db

# Example of how to use it in other modules:
# from .session import get_db
# db_instance = get_db()
# doc = db_instance.get('some_document_id')

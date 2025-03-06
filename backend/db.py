import psycopg2
from psycopg2.extras import RealDictCursor
import os

DB_NAME = os.getenv('DB_NAME', 'car_listings')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '0000')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

def get_db_connection():
    """Create and return a new database connection."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def init_db():
    """Initialize the database and create the listings table if it doesn't exist."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS listings (
                id SERIAL PRIMARY KEY,
                title TEXT,
                price TEXT,
                location TEXT,
                mileage TEXT,
                year TEXT,
                link TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

def save_listing(title, price, location, mileage, year, link):
    """Save a new car listing to the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO listings (title, price, location, mileage, year, link) VALUES (%s, %s, %s, %s, %s, %s)',
            (title, price, location, mileage, year, link)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Listing saved: {title} - {price} - {location} - {mileage} - {year}")
    except Exception as e:
        print(f"Error saving listing: {e}")

def get_listings():
    """Retrieve all listings from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute('SELECT * FROM listings ORDER BY created_at DESC')
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error retrieving listings: {e}")
        return []

if __name__ == '__main__':
    init_db()

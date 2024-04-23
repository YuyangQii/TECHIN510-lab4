import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def create_books_table():
    conn = get_db_connection()
    cur = conn.cursor()
    

    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            price NUMERIC,
            rating INTEGER,
            description TEXT
        );
    """)
    
    conn.commit()  
    cur.close()
    conn.close()

def insert_data(data):
    """向数据库中插入书籍数据"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        for book in data:
            cur.execute(
                "INSERT INTO books (title, price, rating, description) VALUES (%s, %s, %s, %s)",
                (book['title'], book['price'], book['rating'], book['description'])
            )
        conn.commit()  
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()

def query_books(search_query='', sort_by='title', order='asc'):
    conn = get_db_connection()
    cur = conn.cursor()
    query = f"""
    SELECT title, price, rating, description FROM books
    WHERE title ILIKE %s OR description ILIKE %s
    ORDER BY {sort_by} {order};
    """
    cur.execute(query, ('%'+search_query+'%', '%'+search_query+'%'))
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books

if __name__ == "__main__":
    create_books_table()  
    print("Database setup complete.")

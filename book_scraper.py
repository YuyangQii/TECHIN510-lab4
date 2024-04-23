import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Create and return a database connection"""
    return psycopg2.connect(DATABASE_URL)

def insert_data(data):
    """Insert scraped data into the database"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        for book in data:
            # Convert rating from string to integer
            rating_conversion = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            rating = rating_conversion.get(book['rating'], 0)

            # Execute the insert statement
            cur.execute(
                "INSERT INTO books (title, price, rating, description) VALUES (%s, %s, %s, %s)",
                (book['title'], book['price'], rating, book['description'])
            )
        conn.commit()
        print(f"{len(data)} books inserted into database successfully.")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")
        conn.rollback()
    finally:
        conn.close()

def scrape_book_details(book_url):
    """Extract book details from its detail page"""
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'].strip() if description_tag else 'No description available'
    return description

def scrape_books(base_url):
    """Scrape all books from the paginated 'Books to Scrape' website"""
    books = []
    url = base_url
    while url:
        print(f"Scraping {url}")
        response = requests.get(url)
        response.encoding = 'utf-8'  # Ensure correct encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        for book in soup.select('ol.row li.col-xs-6.col-sm-4.col-md-3.col-lg-3'):
            title = book.select_one('h3 a')['title']
            detail_url = urljoin(url, book.select_one('h3 a')['href'])
            price_text = book.select_one('.price_color').text
            price = float(price_text.replace('£', '').strip())  # Remove £ symbol and convert to float
            rating = book.select_one('p.star-rating')['class'][1]
            description = scrape_book_details(detail_url)
            books.append({
                'title': title,
                'price': price,
                'rating': rating,
                'description': description
            })
        next_button = soup.find('li', class_='next')
        url = urljoin(url, next_button.find('a')['href']) if next_button else None
    return books

if __name__ == "__main__":
    url = 'http://books.toscrape.com/catalogue/page-1.html'
    books = scrape_books(url)
    insert_data(books)

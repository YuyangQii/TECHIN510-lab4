# TECHIN510-lab4:Accessing Web Resources with Python

# 📚🔍 Easy Book Exploration 
## Introduction
Book Explorer is an interactive web application designed for book enthusiasts. It utilizes web scraping techniques to extract data from online bookstores and provides an interactive interface for users to query and filter through book data based on name, description, ratings, and price. 

## Features
- **Web Scraping**: Code to scrape data from dynamically generated websites for a comprehensive book database.
- **Data Processing**: Includes examples of cleaning and processing the retrieved data for further analysis.
- **Pagination**: Users can navigate through a paginated list of books.
- **Search and Filtering**: Support for book search by title and description, as well as filtering by ratings and price.
- **User Interface**: An intuitive user interface built with Streamlit, including a sidebar for filters.

## Technologies Used
- **Python 3**: The main programming language used.
- **Streamlit**: For building and sharing data applications.
- **Requests**: A library for making HTTP requests.
- **BeautifulSoup**: A library for web scraping.
- **Pandas**: For data manipulation and analysis.
- **PostgreSQL**: For storing and managing book data in a database.

## How to Run This Code
To run this code, open the terminal and execute the following commands:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## What's Included
- `app.py`: The main Python script with Streamlit code for running the web application.
- `requirements.txt`: A file listing the project's dependencies for easy replication of the environment.
- `db.py`: Script for database interactions, including setting up tables and storing data.
- `-book_scraper.py`: Script for scraping book data from web pages.

## What I Learned
- How to effectively scrape web data using Python and manage the scraped data with web techniques and libraries.
- Enhanced understanding of database operations with PostgreSQL, including creating tables, inserting data, and querying databases.
- The construction and deployment of interactive web applications using the Streamlit library.

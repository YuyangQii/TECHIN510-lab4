import streamlit as st
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def get_books(search_query='', min_rating=0, sort_by='title', order='asc', offset=0, limit=20):
    conn = get_db_connection()
    cur = conn.cursor()
    query = f"""
    SELECT title, price, rating, description FROM books
    WHERE (title ILIKE %s OR description ILIKE %s) AND rating >= %s
    ORDER BY {sort_by} {order}
    LIMIT {limit} OFFSET {offset};
    """
    cur.execute(query, ('%'+search_query+'%', '%'+search_query+'%', min_rating))
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books

def get_total_books():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]
    cur.close()
    conn.close()
    return total_books

st.title("📚🔍 Easy Book Exploration")


with st.sidebar:
    st.header("Filter Options")
    search_query = st.text_input("Search by title or description", "")
    min_rating = st.slider("Minimum rating", 0, 5, 1)
    sort_by = st.selectbox("Sort by", options=["title", "price", "rating"], index=0)
    order = st.selectbox("Order", options=["asc", "desc"], index=0)


limit = 20  
if 'offset' not in st.session_state:
    st.session_state['offset'] = 0

total_books = get_total_books() 
total_pages = (total_books + limit - 1) // limit  

if st.sidebar.button("Apply Filter"):
    st.session_state['offset'] = 0  

books = get_books(search_query, min_rating, sort_by, order, st.session_state['offset'], limit)
if books:
    df = pd.DataFrame(books, columns=['Title', 'Price (£)', 'Rating', 'Description'])
    st.dataframe(df)  
else:
    st.write("No books found matching the criteria.")


col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("Previous"):
        if st.session_state['offset'] > 0:
            st.session_state['offset'] -= limit
with col3:
    if st.button("Next"):
        if st.session_state['offset'] + limit < total_books:
            st.session_state['offset'] += limit

page_number = st.session_state['offset'] // limit + 1
st.text(f"Page {page_number} of {total_pages}")

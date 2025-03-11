import streamlit as st
import pandas as pd
import os
from io import BytesIO
import json

LIBRARY_FILE = "library.json"

def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, genre, read_status):
    library.append({
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read_status
    })
    save_library(library)

def remove_book(library, title):
    updated_library = [book for book in library if book["title"].lower() != title.lower()]
    if len(updated_library) < len(library):
        save_library(updated_library)
        return updated_library, "Book removed successfully!"
    return library, "Book not found!"

def search_books(library, keyword):
    return [book for book in library if keyword.lower() in book["title"].lower() or keyword.lower() in book["author"].lower()]

def display_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    return total_books, percentage_read

st.title("📚 Library Manager")
library = load_library()

menu = st.sidebar.selectbox("Menu", ["Add Book", "Remove Book", "Search Book", "View All Books", "Statistics"])

if menu == "Add Book":
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
        genre = st.text_input("Genre")
        read_status = st.checkbox("Mark as Read")
        submitted = st.form_submit_button("Add Book")
        if submitted:
            add_book(library, title, author, year, genre, read_status)
            st.success("Book added successfully!")

elif menu == "Remove Book":
    title_to_remove = st.text_input("Enter the book title to remove")
    if st.button("Remove Book"):
        library, message = remove_book(library, title_to_remove)
        st.success(message)

elif menu == "Search Book":
    search_query = st.text_input("Enter title or author to search")
    if st.button("Search"):
        results = search_books(library, search_query)
        if results:
            for book in results:
                st.write(f"📖 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("No matching books found.")

elif menu == "View All Books":
    if library:
        for book in library:
            st.write(f"📖 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.warning("Your library is empty.")

elif menu == "Statistics":
    total, read_percentage = display_statistics(library)
    st.write(f"📚 Total books: {total}")
    st.write(f"📖 Percentage read: {read_percentage:.2f}%") 



import streamlit as st 
import pandas as pd
import sqlite3 
import os

def sql_executor(raw_code, conn):
    c = conn.cursor()
    c.execute(raw_code)
    data = c.fetchall()
    return data 

def get_table_names(conn):
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    return [table[0] for table in tables]

def Home():
    st.title("SQLlite with Streamlit and Python")
    # Select Database
    db_file_path = st.text_input("Enter Database File Path:")
    if db_file_path:
        # Check if file exists
        if not os.path.exists(db_file_path):
            st.error("Le fichier spécifié n'existe pas.")
            return

        # Display the selected file path
        st.write("Selected Database Path:", db_file_path)

        # Connect to the database
        conn = sqlite3.connect(db_file_path)
        st.success("Database connected successfully.")
        st.subheader("Database details")
        with st.expander("List of tables"):
            tables = get_table_names(conn)
            st.write("Tables:", tables)  # Debugging message
        st.subheader("Table Details")
        if tables:
            for table in tables:
                with st.expander(f"{table}", expanded=False):
                    c = conn.cursor()  # Define cursor here
                    c.execute(f"PRAGMA table_info({table});")
                    columns_info = c.fetchall()
                    column_data = [[col[1], col[2]] for col in columns_info]
                    column_df = pd.DataFrame(column_data, columns=["Column Name", "Column Type"])
                    st.write(column_df,index=False)
        else:
            st.write("No tables found in the database.")
        st.subheader("SQL Query")
        # Columns/Layout
        col1,col2 = st.columns(2)

        with col1:
            with st.form(key='query_form'):
                raw_code = st.text_area("SQL Code Here")
                submit_code = st.form_submit_button("Execute")

        # Results Layouts
        with col2:
            if submit_code:
                st.info("Query Submitted")
                st.code(raw_code)

        # Results

        with st.expander("Result of the query"):
            try:
                query_results = sql_executor(raw_code, conn) 
                query_df = pd.DataFrame(query_results)
                st.dataframe(query_df)
            except:
                st.error("Syntax error")
        
        # Table of Info
        
        # Close the database connection
        conn.close()
def About():
    st.subheader("About John Doe")
    st.write("Nom: Doe")
    st.write("Prénom: John")
    st.write("Groupe: Groupe X")
def main():
    # Menu
    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice =="Home":
        Home()
    elif choice =="About":
        About()
    
if __name__ == '__main__':
    main()

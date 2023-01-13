import sqlite3


"""
table_schema

   CREATE TABLE  fish-cakes
                 (date TEXT NOT NULL,
                 user_id TEXT NOT NULL,
                 total_fish_cakes INT NOT NULL,
                 last_cake_collection TEXT NOT NULL)

"""

def is_sqlite_db(file_path: str):
    """
    returns True if a db is sqlite db
    else return the error
    """
    try:
        conn = sqlite3.connect(file_path)
        return True
    except Exception as e:
        return e

def create_sqlite_table(): 
    conn = sqlite3.connect('cake.db')
    cursor= conn.cursor()

    table_schema = '''CREATE TABLE  fish_cakes
                 (date TEXT NOT NULL,
                 user_id TEXT NOT NULL,
                 total_fish_cakes INT NOT NULL,
                 last_cake_collection TEXT NOT NULL)'''

    cursor.execute(table_schema)

    # Save the changes and close the connection
    conn.commit()
    conn.close()

  

def retrieve_data(db_file, query):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        # Execute the query
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
        return result
    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Close the connection
        cursor.close()
        conn.close()

def main():
    #c.execute("INSERT INTO fish_cakes VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    
    
if __name__ == "__main__":
    main()




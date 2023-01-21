import sqlite3
import time
from datetime import datetime

from tabulate import tabulate
class QueryNotExecutedException(Exception):
    
    def __init__(self, value):
            self.value = value
            
    def __str__(self):
        return(repr( self.value))

class NoDataFetchedError(Exception):
    def __init__(self, value):
            self.value = value
            
    def __str__(self):
        return(repr( self.value))

class UserExistsError(Exception):
    def __init__(self, value):
            self.value = value
            
    def __str__(self):
        return(repr( self.value))


"""
CREATE TABLE  fish_cakes
                 (user_id INT NOT NULL,
                 date TEXT NOT NULL,
                 user_name TEXT NOT NULL
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
                 (user_id INT NOT NULL,
                 date TEXT NOT NULL,
                 user_name TEXT NOT NULL,
                 total_fish_cakes INT NOT NULL,
                 last_cake_collection TEXT NOT NULL)'''

    cursor.execute(table_schema)

    # Save the changes and close the connection
    conn.commit()
    conn.close()

  
def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)

    if cursor.rowcount == 0:
        raise QueryNotExecutedException(f"Query: {query} is not executed")
    conn.commit()

    cursor.close()


def fetch_data(conn, fetch_query):
    # Connect to the database
    cursor = conn.cursor()

    cursor.execute(fetch_query)
    
    result = cursor.fetchall()

    # if result is empty raise error NoDataFetchedError
    if cursor.rowcount == 0: raise NoDataFetchedError(query)

    cursor.close()
    return result


def fetch_single_cell_data(conn, fetch_query):
    """
    doctest


    >>> import sqlite3 
    >>> conn = sqlite3.connect("cake.db")
    >>> data = fetch_single_cell_data(conn, fetch_query = "SELECT user_name FROM fish_cakes WHERE user_id=4954")
    >>> data
    'test_user2'
    >>>

    """
    # Connect to the database
    cursor = conn.cursor()

    cursor.execute(fetch_query)
    
    # since theres only one cell of data only the zero positon is not empty
    result = cursor.fetchone()[0]

    # if result is empty raise error NoDataFetchedError
    if cursor.rowcount == 0: raise NoDataFetchedError(query)

    cursor.close()
    return result


def create_new_user(conn: sqlite3.Connection, user_id :int, user_name: str):

    date = datetime.today()

    # user_exists_query returnw 1 if user_id exists else 0
    user_exists_query = f"SELECT EXISTS (SELECT * FROM fish_cakes WHERE user_id= {user_id})"
    user_insert_query= f"""INSERT INTO fish_cakes
    (user_id, date, user_name, total_fish_cakes, last_cake_collection)
    VALUES ({user_id}, "{date}", "{user_name}", 5000, "{date}");"""

    cursor = conn.cursor()
    cursor.execute(user_exists_query)
    user_exists = cursor.fetchone()[0]
    cursor.close()
    print('User exists:', user_exists)

    if user_exists: raise UserExistsError(f"user_id: {user_id} \n user_name: {user_name}")
    else: execute_query(conn, query = user_insert_query)


def fetch_leaderboard(conn):
    fetch_query = """WITH num_rows AS(SELECT COUNT(*) FROM fish_cakes)
SELECT user_name, total_fish_cakes
FROM fish_cakes
WHERE (SELECT * FROM num_rows) <= 10
ORDER BY total_fish_cakes DESC
LIMIT 10;"""
    leaderboard_data = fetch_data(conn, fetch_query)
    return tabulate(leaderboard_data, headers=["name", "fish_cakes"], tablefmt="simple")
    return leaderboard_table_string

    

def fetch_total_fish_cakes(conn, user_id):

    fetch_query = f"SELECT total_fish_cakes FROM fish_cakes WHERE user_id = '{user_id}'"

    return fetch_single_cell_data(conn, fetch_query)


def add_fish_cakes(conn,  user_id, fish_cakes_to_add):
    
    query = f"UPDATE fish_cakes SET total_fish_cakes = total_fish_cakes + {fish_cakes_to_add} WHERE user_id = '{user_id}'"
    execute_query(conn, query)

def subtract_fish_cakes(conn, user_id, fish_cakes_to_subtract):
    
    """
    uodated only if subtracted value is >= 0

    if user does not have enough amoumt to be sibtracted, NoDataFetchedError is caused
    
    """
    query = f"""UPDATE fish_cakes SET total_fish_cakes =  (total_fish_cakes - {fish_cakes_to_subtract}) 
        WHERE user_id = '{user_id}' AND total_fish_cakes - {fish_cakes_to_subtract} >= 0 
        """
    execute_query(conn, query)


def fetch_last_collection(conn, user_id):
    fetch_query = f"SELECT last_cake_collection FROM fish_cakes WHERE user_id = '{user_id}'"

    return fetch_data(conn, fetch_query)[0][0]

def update_last_collection(conn, user_id, time_to_insert):

    query = f" UPDATE fish_cakes SET last_cake_collection = '{time_to_insert}' WHERE user_id = '{user_id}'"

    execute_query(conn, query)

    

def fetch_last_fish_collection_difference(conn, user_id, update_collection_time =False):
    """
    -> get last collection time
    -> get current time
    -> if update_collection=True: update the old collection time with currecnt time
    -> return their diff
    """

    # converted to datetime for subtracting
    last_collection = datetime.fromisoformat(fetch_last_collection(conn, user_id))
    current_time = datetime.today()

    if update_collection_time:
        update_last_collection(conn, user_id, time_to_insert= current_time)

    time_diff = current_time - last_collection

    # return total difference till 2 decimal points
    return round(time_diff.total_seconds(), 2)




def main():
    import doctest
    doctest.testmod()


    
    
if __name__ == "__main__":
    main()




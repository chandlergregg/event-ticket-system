import mysql.connector
import csv

def get_db_connection(user, password, host = 'localhost', port = '3306'):
    """
    Establishes MySQL connection

    Args:
        user: MySQL username
        password: MySQL password
        host: Optional
        port: Optional

    Returns:
        MySQL connection object
    """

    # Configure connection settings
    connection = None
    config = {
        'user': user,
        'password': password,
        'host': host,
        'port': port
    }

    try:
        connection = mysql.connector.connect(**config)
    except Exception as error:
        print(f"Error while connecting to database: {error}")
    
    return connection

def create_database_table(connection, database, table_name):
    """
    Creates database and table for ticketing system

    Args:
        connection: MySQL connection object
        database: Name of database to be created
        table_name: Name of table to hold ticket info

    Returns:
        None
    
    Raises:
        MySQL error if anything goes wrong with statements
    """

    # Create database, create table
    sql_statement = f"""
        DROP DATABASE IF EXISTS {database};
        CREATE DATABASE {database};
        USE {database};
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name} (
            ticket_id int
            , trans_date date
            , event_id int
            , event_name varchar(50)
            , event_date date
            , event_type varchar(10)
            , event_city varchar(20)
            , event_addr varchar(100)
            , customer_id int
            , price decimal
            , num_tickets int
            , primary key (ticket_id)
        );
    """

    # Split up statement into individual queries
    queries = [ f"{query.strip()};" for query in sql_statement.split(";")[:-1] ]

    # Get cursor from connection, try running all queries, close, and return
    for query in queries:
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
        except Exception as error:
            print(f"Error executing query: {error}")
    
    cursor.close()
    return

def load_third_party(connection, filename, database, table_name, column_string, has_headers = False):
    """
    Loads third party data for ticketing system

    Args:
        connection: MySQL connection object
        filename: Name of csv file from which to load data
        database: Name of database in which to insert
        table_name: Name of table in which to insert
        column_string: String of column names for insert statement
        has_headers: Optional; only to be used if CSV has headers

    Returns:
        None

    Raises:
        MySQL error if anything goes wrong with statements
    """

    # Get cursor object and initialize values list
    insert_values = []

    # Read lines into list
    with open(filename, "r") as file:
    
        csv_reader = csv.reader(file)
        if has_headers: 
            next(csv_reader)

        for line in csv_reader:
            line = [ None if val == '' else val for val in line ]
            insert_values.append(tuple(line))

    # Prepare SQL statement
    values_string = "(" + ("%s," * (len(line) - 1)) + "%s)"
    statement = f"INSERT INTO {table_name} {column_string} VALUES {values_string}"
    
    # Get cursor and execute insert statement
    cursor = connection.cursor()
    try:
        cursor.executemany(statement, insert_values)
        connection.commit()
    except Exception as error:
        print(f"Error while executing statement: {error}")

    # Close cursor, return
    cursor.close()
    return

def query_popular_tickets(connection, database, table_name):
    """
    Print 3 most popular events by total tickets sold

    Args:
        connection: MySQL connection object
        database: Name of database from which to query
        table_name: Name of table from which to query

    Returns:
        List of 3 most popular events

    Raises:
        MySQL error if anything goes wrong with statements
    """

    # Get the most popular ticket in the past month
    sql_statement = f"""
        SELECT event_name
        FROM {database}.{table_name}
        GROUP BY event_name
        ORDER BY sum(num_tickets)
        LIMIT 3
    """

    # Query for records
    try:
        cursor = connection.cursor()
        cursor.execute(sql_statement)
        records = cursor.fetchall()
    except Exception as error:
        print(f"Error executing query: {error}")

    # Print results
    print("Most popular events for the last month:")
    for record in records:
        print(f"- {record[0]}")
        
    # Close cursor and return
    cursor.close()
    return records

def main():

    # Connection settings
    user = 'root'
    password = ''
    
    # File to load and table settings
    filename = 'third_party_sales.csv'
    database = 'ticketing_system'
    table_name = 'ticket_sales'
    column_string = "(ticket_id, trans_date, event_id, event_name, event_date, \
        event_type, event_city, customer_id, price, num_tickets)"
    
    # Establish connection, create db, load third party data
    connection = get_db_connection(user, password)
    create_database_table(connection, database, table_name)
    load_third_party(connection, filename, database, table_name, column_string)

    # Get most popular events
    query_popular_tickets(connection, database, table_name)

    # Disconnect
    connection.close()
    return

if __name__ == "__main__":
    main()
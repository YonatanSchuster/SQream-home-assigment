import time
from datetime import datetime  # Add this import
import psycopg2
import re
import os
from io import StringIO
from env import Env
from queries import Queries


def make_connection():
    try:
        connect = psycopg2.connect(
            database="SQream",
            user="postgres",
            password="0543036908",
            host="localhost",
            port="5432"
        )
        connect.autocommit = True
        cursor = connect.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'SQream';")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE 'SQream';")
        cursor.close()
        print("connected")
        return connect
    except psycopg2.OperationalError as e:
        print("Error connecting to the DB: " , e)
        return None



def create_schema():
    connection = make_connection()
    if not connection:
        return
    connect = connection.cursor()
    print("create_schema after connection")
    with open('Schema/tpch-schema.sql', 'r') as data:
        queries = data.read().split(";")
        for query in queries:
            if not query.strip():
                continue
            connect.execute(query)

    connection.commit()
    connection.close()


def parse_schema_file(file_path):
    tables = []
    table_columns = {}

    with open(file_path, 'r') as file:
        schema_content = file.read()
    # Split the schema content into separate queries
    schema_queries = schema_content.split(';')
    for query in schema_queries:
        query = query.strip()
        if query.startswith("CREATE TABLE"):
            lines = query.split('\n')
            table_name = lines[0].split()[-1]

            columns = []
            for line in lines[1:]:
                line = line.strip().rstrip(',')
                if line:
                    column_name = line.split()[0]
                    columns.append(column_name)
            table_columns[table_name] = ", ".join(columns).replace("(,", "").replace(", )", "")
            tables.append(table_name)

    return tables, table_columns




# Commit the changes and close the connection

def load_data():
    connection = make_connection()
    if not connection:
        return

    # Define column names for each table using parse_schema_file function
    tables, table_columns = parse_schema_file('Schema/tpch-schema.sql')

    with connection.cursor() as cursor:
        # Load data from tpch_data files for each table
        for table in tables:
            tbl_file = os.path.join('/Users/yonatanschuster/PycharmProjects/SQream-home-assigment/tpch_data', f"{table}.tbl")
            with open(tbl_file, "r") as file:
                lines = [line.strip() for line in file if not line.startswith('|')]

            lines_data = "\n".join(lines)

            columns = table_columns[table]
            copy_query = f"COPY {table} ({columns}) FROM STDIN DELIMITER '|' CSV;"
            cursor.copy_expert(copy_query, file=StringIO(lines_data))
            print(f"{table} - done!")

    connection.commit()
    connection.close()

def create_results():
    connection = make_connection()
    if not  connection:
        return
    cursor = connection.cursor()
    cursor.execute(Queries.create_table_query %"tpch_results")
    cursor.commit()
    cursor.close()

def save_results(query_name, execution_time):
    connection = make_connection()
    if not connection:
        return
    cursor = connection.cursor()

    # Get the current timestamp
    run_datetime = datetime.now()

    # Use the correct insert_query with three placeholders for values
    cursor.execute(Queries.insert_query, (run_datetime, query_name, execution_time))

    connection.commit()
    connection.close()

def run_benchmark(args):

    connection = make_connection()
    if not connection:
        return
    cursor = connection.cursor()

    # Run tpch queries and calculate execution time
    query_benchmark = []
    queries = {
        "tpch5": Queries.tpch_queries.get('tpch5'),
        "tpch7": Queries.tpch_queries.get('tpch7')
    }

    for query_name, query in queries.items():
        if query is None:  # Check if the query was retrieved successfully
            print(f"Query {query_name} not found.")
            continue
        started_at = time.time()
        cursor.execute(query)
        execution_time = time.time() - started_at
        query_benchmark.append((query_name, execution_time))
        print(f"exec time: {execution_time:.2f} seconds")  # Fix the execution time printing
    connection.close()

    for query_name, execution_time in query_benchmark:
        print(f"The execution time for {query_name}. is: {execution_time:.2f} seconds")

        if args.save_results:
            save_results(query_name, execution_time)

def fetch_results():
    connection = make_connection()
    if not connection:
        return

    cursor = connection.cursor()

    # Define the SELECT query to fetch data from tpch_results table
    select_query = Queries.select_query

    try:
        # Execute the SELECT query
        cursor.execute(select_query)

        # Fetch all the rows from the result set
        results = cursor.fetchall()
        for result in results:
            run_datetime, tpch_query_name, benchmark_result = result
            print(f"Run Datetime: {run_datetime}, Query Name: {tpch_query_name}, Benchmark Result: {benchmark_result}")

    except psycopg2.Error as e:
        print(f"Error fetching data from tpch_results: {e}")

    connection.close()
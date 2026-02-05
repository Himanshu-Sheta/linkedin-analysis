import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="testdb",   # use your real DB name
        user="postgres",
        password="1234"        # your real password
    )

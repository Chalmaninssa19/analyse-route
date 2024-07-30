import psycopg2

# class pour avoir le connection
def get_connection():
    return psycopg2.connect(database="road", host="localhost", user="postgres", password="postgres")
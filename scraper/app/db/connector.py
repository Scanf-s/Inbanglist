import os
from psycopg2 import connect, extras, pool
from psycopg2 import Error as DB_Error
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

connection_pool = pool.SimpleConnectionPool(1, 10,
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

def execute_query(query, params=None, many=False):
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cur:
            if many:
                extras.execute_values(cur, query, params)
            else:
                cur.execute(query, params)
            conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        raise
    finally:
        connection_pool.putconn(conn)

def truncate_table():
    truncate_query = "TRUNCATE TABLE live_streaming_table RESTART IDENTITY;"
    execute_query(truncate_query)

def insert(datas):
    truncate_table()
    insert_query = """
        INSERT INTO live_streaming_table
        (channel_name, thumbnail, concurrent_viewers, title, platform, 
        streaming_link, channel_link, channel_description, 
        channel_followers, created_at, updated_at, channel_profile_image)
        VALUES %s
    """

    values = [tuple(data.values()) for data in datas]
    execute_query(insert_query, values, many=True)

def select_all():
    select_query = """
        SELECT * FROM live_streaming_table;
    """
    
    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()
        cur.execute(select_query)
        rows = cur.fetchall()
        return rows
    except DB_Error as e:
        print(f"Error: {e}")
    finally:
        cur.close()

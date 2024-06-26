import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

def insert(datas):
    truncate_query = """
        TRUNCATE TABLE live_streaming_table RESTART IDENTITY;
    """

    insert_query = """
        INSERT INTO live_streaming_table (channel_name, thumbnail, concurrent_viewers, title, platform, streaming_link, channel_link, channel_description, followers, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = [tuple(data.values()) for data in datas]

    try:
        cur = conn.cursor()
        cur.execute(truncate_query)
        cur.executemany(insert_query, values)
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def select_all():
    select_query = """
        SELECT * FROM live_streaming_table;
    """
    
    try:
        cur = conn.cursor()
        cur.execute(select_query)
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cur.close()

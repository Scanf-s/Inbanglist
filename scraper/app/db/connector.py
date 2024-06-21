import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER= os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOST= os.getenv("DB_HOST")
DB_PORT= os.getenv("DB_PORT")

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

def insert(datas):
    for jsons in datas:
        print(len(jsons))
        platform = jsons.pop(0) 
        if platform != 'youtube':
            continue
        print(len(jsons))
        
        insert_query = """
            INSERT INTO {} (thumbnail, link, title, channel_name, viewers)
            VALUES {}
        """.format(platform, ', '.join(['%s'] * len(jsons)))

        cur = conn.cursor()
        values = [tuple(json.values()) for json in jsons]
        cur.execute(insert_query, values)

        conn.commit()

    cur.close()
    conn.close()

        
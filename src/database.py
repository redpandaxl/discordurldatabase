import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        client_encoding='UTF8'
    )
    return conn


def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls_data (
            id SERIAL PRIMARY KEY,
            channel_name VARCHAR(255),
            channel_id BIGINT,
            timestamp TIMESTAMP,
            url TEXT,
            author VARCHAR(255),
            message_content TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


def insert_url_data(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = sql.SQL("""
        INSERT INTO urls_data (channel_name, channel_id, timestamp, url, author, message_content)
        VALUES (%s, %s, %s, %s, %s, %s)
    """)
    cursor.execute(insert_query, (
        data['channel_name'],
        data['channel_id'],
        data['timestamp'],
        data['url'],
        data['author'],
        data['message_content']
    ))
    conn.commit()
    cursor.close()
    conn.close()

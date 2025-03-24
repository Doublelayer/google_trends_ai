import sqlite3
import json

from logger_config import logger

def create_table():
    logger.info("Start creating database table")
    conn = sqlite3.connect('trends.db')
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trends (
            trend TEXT,
            search_volume TEXT,
            summary TEXT,
            urls TEXT
        )
        ''')
    finally:
        conn.commit()
        conn.close()

def is_trend_exists(trend_name):
    conn = sqlite3.connect('trends.db')
    try:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT 1 FROM trends WHERE trend = ? LIMIT 1
        ''', (trend_name,))
        result = cursor.fetchone()
        found_ = result is not None
        logger.info(f"Trend found in database: {found_}")
        return found_
    finally:
        conn.close()

def save_trends(items):
    logger.info(f"Start saving {len(items)} trends to database")
    conn = sqlite3.connect('trends.db')
    try:
        cursor = conn.cursor()
        cursor.executemany('''
        INSERT INTO trends (trend, search_volume, summary, urls)
        VALUES (?, ?, ?, ?)
        ''', [(item['trend'], item['search_volume'], item['summary'], json.dumps(item['sources'])) for item in items])
    finally:
        conn.commit()
        conn.close()

create_table()
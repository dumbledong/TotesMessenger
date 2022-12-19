import os
import sys
import sqlite3

from urllib.parse import urlparse

from settings import IGNORED_BOTH, WATCHED_LINKS, WATCHED_SOURCES, IGNORED_USERS


db = sqlite3.connect('totes.sqlite3')
cur = db.cursor()

def create_tables():
    """
    Create tables.
    """

    cur.execute("""
    CREATE TABLE subreddits (
        name         TEXT  PRIMARY KEY,
        watch_source BOOLEAN      DEFAULT FALSE,
        watch_link   BOOLEAN      DEFAULT FALSE,
        language     TEXT         DEFAULT 'en',
        t            TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE users (
        name         TEXT  PRIMARY KEY,
        watch_source  BOOLEAN      DEFAULT FALSE,
        watch_link    BOOLEAN      DEFAULT FALSE,
        t            TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE sources (
        id         TEXT  PRIMARY KEY,
        reply      TEXT  UNIQUE,
        subreddit  TEXT,
        author     TEXT,
        title      TEXT,
        watch      BOOLEAN      DEFAULT FALSE,
        t          TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE links (
        id         TEXT   PRIMARY KEY,
        source     TEXT,
        subreddit  TEXT,
        author     TEXT,
        title      TEXT,
        permalink  TEXT,
        watch      BOOLEAN       DEFAULT TRUE,
        t          TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE INDEX ON links (source)
    """)

    db.commit()
    print("Tables ready.")

def sub_exists(sub):
    cur.execute("SELECT 1 FROM subreddits WHERE name=? LIMIT 1", (sub,))
    return True if cur.fetchone() else False

def user_exists(user):
    cur.execute("SELECT 1 FROM users WHERE name=? LIMIT 1", (user,))
    return True if cur.fetchone() else False

def populate_db():
    for sub in WATCHED_SOURCES:
        if sub_exists(sub):
            print("Updating {}".format(sub))
            cur.execute("""
            UPDATE subreddits SET watch_source=%s
            WHERE name=%s
            """, (True, sub))
        else:
            print("Inserting {}".format(sub))
            cur.execute("""
            INSERT INTO subreddits (name, watch_source)
            VALUES (%s, %s)
            """, (sub, True))

    for sub in IGNORED_BOTH:
        if sub_exists(sub):
            print("Updating {}".format(sub))
            cur.execute("""
            UPDATE subreddits SET watch_source=%s, watch_link=%s
            WHERE name=%s
            """, (False, False, sub))
        else:
            print("Inserting {}".format(sub))
            cur.execute("""
            INSERT INTO subreddits (name, watch_source, watch_link)
            VALUES (%s, %s, %s)
            """, (sub, False, False))

    for sub in WATCHED_LINKS:
        if sub_exists(sub):
            print("Updating {}".format(sub))
            cur.execute("""
            UPDATE subreddits SET watch_link=%s
            WHERE name=%s
            """, (True, sub))
        else:
            print("Inserting {}".format(sub))
            cur.execute("""
            INSERT INTO subreddits (name, watch_link)
            VALUES (%s, %s)
            """, (sub, True))

    for user in IGNORED_USERS:
        if user_exists(user):
            print("Updating {}".format(user))
            cur.execute("""
            UPDATE users SET watch_link=%s
            WHERE name=%s
            """, (False, user))
        else:
            print("Inserting {}".format(user))
            cur.execute("""
            INSERT INTO users (name, watch_link) VALUES (%s, %s)
            """, (user, False))

    db.commit()
    print("Default settings setup.")

if __name__ == '__main__':
    if 'create' in sys.argv:
        create_tables()

    if 'populate' in sys.argv:
        populate_db()

db.close()


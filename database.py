import sqlite3

def init_db():
    conn = sqlite3.connect("auctions.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS auctions (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              start_price REAL NOT NULL,
              current_price REAL NOT NULL,
              status TEXT DEFAULT 'active'
          )
      """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS bids (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              auction_id INTEGER NOT NULL,
              bidder_name TEXT NOT NULL,
              amount REAL NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (auction_id) REFERENCES auctions (id)
          )
      """)


    conn.commit()
    conn.close()

init_db()


def create_auction(title, start_price):
    conn = sqlite3.connect("auctions.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO auctions(title, start_price, current_price) VALUES (?, ?, ?)", (title, start_price, start_price))

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return new_id

def place_bid(auction_id, bidder_name, amount):
    conn = sqlite3.connect("auctions.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO bids(auction_id, bidder_name, amount) VALUES (?, ?, ?)",(auction_id, bidder_name, amount))

    cursor.execute("UPDATE auctions SET current_price = ? where id = ?",(amount, auction_id))

    conn.commit()
    conn.close()

def get_auction(auction_id):
    conn = sqlite3.connect("auctions.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, start_price, current_price, status FROM auctions WHERE id = ?",(auction_id,))

    row = cursor.fetchone()

    if row:
      return {
          "id": row[0],
          "title": row[1],
          "start_price": row[2],
          "current_price": row[3],
          "status": row[4]
      }
    return None

create_auction("Mechanical Keyboard", 50.0)

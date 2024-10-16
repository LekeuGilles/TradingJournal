# src/database.py

import sqlite3


def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect('../data/trading_journal.db')



def create_table():
    """Create the trades table if it doesn't exist."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_type TEXT NOT NULL,
        trading_pair TEXT NOT NULL,
        entry_price REAL NOT NULL,
        exit_price REAL,
        position_size REAL NOT NULL,
        trade_date TEXT NOT NULL,
        notes TEXT
    )
    ''')

    conn.commit()
    conn.close()


def add_trade(trade_type, trading_pair, entry_price, exit_price, position_size, trade_date, notes):
    """Add a new trade to the database."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO trades (trade_type, trading_pair, entry_price, exit_price, position_size, trade_date, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (trade_type, trading_pair, entry_price, exit_price, position_size, trade_date, notes))

    conn.commit()
    conn.close()
    print("Trade added successfully!")


def fetch_all_trades():
    """Fetch all trades from the database."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM trades')
    trades = cursor.fetchall()

    conn.close()
    return trades  # Return the list of trades


# Call this function in the main block if you want to see all trades after adding them
if __name__ == "__main__":
    create_table()
    add_trade('buy', 'BTC/USDT', 45000, None, 0.1, '2024-10-14', 'First trade in the journal.')
    add_trade('sell', 'ETH/USDT', 3000, 3100, 0.5, '2024-10-15', 'Profitable trade.')
    fetch_all_trades()  # Fetch and print trades

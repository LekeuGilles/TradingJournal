# src/gui.py

import tkinter as tk
from tkinter import messagebox, ttk
from src.database import add_trade, fetch_all_trades
from src.bybit_api import get_wallet_balance

class TradingJournalApp:
    def __init__(self, master):
        self.master = master
        master.title("Bybit Trading Journal")
        master.geometry("600x400")  # Set a window size
        master.configure(bg="#FFFFFF")  # White background

        self.fetch_wallet_balance_button = tk.Button(master, text="Fetch Wallet Balance",
                                                     command=self.fetch_wallet_balance, bg="#007ACC", fg="#FFFFFF")
        self.fetch_wallet_balance_button.pack(pady=10)

        # Trade Entry Frame
        self.entry_frame = tk.Frame(master, bg="#FFFFFF")
        self.entry_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

        # Trade Type
        self.trade_type_label = tk.Label(self.entry_frame, text="Trade Type:", bg="#FFFFFF", fg="#000000")
        self.trade_type_label.grid(row=0, column=0, sticky="w", pady=5)
        self.trade_type = ttk.Combobox(self.entry_frame, values=["Buy", "Sell"], style="TCombobox")
        self.trade_type.grid(row=0, column=1, pady=5)

        # Trading Pair
        self.trading_pair_label = tk.Label(self.entry_frame, text="Trading Pair:", bg="#FFFFFF", fg="#000000")
        self.trading_pair_label.grid(row=1, column=0, sticky="w", pady=5)
        self.trading_pair = tk.Entry(self.entry_frame, bg="#F0F0F0", fg="#000000", insertbackground='black')
        self.trading_pair.grid(row=1, column=1, pady=5)

        # Entry Price
        self.entry_price_label = tk.Label(self.entry_frame, text="Entry Price:", bg="#FFFFFF", fg="#000000")
        self.entry_price_label.grid(row=2, column=0, sticky="w", pady=5)
        self.entry_price = tk.Entry(self.entry_frame, bg="#F0F0F0", fg="#000000", insertbackground='black')
        self.entry_price.grid(row=2, column=1, pady=5)

        # Exit Price
        self.exit_price_label = tk.Label(self.entry_frame, text="Exit Price:", bg="#FFFFFF", fg="#000000")
        self.exit_price_label.grid(row=3, column=0, sticky="w", pady=5)
        self.exit_price = tk.Entry(self.entry_frame, bg="#F0F0F0", fg="#000000", insertbackground='black')
        self.exit_price.grid(row=3, column=1, pady=5)

        # Position Size
        self.position_size_label = tk.Label(self.entry_frame, text="Position Size:", bg="#FFFFFF", fg="#000000")
        self.position_size_label.grid(row=4, column=0, sticky="w", pady=5)
        self.position_size = tk.Entry(self.entry_frame, bg="#F0F0F0", fg="#000000", insertbackground='black')
        self.position_size.grid(row=4, column=1, pady=5)

        # Trade Date
        self.trade_date_label = tk.Label(self.entry_frame, text="Trade Date:", bg="#FFFFFF", fg="#000000")
        self.trade_date_label.grid(row=5, column=0, sticky="w", pady=5)
        self.trade_date = tk.Entry(self.entry_frame, bg="#F0F0F0", fg="#000000", insertbackground='black')
        self.trade_date.grid(row=5, column=1, pady=5)

        # Notes
        self.notes_label = tk.Label(self.entry_frame, text="Notes:", bg="#FFFFFF", fg="#000000")
        self.notes_label.grid(row=6, column=0, sticky="w", pady=5)
        self.notes = tk.Entry(self.entry_frame, bg="#F0F0F0", fg="#000000", insertbackground='black')
        self.notes.grid(row=6, column=1, pady=5)

        # Submit Button
        self.submit_button = tk.Button(master, text="Add Trade", command=self.add_trade, bg="#007ACC", fg="#FFFFFF")
        self.submit_button.pack(pady=10)

        # Trade History Display
        self.history_frame = tk.Frame(master, bg="#FFFFFF")
        self.history_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.history_label = tk.Label(self.history_frame, text="Trade History:", bg="#FFFFFF", fg="#000000")
        self.history_label.pack()

        self.history_tree = ttk.Treeview(self.history_frame, columns=("Trade Type", "Trading Pair", "Entry Price", "Exit Price", "Position Size", "Trade Date", "Notes"), show='headings')
        self.history_tree.tag_configure('oddrow', background='#F0F0F0')
        self.history_tree.tag_configure('evenrow', background='#FFFFFF')

        for col in self.history_tree["columns"]:
            self.history_tree.heading(col, text=col, anchor=tk.W)
            self.history_tree.column(col, anchor=tk.W)  # Align columns to the left

        self.history_tree.pack(fill=tk.BOTH, expand=True)

        self.load_trade_history()

    def add_trade(self):
        """Add trade to the database and refresh trade history."""
        try:
            trade_type = self.trade_type.get()
            trading_pair = self.trading_pair.get()
            entry_price = float(self.entry_price.get())
            exit_price = float(self.exit_price.get()) if self.exit_price.get() else None
            position_size = float(self.position_size.get())
            trade_date = self.trade_date.get()
            notes = self.notes.get()

            add_trade(trade_type, trading_pair, entry_price, exit_price, position_size, trade_date, notes)
            self.load_trade_history()  # Refresh trade history display
            messagebox.showinfo("Success", "Trade added successfully!")
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid data.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_trade_history(self):
        """Load and display trade history from the database."""
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)  # Clear existing entries

        trades = fetch_all_trades()  # Fetch trades from the database
        for index, trade in enumerate(trades):
            if index % 2 == 0:
                self.history_tree.insert("", "end", values=trade[1:], tags=('evenrow',))  # Skip the ID field
            else:
                self.history_tree.insert("", "end", values=trade[1:], tags=('oddrow',))

    def fetch_wallet_balance(self):
        """Fetch and display the wallet balance."""
        try:
            wallet_balance = get_wallet_balance("your_api_key", "your_api_secret")
            if wallet_balance:
                balance_info = f"Wallet Balance:\n" \
                               f"Total: {wallet_balance.get('total', 'N/A')}\n" \
                               f"Available: {wallet_balance.get('available', 'N/A')}\n" \
                               f"Locked: {wallet_balance.get('locked', 'N/A')}"
                messagebox.showinfo("Wallet Balance", balance_info)
            else:
                messagebox.showerror("Error", "Could not fetch wallet balance.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingJournalApp(root)
    root.mainloop()

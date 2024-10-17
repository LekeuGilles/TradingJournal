import tkinter as tk
from tkinter import messagebox, ttk
from src.database import add_trade, fetch_all_trades
import os
import requests
from src.bybit_api import get_wallet_balance

class TradingJournalApp:
    def __init__(self, master):
        self.master = master
        master.title("Bybit Trading Journal")
        master.geometry("800x600")  # Adjusted window size
        master.configure(bg="#FFFFFF")  # White background

        self.fetch_wallet_balance_button = tk.Button(master, text="Fetch Wallet Balance",
                                                     command=self.display_wallet_balance, bg="#007ACC", fg="#FFFFFF")
        self.fetch_wallet_balance_button.pack(pady=10)

        # Wallet Balance Display
        self.balance_frame = tk.Frame(master, bg="#000000", bd=2, relief=tk.RIDGE)
        self.balance_frame.place(relx=0.75, rely=0.05, anchor='n')

        self.balance_label = tk.Label(self.balance_frame, text="Wallet Balance (USD):", bg="#FFFFFF", fg="#000000")
        self.balance_label.pack()

        self.balance_value = tk.Label(self.balance_frame, text="", bg="#FFFFFF", fg="#000000")
        self.balance_value.pack()

        # Currency Conversion Button
        self.convert_button = tk.Button(self.balance_frame, text="Convert to EUR", command=self.convert_to_eur, bg="#007ACC", fg="#FFFFFF")
        self.convert_button.pack(pady=10)

        self.eur_value_label = tk.Label(self.balance_frame, text="", bg="#FFFFFF", fg="red")
        self.eur_value_label.pack()

        # Trade Entry Frame
        self.entry_frame = tk.Frame(master, bg="#FFFFFF")
        self.entry_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

        self.setup_entry_fields()

        # Trade History Display
        self.history_frame = tk.Frame(master, bg="#FFFFFF")
        self.history_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)
        self.setup_history_display()

        self.load_trade_history()

    def setup_entry_fields(self):
        # Setup labels and entry fields for trade data
        labels = ["Trade Type:", "Trading Pair:", "Entry Price:", "Exit Price:", "Position Size:", "Trade Date:", "Notes:"]
        attributes = ["trade_type", "trading_pair", "entry_price", "exit_price", "position_size", "trade_date", "notes"]
        for i, label in enumerate(labels):
            setattr(self, attributes[i] + '_label', tk.Label(self.entry_frame, text=label, bg="#FFFFFF", fg="#000000"))
            getattr(self, attributes[i] + '_label').grid(row=i, column=0, sticky="w", pady=5)
            if attributes[i] == "trade_type":
                setattr(self, attributes[i], ttk.Combobox(self.entry_frame, values=["Buy", "Sell"], state="readonly"))
            else:
                setattr(self, attributes[i], tk.Entry(self.entry_frame, bg="#F0F0F0", fg="#000000", insertbackground='black'))
            getattr(self, attributes[i]).grid(row=i, column=1, pady=5, padx=10, sticky="ew")

        self.submit_button = tk.Button(self.entry_frame, text="Add Trade", command=self.add_trade, bg="#007ACC", fg="#FFFFFF")
        self.submit_button.grid(row=len(labels), columnspan=2, pady=10)

    def setup_history_display(self):
        self.history_label = tk.Label(self.history_frame, text="Trade History:", bg="#FFFFFF", fg="#000000")
        self.history_label.pack()
        self.history_tree = ttk.Treeview(self.history_frame, columns=("Trade Type", "Trading Pair", "Entry Price", "Exit Price", "Position Size", "Trade Date", "Notes"), show='headings')
        for col in self.history_tree["columns"]:
            self.history_tree.heading(col, text=col, anchor=tk.W)
            self.history_tree.column(col, anchor=tk.W)
        self.history_tree.pack(fill=tk.BOTH, expand=True)

    def display_wallet_balance(self):
        """Fetch the wallet balance and update the GUI."""
        api_key = os.getenv("BYBIT_API_KEY")
        api_secret = os.getenv("BYBIT_API_SECRET")
        balance_data = get_wallet_balance(api_key, api_secret)
        if balance_data and 'result' in balance_data:
            balance_info = f"Total: {balance_data['total']}\nAvailable: {balance_data['available']}"
            self.balance_value.config(text=balance_info)
        else:
            messagebox.showerror("Error", "Failed to fetch wallet balance.")

    def convert_to_eur(self):
        """Convert USD to EUR."""
        try:
            usd_amount = float(self.balance_value.cget("text").split()[1])
            eur_rate = self.fetch_eur_rate()
            eur_amount = usd_amount * eur_rate
            self.eur_value_label.config(text=f"€{eur_amount:.2f} EUR")
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))

    def fetch_eur_rate(self):
        # Placeholder for fetching the EUR conversion rate
        return 0.95  # Example: 1 USD = 0.95 EUR

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
            self.load_trade_history()
            messagebox.showinfo("Success", "Trade added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_trade_history(self):
        """Load and display trade history from the database."""
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)  # Clear existing entries
        trades = fetch_all_trades()
        for index, trade in enumerate(trades):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.history_tree.insert("", "end", values=trade[1:], tags=(tag,))

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingJournalApp(root)
    root.mainloop()

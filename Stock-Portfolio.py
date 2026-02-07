import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import os

class StockPortfolioTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker - Indian Rupees")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2c3e50")
        
        # Hardcoded stock prices in Indian Rupees (₹)
        self.stock_prices_inr = {
            "AAPL": 15000.50,   # Apple Inc.
            "TSLA": 20875.25,   # Tesla Inc.
            "MSFT": 28350.80,   # Microsoft
            "GOOGL": 12150.40,  # Alphabet (Google)
            "AMZN": 14608.75,   # Amazon
            "NVDA": 79217.50,   # NVIDIA
            "META": 40437.50,   # Meta Platforms
            "RELIANCE": 2850.60, # Reliance Industries
            "TCS": 3850.75,     # Tata Consultancy Services
            "INFY": 1650.25,    # Infosys
            "HDFCBANK": 1750.40, # HDFC Bank
            "WIPRO": 525.30,    # Wipro
            "HINDUNILVR": 2450.80, # Hindustan Unilever
            "ITC": 435.60,      # ITC Limited
            "SBIN": 650.75      # State Bank of India
        }
        
        self.portfolio = {}
        self.setup_ui()
        
    def setup_ui(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg="#34495e", height=80)
        title_frame.pack(fill="x", pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="📈 STOCK PORTFOLIO TRACKER (INDIAN RUPEES)",
            font=("Arial", 20, "bold"),
            fg="#ecf0f1",
            bg="#34495e"
        )
        title_label.pack(expand=True)
        
        # Main Container
        main_container = tk.Frame(self.root, bg="#2c3e50")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left Frame - Input Section
        left_frame = tk.Frame(main_container, bg="#34495e", relief=tk.RAISED, bd=2)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Available Stocks Section
        stocks_frame = tk.LabelFrame(left_frame, text="📊 Available Stocks", 
                                    font=("Arial", 12, "bold"),
                                    bg="#34495e", fg="#ecf0f1", relief=tk.GROOVE)
        stocks_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview for stocks
        columns = ("Stock", "Price (₹)")
        self.stock_tree = ttk.Treeview(stocks_frame, columns=columns, show="headings", height=10)
        
        # Configure columns
        self.stock_tree.heading("Stock", text="Stock Symbol")
        self.stock_tree.heading("Price (₹)", text="Current Price (₹)")
        self.stock_tree.column("Stock", width=150)
        self.stock_tree.column("Price (₹)", width=150)
        
        # Add scrollbar
        stock_scroll = ttk.Scrollbar(stocks_frame, orient="vertical", command=self.stock_tree.yview)
        self.stock_tree.configure(yscrollcommand=stock_scroll.set)
        
        self.stock_tree.pack(side="left", fill="both", expand=True, padx=(10, 0))
        stock_scroll.pack(side="right", fill="y", padx=(0, 10))
        
        # Populate stock list
        self.populate_stock_list()
        
        # Portfolio Input Section
        input_frame = tk.LabelFrame(left_frame, text="➕ Add to Portfolio", 
                                   font=("Arial", 12, "bold"),
                                   bg="#34495e", fg="#ecf0f1", relief=tk.GROOVE)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Stock selection
        tk.Label(input_frame, text="Stock Symbol:", 
                bg="#34495e", fg="#ecf0f1", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.stock_var = tk.StringVar()
        stock_combo = ttk.Combobox(input_frame, textvariable=self.stock_var, 
                                  values=list(self.stock_prices_inr.keys()),
                                  state="readonly", width=20)
        stock_combo.grid(row=0, column=1, padx=5, pady=5)
        stock_combo.set("Select Stock")
        
        # Quantity input
        tk.Label(input_frame, text="Quantity:", 
                bg="#34495e", fg="#ecf0f1", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.quantity_var = tk.StringVar()
        quantity_entry = tk.Entry(input_frame, textvariable=self.quantity_var, 
                                 font=("Arial", 10), width=23)
        quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Add button
        add_button = tk.Button(input_frame, text="Add Stock", 
                              command=self.add_to_portfolio,
                              bg="#27ae60", fg="white",
                              font=("Arial", 10, "bold"),
                              relief=tk.RAISED, cursor="hand2")
        add_button.grid(row=2, column=0, columnspan=2, pady=10, padx=5, sticky="ew")
        
        # Clear button
        clear_button = tk.Button(input_frame, text="Clear Portfolio", 
                                command=self.clear_portfolio,
                                bg="#e74c3c", fg="white",
                                font=("Arial", 10, "bold"),
                                relief=tk.RAISED, cursor="hand2")
        clear_button.grid(row=3, column=0, columnspan=2, pady=(0, 10), padx=5, sticky="ew")
        
        # Right Frame - Portfolio Display
        right_frame = tk.Frame(main_container, bg="#34495e", relief=tk.RAISED, bd=2)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Portfolio Treeview
        portfolio_frame = tk.LabelFrame(right_frame, text="📋 Your Portfolio", 
                                       font=("Arial", 12, "bold"),
                                       bg="#34495e", fg="#ecf0f1", relief=tk.GROOVE)
        portfolio_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("Stock", "Quantity", "Price (₹)", "Value (₹)")
        self.portfolio_tree = ttk.Treeview(portfolio_frame, columns=columns, show="headings", height=12)
        
        # Configure columns
        self.portfolio_tree.heading("Stock", text="Stock Symbol")
        self.portfolio_tree.heading("Quantity", text="Quantity")
        self.portfolio_tree.heading("Price (₹)", text="Price per Share (₹)")
        self.portfolio_tree.heading("Value (₹)", text="Total Value (₹)")
        
        self.portfolio_tree.column("Stock", width=100)
        self.portfolio_tree.column("Quantity", width=80)
        self.portfolio_tree.column("Price (₹)", width=120)
        self.portfolio_tree.column("Value (₹)", width=120)
        
        # Add scrollbar
        portfolio_scroll = ttk.Scrollbar(portfolio_frame, orient="vertical", command=self.portfolio_tree.yview)
        self.portfolio_tree.configure(yscrollcommand=portfolio_scroll.set)
        
        self.portfolio_tree.pack(side="left", fill="both", expand=True, padx=(10, 0))
        portfolio_scroll.pack(side="right", fill="y", padx=(0, 10))
        
        # Total Value Display
        total_frame = tk.Frame(right_frame, bg="#34495e")
        total_frame.pack(fill="x", padx=10, pady=10)
        
        self.total_label = tk.Label(total_frame, 
                                   text="Total Portfolio Value: ₹0.00",
                                   font=("Arial", 14, "bold"),
                                   bg="#34495e", fg="#f1c40f")
        self.total_label.pack(pady=10)
        
        # Buttons Frame
        button_frame = tk.Frame(right_frame, bg="#34495e")
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Calculate Button
        calc_button = tk.Button(button_frame, text="Calculate Total",
                               command=self.calculate_total,
                               bg="#3498db", fg="white",
                               font=("Arial", 11, "bold"),
                               relief=tk.RAISED, cursor="hand2",
                               width=15)
        calc_button.pack(side="left", padx=5)
        
        # Save Button
        save_button = tk.Button(button_frame, text="Save to TXT File",
                               command=self.save_to_file,
                               bg="#9b59b6", fg="white",
                               font=("Arial", 11, "bold"),
                               relief=tk.RAISED, cursor="hand2",
                               width=15)
        save_button.pack(side="left", padx=5)
        
        # Preview Button
        preview_button = tk.Button(button_frame, text="Preview Report",
                                  command=self.preview_report,
                                  bg="#e67e22", fg="white",
                                  font=("Arial", 11, "bold"),
                                  relief=tk.RAISED, cursor="hand2",
                                  width=15)
        preview_button.pack(side="left", padx=5)
        
        # Status Bar
        self.status_bar = tk.Label(self.root, text="Ready", 
                                  bg="#34495e", fg="#ecf0f1",
                                  font=("Arial", 10), anchor="w",
                                  relief=tk.SUNKEN)
        self.status_bar.pack(side="bottom", fill="x")
    
    def populate_stock_list(self):
        """Populate the stock list in the treeview"""
        for stock, price in self.stock_prices_inr.items():
            self.stock_tree.insert("", "end", values=(stock, f"₹{price:,.2f}"))
    
    def add_to_portfolio(self):
        """Add selected stock to portfolio"""
        stock = self.stock_var.get()
        quantity_str = self.quantity_var.get()
        
        if stock == "Select Stock" or not stock:
            messagebox.showwarning("Warning", "Please select a stock symbol!")
            return
        
        if not quantity_str.isdigit():
            messagebox.showwarning("Warning", "Please enter a valid quantity (whole number)!")
            return
        
        quantity = int(quantity_str)
        if quantity <= 0:
            messagebox.showwarning("Warning", "Quantity must be greater than 0!")
            return
        
        # Check if stock already in portfolio
        if stock in self.portfolio:
            self.portfolio[stock] += quantity
            # Update existing entry
            for item in self.portfolio_tree.get_children():
                values = self.portfolio_tree.item(item)["values"]
                if values[0] == stock:
                    price = self.stock_prices_inr[stock]
                    new_quantity = self.portfolio[stock]
                    new_value = price * new_quantity
                    self.portfolio_tree.item(item, values=(
                        stock, new_quantity, f"₹{price:,.2f}", f"₹{new_value:,.2f}"
                    ))
                    break
        else:
            # Add new entry
            self.portfolio[stock] = quantity
            price = self.stock_prices_inr[stock]
            value = price * quantity
            self.portfolio_tree.insert("", "end", values=(
                stock, quantity, f"₹{price:,.2f}", f"₹{value:,.2f}"
            ))
        
        # Clear inputs
        self.stock_var.set("Select Stock")
        self.quantity_var.set("")
        
        self.update_status(f"Added {quantity} shares of {stock}")
    
    def clear_portfolio(self):
        """Clear the entire portfolio"""
        if not self.portfolio:
            messagebox.showinfo("Info", "Portfolio is already empty!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the entire portfolio?"):
            self.portfolio.clear()
            for item in self.portfolio_tree.get_children():
                self.portfolio_tree.delete(item)
            self.total_label.config(text="Total Portfolio Value: ₹0.00")
            self.update_status("Portfolio cleared")
    
    def calculate_total(self):
        """Calculate total portfolio value"""
        total_value = 0
        
        for item in self.portfolio_tree.get_children():
            values = self.portfolio_tree.item(item)["values"]
            value_str = values[3].replace("₹", "").replace(",", "")
            total_value += float(value_str)
        
        # Format with lakhs/crores if needed
        if total_value >= 10000000:  # 1 Crore
            crores = total_value / 10000000
            display_text = f"Total Portfolio Value: ₹{total_value:,.2f} (₹{crores:.2f} Crores)"
        elif total_value >= 100000:  # 1 Lakh
            lakhs = total_value / 100000
            display_text = f"Total Portfolio Value: ₹{total_value:,.2f} (₹{lakhs:.2f} Lakhs)"
        else:
            display_text = f"Total Portfolio Value: ₹{total_value:,.2f}"
        
        self.total_label.config(text=display_text)
        self.update_status(f"Calculated total: ₹{total_value:,.2f}")
    
    def save_to_file(self):
        """Save portfolio to text file"""
        if not self.portfolio:
            messagebox.showwarning("Warning", "Portfolio is empty! Add some stocks first.")
            return
        
        # Calculate total if not already calculated
        total_value = 0
        portfolio_items = []
        
        for item in self.portfolio_tree.get_children():
            values = self.portfolio_tree.item(item)["values"]
            value_str = values[3].replace("₹", "").replace(",", "")
            total_value += float(value_str)
            portfolio_items.append(values)
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_str = datetime.now().strftime("%d-%m-%Y")
        
        # Create filename with timestamp
        filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("=" * 70 + "\n")
                file.write(" " * 20 + "PORTFOLIO SUMMARY (INDIAN RUPEES)\n")
                file.write("=" * 70 + "\n")
                file.write(f"Generated on: {timestamp}\n")
                file.write(f"Date: {date_str}\n\n")
                
                file.write("STOCK HOLDINGS:\n")
                file.write("-" * 70 + "\n")
                file.write(f"{'Stock':<12} {'Quantity':<12} {'Price (₹)':<15} {'Value (₹)':<20}\n")
                file.write("-" * 70 + "\n")
                
                for item in portfolio_items:
                    stock, qty, price, value = item
                    file.write(f"{stock:<12} {qty:<12} {price:<15} {value:<20}\n")
                
                file.write("-" * 70 + "\n")
                file.write(f"{'TOTAL PORTFOLIO VALUE:':<39} ₹{total_value:,.2f}\n")
                
                # Add Indian numbering system
                if total_value >= 10000000:
                    crores = total_value / 10000000
                    file.write(f"{'IN WORDS:':<39} ₹{crores:.2f} Crores\n")
                elif total_value >= 100000:
                    lakhs = total_value / 100000
                    file.write(f"{'IN WORDS:':<39} ₹{lakhs:.2f} Lakhs\n")
                
                file.write("=" * 70 + "\n\n")
                
                # Summary
                file.write("SUMMARY:\n")
                file.write("-" * 70 + "\n")
                file.write(f"• Number of different stocks: {len(self.portfolio)}\n")
                file.write(f"• Total shares held: {sum(self.portfolio.values())}\n")
                
                if portfolio_items:
                    # Find largest holding
                    largest_item = max(portfolio_items, key=lambda x: float(x[3].replace("₹", "").replace(",", "")))
                    file.write(f"• Largest holding: {largest_item[0]} (Value: {largest_item[3]})\n")
                
                file.write("\n" + "=" * 70 + "\n")
                file.write("Note: Prices are for demonstration purposes only\n")
                file.write("=" * 70 + "\n")
            
            messagebox.showinfo("Success", f"Portfolio saved to:\n{os.path.abspath(filename)}")
            self.update_status(f"Portfolio saved to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def preview_report(self):
        """Show preview of the report in a new window"""
        if not self.portfolio:
            messagebox.showwarning("Warning", "Portfolio is empty! Add some stocks first.")
            return
        
        # Calculate total
        total_value = 0
        portfolio_items = []
        
        for item in self.portfolio_tree.get_children():
            values = self.portfolio_tree.item(item)["values"]
            value_str = values[3].replace("₹", "").replace(",", "")
            total_value += float(value_str)
            portfolio_items.append(values)
        
        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Portfolio Report Preview")
        preview_window.geometry("800x600")
        preview_window.configure(bg="#2c3e50")
        
        # Title
        title_label = tk.Label(preview_window, 
                              text="📄 Portfolio Report Preview",
                              font=("Arial", 16, "bold"),
                              bg="#2c3e50", fg="#ecf0f1")
        title_label.pack(pady=10)
        
        # Text area with scrollbar
        text_frame = tk.Frame(preview_window, bg="#34495e")
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        text_area = scrolledtext.ScrolledText(text_frame, 
                                             font=("Courier New", 10),
                                             bg="#1c2833", fg="#ecf0f1",
                                             wrap=tk.WORD)
        text_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Generate report text
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_str = datetime.now().strftime("%d-%m-%Y")
        
        report_text = "=" * 70 + "\n"
        report_text += " " * 20 + "PORTFOLIO SUMMARY (INDIAN RUPEES)\n"
        report_text += "=" * 70 + "\n"
        report_text += f"Generated on: {timestamp}\n"
        report_text += f"Date: {date_str}\n\n"
        
        report_text += "STOCK HOLDINGS:\n"
        report_text += "-" * 70 + "\n"
        report_text += f"{'Stock':<12} {'Quantity':<12} {'Price (₹)':<15} {'Value (₹)':<20}\n"
        report_text += "-" * 70 + "\n"
        
        for item in portfolio_items:
            stock, qty, price, value = item
            report_text += f"{stock:<12} {qty:<12} {price:<15} {value:<20}\n"
        
        report_text += "-" * 70 + "\n"
        report_text += f"{'TOTAL PORTFOLIO VALUE:':<39} ₹{total_value:,.2f}\n"
        
        # Add Indian numbering system
        if total_value >= 10000000:
            crores = total_value / 10000000
            report_text += f"{'IN WORDS:':<39} ₹{crores:.2f} Crores\n"
        elif total_value >= 100000:
            lakhs = total_value / 100000
            report_text += f"{'IN WORDS:':<39} ₹{lakhs:.2f} Lakhs\n"
        
        report_text += "=" * 70 + "\n"
        
        # Insert text
        text_area.insert("1.0", report_text)
        text_area.configure(state="disabled")  # Make read-only
        
        # Close button
        close_button = tk.Button(preview_window, text="Close Preview",
                                command=preview_window.destroy,
                                bg="#e74c3c", fg="white",
                                font=("Arial", 10, "bold"))
        close_button.pack(pady=10)
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.config(text=f"Status: {message}")

def main():
    root = tk.Tk()
    app = StockPortfolioTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
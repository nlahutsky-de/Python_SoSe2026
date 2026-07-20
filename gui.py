# gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import re
from datetime import datetime
from logic import ExpenseManager
from utils import (
    validate_amount,
    validate_description,
    validate_date,
    validate_category
)
    

class FinanceApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("1050x700")
        self.root.minsize(400, 400)
        
        self.manager = ExpenseManager()
        self._load_seed_data()
        self._create_input_panel()
        self._create_display_panel()
        self.refresh_all_views()

    # Add sample transactions
    def _load_seed_data(self):
        self.manager.add_transaction("Income", "Monthly Paycheck", 3200.00, "2026-07-01", "Salary/Inflow")
        self.manager.add_transaction("Expense", "Apartment Rent", 850.00, "2026-07-02", "Housing")
        self.manager.add_transaction("Expense", "Electric Utility Bill", 95.00, "2026-07-03", "Utilities")
        self.manager.add_transaction("Income", "Freelance Coding Design", 450.00, "2026-07-05", "Salary/Inflow")


    def _create_input_panel(self):
        input_frame = ttk.LabelFrame(self.root, text=" Add Transaction ", padding=15)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=15, pady=10)
        
        # First row
        ttk.Label(input_frame, text="Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.type_combobox = ttk.Combobox(input_frame, values=["Expense", "Income"], width=10, state="readonly")
        self.type_combobox.set("Expense")
        self.type_combobox.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Description:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.desc_entry = ttk.Entry(input_frame, width=20)
        self.desc_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Amount (€):").grid(row=0, column=4, sticky=tk.W, pady=5)
        self.amount_entry = ttk.Entry(input_frame, width=10)
        self.amount_entry.grid(row=0, column=5, padx=5, pady=5)
        
        # Second row
        ttk.Label(input_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Button(input_frame, text="Add Category", command=lambda: self.add_category(parent=self.root)).grid(row=2, column=1, sticky=tk.W, pady=5)
        self.cat_combobox = ttk.Combobox(input_frame, width=15, state="readonly")
        self.cat_combobox.grid(row=1, column=1, padx=5, pady=5)
        self._update_category_combobox()
 
        # Date Input
        ttk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=1, column=3, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=1, column=6, columnspan=2, padx=10, sticky=tk.E)
        ttk.Button(btn_frame, text="Log Transaction", command=self.handle_add_transaction).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="Edit Selected", command=self.open_edit_dialog).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="Delete Row", command=self.handle_delete_transaction).pack(side=tk.LEFT, padx=3)
        
       
    # Creates the main display.
    def _create_display_panel(self):
        # Financial Summary Row Dashboard Cards
        self.metrics_frame = ttk.LabelFrame(self.root, text=" Summary ", padding=10)
        self.metrics_frame.pack(fill=tk.X, padx=15, pady=5)
        
        self.income_lbl = ttk.Label(self.metrics_frame, text="Total Income: €0.00", font=("Helvetica", 10, "bold"), foreground="#27ae60")
        self.income_lbl.pack(side=tk.LEFT, expand=True)
        
        self.expense_lbl = ttk.Label(self.metrics_frame, text="Total Expenses: €0.00", font=("Helvetica", 10, "bold"), foreground="#c0392b")
        self.expense_lbl.pack(side=tk.LEFT, expand=True)
        
        self.savings_lbl = ttk.Label(self.metrics_frame, text="Net Savings: €0.00", font=("Helvetica", 11, "bold"), foreground="#2980b9")
        self.savings_lbl.pack(side=tk.LEFT, expand=True)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # TAB1: Transactions
        self.tab_all = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_all, text=" Transactions")
        
        columns = ("id", "type", "period", "description", "category", "amount")
        self.ledger_tree = ttk.Treeview(self.tab_all, columns=columns, show="headings")
        self.ledger_tree.heading("id", text="ID")
        self.ledger_tree.heading("type", text="Type")
        self.ledger_tree.heading("period", text="Period")
        self.ledger_tree.heading("description", text="Description")
        self.ledger_tree.heading("category", text="Category")
        self.ledger_tree.heading("amount", text="Amount")
        
        self.ledger_tree.column("id", width=50, anchor=tk.CENTER)
        self.ledger_tree.column("type", width=90, anchor=tk.CENTER)
        self.ledger_tree.column("period", width=120, anchor=tk.CENTER)
        self.ledger_tree.column("description", width=260, anchor=tk.W)
        self.ledger_tree.column("category", width=150, anchor=tk.CENTER)
        self.ledger_tree.column("amount", width=100, anchor=tk.E)
        self.ledger_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # TAB2: Categories Insights
        self.tab_categories = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_categories, text=" Categories Insights ")
        
        table_side_frame = ttk.Frame(self.tab_categories)
        table_side_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.category_tree = ttk.Treeview(table_side_frame, columns=("category", "total"), show="headings")
        self.category_tree.heading("category", text="Expense Category")
        self.category_tree.heading("total", text="Total Accumulation Outflow (€)")
        self.category_tree.pack(fill=tk.BOTH, expand=True)
        
        chart_side_frame = ttk.LabelFrame(self.tab_categories, text=" Analytics ", padding=10)
        chart_side_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=5)
        
        self.chart_canvas = tk.Canvas(chart_side_frame, width=420, height=360, bg="white", highlightthickness=0)
        self.chart_canvas.pack(fill=tk.BOTH, expand=True)

        # TAB3: Timeline 
        self.tab_timeline = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_timeline, text="Timeline Summary")
        
        self.timeline_tree = ttk.Treeview(self.tab_timeline, columns=("period", "income", "expense", "savings"), show="headings")
        self.timeline_tree.heading("period", text="Month Cycle")
        self.timeline_tree.heading("income", text="Total Cash Inflow (€)")
        self.timeline_tree.heading("expense", text="Total Cash Outflow (€)")
        self.timeline_tree.heading("savings", text="Net Monthly Savings (€)")
        self.timeline_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _update_category_combobox(self):
        categories = list(self.manager._category_rules.keys())
        self.cat_combobox['values'] = ["Auto-Categorize"] + categories
        self.cat_combobox.set("Auto-Categorize")

    def _is_valid_date(self, date_string):
        # Validate the date format YYYY-MM-DD
        return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date_string))

    def handle_add_transaction(self):
        t_type = self.type_combobox.get()
        desc = self.desc_entry.get().strip()
        amt_str = self.amount_entry.get().strip()
        chosen_cat = self.cat_combobox.get()
        date_str = self.date_entry.get().strip()
        
        try:
            desc = validate_description(desc)
            amount = validate_amount(amt_str)
            date_str = validate_date(date_str)

            if chosen_cat != "Auto-Categorize":
                chosen_cat = validate_category(chosen_cat)

        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
            return

        self.manager.add_transaction(t_type, desc, amount, date_str, chosen_cat)
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.refresh_all_views()

    def add_category(self, parent=None):
        new_cat = simpledialog.askstring(
            "New Category", 
            "Enter name for the new category:", parent=parent
        )
        if not new_cat:
            return
        
        new_cat = new_cat.strip().title()
        if not new_cat:
            messagebox.showwarning("Warning", "Category name cannot be empty.", parent=parent)
            return
        if new_cat in self.manager._category_rules:
            messagebox.showwarning("Warning", f"'{new_cat}' already exists!", parent=parent)
            return

        keywords_str = simpledialog.askstring(
            "Category Keywords", 
            f"Enter starting keywords for '{new_cat}' (separated by commas) or leave blank:",
        )
        
        keywords_set = set()
        if keywords_str:
            keywords_set = {kw.strip().lower() for kw in keywords_str.split(",") if kw.strip()}

        # Save backend rules
        self.manager.create_category(new_cat)
        if keywords_set:
            self.manager.add_keywords_to_category(new_cat, keywords_set)

        # Update the main window combobox values
        self._update_category_combobox()
                
        messagebox.showinfo("Success", f"Category '{new_cat}' created!", parent=parent)

        return new_cat

    def open_edit_dialog(self):
        selected = self.ledger_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select an item to change.")
            return
            
        values = self.ledger_tree.item(selected[0])['values']
        target_id = int(values[0])
        t_obj = self.manager.transactions[target_id]

        edit_win = tk.Toplevel(self.root)
        edit_win.title(f"Edit Transaction Entry ID: {target_id}")
        edit_win.geometry("420x320")
        edit_win.grab_set()

        main_frame = ttk.Frame(edit_win, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        edit_type = ttk.Combobox(main_frame, values=["Expense", "Income"], state="readonly")
        edit_type.set(t_obj.t_type)
        edit_type.grid(row=0, column=1, pady=5)

        ttk.Label(main_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, pady=5)
        edit_desc = ttk.Entry(main_frame, width=22)
        edit_desc.grid(row=1, column=1, pady=5)
        edit_desc.insert(0, t_obj.description)

        ttk.Label(main_frame, text="Amount (€):").grid(row=2, column=0, sticky=tk.W, pady=5)
        edit_amt = ttk.Entry(main_frame, width=22)
        edit_amt.grid(row=2, column=1, pady=5)
        edit_amt.insert(0, f"{t_obj.amount:.2f}")

        ttk.Label(main_frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W, pady=5)
        edit_date_field = ttk.Entry(main_frame, width=22)
        edit_date_field.grid(row=3, column=1, pady=5)
        edit_date_field.insert(0, t_obj.date)

        ttk.Label(main_frame, text="Category:").grid(row=5, column=0, sticky=tk.W, pady=5)
        edit_cat_frame = ttk.Frame(main_frame)
        edit_cat_frame.grid(row=5, column=1, pady=5, sticky=tk.W)

        all_cats = list(self.manager._category_rules.keys()) + ["Other", "Salary/Inflow"]
        edit_cat = ttk.Combobox(main_frame, values=all_cats, state="readonly", width=18)
        edit_cat.set(t_obj.category)
        edit_cat.grid(row=5, column=1, pady=5)

        # This function handles adding categories inside the edit box
        def add_category_from_edit():
            new_cat = self.add_category(parent=edit_win)
            if not new_cat:
                return
            
            # Refresh local edit combobox values
            updated_cats = list(self.manager._category_rules.keys()) + ["Other", "Salary/Inflow"]
            edit_cat['values'] = updated_cats
            edit_cat.set(new_cat) # Set newly created category as chosen
            
        # Quick small "+" button right in the edit layout
        add_cat_row_frame = ttk.Frame(main_frame)
        add_cat_row_frame.grid(row=6, column=1, pady=2, sticky=tk.W)

        add_edit_cat_btn = ttk.Button(add_cat_row_frame, text="+", width=3, command=add_category_from_edit)
        add_edit_cat_btn.pack(side=tk.LEFT)

        helper_lbl = ttk.Label(add_cat_row_frame, text=" Create New Category", font=("Helvetica", 9, "italic"), foreground="gray")
        helper_lbl.pack(side=tk.LEFT, padx=5)

        def save_changes():
            date_input = edit_date_field.get().strip()
            if not self._is_valid_date(date_input):
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.", parent=edit_win)
                return
            
            try:
                desc = validate_description(edit_desc.get())
                amt = validate_amount(edit_amt.get())
                date_input = validate_date(edit_date_field.get())
                category = validate_category(edit_cat.get())

            except ValueError as e:
                messagebox.showerror("Validation Error", str(e), parent=edit_win)
                return            
        
            self.manager.update_transaction(target_id, edit_type.get(), edit_desc.get().strip(), amt, date_input, edit_cat.get())
            self.refresh_all_views()
            edit_win.destroy()

        btn_box = ttk.Frame(main_frame)
        btn_box.grid(row=7, column=0, columnspan=2, pady=10, sticky=tk.E)
        ttk.Button(btn_box, text="Save Changes", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_box, text="Cancel", command=edit_win.destroy).pack(side=tk.LEFT, padx=5)

    def handle_delete_transaction(self):
        selected = self.ledger_tree.selection()
        if not selected: return
        target_id = int(self.ledger_tree.item(selected[0])['values'][0])
        if self.manager.delete_transaction(target_id):
            self.refresh_all_views()

    def _draw_pie_chart(self, sorted_categories, total_expenses):
        self.chart_canvas.delete("all")
        if total_expenses <= 0:
            self.chart_canvas.create_text(210, 180, text="No expense record distribution yet.", font=("Helvetica", 10, "italic"))
            return

        colors = ["#3498db", "#e74c3c", "#f1c40f", "#9b59b6", "#e67e22", "#1abc9c", "#95a5a6"]
        start_angle = 0.0
        cx, cy, radius = 130, 160, 100
        
        for idx, (category, amount) in enumerate(sorted_categories):
            if amount <= 0: continue
            percentage = amount / total_expenses
            extent_angle = percentage * 360.0
            color = colors[idx % len(colors)]
            
            self.chart_canvas.create_arc(
                cx - radius, cy - radius, cx + radius, cy + radius,
                start=start_angle, extent=extent_angle, fill=color, outline="white"
            )
            
            legend_y = 40 + (idx * 24)
            self.chart_canvas.create_rectangle(250, legend_y, 265, legend_y + 12, fill=color, outline="")
            self.chart_canvas.create_text(275, legend_y + 6, text=f"{category} ({percentage:.0%})", anchor=tk.W, font=("Helvetica", 9))
            start_angle += extent_angle

    def refresh_all_views(self):
        # Clear all tables
        for t in (self.ledger_tree, self.category_tree, self.timeline_tree):
            for item in t.get_children(): t.delete(item)

        # 1. Update totals
        totals = self.manager.calculate_totals()
        self.income_lbl.config(text=f"Total Income: €{totals['Income']:.2f}")
        self.expense_lbl.config(text=f"Total Expenses: €{totals['Expense']:.2f}")
        self.savings_lbl.config(text=f"Savings: €{totals['Savings']:.2f}")

        # 2. Update transaction list
        for fid, t in sorted(self.manager.transactions.items(), key=lambda x: x[1].date, reverse=True):
            self.ledger_tree.insert("", tk.END, values=(fid, t.t_type, t.period_string, t.description, t.category, f"€{t.amount:.2f}"))

        # 3. Update category table and pie chart
        cat_totals = self.manager.summarize_by_category()
        sorted_categories = sorted(cat_totals.items(), key=lambda item: item[1], reverse=True)
        for cat, amt in sorted_categories:
            if amt > 0:
                self.category_tree.insert("", tk.END, values=(cat, f"€{amt:.2f}"))
        self._draw_pie_chart(sorted_categories, totals["Expense"])

        # 4. Update timeline
        timeline_data = self.manager.summarize_by_timeline()
        for period, data in sorted(timeline_data.items(), reverse=True):
            p_savings = data["Income"] - data["Expense"]
            self.timeline_tree.insert("", tk.END, values=(period, f"€{data['Income']:.2f}", f"€{data['Expense']:.2f}", f"€{p_savings:.2f}"))


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()

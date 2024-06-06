import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Sharing App")

        self.roommates = []
        self.expenses = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Frame for adding roommates
        self.frame_add_roommate = tk.Frame(self.root)
        self.frame_add_roommate.pack(padx=10, pady=10, fill='x')

        self.label_roommate = tk.Label(self.frame_add_roommate, text="Roommate Name:")
        self.label_roommate.pack(side='left')

        self.entry_roommate = tk.Entry(self.frame_add_roommate)
        self.entry_roommate.pack(side='left', padx=10)

        self.button_add_roommate = tk.Button(self.frame_add_roommate, text="Add Roommate", command=self.add_roommate)
        self.button_add_roommate.pack(side='left')

        self.button_remove_roommate = tk.Button(self.frame_add_roommate, text="Remove Roommate", command=self.remove_roommate)
        self.button_remove_roommate.pack(side='left')

        # Frame for adding expenses
        self.frame_add_expense = tk.Frame(self.root)
        self.frame_add_expense.pack(padx=10, pady=10, fill='x')

        self.label_amount = tk.Label(self.frame_add_expense, text="Amount:")
        self.label_amount.pack(side='left')

        self.entry_amount = tk.Entry(self.frame_add_expense)
        self.entry_amount.pack(side='left', padx=10)

        self.label_description = tk.Label(self.frame_add_expense, text="Description:")
        self.label_description.pack(side='left')

        self.entry_description = tk.Entry(self.frame_add_expense)
        self.entry_description.pack(side='left', padx=10)

        self.label_payer = tk.Label(self.frame_add_expense, text="Payer:")
        self.label_payer.pack(side='left')

        self.payer_var = tk.StringVar()
        self.payer_menu = ttk.Combobox(self.frame_add_expense, textvariable=self.payer_var)
        self.payer_menu.pack(side='left', padx=10)

        self.button_add_expense = tk.Button(self.frame_add_expense, text="Add Expense", command=self.add_expense)
        self.button_add_expense.pack(side='left')

        self.button_remove_expense = tk.Button(self.frame_add_expense, text="Remove Expense", command=self.remove_expense)
        self.button_remove_expense.pack(side='left')

        # Button to calculate balances
        self.button_calculate = tk.Button(self.root, text="Calculate Balances", command=self.calculate_balances)
        self.button_calculate.pack(pady=10)

        # Display for roommates
        self.label_roommates = tk.Label(self.root, text="Roommates:")
        self.label_roommates.pack()

        self.listbox_roommates = tk.Listbox(self.root)
        self.listbox_roommates.pack(padx=10, pady=10, fill='x')

        # Display for expenses
        self.label_expenses = tk.Label(self.root, text="Expenses:")
        self.label_expenses.pack()

        self.listbox_expenses = tk.Listbox(self.root)
        self.listbox_expenses.pack(padx=10, pady=10, fill='x')

        # Display for balances
        self.label_balances = tk.Label(self.root, text="Balances:")
        self.label_balances.pack()

        self.text_balances = tk.Text(self.root, height=10, width=50)
        self.text_balances.pack(padx=10, pady=10)

        # Menu for saving and loading data
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save Data", command=self.save_data)
        self.file_menu.add_command(label="Load Data", command=self.load_data)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

    def add_roommate(self):
        roommate_name = self.entry_roommate.get().strip()
        if roommate_name and roommate_name not in self.roommates:
            self.roommates.append(roommate_name)
            self.entry_roommate.delete(0, tk.END)
            self.listbox_roommates.insert(tk.END, roommate_name)
            self.update_payer_menu()
        else:
            messagebox.showerror("Error", "Roommate name cannot be empty or duplicate")

    def remove_roommate(self):
        selected_index = self.listbox_roommates.curselection()
        if selected_index:
            roommate_name = self.listbox_roommates.get(selected_index)
            self.roommates.remove(roommate_name)
            self.listbox_roommates.delete(selected_index)
            self.update_payer_menu()
        else:
            messagebox.showerror("Error", "Please select a roommate to remove")

    def update_payer_menu(self):
        self.payer_menu['values'] = self.roommates

    def add_expense(self):
        amount = self.entry_amount.get().strip()
        description = self.entry_description.get().strip()
        payer = self.payer_var.get().strip()

        if not amount or not description or not payer:
            messagebox.showerror("Error", "All fields must be filled")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return

        expense = {
            'amount': amount,
            'description': description,
            'payer': payer,
            'participants': self.roommates[:]
        }
        self.expenses.append(expense)
        self.entry_amount.delete(0, tk.END)
        self.entry_description.delete(0, tk.END)
        self.payer_var.set('')
        self.listbox_expenses.insert(tk.END, f"{description}: {amount} (Paid by {payer})")
        messagebox.showinfo("Success", "Expense added successfully")

    def remove_expense(self):
        selected_index = self.listbox_expenses.curselection()
        if selected_index:
            self.expenses.pop(selected_index[0])
            self.listbox_expenses.delete(selected_index)
        else:
            messagebox.showerror("Error", "Please select an expense to remove")

    def calculate_balances(self):
        balances = {roommate: 0 for roommate in self.roommates}
        for expense in self.expenses:
            split_amount = expense['amount'] / len(self.roommates)
            balances[expense['payer']] += expense['amount'] - split_amount
            for participant in expense['participants']:
                if participant != expense['payer']:
                    balances[participant] -= split_amount

        self.text_balances.delete(1.0, tk.END)
        for roommate, balance in balances.items():
            self.text_balances.insert(tk.END, f"{roommate}: {balance:.2f}\n")

    def save_data(self):
        data = {
            'roommates': self.roommates,
            'expenses': self.expenses
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(data, f)
            messagebox.showinfo("Success", "Data saved successfully")

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                data = json.load(f)
            self.roommates = data['roommates']
            self.expenses = data['expenses']
            self.listbox_roommates.delete(0, tk.END)
            self.listbox_expenses.delete(0, tk.END)
            for roommate in self.roommates:
                self.listbox_roommates.insert(tk.END, roommate)
            for expense in self.expenses:
                self.listbox_expenses.insert(tk.END, f"{expense['description']}: {expense['amount']} (Paid by {expense['payer']})")
            self.update_payer_menu()
            messagebox.showinfo("Success", "Data loaded successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()

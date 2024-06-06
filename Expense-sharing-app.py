class Expense:
    def __init__(self, amount, description, date, people_involved):
        self.amount = amount
        self.description = description
        self.date = date
        self.people_involved = people_involved

class BillSplitter:
    def __init__(self):
        self.expenses = []
        self.balances = {}

    def add_expense(self, expense):
        self.expenses.append(expense)
        self.update_balances(expense)

    def update_balances(self, expense):
        total_people = len(expense.people_involved)
        individual_share = expense.amount / total_people
        for person in expense.people_involved:
            if person not in self.balances:
                self.balances[person] = 0
            self.balances[person] += individual_share

    def calculate_balance(self):
        for expense in self.expenses:
            for person in expense.people_involved:
                self.balances[person] -= expense.amount / len(expense.people_involved)

    def get_balance(self):
        return self.balances

# Sample usage
bill_splitter = BillSplitter()

expense1 = Expense(100, "Groceries", "2024-06-06", ["Alice", "Bob"])
bill_splitter.add_expense(expense1)

expense2 = Expense(50, "Dinner", "2024-06-06", ["Alice", "Charlie"])
bill_splitter.add_expense(expense2)

bill_splitter.calculate_balance()
print(bill_splitter.get_balance())

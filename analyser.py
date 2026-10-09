

def calculate_totals(transactions):
    total_income = 0
    total_expenses = 0

    for transaction in transactions:
        money_in = transaction[1]
        money_out = transaction[2]

        if money_in > 0:
            total_income += money_in

        if money_out > 0:
            total_expenses += money_out

    return total_income, total_expenses


transactions = [
    ["Payment Received", 500, 0],
    ["Groceries", 0, 150],
    ["Airtime", 0, 50],
    ["Money Received", 200, 0]
]

income, expenses = calculate_totals(transactions)
balance = income - expenses

print(f"Total income: R{income:.2f}")
print(f"Total expenses: R{expenses:.2f}")
print(f"Money left: R{balance:.2f}")
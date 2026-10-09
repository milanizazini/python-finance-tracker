
transactions = [
    ["Payment Received", 500, 0],
    ["Groceries", 0, 150],
    ["Airtime", 0, 50],
    ["Money Received", 200, 0]
]

total_income = 0
total_expenses = 0

for transaction in transactions:
    description = transaction[0]
    money_in = transaction[1]
    money_out = transaction[2]

    if money_in > 0:
        total_income = total_income + money_in
    else:
        total_expenses = total_expenses + money_out

print("Total income:", total_income)
print("Total expenses:", total_expenses)
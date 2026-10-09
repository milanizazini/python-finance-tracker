


import re

def parse_transactions(filename="data/statement_text.txt"):
    transactions = []

    with open(filename, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()

    for line in lines:
        match = re.match(
            r"^(\d{2}/\d{2}/\d{4})\s+(.+)$",
            line.strip()
        )

        if not match:
            continue

        date, rest = match.groups()

        # Find the category and monetary values at the end.
        # This recognises simple transaction rows such as:
        # 11/07/2026 Payment Received: L Bonya Other Income 700.00 2 296.13
        amount_match = re.search(
            r"\s+([A-Za-z][A-Za-z &/]*)\s+"
            r"(-?[\d ]+\.\d{2})\s+"
            r"([\d ]+\.\d{2})$",
            rest
        )

        if not amount_match:
            continue

        category = amount_match.group(1).strip()
        first_amount = float(amount_match.group(2).replace(" ", ""))
        balance = float(amount_match.group(3).replace(" ", ""))

        description = rest[:amount_match.start()].strip()

        money_in = 0.0
        money_out = 0.0

        if first_amount > 0:
            money_in = first_amount
        elif first_amount < 0:
            money_out = abs(first_amount)

        transactions.append({
            "Date": date,
            "Description": description,
            "Category": category,
            "Money In": money_in,
            "Money Out": money_out,
            "Balance": balance
        })

    return transactions


if __name__ == "__main__":
    records = parse_transactions()

    print("Transactions parsed:", len(records))

    for record in records[:10]:
        print(record)
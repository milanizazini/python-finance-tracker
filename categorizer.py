
def categorize_transaction(description):
    description = description.lower()

    if any(word in description for word in ["shoprite", "checkers", "woolworths", "groceries", "food", "pick n pay"]):
        return "Groceries"

    elif any(word in description for word in ["uber", "bolt", "taxi", "petrol", "fuel"]):
        return "Transport"

    elif any(word in description for word in ["airtime", "data", "vodacom", "mtn", "telkom"]):
        return "Phone and Data"

    elif any(word in description for word in ["salary", "payment received", "money received"]):
        return "Income"

    elif any(word in description for word in ["electricity", "water", "rent"]):
        return "Utilities"

    elif any(word in description for word in ["transfer", "payment to"]):
        return "Transfer"

    else:
        return "Other"


# Test the categorizer
if __name__ == "__main__":
    test_transactions = [
        "Shoprite purchase",
        "Airtime",
        "Payment Received",
        "Uber trip",
        "Electricity payment"
    ]

    for transaction in test_transactions:
        category = categorize_transaction(transaction)
        print(transaction, "->", category)
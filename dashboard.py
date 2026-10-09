

import streamlit as st
import pandas as pd
from transaction_parser import parse_transactions
from categorizer import categorize_transaction

# Page settings
st.set_page_config(
    page_title="My Finance Tracker",
    page_icon="🌸",
    layout="wide"
)

# Dusty pink and white styling
st.markdown("""
<style>
    .stApp {
        background-color: #fff9fa;
        color: #49343d;
    }

    h1, h2, h3 {
        color: #98566e;
    }

    div[data-testid="stMetric"] {
        background-color: #f8e8ed;
        border: 1px solid #efd3dc;
        padding: 20px;
        border-radius: 15px;
    }

    div[data-testid="stMetricLabel"] {
        color: #795361;
    }

    div[data-testid="stMetricValue"] {
        color: #98566e;
    }
</style>
""", unsafe_allow_html=True)

# Dashboard heading
st.title("🌸 My Finance Tracker")
st.write("Your personal money overview")
st.divider()

# Load real transactions from your existing parser
try:
    transactions = parse_transactions()

    if not transactions:
        st.warning(
            "No transactions were found. "
            "Check data/statement_text.txt."
        )
        st.stop()

    df = pd.DataFrame(transactions)

except FileNotFoundError:
    st.error(
        "Statement text file not found. "
        "Please run pdf_reader.py first."
    )
    st.stop()

except Exception as error:
    st.error(f"Could not load transactions: {error}")
    st.stop()

# Ensure required columns exist
for column in ["Date", "Description", "Money In", "Money Out"]:
    if column not in df.columns:
        df[column] = 0.0 if column in [
            "Money In", "Money Out"
        ] else ""

# Convert amounts to numbers
for column in ["Money In", "Money Out"]:
    df[column] = pd.to_numeric(
        df[column], errors="coerce"
    ).fillna(0.0)

# Use your existing categorizer

# Prepare dates for filtering
df["Parsed Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True,
    errors="coerce"
)

valid_dates = df["Parsed Date"].dropna()

if not valid_dates.empty:
    st.subheader("📅 Filter by Date")

    date_col1, date_col2 = st.columns(2)

    with date_col1:
        start_date = st.date_input(
            "Start date",
            value=valid_dates.min().date(),
            min_value=valid_dates.min().date(),
            max_value=valid_dates.max().date()
        )

    with date_col2:
        end_date = st.date_input(
            "End date",
            value=valid_dates.max().date(),
            min_value=valid_dates.min().date(),
            max_value=valid_dates.max().date()
        )

    if start_date > end_date:
        st.error("Start date cannot be after end date.")
        st.stop()

    df = df[
        (df["Parsed Date"].dt.date >= start_date)
        & (df["Parsed Date"].dt.date <= end_date)
    ].copy()


# Calculate totals from parsed records
total_income = df["Money In"].sum()
total_expenses = df["Money Out"].sum()
balance = total_income - total_expenses

# Summary cards
col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Total Income",
    f"R {total_income:,.2f}"
)

col2.metric(
    "🛍️ Total Expenses",
    f"R {total_expenses:,.2f}"
)

col3.metric(
    "💗 Money Left",
    f"R {balance:,.2f}"
)

st.divider()

# Spending overview
left, right = st.columns(2)

with left:
    st.subheader("📊 Spending by Category")

    expenses = df[df["Money Out"] > 0]

    if not expenses.empty:
        category_totals = expenses.groupby(
            "Category"
        )["Money Out"].sum().sort_values(
            ascending=False
        )

        st.bar_chart(category_totals)
    else:
        st.info("No expenses found in the parsed data.")

with right:
    st.subheader("💡 Financial Summary")

    st.write(f"**Transactions loaded:** {len(df)}")
    st.write(f"**Income received:** R {total_income:,.2f}")
    st.write(f"**Money spent:** R {total_expenses:,.2f}")

    if total_income > 0:
        remaining_rate = balance / total_income * 100
        st.write(
            f"**Net amount remaining:** {remaining_rate:.1f}% of income"
        )

st.divider()

# Transaction table
st.subheader("🧾 Your Transactions")

# Date filter
df["Parsed Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True,
    errors="coerce"
)

valid_dates = df["Parsed Date"].dropna()

if not valid_dates.empty:
    start_date, end_date = st.date_input(
        "Filter transactions by date",
        value=(
            valid_dates.min().date(),
            valid_dates.max().date()
        ),
        min_value=valid_dates.min().date(),
        max_value=valid_dates.max().date()
    )

    df = df[
        (df["Parsed Date"].dt.date >= start_date)
        & (df["Parsed Date"].dt.date <= end_date)
    ]

search = st.text_input(
    "Search transactions",
    placeholder="Search by description or category..."
)

filtered_df = df.copy()

if search:
    mask = (
        filtered_df["Description"].astype(str).str.contains(
            search, case=False, na=False
        )
        | filtered_df["Category"].astype(str).str.contains(
            search, case=False, na=False
        )
    )
    filtered_df = filtered_df[mask]

# Sort dates correctly for display
filtered_df["_sort_date"] = pd.to_datetime(
    filtered_df["Date"],
    dayfirst=True,
    errors="coerce"
)

filtered_df = filtered_df.sort_values(
    "_sort_date", ascending=False
).drop(columns=["_sort_date"])

# Choose and order the columns displayed in the table
display_columns = [
    "Date",
    "Description",
    "Category",
    "Money In",
    "Money Out"
]

# Include Balance if your parser extracted it
if "Balance" in filtered_df.columns:
    display_columns.append("Balance")

# Display only columns that exist
display_columns = [
    column for column in display_columns
    if column in filtered_df.columns
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Money In": st.column_config.NumberColumn(
            "Money In (R)",
            format="R %.2f"
        ),
        "Money Out": st.column_config.NumberColumn(
            "Money Out (R)",
            format="R %.2f"
        ),
        "Balance": st.column_config.NumberColumn(
            "Balance (R)",
            format="R %.2f"
        )
    }
)

st.caption(
    "Data loaded from your statement text. "
    "Please verify the parsed amounts and fees before relying on totals."
)
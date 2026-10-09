Python Finance Tracker
A personal finance dashboard built with Python to help users understand their income and spending.
Features:
-Extracts text from bank statements in PDF format.
-Parses transaction details, including dates, descriptions, and amounts.
-Categorizes transactions into spending categories.
-Calculates total income and expenses.
-Displays spending summaries and charts.
-Filters transactions by date.
-Searches transactions by description.
-Presents financial information in a dusty-pink dashboard

Technologies used:
-Python
-Streamlit
-Pandas
-pdfplumber

How to run:
Install Python.
Open the project folder in PyCharm.
Install the required libraries:
   pip install streamlit pandas pdfplumber
Place your bank statement PDF in the appropriate data folder.
Run the PDF reader and transaction parser if needed.
Start the dashboard:
  python -m streamlit run dashboard.py
  Open the local URL shown in the terminal.

Project Purpose:
This project helped me practise Python programming, text parsing, data analysis, and dashboard development while building a practical tool for exploring personal financial transactions.

Privacy:
Use sample or anonymised financial data when sharing this project publicly. Never upload real bank statements or sensitive account information to a public repository.
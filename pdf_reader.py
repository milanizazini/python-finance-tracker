import pdfplumber

pdf = pdfplumber.open("data/account_statement.pdf")
text =""

for page in pdf.pages:
    tables = page.extract_tables()

    if tables:
        for table in tables:
            for row in table:
                print(row)
    else:
        print("No table detected on this page.")

    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"

pdf.close()
if text:
    print(text[:3000])
else:
    print("No text was found in the PDF")

if text:
    with open("data/statement_text.txt", "w", encoding="utf-8") as file:
        file.write(text)
    print("Statement text saved successfully!")
else:
    print("No text was found in the PDF.")
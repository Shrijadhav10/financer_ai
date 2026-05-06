# data_loader.py
 
import pandas as pd
from categorizer import categorize, normalize


def load_data(file_path):
    all_sheets = pd.read_excel(file_path, sheet_name=None)
    		
    documents = []
    dataframes = []

    for sheet_name, df in all_sheets.items():
        # print(f"Reading sheet: {sheet_name}")

        # Normalize columns
        df.columns = df.columns.str.strip().str.lower()

        # Handle missing values
        # Remove unwanted columns
        df = df.loc[:, ~df.columns.str.contains('^unnamed')]

        # --------------------------
        # HANDLE MISSING VALUES
        # --------------------------
        df = df.fillna('')

        # --------------------------
        # CLEAN EXPENSE COLUMN
        # --------------------------
        df['expense'] = df['expense'].astype(str).str.strip().str.lower()

        # Remove empty expense rows
        df = df[df['expense'] != '']

        # ✅ Clean price column
        df['price'] = df['price'].astype(str)  # convert everything to string first

        # Remove ₹ symbol and spaces
        df['price'] = df['price'].str.replace('₹', '', regex=False).str.strip()

        # Convert to numeric
        df['price'] = pd.to_numeric(df['price'], errors='coerce')

        # Replace NaN with 0
        df['price'] = df['price'].fillna(0)

        # ✅ Convert date column
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])

        # ✅ Categorize expenses
        # REMOVE INVALID ENTRIES
        # --------------------------
        invalid_values = ["august", "december", "total"]
        df = df[~df['expense'].isin(invalid_values)]

        # --------------------------
        # APPLY NORMALIZATION + CATEGORY
        # --------------------------
        df['expense'] = df['expense'].str.strip().str.lower()
        df['expense'] = df['expense'].apply(normalize)
        df['category'] = df['expense'].apply(categorize)


        for _, row in df.iterrows():
            date = row.get('date')
            expense = str(row.get('expense', '')).strip().lower()
            price = row.get('price', 0)

            if pd.isna(date) or not expense:
                continue

            # Format date nicely
            date_str = date.strftime("%d %b %Y")  # e.g., 01 Jan 2024

            text = f"on {date_str}, spent ₹{price} on {expense}"
            documents.append(text)

    # print(f"\n✅ Total records loaded: {len(documents)}")
     # ✅ Combine all sheets into one dataframe
        dataframes.append(df)

    full_df = pd.concat(dataframes, ignore_index=True)

    return documents, full_df
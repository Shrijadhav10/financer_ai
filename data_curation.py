import pandas as pd
from datetime import datetime
import calendar

# ==========================
# CONFIGURATION
# ==========================
def refresh_finance():
    # all your existing code here
    INPUT_FILE = r"G:\My Drive\Finanace\expense.xlsx"
    OUTPUT_FILE = r"G:\My Drive\Finanace\finance_curated.csv"

    MONTHS = [m.lower() for m in calendar.month_name if m]

    def is_month_total_row(expense_value):
        expense_text = str(expense_value).strip().lower()

        if not expense_text:
            return False

        return expense_text in MONTHS or expense_text == "total"

    # ==========================
    # PROCESSING
    # ==========================

    all_records = []

    excel = pd.ExcelFile(INPUT_FILE)

    for sheet_name in excel.sheet_names:

        if sheet_name.strip().lower() == "budget":
            print(f"Skipping sheet: {sheet_name}")
            continue

        print(f"Processing sheet: {sheet_name}")

        year = int(sheet_name)

        df = pd.read_excel(
            INPUT_FILE,
            sheet_name=sheet_name,
            header=None
        )

        current_month = None
        current_day = None

        for _, row in df.iterrows():

            col_a = row[0] if len(row) > 0 else None
            expense = row[1] if len(row) > 1 else None
            price = row[2] if len(row) > 2 else None

            # --------------------------
            # Skip completely empty rows
            # --------------------------
            if pd.isna(col_a) and pd.isna(expense) and pd.isna(price):
                continue

            # --------------------------
            # Detect Month
            # --------------------------
            if isinstance(col_a, str):

                value = col_a.strip().lower()

                if value in MONTHS:
                    current_month = value.capitalize()
                    current_day = None
                    continue

            # --------------------------
            # Detect Day
            # --------------------------
            if pd.notna(col_a):

                try:
                    day = int(float(col_a))

                    if 1 <= day <= 31:
                        current_day = day

                except:
                    pass

            # --------------------------
            # Expense Row Validation
            # --------------------------
            if pd.isna(expense):
                continue

            if is_month_total_row(expense):
                continue

            if current_month is None:
                continue

            if current_day is None:
                continue

            try:

                full_date = pd.to_datetime(
                    f"{current_day}-{current_month}-{year}",
                    format="%d-%B-%Y"
                )

                all_records.append({
                    "Day": current_day,
                    "Month": current_month,
                    "Year": year,
                    "Date": full_date.strftime("%Y-%m-%d"),
                    "Expense": str(expense).lower().strip(),
                    "Price": float(price) if pd.notna(price) else 0
                })

            except Exception as e:
                print(
                    f"Skipping row: "
                    f"Year={year}, "
                    f"Month={current_month}, "
                    f"Day={current_day}"
                )

    # ==========================
    # OUTPUT
    # ==========================

    curated_df = pd.DataFrame(all_records)

    curated_df = curated_df.sort_values(
        by=["Year", "Date"]
    )

    curated_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nDone!")
    print(f"Records created: {len(curated_df)}")
    print(f"Saved to: {OUTPUT_FILE}")

    print("\nSample Data:")
    print(curated_df.head())

    return curated_df

if __name__ == "__main__":
    refresh_finance()

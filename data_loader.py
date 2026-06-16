"""Load and normalize expense data."""

from pathlib import Path

import pandas as pd

from categorizer import categorize, normalize


def load_data(file_path):
    file_suffix = Path(file_path).suffix.lower()

    if file_suffix in {".xlsx", ".xls", ".xlsm"}:
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)

    documents = []

    # Normalize columns
    df.columns = df.columns.str.strip().str.lower()

    # Remove unwanted columns
    df = df.loc[:, ~df.columns.str.contains('^unnamed')]

    # Fill nulls
    df = df.fillna('')

    # Clean expense
    df['expense'] = (
        df['expense']
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Remove empty expense rows
    df = df[df['expense'] != '']

    # Clean price
    df['price'] = pd.to_numeric(
        df['price'],
        errors='coerce'
    ).fillna(0)

    # Convert date
    df['date'] = pd.to_datetime(
        df['date'],
        errors='coerce'
    )

    df = df.dropna(subset=['date'])

    # Normalize expense names
    df['expense'] = df['expense'].apply(normalize)

    # Categorize
    df['category'] = df['expense'].apply(categorize)

    # Create RAG documents
    for _, row in df.iterrows():

        date_str = row['date'].strftime("%d %b %Y")

        text = (
            f"on {date_str}, "
            f"spent â‚¹{row['price']} "
            f"on {row['expense']} "
            f"in category {row['category']}"
        )

        documents.append(text)

    return documents, df

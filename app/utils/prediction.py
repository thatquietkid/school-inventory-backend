import pandas as pd
import os

# Define paths
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, 'extended_school_inventory_6_years.csv')

def load_data():
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    # Convert and sort by date
    df['Month'] = pd.to_datetime(df['Month'], errors='coerce')
    df = df.dropna(subset=['Month'])
    df = df.sort_values(by='Month')

    # Create time-based features
    df['Month_Num'] = df['Month'].dt.month
    df['Year'] = df['Month'].dt.year

    # Create lag feature (last month’s usage)
    df['Usage_Last_Month'] = df.groupby('Item Name')['Quantity Used'].shift(1)
    df['Usage_2_Months_Ago'] = df.groupby('Item Name')['Quantity Used'].shift(2)

    # Average usage over 3 months
    df['Average_3_Month_Usage'] = df[['Quantity Used', 'Usage_Last_Month', 'Usage_2_Months_Ago']].mean(axis=1)

    # Is there an increasing trend?
    df['Is_Increasing_Trend'] = (
        (df['Quantity Used'] > df['Usage_Last_Month']) &
        (df['Usage_Last_Month'] > df['Usage_2_Months_Ago'])
    ).astype(int)

    # Create next-month usage as the target
    df['Usage_Next_Month'] = df.groupby('Item Name')['Quantity Used'].shift(-1)

    # Optional: Add previous procurement if available
    if 'Procurement' in df.columns:
        df['Procurement_Last_Month'] = df.groupby('Item Name')['Procurement'].shift(1)

    # Drop incomplete rows
    df = df.dropna(subset=[
        'Usage_Last_Month', 'Usage_2_Months_Ago', 'Average_3_Month_Usage',
        'Usage_Next_Month', 'Quantity Remaining', 'Total Quantity'
    ])

    return df

def preprocess(df):
    df_encoded = pd.get_dummies(df, columns=["Category", "Item Name", "Condition"])

    feature_cols = [
        "Usage_Last_Month",
        "Usage_2_Months_Ago",
        "Average_3_Month_Usage",
        "Is_Increasing_Trend",
        "Quantity Remaining",
        "Total Quantity"
    ] + [
        col for col in df_encoded.columns if col.startswith("Category_") or 
                                              col.startswith("Item Name_") or 
                                              col.startswith("Condition_")
    ]

    X = df_encoded[feature_cols]
    return df_encoded, X, feature_cols

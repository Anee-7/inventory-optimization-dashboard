import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv("D:/Inventory/Supermarket_stock.csv - Sheet1.csv")

# Quick check
print(df.shape)
print(df.head())
print(df.dtypes)

# ---- EDA ----
print("\n=== INVENTORY OVERVIEW ===")
print(f"Total Products: {len(df)}")
print(f"Total Categories: {df['Category'].nunique()}")
print(f"\nStock Status Distribution:")
print(df['Stock_Status'].value_counts())
print(f"\nCategory wise product count:")
print(df['Category'].value_counts())
print(f"\nTotal Inventory Value: ₹{(df['Cost_Price'] * df['Current_Stock']).sum():,.2f}")
print(f"Total Revenue Potential: ₹{(df['Selling_Price'] * df['Current_Stock']).sum():,.2f}")


# ---- ABC ANALYSIS ----
print("\n=== ABC ANALYSIS ===")

# Calculate revenue potential per product
df['Revenue_Potential'] = df['Selling_Price'] * df['Current_Stock']

# Sort by revenue descending
df = df.sort_values('Revenue_Potential', ascending=False)

# Calculate cumulative revenue percentage
df['Cumulative_Revenue'] = df['Revenue_Potential'].cumsum()
total_revenue = df['Revenue_Potential'].sum()
df['Cumulative_Pct'] = (df['Cumulative_Revenue'] / total_revenue) * 100

# Assign ABC class
def assign_abc(pct):
    if pct <= 70:
        return 'A'
    elif pct <= 90:
        return 'B'
    else:
        return 'C'

df['ABC_Class'] = df['Cumulative_Pct'].apply(assign_abc)

# Summary
print(df.groupby('ABC_Class')['Product_Name'].count())
print("\nABC Class Distribution:")
print(df.groupby('ABC_Class')[['Revenue_Potential']].sum())

# ---- ABC + STOCK STATUS COMBINED ----
print("\n=== CRITICAL PRODUCTS BY ABC CLASS ===")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
critical_abc = df[df['Stock_Status'] == 'Critical'][['Product_Name', 
               'Category', 'Stock_Status', 'ABC_Class', 
               'Days_of_Stock_Remaining', 'Revenue_Potential']]
print(critical_abc.sort_values('Revenue_Potential', ascending=False))

# ---- EXPORT FOR POWER BI ----
df.to_csv("D:/Inventory/inventory_final.csv", index=False)
print("\n✅ Final dataset exported for Power BI")
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
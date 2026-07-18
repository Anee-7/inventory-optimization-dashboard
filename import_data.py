import pandas as pd
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="J_Inventory"
)

# Read CSV and fix it
df = pd.read_csv("D:/Inventory/Supermarket_stock.csv - Sheet1.csv")

# Drop the empty column
df = df.drop(columns=['Unnamed: 12'])

# Rename columns to match MySQL table
df.columns = ['Product_ID', 'Product_Name', 'Category', 'Cost_Price', 
              'Selling_Price', 'Current_Stock', 'Avg_Daily_Sales', 
              'Lead_Time_Days', 'Last_Restock_Date', 'Reorder_Point', 
              'Days_of_Stock_Remaining', 'Stock_Status']

print(df.columns.tolist())
print(df.shape)

# Import to MySQL
cursor = conn.cursor()
for _, row in df.iterrows():
    sql = """INSERT INTO inventory VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(sql, tuple(row))

conn.commit()
print(f"Successfully imported {len(df)} rows")
cursor.close()
conn.close()
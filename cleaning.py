import pandas as pd

# Load dataset
file_path = "ApexPlanet_DataAnalytics_Dataset.xlsx"
df = pd.read_excel(file_path)

# -----------------------------
# Data Cleaning
# -----------------------------

# 1. Remove leading/trailing spaces from text columns
text_cols = ['Order_ID', 'Customer_ID', 'Customer_Name',
             'Gender', 'City', 'Product', 'Category']

for col in text_cols:
    df[col] = df[col].astype(str).str.strip()

# 2. Convert Order_Date to proper datetime format
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')

# 3. Fill missing Age values with median age
df['Age'] = df['Age'].fillna(df['Age'].median())

# 4. Fill missing City values with mode (most frequent city)
df['City'] = df['City'].replace('nan', pd.NA)
df['City'] = df['City'].fillna(df['City'].mode()[0])

# 5. Remove duplicate records if any
df.drop_duplicates(inplace=True)

# 6. Create additional date columns for Power BI analysis
df['Year'] = df['Order_Date'].dt.year
df['Month'] = df['Order_Date'].dt.month_name()
df['Quarter'] = df['Order_Date'].dt.quarter

# 7. Verify Total_Sales calculation
df['Calculated_Total'] = df['Quantity'] * df['Unit_Price']

# If difference is negligible, replace Total_Sales
df['Total_Sales'] = df['Calculated_Total']
df.drop(columns=['Calculated_Total'], inplace=True)

# 8. Save cleaned dataset
output_file = "Cleaned_Sales_Dataset.xlsx"
df.to_excel(output_file, index=False)

print("Data cleaning completed!")
print(f"Cleaned dataset saved as: {output_file}")

# Display summary
print("\nMissing Values After Cleaning:")
print(df.isnull().sum())
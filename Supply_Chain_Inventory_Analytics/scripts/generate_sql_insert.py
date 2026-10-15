import pandas as pd
import os

print("Generating SQL INSERT script from Excel workbook...")

excel_path = "Supply_Chain_Inventory_Analytics/data/walmart_style_supermarket_supply_chain_dataset.xlsx"
sql_output_path = "Supply_Chain_Inventory_Analytics/sql/insert_data.sql"

xl = pd.ExcelFile(excel_path)

with open(sql_output_path, "w", encoding="utf-8") as f:
    f.write("-- =============================================================================\n")
    f.write("-- SUPPLY CHAIN & INVENTORY MANAGEMENT ANALYTICS - DATA INSERTION SCRIPT\n")
    f.write("-- Automatically generated from walmart_style_supermarket_supply_chain_dataset.xlsx\n")
    f.write("-- =============================================================================\n\n")

    # Table insertion order to maintain FK constraints
    tables_order = [
        ("Products", "Products"),
        ("Suppliers", "Suppliers"),
        ("Stores", "Stores"),
        ("Customers", "Customers"),
        ("Inventory", "Inventory"),
        ("Sales_Orders", "Sales_Orders"),
        ("Purchases", "Purchases"),
        ("Returns", "Returns")
    ]

    for table_name, sheet_name in tables_order:
        print(f"Processing table: {table_name}...")
        df = xl.parse(sheet_name)
        
        f.write(f"-- -----------------------------------------------------------------------------\n")
        f.write(f"-- INSERT DATA INTO TABLE: {table_name} ({len(df)} records)\n")
        f.write(f"-- -----------------------------------------------------------------------------\n")
        
        # Process in batches of 500 for SQL performance
        batch_size = 500
        for i in range(0, len(df), batch_size):
            batch_df = df.iloc[i:i+batch_size]
            cols_str = ", ".join(batch_df.columns)
            f.write(f"INSERT INTO {table_name} ({cols_str}) VALUES\n")
            
            row_strings = []
            for _, row in batch_df.iterrows():
                vals = []
                for val in row:
                    if pd.isna(val):
                        vals.append("NULL")
                    elif isinstance(val, (int, float, bool)):
                        vals.append(str(val))
                    else:
                        val_str = str(val).replace("'", "''")
                        vals.append(f"'{val_str}'")
                row_strings.append("(" + ", ".join(vals) + ")")
                
            f.write(",\n".join(row_strings) + ";\n\n")

print(f"SQL INSERT script successfully written to: {sql_output_path}")

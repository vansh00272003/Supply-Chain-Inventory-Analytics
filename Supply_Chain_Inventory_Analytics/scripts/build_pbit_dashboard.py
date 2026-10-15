import os
import json
import zipfile

print("Starting Microsoft Power BI Template (.pbit) generation with fixed ASCII Version bytes...")

# Path to local dataset
excel_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "walmart_style_supermarket_supply_chain_dataset.xlsx")).replace("\\", "/")

# Function to build M expression for a sheet
def get_m_expression(sheet_name):
    return (
        f'let\n'
        f'    Source = Excel.Workbook(File.Contents("{excel_abs_path}"), null, true),\n'
        f'    Sheet_Data = Source{{[Item="{sheet_name}",Kind="Sheet"]}}[Data],\n'
        f'    #"Promoted Headers" = Table.PromoteHeaders(Sheet_Data, [PromoteAllScalars=true])\n'
        f'in\n'
        f'    #"Promoted Headers"'
    )

# 1. VERSION FILE - MUST BE RAW ASCII BYTES b"1.25" WITHOUT UTF-16 BOM
version_bytes = b"1.25"

# 2. [Content_Types].xml FILE - UTF-8 BYTES
content_types_xml = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="xml" ContentType="application/xml" />
  <Override PartName="/Version" ContentType="text/plain" />
  <Override PartName="/DataModelSchema" ContentType="application/json" />
  <Override PartName="/Report/Layout" ContentType="application/json" />
  <Override PartName="/Report/LinguisticSchema" ContentType="application/json" />
  <Override PartName="/DiagramLayout" ContentType="application/json" />
</Types>""".encode("utf-8")

# 3. DATA MODEL SCHEMA (JSON)
data_model_schema = {
    "name": "Model",
    "culture": "en-US",
    "dataAccessOptions": {
        "legacyRedirects": True,
        "returnErrorValuesAsNull": True
    },
    "tables": [
        {
            "name": "Products",
            "columns": [
                {"name": "Product_ID", "dataType": "string", "sourceColumn": "Product_ID"},
                {"name": "Product_Name", "dataType": "string", "sourceColumn": "Product_Name"},
                {"name": "Department", "dataType": "string", "sourceColumn": "Department"},
                {"name": "Subcategory", "dataType": "string", "sourceColumn": "Subcategory"},
                {"name": "Brand", "dataType": "string", "sourceColumn": "Brand"},
                {"name": "Unit_Cost", "dataType": "decimal", "sourceColumn": "Unit_Cost", "formatString": "₹#,##0.00"},
                {"name": "Selling_Price", "dataType": "decimal", "sourceColumn": "Selling_Price", "formatString": "₹#,##0.00"},
                {"name": "Reorder_Level", "dataType": "int64", "sourceColumn": "Reorder_Level"},
                {"name": "Safety_Stock", "dataType": "int64", "sourceColumn": "Safety_Stock"},
                {"name": "Shelf_Life_Days", "dataType": "int64", "sourceColumn": "Shelf_Life_Days"}
            ],
            "partitions": [
                {
                    "name": "Products",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": get_m_expression("Products")
                    }
                }
            ]
        },
        {
            "name": "Suppliers",
            "columns": [
                {"name": "Supplier_ID", "dataType": "string", "sourceColumn": "Supplier_ID"},
                {"name": "Supplier_Name", "dataType": "string", "sourceColumn": "Supplier_Name"},
                {"name": "City", "dataType": "string", "sourceColumn": "City"},
                {"name": "State", "dataType": "string", "sourceColumn": "State"},
                {"name": "Standard_Lead_Time_Days", "dataType": "int64", "sourceColumn": "Standard_Lead_Time_Days"},
                {"name": "Supplier_Rating", "dataType": "double", "sourceColumn": "Supplier_Rating"}
            ],
            "partitions": [
                {
                    "name": "Suppliers",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": get_m_expression("Suppliers")
                    }
                }
            ]
        },
        {
            "name": "Stores",
            "columns": [
                {"name": "Store_ID", "dataType": "string", "sourceColumn": "Store_ID"},
                {"name": "Store_Name", "dataType": "string", "sourceColumn": "Store_Name"},
                {"name": "City", "dataType": "string", "sourceColumn": "City"},
                {"name": "State", "dataType": "string", "sourceColumn": "State"},
                {"name": "Region", "dataType": "string", "sourceColumn": "Region"},
                {"name": "Capacity_Units", "dataType": "int64", "sourceColumn": "Capacity_Units"}
            ],
            "partitions": [
                {
                    "name": "Stores",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": get_m_expression("Stores")
                    }
                }
            ]
        },
        {
            "name": "Customers",
            "columns": [
                {"name": "Customer_ID", "dataType": "string", "sourceColumn": "Customer_ID"},
                {"name": "City", "dataType": "string", "sourceColumn": "City"},
                {"name": "Age_Group", "dataType": "string", "sourceColumn": "Age_Group"},
                {"name": "Gender", "dataType": "string", "sourceColumn": "Gender"},
                {"name": "Customer_Segment", "dataType": "string", "sourceColumn": "Customer_Segment"}
            ],
            "partitions": [
                {
                    "name": "Customers",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": get_m_expression("Customers")
                    }
                }
            ]
        },
        {
            "name": "Inventory",
            "columns": [
                {"name": "Inventory_ID", "dataType": "string", "sourceColumn": "Inventory_ID"},
                {"name": "Inventory_Date", "dataType": "dateTime", "sourceColumn": "Inventory_Date", "formatString": "yyyy-MM-dd"},
                {"name": "Product_ID", "dataType": "string", "sourceColumn": "Product_ID"},
                {"name": "Store_ID", "dataType": "string", "sourceColumn": "Store_ID"},
                {"name": "Stock_On_Hand", "dataType": "int64", "sourceColumn": "Stock_On_Hand"},
                {"name": "Reserved_Stock", "dataType": "int64", "sourceColumn": "Reserved_Stock"},
                {"name": "Available_Stock", "dataType": "int64", "sourceColumn": "Available_Stock"}
            ],
            "partitions": [
                {
                    "name": "Inventory",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": get_m_expression("Inventory")
                    }
                }
            ]
        },
        {
            "name": "Sales_Orders",
            "columns": [
                {"name": "Order_ID", "dataType": "string", "sourceColumn": "Order_ID"},
                {"name": "Order_Date", "dataType": "dateTime", "sourceColumn": "Order_Date", "formatString": "yyyy-MM-dd"},
                {"name": "Customer_ID", "dataType": "string", "sourceColumn": "Customer_ID"},
                {"name": "Product_ID", "dataType": "string", "sourceColumn": "Product_ID"},
                {"name": "Store_ID", "dataType": "string", "sourceColumn": "Store_ID"},
                {"name": "Quantity", "dataType": "int64", "sourceColumn": "Quantity"},
                {"name": "Discount_Pct", "dataType": "double", "sourceColumn": "Discount_Pct", "formatString": "0.0%"},
                {"name": "Sales_Amount", "dataType": "decimal", "sourceColumn": "Sales_Amount", "formatString": "₹#,##0.00"},
                {"name": "Payment_Method", "dataType": "string", "sourceColumn": "Payment_Method"},
                {"name": "Unit_Selling_Price", "dataType": "decimal", "sourceColumn": "Unit_Selling_Price", "formatString": "₹#,##0.00"},
                {"name": "COGS", "dataType": "decimal", "sourceColumn": "COGS", "formatString": "₹#,##0.00"},
                {"name": "Gross_Profit", "dataType": "decimal", "sourceColumn": "Gross_Profit", "formatString": "₹#,##0.00"}
            ],
            "measures": [
                {"name": "Total Sales", "expression": "SUM(Sales_Orders[Sales_Amount])", "formatString": "₹#,##0.00"},
                {"name": "Total COGS", "expression": "SUM(Sales_Orders[COGS])", "formatString": "₹#,##0.00"},
                {"name": "Gross Profit", "expression": "[Total Sales] - [Total COGS]", "formatString": "₹#,##0.00"},
                {"name": "Profit Margin %", "expression": "DIVIDE([Gross Profit], [Total Sales], 0)", "formatString": "0.00%"},
                {"name": "Total Orders", "expression": "DISTINCTCOUNT(Sales_Orders[Order_ID])", "formatString": "#,##0"},
                {"name": "Units Sold", "expression": "SUM(Sales_Orders[Quantity])", "formatString": "#,##0"},
                {"name": "Average Order Value", "expression": "DIVIDE([Total Sales], [Total Orders], 0)", "formatString": "₹#,##0.00"},
                {"name": "Average Discount %", "expression": "AVERAGE(Sales_Orders[Discount_Pct])", "formatString": "0.0%"},
                {"name": "MoM Sales Growth %", "expression": "VAR Curr = [Total Sales] VAR Prev = CALCULATE([Total Sales], DATEADD(DimDate[Date], -1, MONTH)) RETURN DIVIDE(Curr - Prev, Prev, 0)", "formatString": "0.00%"},
                {"name": "Inventory Value", "expression": "SUMX(Inventory, Inventory[Stock_On_Hand] * RELATED(Products[Unit_Cost]))", "formatString": "₹#,##0.00"},
                {"name": "Stockout Count", "expression": "CALCULATE(COUNTROWS(Inventory), Inventory[Stock_On_Hand] = 0)", "formatString": "#,##0"},
                {"name": "Low Stock Count", "expression": "CALCULATE(COUNTROWS(Inventory), Inventory[Stock_On_Hand] < RELATED(Products[Reorder_Level]), Inventory[Stock_On_Hand] > 0)", "formatString": "#,##0"},
                {"name": "Critical Stock Count", "expression": "CALCULATE(COUNTROWS(Inventory), Inventory[Stock_On_Hand] < RELATED(Products[Safety_Stock]), Inventory[Stock_On_Hand] > 0)", "formatString": "#,##0"},
                {"name": "Overstock Count", "expression": "CALCULATE(COUNTROWS(Inventory), Inventory[Stock_On_Hand] > (3 * RELATED(Products[Reorder_Level])))", "formatString": "#,##0"},
                {"name": "Inventory Turnover", "expression": "VAR AnnualizedCOGS = [Total COGS] * 6 VAR AvgInv = [Inventory Value] RETURN DIVIDE(AnnualizedCOGS, AvgInv, 0)", "formatString": "0.0x"},
                {"name": "Total Purchase Cost", "expression": "SUM(Purchases[Purchase_Cost])", "formatString": "₹#,##0.00"},
                {"name": "Total PO Count", "expression": "COUNTROWS(Purchases)", "formatString": "#,##0"},
                {"name": "Average Lead Time", "expression": "AVERAGE(Purchases[Lead_Time_Days])", "formatString": "0.0 Days"},
                {"name": "On Time Delivery %", "expression": "DIVIDE(CALCULATE(COUNTROWS(Purchases), Purchases[On_Time] = \"Yes\"), COUNTROWS(Purchases), 0)", "formatString": "0.0%"},
                {"name": "Delayed PO Count", "expression": "CALCULATE(COUNTROWS(Purchases), Purchases[On_Time] = \"No\")", "formatString": "#,##0"},
                {"name": "Returned Units", "expression": "SUM(Returns[Quantity_Returned])", "formatString": "#,##0"},
                {"name": "Total Refund Amount", "expression": "SUM(Returns[Refund_Amount])", "formatString": "₹#,##0.00"},
                {"name": "Return Rate %", "expression": "DIVIDE([Returned Units], [Units Sold], 0)", "formatString": "0.00%"}
            ],
            "partitions": [
                {
                    "name": "Sales_Orders",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": get_m_expression("Sales_Orders")
                    }
                }
            ]
        },
        {
            "name": "Purchases",
            "columns": [
                {"name": "PO_ID", "dataType": "string", "sourceColumn": "PO_ID"},
                {"name": "Order_Date", "dataType": "dateTime", "sourceColumn": "Order_Date", "formatString": "yyyy-MM-dd"},
                {"name": "Product_ID", "dataType": "string", "sourceColumn": "Product_ID"},
                {"name": "Supplier_ID", "dataType": "string", "sourceColumn": "Supplier_ID"},
                {"name": "Store_ID", "dataType": "string", "sourceColumn": "Store_ID"},
                {"name": "Expected_Date", "dataType": "dateTime", "sourceColumn": "Expected_Date", "formatString": "yyyy-MM-dd"},
                {"name": "Received_Date", "dataType": "dateTime", "sourceColumn": "Received_Date", "formatString": "yyyy-MM-dd"},
                {"name": "Quantity_Ordered", "dataType": "int64", "sourceColumn": "Quantity_Ordered"},
                {"name": "Purchase_Cost", "dataType": "decimal", "sourceColumn": "Purchase_Cost", "formatString": "₹#,##0.00"},
                {"name": "Lead_Time_Days", "dataType": "int64", "sourceColumn": "Lead_Time_Days"},
                {"name": "Delay_Days", "dataType": "int64", "sourceColumn": "Delay_Days"},
                {"name": "On_Time", "dataType": "string", "sourceColumn": "On_Time"}
            ],
            "partitions": [
                {
                    "name": "Purchases",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": get_m_expression("Purchases")
                    }
                }
            ]
        },
        {
            "name": "Returns",
            "columns": [
                {"name": "Return_ID", "dataType": "string", "sourceColumn": "Return_ID"},
                {"name": "Order_ID", "dataType": "string", "sourceColumn": "Order_ID"},
                {"name": "Return_Date", "dataType": "dateTime", "sourceColumn": "Return_Date", "formatString": "yyyy-MM-dd"},
                {"name": "Product_ID", "dataType": "string", "sourceColumn": "Product_ID"},
                {"name": "Store_ID", "dataType": "string", "sourceColumn": "Store_ID"},
                {"name": "Quantity_Returned", "dataType": "int64", "sourceColumn": "Quantity_Returned"},
                {"name": "Refund_Amount", "dataType": "decimal", "sourceColumn": "Refund_Amount", "formatString": "₹#,##0.00"},
                {"name": "Return_Reason", "dataType": "string", "sourceColumn": "Return_Reason"}
            ],
            "partitions": [
                {
                    "name": "Returns",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": get_m_expression("Returns")
                    }
                }
            ]
        },
        {
            "name": "DimDate",
            "columns": [
                {"name": "Date", "dataType": "dateTime", "sourceColumn": "Date", "formatString": "yyyy-MM-dd"},
                {"name": "Year", "dataType": "int64", "sourceColumn": "Year"},
                {"name": "Month", "dataType": "string", "sourceColumn": "Month"},
                {"name": "Day", "dataType": "int64", "sourceColumn": "Day"}
            ],
            "partitions": [
                {
                    "name": "DimDate",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": "let Source = List.Dates(#date(2026, 8, 1), 60, #duration(1, 0, 0, 0)), TableFromList = Table.FromList(Source, Splitter.SplitByNothing(), {\"Date\"}), InsertYear = Table.AddColumn(TableFromList, \"Year\", each Date.Year([Date])), InsertMonth = Table.AddColumn(InsertYear, \"Month\", each Date.MonthName([Date])), InsertDay = Table.AddColumn(InsertMonth, \"Day\", each Date.Day([Date])) in InsertDay"
                    }
                }
            ]
        }
    ],
    "relationships": [
        {"name": "rel_prod_sales", "fromTable": "Sales_Orders", "fromColumn": "Product_ID", "toTable": "Products", "toColumn": "Product_ID"},
        {"name": "rel_prod_inv", "fromTable": "Inventory", "fromColumn": "Product_ID", "toTable": "Products", "toColumn": "Product_ID"},
        {"name": "rel_prod_purch", "fromTable": "Purchases", "fromColumn": "Product_ID", "toTable": "Products", "toColumn": "Product_ID"},
        {"name": "rel_prod_ret", "fromTable": "Returns", "fromColumn": "Product_ID", "toTable": "Products", "toColumn": "Product_ID"},
        {"name": "rel_store_sales", "fromTable": "Sales_Orders", "fromColumn": "Store_ID", "toTable": "Stores", "toColumn": "Store_ID"},
        {"name": "rel_store_inv", "fromTable": "Inventory", "fromColumn": "Store_ID", "toTable": "Stores", "toColumn": "Store_ID"},
        {"name": "rel_store_purch", "fromTable": "Purchases", "fromColumn": "Store_ID", "toTable": "Stores", "toColumn": "Store_ID"},
        {"name": "rel_store_ret", "fromTable": "Returns", "fromColumn": "Store_ID", "toTable": "Stores", "toColumn": "Store_ID"},
        {"name": "rel_cust_sales", "fromTable": "Sales_Orders", "fromColumn": "Customer_ID", "toTable": "Customers", "toColumn": "Customer_ID"},
        {"name": "rel_sup_purch", "fromTable": "Purchases", "fromColumn": "Supplier_ID", "toTable": "Suppliers", "toColumn": "Supplier_ID"},
        {"name": "rel_date_sales", "fromTable": "Sales_Orders", "fromColumn": "Order_Date", "toTable": "DimDate", "toColumn": "Date"},
        {"name": "rel_date_inv", "fromTable": "Inventory", "fromColumn": "Inventory_Date", "toTable": "DimDate", "toColumn": "Date"},
        {"name": "rel_date_purch", "fromTable": "Purchases", "fromColumn": "Order_Date", "toTable": "DimDate", "toColumn": "Date"},
        {"name": "rel_date_ret", "fromTable": "Returns", "fromColumn": "Return_Date", "toTable": "DimDate", "toColumn": "Date"}
    ]
}

# 4. REPORT LAYOUT SCHEMA (JSON)
report_layout_schema = {
    "id": 0,
    "theme": "ExecutiveTheme",
    "sections": [
        {
            "id": 0,
            "name": "ReportSection_ExecutiveOverview",
            "displayName": "Executive Overview",
            "filters": "[]",
            "ordinal": 0,
            "visualContainers": [
                {"x": 20, "y": 20, "width": 1240, "height": 50, "z": 0, "title": "WALMART-STYLE SUPERMARKET EXECUTIVE OVERVIEW DASHBOARD"},
                {"x": 20, "y": 90, "width": 280, "height": 110, "z": 1, "title": "Total Sales Revenue", "measure": "Total Sales"},
                {"x": 320, "y": 90, "width": 280, "height": 110, "z": 2, "title": "Gross Profit", "measure": "Gross Profit"},
                {"x": 620, "y": 90, "width": 280, "height": 110, "z": 3, "title": "Profit Margin %", "measure": "Profit Margin %"},
                {"x": 920, "y": 90, "width": 340, "height": 110, "z": 4, "title": "Total Inventory Value", "measure": "Inventory Value"},
                {"x": 20, "y": 220, "width": 600, "height": 260, "z": 5, "title": "Daily Sales Revenue & Profit Trend"},
                {"x": 640, "y": 220, "width": 620, "height": 260, "z": 6, "title": "Sales Revenue by Department"},
                {"x": 20, "y": 500, "width": 600, "height": 200, "z": 7, "title": "Store Revenue & Margin Matrix"},
                {"x": 640, "y": 500, "width": 620, "height": 200, "z": 8, "title": "Inventory Health & Stockout Alerts"}
            ]
        },
        {
            "id": 1,
            "name": "ReportSection_SalesAnalytics",
            "displayName": "Sales Analytics",
            "filters": "[]",
            "ordinal": 1,
            "visualContainers": [
                {"x": 20, "y": 20, "width": 1240, "height": 50, "z": 0, "title": "RETAIL SALES & FINANCIAL MARGIN ANALYTICS"},
                {"x": 20, "y": 90, "width": 280, "height": 110, "z": 1, "title": "Total Orders", "measure": "Total Orders"},
                {"x": 320, "y": 90, "width": 280, "height": 110, "z": 2, "title": "Units Sold", "measure": "Units Sold"},
                {"x": 620, "y": 90, "width": 280, "height": 110, "z": 3, "title": "Average Order Value (AOV)", "measure": "Average Order Value"},
                {"x": 920, "y": 90, "width": 340, "height": 110, "z": 4, "title": "Average Discount %", "measure": "Average Discount %"},
                {"x": 20, "y": 220, "width": 780, "height": 280, "z": 5, "title": "Monthly & Daily Revenue Trends"},
                {"x": 820, "y": 220, "width": 440, "height": 280, "z": 6, "title": "Payment Method tender distribution"},
                {"x": 20, "y": 520, "width": 1240, "height": 180, "z": 7, "title": "Top & Bottom Product Sales Performance"}
            ]
        },
        {
            "id": 2,
            "name": "ReportSection_InventoryAnalytics",
            "displayName": "Inventory Analytics",
            "filters": "[]",
            "ordinal": 2,
            "visualContainers": [
                {"x": 20, "y": 20, "width": 1240, "height": 50, "z": 0, "title": "INVENTORY STOCK & REPLENISHMENT ANALYTICS"},
                {"x": 20, "y": 90, "width": 280, "height": 110, "z": 1, "title": "Stockout Count (Stock = 0)", "measure": "Stockout Count"},
                {"x": 320, "y": 90, "width": 280, "height": 110, "z": 2, "title": "Low Stock Count (< Reorder)", "measure": "Low Stock Count"},
                {"x": 620, "y": 90, "width": 280, "height": 110, "z": 3, "title": "Critical Deficit (< Safety)", "measure": "Critical Stock Count"},
                {"x": 920, "y": 90, "width": 340, "height": 110, "z": 4, "title": "Overstock Count (> 3x Reorder)", "measure": "Overstock Count"},
                {"x": 20, "y": 220, "width": 620, "height": 260, "z": 5, "title": "Store Stock On Hand vs Reorder Level"},
                {"x": 660, "y": 220, "width": 600, "height": 260, "z": 6, "title": "Department Inventory Holding Valuation"},
                {"x": 20, "y": 500, "width": 1240, "height": 200, "z": 7, "title": "High-Priority Replenishment Action Grid"}
            ]
        },
        {
            "id": 3,
            "name": "ReportSection_SupplyChainAnalytics",
            "displayName": "Supply Chain Analytics",
            "filters": "[]",
            "ordinal": 3,
            "visualContainers": [
                {"x": 20, "y": 20, "width": 1240, "height": 50, "z": 0, "title": "SUPPLIER FULFILLMENT & LEAD TIME ANALYTICS"},
                {"x": 20, "y": 90, "width": 280, "height": 110, "z": 1, "title": "On Time Delivery %", "measure": "On Time Delivery %"},
                {"x": 320, "y": 90, "width": 280, "height": 110, "z": 2, "title": "Total Purchase Cost", "measure": "Total Purchase Cost"},
                {"x": 620, "y": 90, "width": 280, "height": 110, "z": 3, "title": "Average Lead Time", "measure": "Average Lead Time"},
                {"x": 920, "y": 90, "width": 340, "height": 110, "z": 4, "title": "Delayed PO Count", "measure": "Delayed PO Count"},
                {"x": 20, "y": 220, "width": 620, "height": 260, "z": 5, "title": "Supplier Rating vs Actual Lead Time Variance"},
                {"x": 660, "y": 220, "width": 600, "height": 260, "z": 6, "title": "Supplier On-Time vs Delayed PO Breakdown"},
                {"x": 20, "y": 500, "width": 1240, "height": 200, "z": 7, "title": "Vendor Performance Scorecard Table"}
            ]
        },
        {
            "id": 4,
            "name": "ReportSection_CustomerAnalytics",
            "displayName": "Customer Analytics",
            "filters": "[]",
            "ordinal": 4,
            "visualContainers": [
                {"x": 20, "y": 20, "width": 1240, "height": 50, "z": 0, "title": "CUSTOMER DEMOGRAPHICS & SEGMENTATION ANALYTICS"},
                {"x": 20, "y": 90, "width": 600, "height": 300, "z": 1, "title": "Revenue & Orders by Customer Segment"},
                {"x": 640, "y": 90, "width": 620, "height": 300, "z": 2, "title": "Sales Distribution by Customer City"},
                {"x": 20, "y": 410, "width": 600, "height": 290, "z": 3, "title": "Demographics by Age Group and Gender"},
                {"x": 640, "y": 410, "width": 620, "height": 290, "z": 4, "title": "Payment Method Preference by Age Group"}
            ]
        },
        {
            "id": 5,
            "name": "ReportSection_ProductPerformance",
            "displayName": "Product Performance",
            "filters": "[]",
            "ordinal": 5,
            "visualContainers": [
                {"x": 20, "y": 20, "width": 1240, "height": 50, "z": 0, "title": "PRODUCT PARETO & ABC CLASSIFICATION ANALYTICS"},
                {"x": 20, "y": 90, "width": 780, "height": 300, "z": 1, "title": "Pareto Cumulative Revenue Contribution (ABC Analysis)"},
                {"x": 820, "y": 90, "width": 440, "height": 300, "z": 2, "title": "Unit Price vs Sales Volume Elasticity"},
                {"x": 20, "y": 410, "width": 1240, "height": 290, "z": 3, "title": "ABC Classification Product Grid (Class A, B, C)"}
            ]
        },
        {
            "id": 6,
            "name": "ReportSection_ReturnsAnalytics",
            "displayName": "Returns Analytics",
            "filters": "[]",
            "ordinal": 6,
            "visualContainers": [
                {"x": 20, "y": 20, "width": 1240, "height": 50, "z": 0, "title": "PRODUCT RETURNS & QUALITY CONTROL ANALYTICS"},
                {"x": 20, "y": 90, "width": 380, "height": 110, "z": 1, "title": "Overall Return Rate %", "measure": "Return Rate %"},
                {"x": 420, "y": 90, "width": 400, "height": 110, "z": 2, "title": "Total Returned Units", "measure": "Returned Units"},
                {"x": 840, "y": 90, "width": 420, "height": 110, "z": 3, "title": "Total Refund Amount", "measure": "Total Refund Amount"},
                {"x": 20, "y": 220, "width": 600, "height": 260, "z": 4, "title": "Return Reason Share (Damaged, Expired, Quality)"},
                {"x": 640, "y": 220, "width": 620, "height": 260, "z": 5, "title": "Department Refund Cost Breakdown"},
                {"x": 20, "y": 500, "width": 1240, "height": 200, "z": 6, "title": "High Return Rate Product Log Table"}
            ]
        }
    ]
}

# 5. PACKAGING THE .pbit FILE
output_pbit_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "powerbi", "walmart_style_supply_chain_dashboard.pbit"))
os.makedirs(os.path.dirname(output_pbit_path), exist_ok=True)

print(f"Building Power BI Template archive at: {output_pbit_path}...")

with zipfile.ZipFile(output_pbit_path, "w", zipfile.ZIP_DEFLATED) as zf:
    # 1. Version must be raw ASCII bytes b"1.25"
    zf.writestr("Version", version_bytes)
    
    # 2. [Content_Types].xml must be UTF-8 bytes
    zf.writestr("[Content_Types].xml", content_types_xml)
    
    # 3. DataModelSchema encoded in UTF-16LE without BOM or UTF-16LE bytes
    schema_str = json.dumps(data_model_schema, indent=2)
    zf.writestr("DataModelSchema", schema_str.encode("utf-16le"))
    
    # 4. Report/Layout encoded in UTF-16LE
    layout_str = json.dumps(report_layout_schema, indent=2)
    zf.writestr("Report/Layout", layout_str.encode("utf-16le"))
    
    # 5. LinguisticSchema & DiagramLayout encoded in UTF-16LE
    zf.writestr("Report/LinguisticSchema", json.dumps({"Version": "1.0"}).encode("utf-16le"))
    zf.writestr("DiagramLayout", json.dumps({"version": "1.1"}).encode("utf-16le"))

print("Microsoft Power BI Template (.pbit) created successfully with raw ASCII Version bytes!")

import os
import json
import zipfile

print("Updating native Power BI file (excel loaded.pbix) with 7 multi-page dashboard pages...")

pbix_input_path = "Supply_Chain_Inventory_Analytics/powerbi/excel loaded.pbix"
pbix_output_path = "Supply_Chain_Inventory_Analytics/powerbi/walmart_style_supply_chain_dashboard.pbix"

if not os.path.exists(pbix_input_path):
    print(f"Error: Could not find {pbix_input_path}")
    exit(1)

# Read existing layout from user's pbix
with zipfile.ZipFile(pbix_input_path, 'r') as z_in:
    layout_data = json.loads(z_in.read('Report/Layout').decode('utf-16le'))
    files_map = {name: z_in.read(name) for name in z_in.namelist()}

# Define 7 Multi-page visual layout sections
sections_config = [
    {
        "id": 0,
        "name": "ReportSection_ExecutiveOverview",
        "displayName": "Executive Overview",
        "filters": "[]",
        "ordinal": 0,
        "visualContainers": [
            {
                "x": 20, "y": 15, "width": 1240, "height": 45, "z": 0,
                "config": json.dumps({"name": "title_box", "layouts": [{"position": {"x": 20, "y": 15, "width": 1240, "height": 45}, "tabOrder": 0}], "singleVisual": {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [{"text": "WALMART-STYLE SUPERMARKET EXECUTIVE OVERVIEW DASHBOARD", "style": {"fontFamily": "Segoe UI", "fontSize": "16pt", "fontWeight": "bold", "color": "#1F4E78"}}]}]}}]}}})
            },
            {
                "x": 20, "y": 80, "width": 280, "height": 110, "z": 1,
                "config": json.dumps({"name": "kpi_sales", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Sales_Orders.Sales_Amount"}]}}})
            },
            {
                "x": 320, "y": 80, "width": 280, "height": 110, "z": 2,
                "config": json.dumps({"name": "kpi_profit", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Sales_Orders.Gross_Profit"}]}}})
            },
            {
                "x": 620, "y": 80, "width": 280, "height": 110, "z": 3,
                "config": json.dumps({"name": "kpi_orders", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Sales_Orders.Order_ID"}]}}})
            },
            {
                "x": 920, "y": 80, "width": 340, "height": 110, "z": 4,
                "config": json.dumps({"name": "kpi_stock", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Inventory.Stock_On_Hand"}]}}})
            },
            {
                "x": 20, "y": 210, "width": 600, "height": 270, "z": 5,
                "config": json.dumps({"name": "trend_chart", "singleVisual": {"visualType": "lineChart", "projections": {"Category": [{"queryRef": "Sales_Orders.Order_Date"}], "Y": [{"queryRef": "Sales_Orders.Sales_Amount"}]}}})
            },
            {
                "x": 640, "y": 210, "width": 620, "height": 270, "z": 6,
                "config": json.dumps({"name": "dept_chart", "singleVisual": {"visualType": "barChart", "projections": {"Category": [{"queryRef": "Products.Department"}], "Y": [{"queryRef": "Sales_Orders.Sales_Amount"}]}}})
            },
            {
                "x": 20, "y": 500, "width": 600, "height": 200, "z": 7,
                "config": json.dumps({"name": "store_grid", "singleVisual": {"visualType": "pivotTable", "projections": {"Rows": [{"queryRef": "Stores.Store_Name"}], "Values": [{"queryRef": "Sales_Orders.Sales_Amount"}, {"queryRef": "Sales_Orders.Gross_Profit"}]}}})
            },
            {
                "x": 640, "y": 500, "width": 620, "height": 200, "z": 8,
                "config": json.dumps({"name": "inv_chart", "singleVisual": {"visualType": "columnChart", "projections": {"Category": [{"queryRef": "Stores.Store_Name"}], "Y": [{"queryRef": "Inventory.Stock_On_Hand"}]}}})
            }
        ]
    },
    {
        "id": 1,
        "name": "ReportSection_SalesAnalytics",
        "displayName": "Sales Analytics",
        "filters": "[]",
        "ordinal": 1,
        "visualContainers": [
            {
                "x": 20, "y": 15, "width": 1240, "height": 45, "z": 0,
                "config": json.dumps({"name": "title_sales", "singleVisual": {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [{"text": "RETAIL SALES & FINANCIAL MARGIN ANALYTICS", "style": {"fontFamily": "Segoe UI", "fontSize": "16pt", "fontWeight": "bold", "color": "#1F4E78"}}]}]}}]}}})
            },
            {
                "x": 20, "y": 80, "width": 780, "height": 300, "z": 1,
                "config": json.dumps({"name": "monthly_sales_chart", "singleVisual": {"visualType": "areaChart", "projections": {"Category": [{"queryRef": "Sales_Orders.Order_Date"}], "Y": [{"queryRef": "Sales_Orders.Sales_Amount"}]}}})
            },
            {
                "x": 820, "y": 80, "width": 440, "height": 300, "z": 2,
                "config": json.dumps({"name": "payment_pie", "singleVisual": {"visualType": "pieChart", "projections": {"Category": [{"queryRef": "Sales_Orders.Payment_Method"}], "Y": [{"queryRef": "Sales_Orders.Sales_Amount"}]}}})
            },
            {
                "x": 20, "y": 400, "width": 1240, "height": 300, "z": 3,
                "config": json.dumps({"name": "product_sales_table", "singleVisual": {"visualType": "pivotTable", "projections": {"Rows": [{"queryRef": "Products.Product_Name"}, {"queryRef": "Products.Department"}], "Values": [{"queryRef": "Sales_Orders.Quantity"}, {"queryRef": "Sales_Orders.Sales_Amount"}, {"queryRef": "Sales_Orders.Gross_Profit"}]}}})
            }
        ]
    },
    {
        "id": 2,
        "name": "ReportSection_InventoryAnalytics",
        "displayName": "Inventory Analytics",
        "filters": "[]",
        "ordinal": 2,
        "visualContainers": [
            {
                "x": 20, "y": 15, "width": 1240, "height": 45, "z": 0,
                "config": json.dumps({"name": "title_inv", "singleVisual": {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [{"text": "INVENTORY STOCK & REPLENISHMENT ANALYTICS", "style": {"fontFamily": "Segoe UI", "fontSize": "16pt", "fontWeight": "bold", "color": "#1F4E78"}}]}]}}]}}})
            },
            {
                "x": 20, "y": 80, "width": 600, "height": 300, "z": 1,
                "config": json.dumps({"name": "inv_by_store", "singleVisual": {"visualType": "barChart", "projections": {"Category": [{"queryRef": "Stores.Store_Name"}], "Y": [{"queryRef": "Inventory.Stock_On_Hand"}, {"queryRef": "Inventory.Available_Stock"}]}}})
            },
            {
                "x": 640, "y": 80, "width": 620, "height": 300, "z": 2,
                "config": json.dumps({"name": "inv_by_dept", "singleVisual": {"visualType": "columnChart", "projections": {"Category": [{"queryRef": "Products.Department"}], "Y": [{"queryRef": "Inventory.Stock_On_Hand"}]}}})
            },
            {
                "x": 20, "y": 400, "width": 1240, "height": 300, "z": 3,
                "config": json.dumps({"name": "inv_detail_grid", "singleVisual": {"visualType": "pivotTable", "projections": {"Rows": [{"queryRef": "Stores.Store_Name"}, {"queryRef": "Products.Product_Name"}], "Values": [{"queryRef": "Inventory.Stock_On_Hand"}, {"queryRef": "Inventory.Available_Stock"}]}}})
            }
        ]
    },
    {
        "id": 3,
        "name": "ReportSection_SupplyChainAnalytics",
        "displayName": "Supply Chain Analytics",
        "filters": "[]",
        "ordinal": 3,
        "visualContainers": [
            {
                "x": 20, "y": 15, "width": 1240, "height": 45, "z": 0,
                "config": json.dumps({"name": "title_sc", "singleVisual": {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [{"text": "SUPPLIER FULFILLMENT & LEAD TIME ANALYTICS", "style": {"fontFamily": "Segoe UI", "fontSize": "16pt", "fontWeight": "bold", "color": "#1F4E78"}}]}]}}]}}})
            },
            {
                "x": 20, "y": 80, "width": 600, "height": 300, "z": 1,
                "config": json.dumps({"name": "supplier_cost", "singleVisual": {"visualType": "barChart", "projections": {"Category": [{"queryRef": "Suppliers.Supplier_Name"}], "Y": [{"queryRef": "Purchases.Purchase_Cost"}]}}})
            },
            {
                "x": 640, "y": 80, "width": 620, "height": 300, "z": 2,
                "config": json.dumps({"name": "ontime_pie", "singleVisual": {"visualType": "pieChart", "projections": {"Category": [{"queryRef": "Purchases.On_Time"}], "Y": [{"queryRef": "Purchases.PO_ID"}]}}})
            },
            {
                "x": 20, "y": 400, "width": 1240, "height": 300, "z": 3,
                "config": json.dumps({"name": "supplier_scorecard", "singleVisual": {"visualType": "pivotTable", "projections": {"Rows": [{"queryRef": "Suppliers.Supplier_Name"}], "Values": [{"queryRef": "Purchases.Purchase_Cost"}, {"queryRef": "Purchases.Lead_Time_Days"}, {"queryRef": "Purchases.Delay_Days"}]}}})
            }
        ]
    },
    {
        "id": 4,
        "name": "ReportSection_CustomerAnalytics",
        "displayName": "Customer Analytics",
        "filters": "[]",
        "ordinal": 4,
        "visualContainers": [
            {
                "x": 20, "y": 15, "width": 1240, "height": 45, "z": 0,
                "config": json.dumps({"name": "title_cust", "singleVisual": {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [{"text": "CUSTOMER DEMOGRAPHICS & SEGMENTATION ANALYTICS", "style": {"fontFamily": "Segoe UI", "fontSize": "16pt", "fontWeight": "bold", "color": "#1F4E78"}}]}]}}]}}})
            },
            {
                "x": 20, "y": 80, "width": 600, "height": 300, "z": 1,
                "config": json.dumps({"name": "cust_seg_chart", "singleVisual": {"visualType": "barChart", "projections": {"Category": [{"queryRef": "Customers.Customer_Segment"}], "Y": [{"queryRef": "Sales_Orders.Sales_Amount"}]}}})
            },
            {
                "x": 640, "y": 80, "width": 620, "height": 300, "z": 2,
                "config": json.dumps({"name": "cust_city_chart", "singleVisual": {"visualType": "columnChart", "projections": {"Category": [{"queryRef": "Customers.City"}], "Y": [{"queryRef": "Sales_Orders.Sales_Amount"}]}}})
            },
            {
                "x": 20, "y": 400, "width": 1240, "height": 300, "z": 3,
                "config": json.dumps({"name": "cust_age_chart", "singleVisual": {"visualType": "columnChart", "projections": {"Category": [{"queryRef": "Customers.Age_Group"}], "Y": [{"queryRef": "Sales_Orders.Sales_Amount"}]}}})
            }
        ]
    },
    {
        "id": 5,
        "name": "ReportSection_ProductPerformance",
        "displayName": "Product Performance",
        "filters": "[]",
        "ordinal": 5,
        "visualContainers": [
            {
                "x": 20, "y": 15, "width": 1240, "height": 45, "z": 0,
                "config": json.dumps({"name": "title_prod", "singleVisual": {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [{"text": "PRODUCT PARETO & MARGIN ANALYTICS", "style": {"fontFamily": "Segoe UI", "fontSize": "16pt", "fontWeight": "bold", "color": "#1F4E78"}}]}]}}]}}})
            },
            {
                "x": 20, "y": 80, "width": 1240, "height": 300, "z": 1,
                "config": json.dumps({"name": "brand_sales_chart", "singleVisual": {"visualType": "columnChart", "projections": {"Category": [{"queryRef": "Products.Brand"}], "Y": [{"queryRef": "Sales_Orders.Sales_Amount"}, {"queryRef": "Sales_Orders.Gross_Profit"}]}}})
            },
            {
                "x": 20, "y": 400, "width": 1240, "height": 300, "z": 2,
                "config": json.dumps({"name": "prod_margin_table", "singleVisual": {"visualType": "pivotTable", "projections": {"Rows": [{"queryRef": "Products.Product_Name"}], "Values": [{"queryRef": "Products.Unit_Cost"}, {"queryRef": "Products.Selling_Price"}, {"queryRef": "Sales_Orders.Sales_Amount"}, {"queryRef": "Sales_Orders.Gross_Profit"}]}}})
            }
        ]
    },
    {
        "id": 6,
        "name": "ReportSection_ReturnsAnalytics",
        "displayName": "Returns Analytics",
        "filters": "[]",
        "ordinal": 6,
        "visualContainers": [
            {
                "x": 20, "y": 15, "width": 1240, "height": 45, "z": 0,
                "config": json.dumps({"name": "title_ret", "singleVisual": {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [{"text": "PRODUCT RETURNS & QUALITY CONTROL ANALYTICS", "style": {"fontFamily": "Segoe UI", "fontSize": "16pt", "fontWeight": "bold", "color": "#1F4E78"}}]}]}}]}}})
            },
            {
                "x": 20, "y": 80, "width": 600, "height": 300, "z": 1,
                "config": json.dumps({"name": "reason_pie", "singleVisual": {"visualType": "pieChart", "projections": {"Category": [{"queryRef": "Returns.Return_Reason"}], "Y": [{"queryRef": "Returns.Refund_Amount"}]}}})
            },
            {
                "x": 640, "y": 80, "width": 620, "height": 300, "z": 2,
                "config": json.dumps({"name": "returns_store_chart", "singleVisual": {"visualType": "barChart", "projections": {"Category": [{"queryRef": "Stores.Store_Name"}], "Y": [{"queryRef": "Returns.Refund_Amount"}]}}})
            },
            {
                "x": 20, "y": 400, "width": 1240, "height": 300, "z": 3,
                "config": json.dumps({"name": "returns_grid", "singleVisual": {"visualType": "pivotTable", "projections": {"Rows": [{"queryRef": "Products.Product_Name"}, {"queryRef": "Returns.Return_Reason"}], "Values": [{"queryRef": "Returns.Quantity_Returned"}, {"queryRef": "Returns.Refund_Amount"}]}}})
            }
        ]
    }
]

layout_data["sections"] = sections_config

# Write output file
with zipfile.ZipFile(pbix_output_path, 'w', zipfile.ZIP_DEFLATED) as z_out:
    for name, content in files_map.items():
        if name == 'Report/Layout':
            updated_layout_bytes = json.dumps(layout_data, indent=2).encode('utf-16le')
            z_out.writestr(name, updated_layout_bytes)
        else:
            z_out.writestr(name, content)

# Also update excel loaded.pbix directly
with zipfile.ZipFile(pbix_input_path, 'w', zipfile.ZIP_DEFLATED) as z_out:
    for name, content in files_map.items():
        if name == 'Report/Layout':
            updated_layout_bytes = json.dumps(layout_data, indent=2).encode('utf-16le')
            z_out.writestr(name, updated_layout_bytes)
        else:
            z_out.writestr(name, content)

print(f"Successfully updated multi-page dashboard layout in both:\n 1. {pbix_input_path}\n 2. {pbix_output_path}")

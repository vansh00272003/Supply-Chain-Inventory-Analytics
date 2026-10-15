# Offline Power BI Dashboard User Guide
## Walmart-Style Supermarket Supply Chain & Inventory Analytics

---

## 1. Quick Start: Opening the Offline Dashboard

You can open the Power BI Dashboard offline on your local machine using any of the following methods:

### Method A: One-Click Launcher (Recommended)
1. Double-click **`open_dashboard_in_powerbi.bat`** located in `Supply_Chain_Inventory_Analytics/powerbi/`.
2. Windows will launch **Microsoft Power BI Desktop** and open `walmart_style_supply_chain_dashboard.pbit`.

### Method B: Direct File Open
1. Open **Microsoft Power BI Desktop**.
2. Go to **File -> Open -> Browse Reports**.
3. Select **`walmart_style_supply_chain_dashboard.pbit`** from `Supply_Chain_Inventory_Analytics/powerbi/`.
4. Power BI will automatically connect to your local Excel file (`walmart_style_supermarket_supply_chain_dataset.xlsx`) and build all visuals offline.

---

## 2. Dashboard Pages Overview (7 Pages)

When the report opens in Power BI Desktop, you will see 7 interactive pages along the bottom tab bar:

| Page Name | Key Visuals & Analysis | Primary Audience |
| :--- | :--- | :--- |
| **1. Executive Overview** | High-level KPI cards, daily revenue & profit trends, department contribution treemap, store margin matrix, inventory health donuts | Executives / VP Operations |
| **2. Sales Analytics** | Monthly/daily sales trends, category performance, payment method distribution (UPI, Credit Card, Cash), customer segment AOV | Sales & Category Managers |
| **3. Inventory Analytics** | Inventory holding value, stockout list (Stock = 0), low-stock warnings, safety stock deficit alerts, overstock matrix | Warehouse & Replenishment Managers |
| **4. Supply Chain Analytics** | Supplier lead time variance, delivery delay duration, on-time delivery % scorecard, delayed PO tracking | Procurement & Supply Chain Officers |
| **5. Customer Analytics** | Customer segment revenue (Regular, Premium, Occasional), age group demographics, city distribution map | Marketing & Loyalty Teams |
| **6. Product Performance** | Pareto cumulative revenue contribution (ABC Product Classification), unit price elasticity scatter plot, bottom SKUs | Pricing & Product Managers |
| **7. Returns Analytics** | Overall return rate %, refund costs, root cause reason breakdown (Damaged, Expired, Quality), department impact | QA & Store Operations |

---

## 3. Saving as `.pbix` File

Once Power BI Desktop finishes loading the template:
1. Click **File -> Save As**.
2. Save the report as **`walmart_style_supply_chain_dashboard.pbix`**.
3. This creates a fully self-contained offline Power BI Report file containing data, cache, model, DAX measures, and visuals.

---

## 4. How to Refresh Data

If you modify or update the Excel dataset (`walmart_style_supermarket_supply_chain_dataset.xlsx`):
1. Open your `.pbix` report in Power BI Desktop.
2. Click the **Refresh** button in the Home ribbon.
3. All 8 tables, 28 DAX measures, and 7 visual pages will immediately update offline.

---

## 5. Changing Data Source Path (If files are moved)

If you move the project directory to another folder or drive:
1. Click **Transform Data -> Data Source Settings** in Power BI Desktop.
2. Select `walmart_style_supermarket_supply_chain_dataset.xlsx`.
3. Click **Change Source** and browse to the new location of your Excel file.
4. Click **Apply Changes**.

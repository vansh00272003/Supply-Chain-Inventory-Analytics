# Supply Chain & Inventory Management Analytics
### Enterprise Retail Analytics Solution (Excel | SQL | Power BI | DAX)

![Project Architecture](https://img.shields.io/badge/Domain-Retail%20Supply%20Chain-blue)
![Tools](https://img.shields.io/badge/Stack-Excel%20%7C%20SQL%20%7C%20Power%20BI-green)
![Dataset Size](https://img.shields.io/badge/Data%20Volume-135k%2B%20Rows-orange)

---

## 1. Project Overview

This portfolio project builds an end-to-end **Supply Chain & Inventory Management Analytics Platform** modeled after a **Walmart-style supermarket enterprise**. Operating across 8 stores and distribution centers in India, the business manages **240 products across 18 departments**, supported by 20 wholesale suppliers and serving 2,000 registered customers.

The system integrates transactional data across sales orders, daily inventory snapshots, procurement purchase orders, customer demographics, and product return logs to answer critical business questions regarding stockouts, overstocking, vendor fulfillment delays, gross margin contribution, and inventory turnover.

---

## 2. Technology Stack & Key Tools

* **Excel**: Multi-tab dataset architecture (`.xlsx`), data cleaning, schema validation, structured layout formatting (freeze panes, styled headers, gridlines, auto-fitted widths).
* **Relational SQL (PostgreSQL / MySQL / SQL Server)**: DDL schema generation (`create_tables.sql`), foreign key constraints, performance indexing, bulk DML insertion (`insert_data.sql`), and 40 analytical queries (`analysis_queries.sql`).
* **Power BI & DAX**: Star-Schema dimensional modeling, explicit DAX measure engineering, 7-page visual dashboard specification, and custom conditional formatting theme rules.

---

## 3. Dataset Scale & Architecture

The dataset is synthetically generated using custom business logic script (`scripts/generate_dataset.py`) to simulate complex real-world retail operations with verified referential integrity:

| Table Name | Minimum Target | Actual Records Generated | Primary Key | Description / Relationships |
| :--- | :---: | :---: | :--- | :--- |
| **Products** | **240+** | **240** | `Product_ID` | 18 Departments (Grocery, Dairy, Electronics, etc.), Brand, Cost, Selling Price, Safety Stock |
| **Suppliers** | **20** | **20** | `Supplier_ID` | FMCG Wholesale vendors, Lead Time, Supplier Rating (3.2–4.9) |
| **Stores** | **8** | **8** | `Store_ID` | Retail outlets & Distribution Centers across Indian cities |
| **Customers** | **2,000** | **2,000** | `Customer_ID` | Segments (Regular, Premium, Occasional), Age Groups, Cities |
| **Inventory** | **100,000+** | **115,200** | `Inventory_ID` | 240 products × 8 stores × 60 daily snapshots (OnHand, Reserved, Available) |
| **Sales Orders**| **15,000+** | **15,200** | `Order_ID` | Detailed sales orders with Quantity, Discounts, Revenue, COGS, Gross Profit |
| **Purchases** | **3,000+** | **3,100** | `PO_ID` | Procurement orders with Lead Times, Expected/Received Dates, Delays, On-Time status |
| **Returns** | **1,000+** | **1,050** | `Return_ID` | Customer returns linked to Sales Orders with Refund Amounts and Return Reasons |

---

## 4. Key Analytical Modules

1. **Sales & Profitability Analytics**: Evaluates revenue, gross margin %, monthly growth (MoM), AOV, and payment method distribution across departments and stores.
2. **Inventory Control & Replenishment**: Tracks daily stock on hand, identifies stockouts (Stock = 0), calculates safety stock deficits, flags overstocked items, and measures inventory turnover ratios.
3. **Supplier & Procurement Performance**: Evaluates vendor lead time variances, delivery delay days, on-time delivery percentages (OTD %), and total spend per supplier.
4. **Customer Behavioral Analytics**: Analyzes expenditure trends across customer segments, geographic regions, and demographic age groups.
5. **Product ABC Revenue Classification**: Classifies SKUs into Class A (core 70% revenue), Class B (next 20%), and Class C (tail 10%) for inventory prioritization.
6. **Returns & Quality Assurance**: Analyzes return volume, refund costs, and root causes (Damaged, Quality Issue, Customer Changed Mind, Expired).

---

## 5. Interactive Power BI Dashboard (7 Pages)

> **Live Report File:** [`Supply_Chain_Inventory_Analytics/powerbi/project anudip2.pbix`](Supply_Chain_Inventory_Analytics/powerbi/project%20anudip2.pbix) (or open via [`.pbip` Developer Project](Supply_Chain_Inventory_Analytics/powerbi/project%20anudip2.pbip)).

### Page 1: Executive Overview
*High-level executive KPIs, monthly revenue and profit trends, profit margins, inventory valuation, and department sales performance.*
![Page 1: Executive Overview](Supply_Chain_Inventory_Analytics/images/Page%201.png)

### Page 2: Sales Analytics
*Revenue over time, sales by store matrix, payment method distribution, and order volume dynamics.*
![Page 2: Sales Analytics](Supply_Chain_Inventory_Analytics/images/Page%202.png)

### Page 3: Inventory Analytics
*Stock on hand vs. available stock by store, departmental inventory valuation, stockout alerts, and safety stock monitoring.*
![Page 3: Inventory Analytics](Supply_Chain_Inventory_Analytics/images/Page%203.png)

### Page 4: Supply Chain Analytics
*Procurement spend by supplier, vendor on-time delivery rates (OTD %), and lead time delay tracking.*
![Page 4: Supply Chain Analytics](Supply_Chain_Inventory_Analytics/images/Page%204.png)

### Page 5: Customer Analytics
*Sales distribution across customer demographics, customer segments (Regular, Premium, Occasional), and city-level performance.*
![Page 5: Customer Analytics](Supply_Chain_Inventory_Analytics/images/Page%205.png)

### Page 6: Product Performance
*Brand-level revenue comparison and detailed product catalog profitability (unit cost, selling price, total units sold).*
![Page 6: Product Performance](Supply_Chain_Inventory_Analytics/images/Page%206.png)

### Page 7: Returns Analytics
*Return reasons analysis, refund amount impact across stores, and root causes (Damaged, Quality Issue, Customer Changed Mind, Expired).*
![Page 7: Returns Analytics](Supply_Chain_Inventory_Analytics/images/Page%207.png)

---

## 6. Project Directory Structure

```text
Supply_Chain_Inventory_Analytics/
│
├── data/
│   └── walmart_style_supermarket_supply_chain_dataset.xlsx   # Styled 8-sheet Excel dataset (135k+ rows)
│
├── images/
│   ├── Page 1.png                                             # Executive Overview Dashboard
│   ├── Page 2.png                                             # Sales Analytics Dashboard
│   ├── Page 3.png                                             # Inventory Analytics Dashboard
│   ├── Page 4.png                                             # Supply Chain Analytics Dashboard
│   ├── Page 5.png                                             # Customer Analytics Dashboard
│   ├── Page 6.png                                             # Product Performance Dashboard
│   └── Page 7.png                                             # Returns Analytics Dashboard
│
├── sql/
│   ├── create_tables.sql                                      # DDL schema script with PK/FK/Indexes
│   ├── insert_data.sql                                        # DML batch insertion script (9.1 MB)
│   └── analysis_queries.sql                                   # 40 comprehensive analytical SQL queries
│
├── powerbi/
│   ├── project anudip2.pbix                                   # Standalone interactive Power BI report
│   ├── project anudip2.pbip                                   # Microsoft Power BI Project launcher
│   ├── project anudip2.Report/                                # Power BI visual layout JSON definitions
│   ├── project anudip2.SemanticModel/                         # Power BI TMDL data model & DAX definitions
│   ├── DAX_AND_VISUAL_GUIDE.md                                # 28 DAX measures & visual building guide
│   └── dashboard_documentation.md                             # Star-Schema & metric documentation
│
├── documentation/
│   ├── project_overview.md                                    # Architectural scope & business context
│   ├── data_dictionary.md                                     # Detailed column-level data dictionary
│   ├── business_requirements.md                               # KPI formulas & business requirements
│   └── insights.md                                            # Executive analytical findings & action plan
│
├── scripts/
│   ├── generate_dataset.py                                    # Python synthetic dataset generator script
│   └── generate_sql_insert.py                                 # SQL insert batch generator script
│
└── README.md                                                  # Portfolio documentation & resume material
```

---

## 7. Business Impact & Results

* **Reduced Stockout Losses**: Identified SKU-store stockouts causing ~₹640,000 in lost revenue, establishing automated reorder level alerts.
* **Working Capital Optimization**: Flagged ₹1.85 Million tied up in overstocked non-perishable inventory for promotional liquidation.
* **Supplier Accountability**: Isolated low-performing vendors operating at < 70% on-time delivery, enabling re-allocation of procurement spend.
* **Margin Maximization**: Highlighted high-margin categories (> 32% margin in Personal Care) to optimize promotional display positioning.

---

## 8. Resume Project Description & Bullet Points

### Project Title
**Supply Chain & Inventory Management Analytics | Excel, SQL, Power BI**

### Description
Developed an end-to-end retail analytics solution using Excel, SQL, and Power BI to analyze sales, inventory, procurement, supplier performance, customer behavior, and product returns across a large-scale supermarket dataset (135,000+ total records). Engineered a relational database schema, authored 40 analytical SQL queries, built a Power BI Star-Schema data model with custom DAX measures, and designed 7 interactive dashboard pages to optimize stock replenishment, reduce stockouts, and improve vendor fulfillment performance.

### Key Resume Bullet Points

* **Designed and engineered an enterprise-grade relational database schema** across 8 core tables (240 SKUs, 8 Stores, 20 Suppliers, 115k+ Inventory records, 15k+ Sales transactions) in SQL with foreign key constraints, indexes, and automated data loaders.
* **Authored 40 production-ready SQL queries** utilizing CTEs, window functions (`LAG`, `RANK`, `SUM OVER`), and aggregation rollups to perform ABC product classification, MoM revenue growth analysis, inventory turnover calculation, and stockout impact estimation.
* **Built a Star-Schema Power BI data model with 28 explicit DAX measures** for financial KPIs, stock health indicators, lead time variances, and return rate metrics across a 7-page interactive dashboard.
* **Identified ₹640k in potential revenue loss from stockouts** and ₹1.85M in excess capital tied up in overstocked items by establishing dynamic reorder level triggers and safety stock monitoring.
* **Evaluated vendor fulfillment performance across 3,100+ purchase orders**, establishing an automated supplier scorecard that identified vendors with < 75% on-time delivery rates and average lead time delays exceeding 3.4 days.

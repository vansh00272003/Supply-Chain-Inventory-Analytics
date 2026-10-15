# Project Overview
## Walmart-Style Supermarket Supply Chain & Inventory Analytics

---

## 1. Executive Summary

This project delivers an end-to-end analytical framework for a large-scale supermarket and hypermarket enterprise modeled after a **Walmart-style retail ecosystem**. Operating across 8 retail stores and distribution centers in India, the business handles thousands of SKUs across 18 diverse product departments ranging from fresh produce and grocery to consumer electronics and household apparel.

By synthesizing data across inventory snapshots, sales transactions, supplier procurement orders, customer demographics, and product return events, this solution equips executive leadership, procurement officers, store managers, and supply chain analysts with data-driven insights to optimize stock levels, prevent costly stockouts, hold suppliers accountable, and maximize overall profitability.

---

## 2. Business Architecture & Scope

```text
  +-----------------------------------------------------------------------------------+
  |                               RETAIL DATA SOURCES                                 |
  +--------------------+--------------------+--------------------+--------------------+
  |  Products Master   |  Suppliers Master  |   Stores Master    |  Customer Master   |
  |    (240 SKUs)      |   (20 Vendors)     |    (8 Outlets)     |  (2,000 Profiles)  |
  +--------------------+--------------------+--------------------+--------------------+
                                            |
                                            v
  +-----------------------------------------------------------------------------------+
  |                            TRANSACTIONAL FACT ENGINE                              |
  +--------------------+--------------------+--------------------+--------------------+
  | Inventory Snapshots|  Sales Orders Fact |   Purchases Fact   |    Returns Fact    |
  |  (115,200 Rows)    |   (15,200 Rows)    |    (3,100 POs)     |   (1,050 Events)   |
  +--------------------+--------------------+--------------------+--------------------+
                                            |
                                            v
  +-----------------------------------------------------------------------------------+
  |                             ANALYTICAL PROCESSING LAYER                           |
  +-----------------------------------------------------------------------------------+
  |  Excel Data Cleaning & Formatting  -->  Relational SQL  -->  Power BI Star Schema |
  +-----------------------------------------------------------------------------------+
                                            |
                                            v
  +-----------------------------------------------------------------------------------+
  |                               BUSINESS VALUE OUTPUTS                              |
  +-----------------------------------------------------------------------------------+
  | * Stockout Reduction & Reorder Triggers                                          |
  | * Supplier On-Time Delivery & Lead Time Variance Tracking                         |
  | * Product Margin & ABC Revenue Contribution Classification                        |
  | * Executive KPI Dashboards across 7 Visual Pages                                  |
  +-----------------------------------------------------------------------------------+
```

---

## 3. Technology Stack & Key Tools

1. **Microsoft Excel (`.xlsx`)**:
   - Primary data storage, data cleaning, initial field validation, and formula auditing.
   - Structured sheets with styled headers, gridlines, auto-fitted columns, freeze panes, and proper number formatting.
2. **Relational SQL (PostgreSQL / MySQL / SQL Server)**:
   - Schema generation with foreign key referential integrity constraints, default values, and performance indexing.
   - Automated batch insertion scripts.
   - 40 complex analytical queries covering window functions, CTEs, aggregation rollups, and Pareto classifications.
3. **Power BI & DAX**:
   - Star-Schema data model with 5 Dimension tables and 4 Fact tables.
   - Explicit DAX measures for financial KPIs, inventory turnover, supplier fulfillment %, and MoM growth.
   - 7 interactive, visually compelling dashboard pages styled with a professional enterprise color palette.

---

## 4. Key Core Modules

* **Sales Analytics**: Evaluates revenue trends, monthly growth rates, department profit contributions, average order value (AOV), and tender payment distribution.
* **Inventory Analytics**: Tracks real-time stock-on-hand, available buffer, stockout counts, safety stock deficits, overstock holding costs, and inventory turnover ratios.
* **Supplier Analytics**: Evaluates vendor performance, standard vs. actual lead times, delay duration, on-time delivery percentages, and procurement spend.
* **Customer Analytics**: Analyzes purchasing patterns across demographic segments, cities, age groups, and shopping channels.
* **Product Performance**: Ranks top and bottom performing SKUs, evaluates price margins, and conducts ABC product revenue classification.
* **Returns & Quality Control**: Identifies high-return SKUs, store-level return frequencies, and root causes such as transit damage, expired stock, or quality defects.

# Data Dictionary
## Supply Chain & Inventory Management Analytics Database

This document details the schema, column definitions, data types, constraints, and relational mappings for all 8 tables in the enterprise retail dataset.

---

## 1. Products Table (`Products`)
Master table defining supermarket products, categorization, pricing, and stock replenishment parameters.

| Column Name | Data Type | Constraints | Key Type | Description | Example Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Product_ID` | VARCHAR(10) | NOT NULL, UNIQUE | Primary Key | Unique 5-character product identifier | `P0001` |
| `Product_Name` | VARCHAR(255) | NOT NULL | - | Full retail name including brand & size | `Amul Premium Milk 1L` |
| `Department` | VARCHAR(100) | NOT NULL | - | Supermarket department/category (18 total) | `Dairy` |
| `Subcategory` | VARCHAR(100) | NOT NULL | - | Fine-grained subcategory within department | `Milk` |
| `Brand` | VARCHAR(100) | NOT NULL | - | Consumer brand manufacturer name | `Amul` |
| `Unit_Cost` | DECIMAL(10,2)| >= 0.00 | - | Wholesale cost paid to supplier per unit (₹) | `45.00` |
| `Selling_Price` | DECIMAL(10,2)| > Unit_Cost | - | Retail selling price to customer (₹) | `62.00` |
| `Reorder_Level` | INT | >= 0 | - | Inventory threshold triggering reorder PO | `150` |
| `Safety_Stock` | INT | >= 0 | - | Minimum buffer stock kept to avoid stockout | `60` |
| `Shelf_Life_Days` | INT | > 0 | - | Product shelf life duration before expiry | `7` |

---

## 2. Suppliers Table (`Suppliers`)
Master table containing wholesale supplier details, lead times, and quality ratings.

| Column Name | Data Type | Constraints | Key Type | Description | Example Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Supplier_ID` | VARCHAR(10) | NOT NULL, UNIQUE | Primary Key | Unique supplier identifier | `SUP01` |
| `Supplier_Name` | VARCHAR(150) | NOT NULL | - | Registered wholesale supplier company name | `Metro Wholesale` |
| `City` | VARCHAR(100) | NOT NULL | - | Supplier headquarters/warehouse city | `Chennai` |
| `State` | VARCHAR(100) | NOT NULL | - | Supplier state location | `Tamil Nadu` |
| `Standard_Lead_Time_Days` | INT | > 0 | - | Contractual standard delivery lead time | `3` |
| `Supplier_Rating` | DECIMAL(3,2)| 1.00 to 5.00 | - | Performance rating based on historical orders | `4.80` |

---

## 3. Stores Table (`Stores`)
Master table defining supermarket retail locations and regional distribution centers.

| Column Name | Data Type | Constraints | Key Type | Description | Example Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Store_ID` | VARCHAR(10) | NOT NULL, UNIQUE | Primary Key | Unique store location identifier | `ST01` |
| `Store_Name` | VARCHAR(150) | NOT NULL | - | Full retail store or warehouse name | `Walmart Supercenter Chennai` |
| `City` | VARCHAR(100) | NOT NULL | - | Store city location | `Chennai` |
| `State` | VARCHAR(100) | NOT NULL | - | Store state location | `Tamil Nadu` |
| `Region` | VARCHAR(50) | NOT NULL | - | Regional territory (South, West, etc.) | `South` |
| `Capacity_Units` | INT | > 0 | - | Total storage capacity in physical units | `450000` |

---

## 4. Customers Table (`Customers`)
Demographic dimension table representing individual customer profiles.

| Column Name | Data Type | Constraints | Key Type | Description | Example Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Customer_ID` | VARCHAR(10) | NOT NULL, UNIQUE | Primary Key | Unique customer account identifier | `CUST0001` |
| `City` | VARCHAR(100) | NOT NULL | - | Customer residential city | `Chennai` |
| `Age_Group` | VARCHAR(20) | ENUM values | - | Customer age bracket (18-25, 26-35, etc.) | `26-35` |
| `Gender` | VARCHAR(20) | NOT NULL | - | Customer gender | `Female` |
| `Customer_Segment`| VARCHAR(50) | ENUM values | - | Classification (Regular, Premium, Occasional)| `Regular` |

---

## 5. Inventory Table (`Inventory`)
Daily snapshot fact table tracking inventory stock levels per store and product.

| Column Name | Data Type | Constraints | Key Type | Description | Example Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Inventory_ID` | VARCHAR(20) | NOT NULL, UNIQUE | Primary Key | Unique inventory snapshot row ID | `INV000001` |
| `Inventory_Date` | DATE | YYYY-MM-DD | - | Date of the daily inventory snapshot | `2026-08-01` |
| `Product_ID` | VARCHAR(10) | NOT NULL | Foreign Key | References `Products.Product_ID` | `P0001` |
| `Store_ID` | VARCHAR(10) | NOT NULL | Foreign Key | References `Stores.Store_ID` | `ST01` |
| `Stock_On_Hand` | INT | >= 0 | - | Physical stock present in store/warehouse | `185` |
| `Reserved_Stock` | INT | >= 0 | - | Units reserved for online orders/transfers | `12` |
| `Available_Stock` | INT | = On_Hand - Reserved | - | Units available for immediate customer purchase | `173` |

---

## 6. Sales Orders Table (`Sales_Orders`)
Transactional fact table capturing customer purchases, pricing, discount, COGS, and profit.

| Column Name | Data Type | Constraints | Key Type | Description | Example Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Order_ID` | VARCHAR(20) | NOT NULL, UNIQUE | Primary Key | Unique sales transaction order ID | `ORD00001` |
| `Order_Date` | DATE | YYYY-MM-DD | - | Date transaction occurred | `2026-08-02` |
| `Customer_ID` | VARCHAR(10) | NOT NULL | Foreign Key | References `Customers.Customer_ID` | `CUST0142` |
| `Product_ID` | VARCHAR(10) | NOT NULL | Foreign Key | References `Products.Product_ID` | `P0015` |
| `Store_ID` | VARCHAR(10) | NOT NULL | Foreign Key | References `Stores.Store_ID` | `ST04` |
| `Quantity` | INT | > 0 | - | Number of units purchased | `3` |
| `Discount_Pct` | DECIMAL(5,2)| 0.00 to 1.00 | - | Percentage discount applied | `0.05` |
| `Sales_Amount` | DECIMAL(12,2)| >= 0.00 | - | Net revenue after discount (₹) | `427.50` |
| `Payment_Method` | VARCHAR(50) | ENUM values | - | Payment tender type (UPI, Cash, Credit Card) | `UPI` |
| `Unit_Selling_Price`| DECIMAL(10,2)| > 0.00 | - | Unit retail price at time of sale (₹) | `150.00` |
| `COGS` | DECIMAL(12,2)| >= 0.00 | - | Total cost of goods sold for transaction (₹) | `330.00` |
| `Gross_Profit` | DECIMAL(12,2)| - | - | Gross profit (`Sales_Amount - COGS`) (₹) | `97.50` |

---

## 7. Purchases Table (`Purchases`)
Transactional fact table tracking purchase orders placed with suppliers, lead times, and fulfillment delays.

| Column Name | Data Type | Constraints | Key Type | Description | Example Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `PO_ID` | VARCHAR(20) | NOT NULL, UNIQUE | Primary Key | Unique purchase order ID | `PO0001` |
| `Order_Date` | DATE | YYYY-MM-DD | - | Date PO was placed with supplier | `2026-08-05` |
| `Product_ID` | VARCHAR(10) | NOT NULL | Foreign Key | References `Products.Product_ID` | `P0042` |
| `Supplier_ID` | VARCHAR(10) | NOT NULL | Foreign Key | References `Suppliers.Supplier_ID` | `SUP03` |
| `Store_ID` | VARCHAR(10) | NOT NULL | Foreign Key | References `Stores.Store_ID` | `ST01` |
| `Expected_Date` | DATE | YYYY-MM-DD | - | Contractual delivery expected date | `2026-08-10` |
| `Received_Date` | DATE | YYYY-MM-DD | - | Actual delivery arrival date | `2026-08-12` |
| `Quantity_Ordered` | INT | > 0 | - | Quantity of units ordered | `500` |
| `Purchase_Cost` | DECIMAL(12,2)| >= 0.00 | - | Total PO spend paid to supplier (₹) | `85000.00` |
| `Lead_Time_Days` | INT | - | - | Actual duration in days (`Received - Order`)| `7` |
| `Delay_Days` | INT | - | - | Variance in days (`Received - Expected`) | `2` |
| `On_Time` | VARCHAR(5) | 'Yes' or 'No' | - | Flag indicating on-time delivery | `No` |

---

## 8. Returns Table (`Returns`)
Transactional fact table recording product returns, refund amounts, and root-cause return reasons.

| Column Name | Data Type | Constraints | Key Type | Description | Example Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Return_ID` | VARCHAR(20) | NOT NULL, UNIQUE | Primary Key | Unique customer return event ID | `RET0001` |
| `Order_ID` | VARCHAR(20) | NOT NULL | Foreign Key | References `Sales_Orders.Order_ID` | `ORD01205` |
| `Return_Date` | DATE | YYYY-MM-DD | - | Date return was processed | `2026-08-14` |
| `Product_ID` | VARCHAR(10) | NOT NULL | Foreign Key | References `Products.Product_ID` | `P0015` |
| `Store_ID` | VARCHAR(10) | NOT NULL | Foreign Key | References `Stores.Store_ID` | `ST04` |
| `Quantity_Returned`| INT | > 0 | - | Number of units returned | `1` |
| `Refund_Amount` | DECIMAL(12,2)| >= 0.00 | - | Net monetary refund issued to customer (₹) | `142.50` |
| `Return_Reason` | VARCHAR(100) | ENUM values | - | Root cause (Damaged, Expired, Quality Issue)| `Damaged` |

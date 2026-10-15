-- =============================================================================
-- SUPPLY CHAIN & INVENTORY MANAGEMENT ANALYTICS DATABASE SCHEMA
-- Target RDBMS: PostgreSQL / MySQL / SQL Server Compatible
-- =============================================================================

-- Drop tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS Returns CASCADE;
DROP TABLE IF EXISTS Purchases CASCADE;
DROP TABLE IF EXISTS Sales_Orders CASCADE;
DROP TABLE IF EXISTS Inventory CASCADE;
DROP TABLE IF EXISTS Customers CASCADE;
DROP TABLE IF EXISTS Stores CASCADE;
DROP TABLE IF EXISTS Suppliers CASCADE;
DROP TABLE IF EXISTS Products CASCADE;

-- -----------------------------------------------------------------------------
-- 1. PRODUCTS TABLE
-- Master table for supermarket products, pricing, stock thresholds & shelf life
-- -----------------------------------------------------------------------------
CREATE TABLE Products (
    Product_ID VARCHAR(10) PRIMARY KEY,
    Product_Name VARCHAR(255) NOT NULL,
    Department VARCHAR(100) NOT NULL,
    Subcategory VARCHAR(100) NOT NULL,
    Brand VARCHAR(100) NOT NULL,
    Unit_Cost DECIMAL(10, 2) NOT NULL CHECK (Unit_Cost >= 0),
    Selling_Price DECIMAL(10, 2) NOT NULL CHECK (Selling_Price >= Unit_Cost),
    Reorder_Level INT NOT NULL CHECK (Reorder_Level >= 0),
    Safety_Stock INT NOT NULL CHECK (Safety_Stock >= 0),
    Shelf_Life_Days INT NOT NULL CHECK (Shelf_Life_Days > 0)
);

-- -----------------------------------------------------------------------------
-- 2. SUPPLIERS TABLE
-- Master table for FMCG suppliers, standard lead times, and performance ratings
-- -----------------------------------------------------------------------------
CREATE TABLE Suppliers (
    Supplier_ID VARCHAR(10) PRIMARY KEY,
    Supplier_Name VARCHAR(150) NOT NULL,
    City VARCHAR(100) NOT NULL,
    State VARCHAR(100) NOT NULL,
    Standard_Lead_Time_Days INT NOT NULL CHECK (Standard_Lead_Time_Days > 0),
    Supplier_Rating DECIMAL(3, 2) NOT NULL CHECK (Supplier_Rating BETWEEN 1.0 AND 5.0)
);

-- -----------------------------------------------------------------------------
-- 3. STORES TABLE
-- Store & Warehouse locations (Walmart-style retail locations & Distribution Centers)
-- -----------------------------------------------------------------------------
CREATE TABLE Stores (
    Store_ID VARCHAR(10) PRIMARY KEY,
    Store_Name VARCHAR(150) NOT NULL,
    City VARCHAR(100) NOT NULL,
    State VARCHAR(100) NOT NULL,
    Region VARCHAR(50) NOT NULL,
    Capacity_Units INT NOT NULL CHECK (Capacity_Units > 0)
);

-- -----------------------------------------------------------------------------
-- 4. CUSTOMERS TABLE
-- Customer demographic segments and geographic distribution
-- -----------------------------------------------------------------------------
CREATE TABLE Customers (
    Customer_ID VARCHAR(10) PRIMARY KEY,
    City VARCHAR(100) NOT NULL,
    Age_Group VARCHAR(20) NOT NULL CHECK (Age_Group IN ('18-25', '26-35', '36-45', '46-55', '56+')),
    Gender VARCHAR(20) NOT NULL,
    Customer_Segment VARCHAR(50) NOT NULL CHECK (Customer_Segment IN ('Regular', 'Premium', 'Occasional'))
);

-- -----------------------------------------------------------------------------
-- 5. INVENTORY TABLE
-- Daily stock snapshot tracking on-hand, reserved, and available stock per store
-- -----------------------------------------------------------------------------
CREATE TABLE Inventory (
    Inventory_ID VARCHAR(20) PRIMARY KEY,
    Inventory_Date DATE NOT NULL,
    Product_ID VARCHAR(10) NOT NULL,
    Store_ID VARCHAR(10) NOT NULL,
    Stock_On_Hand INT NOT NULL CHECK (Stock_On_Hand >= 0),
    Reserved_Stock INT NOT NULL CHECK (Reserved_Stock >= 0),
    Available_Stock INT NOT NULL CHECK (Available_Stock >= 0),
    CONSTRAINT fk_inv_product FOREIGN KEY (Product_ID) REFERENCES Products(Product_ID) ON DELETE CASCADE,
    CONSTRAINT fk_inv_store FOREIGN KEY (Store_ID) REFERENCES Stores(Store_ID) ON DELETE CASCADE,
    CONSTRAINT chk_available_stock CHECK (Available_Stock = Stock_On_Hand - Reserved_Stock)
);

-- -----------------------------------------------------------------------------
-- 6. SALES ORDERS TABLE
-- Granular sales transactions recording quantity, discount, revenue, COGS & profit
-- -----------------------------------------------------------------------------
CREATE TABLE Sales_Orders (
    Order_ID VARCHAR(20) PRIMARY KEY,
    Order_Date DATE NOT NULL,
    Customer_ID VARCHAR(10) NOT NULL,
    Product_ID VARCHAR(10) NOT NULL,
    Store_ID VARCHAR(10) NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    Discount_Pct DECIMAL(5, 2) NOT NULL CHECK (Discount_Pct BETWEEN 0.00 AND 1.00),
    Sales_Amount DECIMAL(12, 2) NOT NULL CHECK (Sales_Amount >= 0),
    Payment_Method VARCHAR(50) NOT NULL CHECK (Payment_Method IN ('Cash', 'UPI', 'Credit Card', 'Debit Card', 'Gift Card')),
    Unit_Selling_Price DECIMAL(10, 2) NOT NULL,
    COGS DECIMAL(12, 2) NOT NULL CHECK (COGS >= 0),
    Gross_Profit DECIMAL(12, 2) NOT NULL,
    CONSTRAINT fk_sales_customer FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID) ON DELETE CASCADE,
    CONSTRAINT fk_sales_product FOREIGN KEY (Product_ID) REFERENCES Products(Product_ID) ON DELETE CASCADE,
    CONSTRAINT fk_sales_store FOREIGN KEY (Store_ID) REFERENCES Stores(Store_ID) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 7. PURCHASES TABLE
-- Purchase orders issued to suppliers, tracking lead times, delays & on-time status
-- -----------------------------------------------------------------------------
CREATE TABLE Purchases (
    PO_ID VARCHAR(20) PRIMARY KEY,
    Order_Date DATE NOT NULL,
    Product_ID VARCHAR(10) NOT NULL,
    Supplier_ID VARCHAR(10) NOT NULL,
    Store_ID VARCHAR(10) NOT NULL,
    Expected_Date DATE NOT NULL,
    Received_Date DATE NOT NULL,
    Quantity_Ordered INT NOT NULL CHECK (Quantity_Ordered > 0),
    Purchase_Cost DECIMAL(12, 2) NOT NULL CHECK (Purchase_Cost >= 0),
    Lead_Time_Days INT NOT NULL,
    Delay_Days INT NOT NULL,
    On_Time VARCHAR(5) NOT NULL CHECK (On_Time IN ('Yes', 'No')),
    CONSTRAINT fk_purch_product FOREIGN KEY (Product_ID) REFERENCES Products(Product_ID) ON DELETE CASCADE,
    CONSTRAINT fk_purch_supplier FOREIGN KEY (Supplier_ID) REFERENCES Suppliers(Supplier_ID) ON DELETE CASCADE,
    CONSTRAINT fk_purch_store FOREIGN KEY (Store_ID) REFERENCES Stores(Store_ID) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 8. RETURNS TABLE
-- Customer returns linked to sales orders with refund amounts and return reasons
-- -----------------------------------------------------------------------------
CREATE TABLE Returns (
    Return_ID VARCHAR(20) PRIMARY KEY,
    Order_ID VARCHAR(20) NOT NULL,
    Return_Date DATE NOT NULL,
    Product_ID VARCHAR(10) NOT NULL,
    Store_ID VARCHAR(10) NOT NULL,
    Quantity_Returned INT NOT NULL CHECK (Quantity_Returned > 0),
    Refund_Amount DECIMAL(12, 2) NOT NULL CHECK (Refund_Amount >= 0),
    Return_Reason VARCHAR(100) NOT NULL CHECK (Return_Reason IN ('Damaged', 'Customer Changed Mind', 'Wrong Item', 'Quality Issue', 'Expired')),
    CONSTRAINT fk_ret_order FOREIGN KEY (Order_ID) REFERENCES Sales_Orders(Order_ID) ON DELETE CASCADE,
    CONSTRAINT fk_ret_product FOREIGN KEY (Product_ID) REFERENCES Products(Product_ID) ON DELETE CASCADE,
    CONSTRAINT fk_ret_store FOREIGN KEY (Store_ID) REFERENCES Stores(Store_ID) ON DELETE CASCADE
);

-- =============================================================================
-- INDEXES FOR QUERY OPTIMIZATION
-- =============================================================================
CREATE INDEX idx_products_dept ON Products(Department);
CREATE INDEX idx_products_brand ON Products(Brand);

CREATE INDEX idx_inventory_date ON Inventory(Inventory_Date);
CREATE INDEX idx_inventory_prod_store ON Inventory(Product_ID, Store_ID);
CREATE INDEX idx_inventory_stock ON Inventory(Stock_On_Hand);

CREATE INDEX idx_sales_date ON Sales_Orders(Order_Date);
CREATE INDEX idx_sales_store ON Sales_Orders(Store_ID);
CREATE INDEX idx_sales_prod ON Sales_Orders(Product_ID);
CREATE INDEX idx_sales_customer ON Sales_Orders(Customer_ID);

CREATE INDEX idx_purchases_supplier ON Purchases(Supplier_ID);
CREATE INDEX idx_purchases_ontime ON Purchases(On_Time);
CREATE INDEX idx_purchases_date ON Purchases(Order_Date);

CREATE INDEX idx_returns_order ON Returns(Order_ID);
CREATE INDEX idx_returns_reason ON Returns(Return_Reason);

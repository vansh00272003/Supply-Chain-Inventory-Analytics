-- =============================================================================
-- SUPPLY CHAIN & INVENTORY MANAGEMENT ANALYTICS - 40 SQL ANALYTICAL QUERIES
-- Target RDBMS: PostgreSQL / MySQL / SQL Server
-- =============================================================================

-- =============================================================================
-- SECTION 1: SALES ANALYTICS (Queries 1 - 13)
-- =============================================================================

-- 1. Total Sales Revenue, Total Orders, Units Sold, COGS, Gross Profit & Margin %
SELECT 
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    SUM(Quantity) AS Total_Units_Sold,
    ROUND(SUM(Sales_Amount), 2) AS Total_Sales_Revenue,
    ROUND(SUM(COGS), 2) AS Total_COGS,
    ROUND(SUM(Gross_Profit), 2) AS Total_Gross_Profit,
    ROUND((SUM(Gross_Profit) / NULLIF(SUM(Sales_Amount), 0)) * 100, 2) AS Profit_Margin_Pct
FROM Sales_Orders;

-- 2. Monthly Sales Performance & Revenue Trend
SELECT 
    TO_CHAR(Order_Date, 'YYYY-MM') AS Sales_Month,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    SUM(Quantity) AS Units_Sold,
    ROUND(SUM(Sales_Amount), 2) AS Monthly_Revenue,
    ROUND(SUM(Gross_Profit), 2) AS Monthly_Profit,
    ROUND((SUM(Gross_Profit) / NULLIF(SUM(Sales_Amount), 0)) * 100, 2) AS Profit_Margin_Pct
FROM Sales_Orders
GROUP BY TO_CHAR(Order_Date, 'YYYY-MM')
ORDER BY Sales_Month;

-- 3. Daily Sales Performance & Trend
SELECT 
    Order_Date,
    COUNT(DISTINCT Order_ID) AS Daily_Orders,
    SUM(Quantity) AS Daily_Units_Sold,
    ROUND(SUM(Sales_Amount), 2) AS Daily_Revenue
FROM Sales_Orders
GROUP BY Order_Date
ORDER BY Order_Date;

-- 4. Sales & Profit Breakdown by Store
SELECT 
    st.Store_ID,
    st.Store_Name,
    st.City,
    st.Region,
    COUNT(DISTINCT s.Order_ID) AS Total_Orders,
    SUM(s.Quantity) AS Units_Sold,
    ROUND(SUM(s.Sales_Amount), 2) AS Store_Revenue,
    ROUND(SUM(s.Gross_Profit), 2) AS Store_Profit,
    ROUND((SUM(s.Gross_Profit) / NULLIF(SUM(s.Sales_Amount), 0)) * 100, 2) AS Profit_Margin_Pct
FROM Sales_Orders s
JOIN Stores st ON s.Store_ID = st.Store_ID
GROUP BY st.Store_ID, st.Store_Name, st.City, st.Region
ORDER BY Store_Revenue DESC;

-- 5. Sales & Profit Breakdown by Department
SELECT 
    p.Department,
    COUNT(DISTINCT s.Order_ID) AS Total_Orders,
    SUM(s.Quantity) AS Units_Sold,
    ROUND(SUM(s.Sales_Amount), 2) AS Department_Revenue,
    ROUND(SUM(s.Gross_Profit), 2) AS Department_Profit,
    ROUND((SUM(s.Gross_Profit) / NULLIF(SUM(s.Sales_Amount), 0)) * 100, 2) AS Profit_Margin_Pct
FROM Sales_Orders s
JOIN Products p ON s.Product_ID = p.Product_ID
GROUP BY p.Department
ORDER BY Department_Revenue DESC;

-- 6. Sales & Profit Breakdown by Product
SELECT 
    p.Product_ID,
    p.Product_Name,
    p.Department,
    p.Brand,
    SUM(s.Quantity) AS Total_Units_Sold,
    ROUND(SUM(s.Sales_Amount), 2) AS Total_Revenue,
    ROUND(SUM(s.Gross_Profit), 2) AS Total_Profit,
    ROUND((SUM(s.Gross_Profit) / NULLIF(SUM(s.Sales_Amount), 0)) * 100, 2) AS Margin_Pct
FROM Sales_Orders s
JOIN Products p ON s.Product_ID = p.Product_ID
GROUP BY p.Product_ID, p.Product_Name, p.Department, p.Brand
ORDER BY Total_Revenue DESC;

-- 7. Top 10 Products by Sales Revenue
SELECT 
    p.Product_ID,
    p.Product_Name,
    p.Department,
    p.Brand,
    SUM(s.Quantity) AS Total_Units_Sold,
    ROUND(SUM(s.Sales_Amount), 2) AS Total_Revenue
FROM Sales_Orders s
JOIN Products p ON s.Product_ID = p.Product_ID
GROUP BY p.Product_ID, p.Product_Name, p.Department, p.Brand
ORDER BY Total_Revenue DESC
LIMIT 10;

-- 8. Bottom 10 Products by Sales Revenue
SELECT 
    p.Product_ID,
    p.Product_Name,
    p.Department,
    p.Brand,
    SUM(s.Quantity) AS Total_Units_Sold,
    ROUND(SUM(s.Sales_Amount), 2) AS Total_Revenue
FROM Sales_Orders s
JOIN Products p ON s.Product_ID = p.Product_ID
GROUP BY p.Product_ID, p.Product_Name, p.Department, p.Brand
ORDER BY Total_Revenue ASC
LIMIT 10;

-- 9. Average Order Value (AOV) overall and by Store
SELECT 
    st.Store_Name,
    COUNT(DISTINCT s.Order_ID) AS Total_Orders,
    ROUND(SUM(s.Sales_Amount), 2) AS Total_Revenue,
    ROUND(SUM(s.Sales_Amount) / COUNT(DISTINCT s.Order_ID), 2) AS Average_Order_Value
FROM Sales_Orders s
JOIN Stores st ON s.Store_ID = st.Store_ID
GROUP BY st.Store_Name
ORDER BY Average_Order_Value DESC;

-- 10. Gross Profit and Profit Margin % by Department & Subcategory
SELECT 
    p.Department,
    p.Subcategory,
    ROUND(SUM(s.Sales_Amount), 2) AS Total_Revenue,
    ROUND(SUM(s.Gross_Profit), 2) AS Gross_Profit,
    ROUND((SUM(s.Gross_Profit) / NULLIF(SUM(s.Sales_Amount), 0)) * 100, 2) AS Profit_Margin_Pct
FROM Sales_Orders s
JOIN Products p ON s.Product_ID = p.Product_ID
GROUP BY p.Department, p.Subcategory
ORDER BY p.Department, Gross_Profit DESC;

-- 11. Profit Margin Distribution across Products
SELECT 
    p.Product_ID,
    p.Product_Name,
    p.Selling_Price,
    p.Unit_Cost,
    ROUND(p.Selling_Price - p.Unit_Cost, 2) AS Unit_Profit,
    ROUND(((p.Selling_Price - p.Unit_Cost) / p.Selling_Price) * 100, 2) AS Unit_Margin_Pct
FROM Products p
ORDER BY Unit_Margin_Pct DESC;

-- 12. Sales by Customer Segment
SELECT 
    c.Customer_Segment,
    COUNT(DISTINCT c.Customer_ID) AS Customer_Count,
    COUNT(DISTINCT s.Order_ID) AS Total_Orders,
    SUM(s.Quantity) AS Total_Units_Purchased,
    ROUND(SUM(s.Sales_Amount), 2) AS Total_Revenue,
    ROUND(AVG(s.Sales_Amount), 2) AS Avg_Transaction_Value
FROM Sales_Orders s
JOIN Customers c ON s.Customer_ID = c.Customer_ID
GROUP BY c.Customer_Segment
ORDER BY Total_Revenue DESC;

-- 13. Payment Method Distribution & Transaction Counts
SELECT 
    Payment_Method,
    COUNT(DISTINCT Order_ID) AS Transaction_Count,
    ROUND(SUM(Sales_Amount), 2) AS Total_Revenue,
    ROUND((COUNT(DISTINCT Order_ID) * 100.0 / (SELECT COUNT(*) FROM Sales_Orders)), 2) AS Transaction_Share_Pct
FROM Sales_Orders
GROUP BY Payment_Method
ORDER BY Transaction_Count DESC;


-- =============================================================================
-- SECTION 2: INVENTORY ANALYTICS (Queries 14 - 22)
-- =============================================================================

-- 14. Current Total Inventory Stock on Hand, Reserved, and Available Stock
SELECT 
    SUM(Stock_On_Hand) AS Total_Stock_On_Hand,
    SUM(Reserved_Stock) AS Total_Reserved_Stock,
    SUM(Available_Stock) AS Total_Available_Stock
FROM Inventory
WHERE Inventory_Date = (SELECT MAX(Inventory_Date) FROM Inventory);

-- 15. Total Current Inventory Value (Stock On Hand * Unit Cost)
SELECT 
    ROUND(SUM(i.Stock_On_Hand * p.Unit_Cost), 2) AS Total_Inventory_Value
FROM Inventory i
JOIN Products p ON i.Product_ID = p.Product_ID
WHERE i.Inventory_Date = (SELECT MAX(Inventory_Date) FROM Inventory);

-- 16. Low-Stock Products Identification (Stock On Hand < Reorder Level)
SELECT 
    st.Store_Name,
    p.Product_ID,
    p.Product_Name,
    p.Department,
    i.Stock_On_Hand,
    p.Reorder_Level,
    p.Safety_Stock,
    (p.Reorder_Level - i.Stock_On_Hand) AS Replenishment_Shortfall
FROM Inventory i
JOIN Products p ON i.Product_ID = p.Product_ID
JOIN Stores st ON i.Store_ID = st.Store_ID
WHERE i.Inventory_Date = (SELECT MAX(Inventory_Date) FROM Inventory)
  AND i.Stock_On_Hand < p.Reorder_Level
ORDER BY Replenishment_Shortfall DESC;

-- 17. Out-of-Stock (Stockout) Products Identification
SELECT 
    st.Store_Name,
    p.Product_ID,
    p.Product_Name,
    p.Department,
    i.Stock_On_Hand,
    p.Safety_Stock,
    p.Reorder_Level
FROM Inventory i
JOIN Products p ON i.Product_ID = p.Product_ID
JOIN Stores st ON i.Store_ID = st.Store_ID
WHERE i.Inventory_Date = (SELECT MAX(Inventory_Date) FROM Inventory)
  AND i.Stock_On_Hand = 0
ORDER BY st.Store_Name, p.Department;

-- 18. Overstocked Products Identification (Stock On Hand > 3 * Reorder Level)
SELECT 
    st.Store_Name,
    p.Product_ID,
    p.Product_Name,
    p.Department,
    i.Stock_On_Hand,
    p.Reorder_Level,
    ROUND(i.Stock_On_Hand * p.Unit_Cost, 2) AS Excess_Inventory_Value
FROM Inventory i
JOIN Products p ON i.Product_ID = p.Product_ID
JOIN Stores st ON i.Store_ID = st.Store_ID
WHERE i.Inventory_Date = (SELECT MAX(Inventory_Date) FROM Inventory)
  AND i.Stock_On_Hand > (3 * p.Reorder_Level)
ORDER BY Excess_Inventory_Value DESC;

-- 19. Inventory Stock & Value Breakdown by Store Location
SELECT 
    st.Store_ID,
    st.Store_Name,
    SUM(i.Stock_On_Hand) AS Total_Stock_Units,
    SUM(i.Available_Stock) AS Available_Units,
    ROUND(SUM(i.Stock_On_Hand * p.Unit_Cost), 2) AS Store_Inventory_Value
FROM Inventory i
JOIN Products p ON i.Product_ID = p.Product_ID
JOIN Stores st ON i.Store_ID = st.Store_ID
WHERE i.Inventory_Date = (SELECT MAX(Inventory_Date) FROM Inventory)
GROUP BY st.Store_ID, st.Store_Name
ORDER BY Store_Inventory_Value DESC;

-- 20. Inventory Stock & Value Breakdown by Product Department
SELECT 
    p.Department,
    SUM(i.Stock_On_Hand) AS Total_Stock_Units,
    ROUND(SUM(i.Stock_On_Hand * p.Unit_Cost), 2) AS Department_Inventory_Value
FROM Inventory i
JOIN Products p ON i.Product_ID = p.Product_ID
WHERE i.Inventory_Date = (SELECT MAX(Inventory_Date) FROM Inventory)
GROUP BY p.Department
ORDER BY Department_Inventory_Value DESC;

-- 21. Products Currently Below Reorder Level across Stores
SELECT 
    p.Product_ID,
    p.Product_Name,
    COUNT(DISTINCT i.Store_ID) AS Stores_Low_In_Stock,
    SUM(i.Stock_On_Hand) AS Total_Available_Stock_Across_Stores
FROM Inventory i
JOIN Products p ON i.Product_ID = p.Product_ID
WHERE i.Inventory_Date = (SELECT MAX(Inventory_Date) FROM Inventory)
  AND i.Stock_On_Hand < p.Reorder_Level
GROUP BY p.Product_ID, p.Product_Name
ORDER BY Stores_Low_In_Stock DESC;

-- 22. Products Currently Below Safety Stock Level (Critical Stockout Risk)
SELECT 
    st.Store_Name,
    p.Product_ID,
    p.Product_Name,
    i.Stock_On_Hand,
    p.Safety_Stock,
    (p.Safety_Stock - i.Stock_On_Hand) AS Critical_Deficit
FROM Inventory i
JOIN Products p ON i.Product_ID = p.Product_ID
JOIN Stores st ON i.Store_ID = st.Store_ID
WHERE i.Inventory_Date = (SELECT MAX(Inventory_Date) FROM Inventory)
  AND i.Stock_On_Hand < p.Safety_Stock
ORDER BY Critical_Deficit DESC;


-- =============================================================================
-- SECTION 3: SUPPLIER ANALYTICS (Queries 23 - 27)
-- =============================================================================

-- 23. Overall Supplier Performance Ranking & Fulfillment Summary
SELECT 
    sup.Supplier_ID,
    sup.Supplier_Name,
    sup.Supplier_Rating,
    COUNT(p.PO_ID) AS Total_POs,
    SUM(p.Quantity_Ordered) AS Total_Units_Ordered,
    ROUND(SUM(p.Purchase_Cost), 2) AS Total_Purchase_Value,
    ROUND(AVG(p.Lead_Time_Days), 2) AS Actual_Avg_Lead_Time,
    ROUND(AVG(p.Delay_Days), 2) AS Avg_Delay_Days,
    ROUND((SUM(CASE WHEN p.On_Time = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(p.PO_ID)), 2) AS On_Time_Delivery_Pct
FROM Suppliers sup
JOIN Purchases p ON sup.Supplier_ID = p.Supplier_ID
GROUP BY sup.Supplier_ID, sup.Supplier_Name, sup.Supplier_Rating
ORDER BY On_Time_Delivery_Pct DESC, Total_Purchase_Value DESC;

-- 24. Average Lead Time in Days by Supplier vs. Standard Lead Time
SELECT 
    sup.Supplier_ID,
    sup.Supplier_Name,
    sup.Standard_Lead_Time_Days,
    ROUND(AVG(p.Lead_Time_Days), 2) AS Actual_Avg_Lead_Time,
    ROUND(AVG(p.Lead_Time_Days) - sup.Standard_Lead_Time_Days, 2) AS Lead_Time_Variance
FROM Suppliers sup
JOIN Purchases p ON sup.Supplier_ID = p.Supplier_ID
GROUP BY sup.Supplier_ID, sup.Supplier_Name, sup.Standard_Lead_Time_Days
ORDER BY Lead_Time_Variance DESC;

-- 25. On-Time Delivery Percentage by Supplier
SELECT 
    sup.Supplier_ID,
    sup.Supplier_Name,
    COUNT(p.PO_ID) AS Total_POs,
    SUM(CASE WHEN p.On_Time = 'Yes' THEN 1 ELSE 0 END) AS On_Time_POs,
    SUM(CASE WHEN p.On_Time = 'No' THEN 1 ELSE 0 END) AS Delayed_POs,
    ROUND((SUM(CASE WHEN p.On_Time = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(p.PO_ID)), 2) AS On_Time_Pct
FROM Suppliers sup
JOIN Purchases p ON sup.Supplier_ID = p.Supplier_ID
GROUP BY sup.Supplier_ID, sup.Supplier_Name
ORDER BY On_Time_Pct ASC;

-- 26. Suppliers with Most Purchase Order Delays (Delay Days > 0)
SELECT 
    sup.Supplier_ID,
    sup.Supplier_Name,
    COUNT(p.PO_ID) AS Delayed_POs,
    SUM(p.Delay_Days) AS Total_Delayed_Days,
    MAX(p.Delay_Days) AS Max_Single_Delay_Days,
    ROUND(AVG(p.Delay_Days), 2) AS Avg_Delay_Days
FROM Suppliers sup
JOIN Purchases p ON sup.Supplier_ID = p.Supplier_ID
WHERE p.Delay_Days > 0
GROUP BY sup.Supplier_ID, sup.Supplier_Name
ORDER BY Delayed_POs DESC, Total_Delayed_Days DESC;

-- 27. Total Purchase Order Volume & Purchase Cost per Supplier
SELECT 
    sup.Supplier_ID,
    sup.Supplier_Name,
    COUNT(p.PO_ID) AS PO_Count,
    SUM(p.Quantity_Ordered) AS Total_Quantity_Purchased,
    ROUND(SUM(p.Purchase_Cost), 2) AS Total_Spend
FROM Suppliers sup
JOIN Purchases p ON sup.Supplier_ID = p.Supplier_ID
GROUP BY sup.Supplier_ID, sup.Supplier_Name
ORDER BY Total_Spend DESC;


-- =============================================================================
-- SECTION 4: RETURNS ANALYTICS (Queries 28 - 32)
-- =============================================================================

-- 28. Overall Return Rate % and Total Refunded Amount
SELECT 
    COUNT(r.Return_ID) AS Total_Return_Events,
    SUM(r.Quantity_Returned) AS Total_Units_Returned,
    ROUND(SUM(r.Refund_Amount), 2) AS Total_Refund_Amount,
    (SELECT SUM(Quantity) FROM Sales_Orders) AS Total_Units_Sold,
    ROUND((SUM(r.Quantity_Returned) * 100.0 / (SELECT SUM(Quantity) FROM Sales_Orders)), 2) AS Return_Rate_Pct
FROM Returns r;

-- 29. Return Quantity & Refund Amount by Product
SELECT 
    p.Product_ID,
    p.Product_Name,
    p.Department,
    SUM(r.Quantity_Returned) AS Units_Returned,
    ROUND(SUM(r.Refund_Amount), 2) AS Total_Refund_Amount,
    COUNT(r.Return_ID) AS Return_Occurrences
FROM Returns r
JOIN Products p ON r.Product_ID = p.Product_ID
GROUP BY p.Product_ID, p.Product_Name, p.Department
ORDER BY Total_Refund_Amount DESC
LIMIT 15;

-- 30. Return Rate & Refund Breakdown by Store
SELECT 
    st.Store_ID,
    st.Store_Name,
    COUNT(r.Return_ID) AS Total_Returns,
    SUM(r.Quantity_Returned) AS Units_Returned,
    ROUND(SUM(r.Refund_Amount), 2) AS Total_Refund_Amount
FROM Returns r
JOIN Stores st ON r.Store_ID = st.Store_ID
GROUP BY st.Store_ID, st.Store_Name
ORDER BY Total_Refund_Amount DESC;

-- 31. Return Reason Distribution (Count & Refund Amount by Reason)
SELECT 
    Return_Reason,
    COUNT(Return_ID) AS Return_Count,
    SUM(Quantity_Returned) AS Units_Returned,
    ROUND(SUM(Refund_Amount), 2) AS Total_Refund_Amount,
    ROUND((COUNT(Return_ID) * 100.0 / (SELECT COUNT(*) FROM Returns)), 2) AS Reason_Share_Pct
FROM Returns
GROUP BY Return_Reason
ORDER BY Return_Count DESC;

-- 32. Highest Return Rate Categories & Departments
SELECT 
    p.Department,
    SUM(r.Quantity_Returned) AS Units_Returned,
    ROUND(SUM(r.Refund_Amount), 2) AS Department_Refund_Amount
FROM Returns r
JOIN Products p ON r.Product_ID = p.Product_ID
GROUP BY p.Department
ORDER BY Department_Refund_Amount DESC;


-- =============================================================================
-- SECTION 5: ADVANCED ANALYTICS (Queries 33 - 40)
-- =============================================================================

-- 33. Inventory Turnover Ratio by Department (COGS / Avg Inventory Value)
WITH Dept_COGS AS (
    SELECT 
        p.Department,
        SUM(s.COGS) AS Total_COGS
    FROM Sales_Orders s
    JOIN Products p ON s.Product_ID = p.Product_ID
    GROUP BY p.Department
),
Dept_Avg_Inv AS (
    SELECT 
        p.Department,
        AVG(i.Stock_On_Hand * p.Unit_Cost) AS Avg_Inventory_Value
    FROM Inventory i
    JOIN Products p ON i.Product_ID = p.Product_ID
    GROUP BY p.Department
)
SELECT 
    c.Department,
    ROUND(c.Total_COGS, 2) AS Annualized_COGS,
    ROUND(a.Avg_Inventory_Value, 2) AS Avg_Inventory_Value,
    ROUND(c.Total_COGS / NULLIF(a.Avg_Inventory_Value, 0), 2) AS Inventory_Turnover_Ratio
FROM Dept_COGS c
JOIN Dept_Avg_Inv a ON c.Department = a.Department
ORDER BY Inventory_Turnover_Ratio DESC;

-- 34. Gross Margin % by Product Category & Subcategory
SELECT 
    p.Department,
    p.Subcategory,
    ROUND(SUM(s.Sales_Amount), 2) AS Total_Revenue,
    ROUND(SUM(s.COGS), 2) AS Total_COGS,
    ROUND(SUM(s.Gross_Profit), 2) AS Gross_Profit,
    ROUND((SUM(s.Gross_Profit) / NULLIF(SUM(s.Sales_Amount), 0)) * 100, 2) AS Gross_Margin_Pct
FROM Sales_Orders s
JOIN Products p ON s.Product_ID = p.Product_ID
GROUP BY p.Department, p.Subcategory
ORDER BY Gross_Margin_Pct DESC;

-- 35. Month-over-Month (MoM) Sales Revenue & Profit Growth %
WITH Monthly_Sales AS (
    SELECT 
        TO_CHAR(Order_Date, 'YYYY-MM') AS Sales_Month,
        SUM(Sales_Amount) AS Monthly_Revenue,
        SUM(Gross_Profit) AS Monthly_Profit
    FROM Sales_Orders
    GROUP BY TO_CHAR(Order_Date, 'YYYY-MM')
)
SELECT 
    Sales_Month,
    ROUND(Monthly_Revenue, 2) AS Monthly_Revenue,
    ROUND(LAG(Monthly_Revenue) OVER (ORDER BY Sales_Month), 2) AS Prior_Month_Revenue,
    ROUND(((Monthly_Revenue - LAG(Monthly_Revenue) OVER (ORDER BY Sales_Month)) / 
           NULLIF(LAG(Monthly_Revenue) OVER (ORDER BY Sales_Month), 0)) * 100, 2) AS Revenue_MoM_Growth_Pct,
    ROUND(Monthly_Profit, 2) AS Monthly_Profit,
    ROUND(((Monthly_Profit - LAG(Monthly_Profit) OVER (ORDER BY Sales_Month)) / 
           NULLIF(LAG(Monthly_Profit) OVER (ORDER BY Sales_Month), 0)) * 100, 2) AS Profit_MoM_Growth_Pct
FROM Monthly_Sales
ORDER BY Sales_Month;

-- 36. Product Revenue Contribution % to Total Company Sales (Pareto Analysis)
WITH Product_Revenue AS (
    SELECT 
        p.Product_ID,
        p.Product_Name,
        p.Department,
        SUM(s.Sales_Amount) AS Revenue
    FROM Sales_Orders s
    JOIN Products p ON s.Product_ID = p.Product_ID
    GROUP BY p.Product_ID, p.Product_Name, p.Department
),
Total_Company_Revenue AS (
    SELECT SUM(Sales_Amount) AS Grand_Total_Revenue FROM Sales_Orders
)
SELECT 
    pr.Product_ID,
    pr.Product_Name,
    pr.Department,
    ROUND(pr.Revenue, 2) AS Revenue,
    ROUND((pr.Revenue * 100.0 / tr.Grand_Total_Revenue), 2) AS Revenue_Contribution_Pct,
    ROUND(SUM(pr.Revenue) OVER (ORDER BY pr.Revenue DESC) * 100.0 / tr.Grand_Total_Revenue, 2) AS Cumulative_Revenue_Pct
FROM Product_Revenue pr
CROSS JOIN Total_Company_Revenue tr
ORDER BY pr.Revenue DESC;

-- 37. Store Contribution % to Total Company Sales
WITH Store_Revenue AS (
    SELECT 
        st.Store_ID,
        st.Store_Name,
        st.City,
        SUM(s.Sales_Amount) AS Revenue
    FROM Sales_Orders s
    JOIN Stores st ON s.Store_ID = st.Store_ID
    GROUP BY st.Store_ID, st.Store_Name, st.City
),
Total_Company_Revenue AS (
    SELECT SUM(Sales_Amount) AS Grand_Total_Revenue FROM Sales_Orders
)
SELECT 
    sr.Store_ID,
    sr.Store_Name,
    sr.City,
    ROUND(sr.Revenue, 2) AS Store_Revenue,
    ROUND((sr.Revenue * 100.0 / tr.Grand_Total_Revenue), 2) AS Store_Contribution_Pct
FROM Store_Revenue sr
CROSS JOIN Total_Company_Revenue tr
ORDER BY sr.Revenue DESC;

-- 38. Supplier Performance Scorecard & Risk Assessment
SELECT 
    sup.Supplier_ID,
    sup.Supplier_Name,
    sup.Supplier_Rating,
    COUNT(p.PO_ID) AS Total_Orders,
    ROUND(AVG(p.Delay_Days), 2) AS Avg_Delay_Days,
    ROUND((SUM(CASE WHEN p.On_Time = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(p.PO_ID)), 2) AS On_Time_Pct,
    CASE 
        WHEN (SUM(CASE WHEN p.On_Time = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(p.PO_ID)) >= 90 THEN 'Low Risk - Preferred'
        WHEN (SUM(CASE WHEN p.On_Time = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(p.PO_ID)) >= 75 THEN 'Medium Risk - Monitor'
        ELSE 'High Risk - Action Required'
    END AS Supplier_Status
FROM Suppliers sup
JOIN Purchases p ON sup.Supplier_ID = p.Supplier_ID
GROUP BY sup.Supplier_ID, sup.Supplier_Name, sup.Supplier_Rating
ORDER BY On_Time_Pct ASC;

-- 39. ABC Product Classification based on Cumulative Revenue Contribution
WITH Product_Rev AS (
    SELECT 
        p.Product_ID,
        p.Product_Name,
        p.Department,
        SUM(s.Sales_Amount) AS Revenue
    FROM Sales_Orders s
    JOIN Products p ON s.Product_ID = p.Product_ID
    GROUP BY p.Product_ID, p.Product_Name, p.Department
),
Cumulative_Rev AS (
    SELECT 
        Product_ID,
        Product_Name,
        Department,
        Revenue,
        SUM(Revenue) OVER (ORDER BY Revenue DESC) * 100.0 / (SELECT SUM(Sales_Amount) FROM Sales_Orders) AS Cum_Pct
    FROM Product_Rev
)
SELECT 
    Product_ID,
    Product_Name,
    Department,
    ROUND(Revenue, 2) AS Revenue,
    ROUND(Cum_Pct, 2) AS Cumulative_Revenue_Pct,
    CASE 
        WHEN Cum_Pct <= 70.0 THEN 'A (Top 70% Revenue)'
        WHEN Cum_Pct <= 90.0 THEN 'B (Next 20% Revenue)'
        ELSE 'C (Bottom 10% Revenue)'
    END AS ABC_Class
FROM Cumulative_Rev
ORDER BY Revenue DESC;

-- 40. Stockout Impact & Potential Lost Sales Analysis
SELECT 
    st.Store_Name,
    p.Department,
    p.Product_Name,
    COUNT(DISTINCT i.Inventory_Date) AS Stockout_Days_Count,
    p.Selling_Price,
    ROUND(COUNT(DISTINCT i.Inventory_Date) * p.Selling_Price * 5, 2) AS Estimated_Lost_Revenue
FROM Inventory i
JOIN Products p ON i.Product_ID = p.Product_ID
JOIN Stores st ON i.Store_ID = st.Store_ID
WHERE i.Stock_On_Hand = 0
GROUP BY st.Store_Name, p.Department, p.Product_Name, p.Selling_Price
ORDER BY Estimated_Lost_Revenue DESC;

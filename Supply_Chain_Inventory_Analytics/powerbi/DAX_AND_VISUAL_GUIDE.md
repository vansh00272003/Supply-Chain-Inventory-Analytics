# Power BI Desktop DAX & Visual Layout Copy-Paste Guide
## Project: Walmart-Style Supermarket Supply Chain & Inventory Analytics

Use this quick copy-paste guide inside **`excel loaded.pbix`** in Power BI Desktop to add all 28 DAX measures and build your 7 multi-page analytical dashboard pages natively!

---

## 1. Quick Copy-Paste DAX Measures

In Power BI Desktop, right-click any table in the **Fields** pane (e.g., `Sales_Orders`), click **New Measure**, and paste these formulas:

### Sales & Financial DAX Measures
```dax
Total Sales = SUM(Sales_Orders[Sales_Amount])
```
```dax
Total COGS = SUM(Sales_Orders[COGS])
```
```dax
Gross Profit = [Total Sales] - [Total COGS]
```
```dax
Profit Margin % = DIVIDE([Gross Profit], [Total Sales], 0)
```
```dax
Total Orders = DISTINCTCOUNT(Sales_Orders[Order_ID])
```
```dax
Units Sold = SUM(Sales_Orders[Quantity])
```
```dax
Average Order Value = DIVIDE([Total Sales], [Total Orders], 0)
```
```dax
Average Discount % = AVERAGE(Sales_Orders[Discount_Pct])
```

### Inventory DAX Measures
```dax
Inventory Value = SUMX(Inventory, Inventory[Stock_On_Hand] * LOOKUPVALUE(Products[Unit_Cost], Products[Product_ID], Inventory[Product_ID]))
```
```dax
Stockout Count = CALCULATE(COUNTROWS(Inventory), Inventory[Stock_On_Hand] = 0)
```
```dax
Low Stock Count = CALCULATE(COUNTROWS(Inventory), FILTER(Inventory, Inventory[Stock_On_Hand] < LOOKUPVALUE(Products[Reorder_Level], Products[Product_ID], Inventory[Product_ID])))
```
```dax
Critical Stock Count = CALCULATE(COUNTROWS(Inventory), FILTER(Inventory, Inventory[Stock_On_Hand] < LOOKUPVALUE(Products[Safety_Stock], Products[Product_ID], Inventory[Product_ID])))
```
```dax
Overstock Count = CALCULATE(COUNTROWS(Inventory), FILTER(Inventory, Inventory[Stock_On_Hand] > (3 * LOOKUPVALUE(Products[Reorder_Level], Products[Product_ID], Inventory[Product_ID]))))
```

### Supply Chain & Supplier DAX Measures
```dax
Total Purchase Cost = SUM(Purchases[Purchase_Cost])
```
```dax
Total PO Count = DISTINCTCOUNT(Purchases[PO_ID])
```
```dax
Average Lead Time = AVERAGE(Purchases[Lead_Time_Days])
```
```dax
On Time Delivery % = DIVIDE(CALCULATE(COUNTROWS(Purchases), Purchases[On_Time] = "Yes"), COUNTROWS(Purchases), 0)
```
```dax
Delayed PO Count = CALCULATE(COUNTROWS(Purchases), Purchases[On_Time] = "No")
```

### Returns DAX Measures
```dax
Returned Units = SUM(Returns[Quantity_Returned])
```
```dax
Total Refund Amount = SUM(Returns[Refund_Amount])
```
```dax
Return Rate % = DIVIDE([Returned Units], [Units Sold], 0)
```

---

## 2. Recommended 7 Dashboard Pages Layout

In Power BI Desktop, click the **`+` (New Page)** button at the bottom to create 7 pages:

1. **Page 1: Executive Overview**
   * Visual 1: Card -> `Total Sales`
   * Visual 2: Card -> `Gross Profit`
   * Visual 3: Card -> `Profit Margin %`
   * Visual 4: Card -> `Inventory Value`
   * Visual 5: Line Chart -> Axis: `Sales_Orders[Order_Date]`, Values: `Total Sales`, `Gross Profit`
   * Visual 6: Clustered Bar Chart -> Axis: `Products[Department]`, Values: `Total Sales`

2. **Page 2: Sales Analytics**
   * Visual 1: Area Chart -> Axis: `Sales_Orders[Order_Date]`, Values: `Total Sales`
   * Visual 2: Pie Chart -> Legend: `Sales_Orders[Payment_Method]`, Values: `Total Sales`
   * Visual 3: Matrix Grid -> Rows: `Stores[Store_Name]`, Values: `Total Sales`, `Gross Profit`

3. **Page 3: Inventory Analytics**
   * Visual 1: Clustered Column Chart -> Axis: `Stores[Store_Name]`, Values: `Stock_On_Hand`, `Available_Stock`
   * Visual 2: Bar Chart -> Axis: `Products[Department]`, Values: `Inventory Value`

4. **Page 4: Supply Chain Analytics**
   * Visual 1: Bar Chart -> Axis: `Suppliers[Supplier_Name]`, Values: `Total Purchase Cost`
   * Visual 2: Donut Chart -> Legend: `Purchases[On_Time]`, Values: `Total PO Count`

5. **Page 5: Customer Analytics**
   * Visual 1: Bar Chart -> Axis: `Customers[Customer_Segment]`, Values: `Total Sales`
   * Visual 2: Column Chart -> Axis: `Customers[City]`, Values: `Total Sales`

6. **Page 6: Product Performance**
   * Visual 1: Column Chart -> Axis: `Products[Brand]`, Values: `Total Sales`
   * Visual 2: Table -> `Products[Product_Name]`, `Products[Unit_Cost]`, `Products[Selling_Price]`, `Total Sales`

7. **Page 7: Returns Analytics**
   * Visual 1: Pie Chart -> Legend: `Returns[Return_Reason]`, Values: `Total Refund Amount`
   * Visual 2: Bar Chart -> Axis: `Stores[Store_Name]`, Values: `Total Refund Amount`

// =============================================================================
// POWER BI DESKTOP INSTANT DATA LOAD SCRIPT
// Project: Walmart-Style Supermarket Supply Chain & Inventory Analytics
// =============================================================================
//
// HOW TO LOAD ALL 8 TABLES INTO POWER BI DESKTOP IN 30 SECONDS:
//
// 1. Open Microsoft Power BI Desktop on your computer.
// 2. Click "Get Data" -> "Excel workbook".
// 3. Select file: walmart_style_supermarket_supply_chain_dataset.xlsx
//    (located in Supply_Chain_Inventory_Analytics/data/)
// 4. In the Navigator window, check ALL 8 tables:
//    [x] Products
//    [x] Suppliers
//    [x] Stores
//    [x] Customers
//    [x] Inventory
//    [x] Sales_Orders
//    [x] Purchases
//    [x] Returns
// 5. Click "Load".
// 6. Power BI Desktop will automatically detect all primary/foreign key relationships!
// =============================================================================

let
    Source = Excel.Workbook(File.Contents("E:/projects/Supply chain managment/Supply_Chain_Inventory_Analytics/data/walmart_style_supermarket_supply_chain_dataset.xlsx"), null, true)
in
    Source

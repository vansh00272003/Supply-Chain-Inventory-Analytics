# Business Requirements & KPI Specifications
## Walmart-Style Supermarket Supply Chain & Inventory Analytics

---

## 1. Overview & Business Intent

Supermarket and hypermarket management requires continuous visibility into sales velocity, inventory holding risk, supplier fulfillment dependability, customer segment behavior, and return losses. The goal of this analytical platform is to provide executive leadership and operational managers with actionable answers to critical business questions.

---

## 2. Core Business Questions Answered

### Inventory Control & Replenishment
1. **Low Stock Alert**: Which SKUs are currently below their designated Reorder Level across retail outlets?
2. **Stockout Incident Tracking**: Which store locations and departments are experiencing zero stock on hand, leading to lost sales?
3. **Overstock Exposure**: Which SKUs are carrying stock levels exceeding 3 times their reorder threshold, tying up working capital?
4. **Inventory Valuation**: What is the current monetary value of stock held in each store and distribution center?
5. **Replenishment Priorities**: Which high-velocity products need immediate purchase order generation to prevent stockout?
6. **Safety Stock Buffer**: How many SKUs have breached their safety stock threshold, creating a critical stockout risk?
7. **Inventory Turnover**: What is the inventory turnover ratio across departments, indicating fast-moving vs. slow-moving categories?

### Sales & Profitability
8. **Revenue Trends**: What are the daily, weekly, and monthly sales revenue trends across retail locations?
9. **Department & Product Ranking**: Which departments, subcategories, and individual SKUs generate the highest revenue and gross profit?
10. **Profit Margin Analysis**: What is the gross profit margin percentage across different product categories?
11. **Average Order Value (AOV)**: What is the average expenditure per transaction, and how does it vary by store and customer segment?
12. **Sales Velocity & Elasticity**: Which products are exhibiting declining sales trends or low price elasticity?

### Supply Chain & Supplier Performance
13. **Supplier Lead Time Variance**: What is the actual lead time for each vendor compared to their contractual standard lead time?
14. **On-Time Delivery %**: What percentage of purchase orders are delivered on or before the expected delivery date for each supplier?
15. **Delayed Purchase Orders**: How many purchase orders were delayed, and what was the average delay duration in days?
16. **Vendor Risk Classification**: Which suppliers pose operational risks due to repeated delivery delays and poor quality?

### Customer Behavior
17. **Segment Contribution**: Which customer segments (Regular, Premium, Occasional) generate the highest lifetime revenue?
18. **Geographic Distribution**: Which cities and metro areas drive the highest retail demand?
19. **Payment Tender Preferences**: What is the distribution of payment methods (UPI, Credit Card, Cash, Gift Card) across customer age groups?

### Returns & Quality Control
20. **Return Rate %**: What percentage of sold units are returned by customers overall and per department?
21. **Root Cause Analysis**: What are the primary reasons for product returns (Damaged, Quality Issue, Customer Changed Mind, Expired)?
22. **Financial Refund Impact**: What is the total monetary refund issued to customers due to product returns?

---

## 3. Key Performance Indicator (KPI) Definitions

| Metric Name | Formula / Logic | Target Threshold / Benchmark | Business Impact |
| :--- | :--- | :--- | :--- |
| **Total Sales Revenue** | `SUM(Sales_Amount)` | Growth > 10% MoM | Top-line revenue health |
| **Gross Profit Margin %** | `(Total Sales - Total COGS) / Total Sales` | Target >= 22% overall | Bottom-line profitability |
| **Average Order Value (AOV)** | `Total Sales / Total Orders` | Target >= ₹450 | Basket size optimization |
| **Inventory Turnover Ratio**| `Annualized COGS / Avg Inventory Value` | Target >= 6.0x | Working capital efficiency |
| **Stockout Rate %** | `(Stockout Items / Total Items) * 100` | Target < 2.0% | Customer satisfaction & sales recovery |
| **On-Time Delivery %** | `(On-Time POs / Total POs) * 100` | Target >= 85.0% | Supply chain reliability |
| **Average Delay Days** | `AVG(Received Date - Expected Date)` | Target < 1.0 Day | Buffer planning & safety stock |
| **Return Rate %** | `(Returned Units / Sold Units) * 100` | Target < 3.0% | Quality assurance & vendor accountability |

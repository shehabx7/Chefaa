# Chefaa
In this project I scraped products data using python scrapy from medications module on Chefaa.com.

- Dashboard Link:
<br>-- Here is the link to the dashboard where you can apply filters and explore the data further.
<br>https://lnkd.in/d2GzrqVf

# Analysis
- Data Overview:<br>
-- Total items scraped: 2539<br>
-- My focus is on exploring the items, so here’s what I’ve noticed.<br>

- Categorization:<br>-
-- The categorization isn’t very accurate. 94% of the items fall into the main categories: Health condition (1320 items) Medications (1070 items)<br>
-- There are 7 available categories in total.<br>

- Brands:<br>-
-- Filtering items by brands is available.<br>
-- 120 brands contain 31% (803) of the items, while the rest are unbranded.<br>

- Prices:<br>-
-- Most items are priced under 447 EGP (97% or 2467 items).<br>
-- The average price is 75 EGP.<br>
-- Some outliers skew the overall average to 106 EGP, which isn’t accurate.<br>

- Features:<br>
--Prescription Requirement: Chefaa.com indicates whether a medication requires a prescription.<br>
-- Low Stock Flag: A helpful feature flags medications with low stock (currently 1.9%).<br>

- Process Details:<br>
-- I scraped the data using Python Scrapy.<br>
-- Cleaned and loaded it into a SQL server database (clean and denormalized).<br>
-- Created the dashboard in Power BI.<br>
-- While the process is not fully automated, it could be automated with a few adjustments.<br>



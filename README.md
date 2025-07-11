# Marketing-Insights-For-E-Commerce-Company1
📌 Project Overview
This project focuses on extracting actionable marketing and sales insights for a leading e-commerce company using real transactional and customer data. The objective is to perform in-depth analytics, customer segmentation, predictive modeling, and dashboarding to support strategic decision-making.

🎯 Business Objectives
Calculate Revenue at Transaction Level

Invoice Value = ((Quantity * Avg_Price) * (1 - Discount_pct) * (1 + GST)) + Delivery_Charges

Perform Exploratory Data Analysis (EDA):

Customer acquisition and retention trends (month-wise)

Revenue trends: new vs existing customers

Role of discounts in driving revenue

Monthly trends by category, location, day-of-week

Monthly KPIs: Revenue, Orders, Tax, Delivery %, Marketing Spend

Customer Segmentation

Heuristic (RFM-based) Segmentation: Premium, Gold, Silver, Standard

Scientific Segmentation: K-Means Clustering and Profile Analysis

Predictive Modeling

Customer Lifetime Value (CLTV) Classification: Low, Medium, High

Next Purchase Day Prediction: 0–30, 30–60, 60–90, 90+ days using classifier models

Market Basket Analysis

Association rule mining to identify frequently co-purchased products

Cohort Analysis

Identify monthly customer cohorts and measure long-term retention behavior

🗂️ Dataset Description
File Name	Description
Online_Sales.csv	Point-of-sales transactions (SKU, quantity, date, price, etc.)
Customers.csv	Customer demographics (ID, gender, location, tenure)
Discount_Coupon.csv	Monthly coupon % per product category
Marketing_Spend.csv	Day-wise spend on online & offline marketing
GSTDetail.csv	GST % applicable per product category
Tax_amount.xlsx	Raw GST sheet (renamed)
CustomersData.xlsx	Raw customer file
Online_Sales.xlsx	Raw sales file
Streamlit Analytical Dashboard2.py	Streamlit app for KPI dashboard
Marketing Insights For E-Commerce Company1.ipynb	Main analysis notebook
requirements.txt	Dependencies to run notebook & Streamlit app

⚙️ Tech Stack
Languages: Python, SQL

Libraries: pandas, numpy, matplotlib, seaborn, plotly, sklearn, mlxtend

Modeling: Logistic Regression, Random Forest, KMeans

Dashboard: Streamlit

EDA & Profiling: seaborn, pandas-profiling

Market Basket Analysis: Apriori (mlxtend)

📌 Key Performance Indicators (KPIs)
Revenue, Orders, AOV

Profit Margin, Discount Impact

Repeat Rate, Churn Rate, Purchase Frequency

Customer Lifetime Value (CLTV)

Marketing Spend % of Revenue

Segment Profiles (Premium to Standard)

🖥️ How to Run the Project
Step 1: Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Step 2: Run the Jupyter Notebook
Open Marketing Insights For E-Commerce Company1.ipynb in Jupyter or VSCode.

Step 3: Launch Streamlit Dashboard
bash
Copy
Edit
streamlit run "Streamlit Analytical Dashboard2.py"
📈 Visual Outputs
Customer Retention Heatmaps

Monthly Revenue Trends

KPI Cards: Orders, CLTV, Spend

Segment-wise Strategy

Association Rules Table

Cohort Behavior Graphs

📦 Future Improvements
Add time-series forecasting for revenue

Integrate LTV modeling using XGBoost/CatBoost

Real-time dashboard integration with DBs

Geo-visualization for location-based KPIs

📄 License
MIT License — free to use and adapt with attribution.


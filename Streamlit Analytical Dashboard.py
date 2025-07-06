import streamlit as st
import pandas as pd
import plotly.express as px
import datetime as dt
import plotly.graph_objects as go

# --- Data Loading and Preprocessing ---
# This section loads the necessary CSV files and performs the initial data cleaning
# and calculations (like Sales_amt, Invoice_amt) to prepare the data for the dashboard.
# This ensures the dashboard is self-contained and runnable.

try:
   cust_data = pd.read_excel(r"C:\Users\DELL\OneDrive\Desktop\rahul\14. Capstone Case Study - Finding-Marketing-Insights\CustomersData.xlsx")
    discount_coupon = pd.read_excel(r"C:\Users\DELL\OneDrive\Desktop\rahul\14. Capstone Case Study - Finding-Marketing-Insights\Discount_Coupon.xlsx")
    marketing_spend = pd.read_excel(r"C:\Users\DELL\OneDrive\Desktop\rahul\14. Capstone Case Study - Finding-Marketing-Insights\Marketing_Spend.xlsx")
    online_sales = pd.read_excel(r"C:\Users\DELL\OneDrive\Desktop\rahul\14. Capstone Case Study - Finding-Marketing-Insights\Online_Sales.xlsx")
    tax_amt = pd.read_excel(r"C:\Users\DELL\OneDrive\Desktop\rahul\14. Capstone Case Study - Finding-Marketing-Insights\Tax_amount.xlsx")

    # Clean column names by removing leading/trailing spaces
    discount_coupon.columns = discount_coupon.columns.str.strip()
    marketing_spend.columns = marketing_spend.columns.str.strip()
    online_sales.columns = online_sales.columns.str.strip()
    tax_amt.columns = tax_amt.columns.str.strip()
    cust_data.columns = cust_data.columns.str.strip()

    # Convert 'Transaction_Date' in online_sales to datetime objects
    online_sales['Transaction_Date'] = pd.to_datetime(online_sales['Transaction_Date'], format='%Y%m%d')
    online_sales['Month'] = online_sales['Transaction_Date'].dt.strftime('%b')
    online_sales['Year_month'] = online_sales['Transaction_Date'].dt.strftime('%Y-%m')
    online_sales['Day_of_Week'] = online_sales['Transaction_Date'].dt.day_name()
    online_sales['Day'] = online_sales['Transaction_Date'].dt.day

    # Convert 'Date' in marketing_spend to datetime objects
    marketing_spend['Date'] = pd.to_datetime(marketing_spend['Date'], format='%m/%d/%Y')
    marketing_spend['Year_month'] = marketing_spend['Date'].dt.strftime('%Y-%m')
    marketing_spend['Total_spend'] = marketing_spend['Offline_Spend'] + marketing_spend['Online_Spend']

    # Merge DataFrames
    online_sales_merged = pd.merge(online_sales, tax_amt, how='left', on='Product_Category')
    online_sales_merged = pd.merge(online_sales_merged, cust_data, how='left', on='CustomerID')

    # Create a common key for merging discount_coupon
    online_sales_merged['Month_Product_Key'] = online_sales_merged['Month'] + '_' + online_sales_merged['Product_Category']
    discount_coupon['Month_Product_Key'] = discount_coupon['Month'] + '_' + discount_coupon['Product_Category']

    # Perform a left merge to bring in Discount_pct from discount_coupon.
    # The column from 'discount_coupon' will be directly named 'Discount_pct'.
    online_sales_merged = pd.merge(online_sales_merged, discount_coupon[['Month_Product_Key', 'Discount_pct']],
                                   how='left', on='Month_Product_Key')

    # Now, handle the final Discount_pct based on Coupon_Status and fill NaNs.
    # If Coupon_Status is 'Not Used', the discount should be 0.
    online_sales_merged.loc[online_sales_merged['Coupon_Status'] == 'Not Used', 'Discount_pct'] = 0

    # Fill any remaining NaNs in Discount_pct with 0.
    online_sales_merged['Discount_pct'].fillna(0, inplace=True)

    # Drop the temporary merge key
    online_sales_merged.drop(columns=['Month_Product_Key'], errors='ignore', inplace=True)


    final_data = online_sales_merged.copy()

    # Calculate Sales_amt and Invoice_amt
    final_data['Sales_amt'] = (final_data['Quantity'] * final_data['Avg_Price']) * (1 - final_data['Discount_pct'] / 100)
    final_data['Invoice_amt'] = (
        (final_data['Quantity'] * final_data['Avg_Price']) *
        (1 - final_data['Discount_pct'] / 100) *
        (1 + final_data['GST'])
    ) + final_data['Delivery_Charges']

except FileNotFoundError:
    st.error("One or more CSV files not found. Please ensure 'Online_Sales.csv', 'Tax_amount.xlsx - GSTDetails.csv', 'Discount_Coupon.csv', 'Marketing_Spend.csv', and 'CustomersData.xlsx - Customers.csv' are in the same directory.")
    st.stop() # Stop the app if files are missing

# --- Dashboard Layout ---
st.set_page_config(layout="wide", page_title="E-commerce Marketing Insights Dashboard", icon="📈")

st.title("📈 E-commerce Marketing Insights Dashboard")
st.markdown("""
    Welcome to the E-commerce Marketing Insights Dashboard! This interactive tool provides a comprehensive overview of key business metrics, sales trends, and customer behavior. Use the filters on the sidebar to explore data by date range, product category, and location.
""")

# --- Filters (Sidebar) ---
st.sidebar.header("Filter Options")

# Date Range Filter
min_date = final_data['Transaction_Date'].min().date()
max_date = final_data['Transaction_Date'].max().date()
selected_dates = st.sidebar.date_input("Select Date Range", [min_date, max_date])

if len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered_data = final_data[(final_data['Transaction_Date'].dt.date >= start_date) &
                               (final_data['Transaction_Date'].dt.date <= end_date)]
else:
    filtered_data = final_data.copy()

# Product Category Filter
all_categories = ['All'] + sorted(filtered_data['Product_Category'].unique().tolist())
selected_category = st.sidebar.selectbox("Select Product Category", all_categories)

if selected_category != 'All':
    filtered_data = filtered_data[filtered_data['Product_Category'] == selected_category]

# Location Filter
all_locations = ['All'] + sorted(filtered_data['Location'].unique().tolist())
selected_location = st.sidebar.selectbox("Select Location", all_locations)

if selected_location != 'All':
    filtered_data = filtered_data[filtered_data['Location'] == selected_location]

st.sidebar.markdown("---")
st.sidebar.info("Adjust filters to dynamically update the dashboard metrics and visualizations.")


# --- KPI Cards ---
st.header("Key Performance Indicators (KPIs)")

col1, col2, col3, col4, col5 = st.columns(5)

total_revenue = filtered_data['Sales_amt'].sum()
total_orders = filtered_data['Transaction_ID'].nunique()
total_customers = filtered_data['CustomerID'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
total_quantity_sold = filtered_data['Quantity'].sum()

with col1:
    st.metric(label="Total Revenue", value=f"₹{total_revenue:,.2f}")
with col2:
    st.metric(label="Total Orders", value=f"{total_orders:,}")
with col3:
    st.metric(label="Total Customers", value=f"{total_customers:,}")
with col4:
    st.metric(label="Average Order Value", value=f"₹{avg_order_value:,.2f}")
with col5:
    st.metric(label="Total Quantity Sold", value=f"{total_quantity_sold:,}")

st.markdown("---")

# --- Visualizations ---
st.header("Detailed Business Metrics")

# Row 1: Monthly Revenue Trend & Customer Acquisition
col_r1_c1, col_r1_c2 = st.columns(2)

with col_r1_c1:
    st.subheader("Monthly Revenue Trend")
    monthly_revenue = filtered_data.groupby('Year_month')['Sales_amt'].sum().reset_index()
    fig_monthly_revenue = px.line(monthly_revenue, x='Year_month', y='Sales_amt',
                                  title='Monthly Total Revenue', markers=True,
                                  labels={'Sales_amt': 'Total Revenue', 'Year_month': 'Month'},
                                  color_discrete_sequence=px.colors.qualitative.Plotly)
    fig_monthly_revenue.update_xaxes(tickangle=45)
    st.plotly_chart(fig_monthly_revenue, use_container_width=True)

with col_r1_c2:
    st.subheader("New Customers Acquired Monthly")
    # Get the first transaction date for each customer
    first_purchase = filtered_data.groupby('CustomerID')['Transaction_Date'].min().reset_index()
    first_purchase['Acquisition_Month'] = first_purchase['Transaction_Date'].dt.strftime('%Y-%m')
    monthly_acquisition = first_purchase.groupby('Acquisition_Month').size().reset_index(name='New_Customers')
    fig_acquisition = px.bar(monthly_acquisition, x='Acquisition_Month', y='New_Customers',
                             title='New Customers Acquired Every Month',
                             labels={'New_Customers': 'Number of New Customers', 'Acquisition_Month': 'Month'},
                             color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_acquisition.update_xaxes(tickangle=45)
    st.plotly_chart(fig_acquisition, use_container_width=True)

# Row 2: Sales by Product Category & Sales by Day of Week
col_r2_c1, col_r2_c2 = st.columns(2)

with col_r2_c1:
    st.subheader("Sales by Product Category")
    sales_by_category = filtered_data.groupby('Product_Category')['Sales_amt'].sum().reset_index().sort_values(by='Sales_amt', ascending=False)
    fig_category_sales = px.bar(sales_by_category.head(10), x='Sales_amt', y='Product_Category',
                                orientation='h', title='Top 10 Product Categories by Revenue',
                                labels={'Sales_amt': 'Total Revenue', 'Product_Category': 'Product Category'},
                                color_discrete_sequence=px.colors.qualitative.Dark24)
    fig_category_sales.update_yaxes(autorange="reversed") # To show highest at top
    st.plotly_chart(fig_category_sales, use_container_width=True)

with col_r2_c2:
    st.subheader("Sales by Day of Week")
    sales_by_day_of_week = filtered_data.groupby('Day_of_Week')['Sales_amt'].sum().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()
    fig_day_sales = px.bar(sales_by_day_of_week, x='Day_of_Week', y='Sales_amt',
                           title='Total Sales by Day of Week',
                           labels={'Sales_amt': 'Total Revenue', 'Day_of_Week': 'Day of Week'},
                           color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_day_sales, use_container_width=True)

# Row 3: Marketing Spend vs. Revenue & Discount Impact
col_r3_c1, col_r3_c2 = st.columns(2)

with col_r3_c1:
    st.subheader("Marketing Spend vs. Total Revenue")
    # Ensure marketing_spend is merged with monthly revenue data
    monthly_summary_dashboard = filtered_data.groupby('Year_month')['Sales_amt'].sum().reset_index()
    monthly_marketing_spend = marketing_spend.groupby('Year_month')['Total_spend'].sum().reset_index()
    marketing_revenue_df = pd.merge(monthly_summary_dashboard, monthly_marketing_spend, on='Year_month', how='left').fillna(0)
    marketing_revenue_df.rename(columns={'Sales_amt': 'Total_Revenue', 'Total_spend': 'Marketing_Spend'}, inplace=True)

    fig_marketing_revenue = px.line(marketing_revenue_df, x='Year_month', y=['Total_Revenue', 'Marketing_Spend'],
                                    title='Marketing Spend vs. Total Revenue Over Time',
                                    labels={'value': 'Amount', 'variable': 'Metric', 'Year_month': 'Month'},
                                    color_discrete_map={'Total_Revenue': 'blue', 'Marketing_Spend': 'red'})
    fig_marketing_revenue.update_xaxes(tickangle=45)
    st.plotly_chart(fig_marketing_revenue, use_container_width=True)

with col_r3_c2:
    st.subheader("Sales Amount by Discount Percentage")
    discount_revenue = filtered_data.groupby('Discount_pct')['Sales_amt'].sum().reset_index()
    fig_discount_revenue = px.bar(discount_revenue, x='Discount_pct', y='Sales_amt',
                                  title='Total Sales Amount by Discount Percentage',
                                  labels={'Sales_amt': 'Total Sales Amount', 'Discount_pct': 'Discount Percentage (%)'},
                                  color_discrete_sequence=px.colors.sequential.Plasma)
    st.plotly_chart(fig_discount_revenue, use_container_width=True)

# Row 4: Customer Retention Heatmap
st.subheader("Customer Retention by Monthly Cohorts")

# Highlight Start: Changes made in this block for robust cohort calculation
# Create a 'CohortGroup' which is the month of the first purchase
# Ensure CustomerID is a column before this groupby
if 'CustomerID' not in filtered_data.columns:
    filtered_data = filtered_data.reset_index() # Defensive check

filtered_data['CohortGroup'] = filtered_data.groupby('CustomerID')['Transaction_Date'].transform('min').dt.strftime('%Y-%m')

# Create 'CohortPeriod' which is the number of months since the first purchase
def get_cohort_period_dashboard(df):
    df['CohortPeriod'] = (df['Transaction_Date'].dt.to_period('M') - df['CohortGroup'].astype('period[M]')).apply(lambda x: x.n)
    return df

# Apply get_cohort_period_dashboard and immediately reset_index()
if not filtered_data.empty:
    # Use group_keys=False to avoid creating group keys as index levels in the result of apply
    # Then reset_index() to ensure CustomerID is a column for subsequent operations
    filtered_data_for_cohort = filtered_data.groupby('CustomerID', group_keys=False).apply(get_cohort_period_dashboard).reset_index()

    # Calculate total users in each cohort and their retention
    cohorts_dashboard = filtered_data_for_cohort.groupby(['CohortGroup', 'CohortPeriod'])['CustomerID'].nunique().reset_index()
    cohorts_dashboard.rename(columns={'CustomerID': 'Total_Users'}, inplace=True)

    cohort_group_size_dashboard = cohorts_dashboard[cohorts_dashboard['CohortPeriod'] == 0].set_index('CohortGroup')['Total_Users']
    cust_retention_dashboard = cohorts_dashboard.pivot_table(index='CohortGroup', columns='CohortPeriod', values='Total_Users')
    cust_retention_dashboard = cust_retention_dashboard.divide(cohort_group_size_dashboard, axis=0) * 100 # Convert to percentage

    # Plotting heatmap using Plotly go.Heatmap
    fig_retention = go.Figure(data=go.Heatmap(
                       z=cust_retention_dashboard.values,
                       x=cust_retention_dashboard.columns.astype(str),
                       y=cust_retention_dashboard.index,
                       colorscale='Greens',
                       colorbar=dict(title='Retention (%)')))

    fig_retention.update_layout(
        title='Customer Retention by Monthly Cohorts (%)',
        xaxis_title='Cohort Period (Months Since Acquisition)',
        yaxis_title='Cohort Group (Acquisition Month)',
        xaxis_nticks=len(cust_retention_dashboard.columns)
    )
    st.plotly_chart(fig_retention, use_container_width=True)
else:
    st.warning("No data available for the selected filters to display Customer Retention.")
# Highlight End: Changes made in this block

st.markdown("---")
st.write("This dashboard provides a high-level overview of key e-commerce metrics. For deeper insights and predictive models, refer to the full marketing insights report.")

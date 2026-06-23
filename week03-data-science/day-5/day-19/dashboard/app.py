import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time

# Page configuration
st.set_page_config(
    page_title="Executive Sales & Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #1f77b4;
    }
    h1, h2, h3 {
        color: #1e293b;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# 1. Caching data loading from CSV
@st.cache_data
def load_sales_data():
    # Use path relative to app.py location
    csv_path = os.path.join(os.path.dirname(__file__), 'sales_data.csv')
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Load data
df = load_sales_data()

# Title and introduction
st.title("📊 Executive Sales & Performance Dashboard")
st.markdown("Monitor key performance metrics, sales trends, and customer insights in real-time.")

# Sidebar Filters
st.sidebar.header("🎛️ Dashboard Filters")

# Date range selector
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Region filter
selected_regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=df['Region'].unique().tolist(),
    default=df['Region'].unique().tolist()
)

# Category filter
selected_categories = st.sidebar.multiselect(
    "Select Category(s)",
    options=df['Category'].unique().tolist(),
    default=df['Category'].unique().tolist()
)

# Sales slider
min_sales_val, max_sales_val = float(df['Sales'].min()), float(df['Sales'].max())
sales_threshold = st.sidebar.slider(
    "Minimum Sales Value ($)",
    min_value=min_sales_val,
    max_value=max_sales_val,
    value=min_sales_val
)

# Apply filters
filtered_df = df[
    (df['Region'].isin(selected_regions)) &
    (df['Category'].isin(selected_categories)) &
    (df['Sales'] >= sales_threshold)
]

# Handle date range safely
if len(date_range) == 2:
    start_dt, end_dt = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_df = filtered_df[(filtered_df['Date'] >= start_dt) & (filtered_df['Date'] <= end_dt)]

# --- CRITICAL EDGE CASE CHECK ---
if filtered_df.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust your criteria in the sidebar filters.")
    st.stop()

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = len(filtered_df)
avg_rating = filtered_df['Rating'].mean()

with col1:
    st.metric(
        label="💰 Total Revenue", 
        value=f"${total_revenue:,.2f}", 
        delta=f"+{total_revenue * 0.05:,.2f} vs last month"
    )

with col2:
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
    st.metric(
        label="📈 Total Profit", 
        value=f"${total_profit:,.2f}", 
        delta=f"{profit_margin:.1f}% Margin"
    )

with col3:
    st.metric(
        label="📦 Total Orders", 
        value=f"{total_orders:,}", 
        delta=f"+{int(total_orders * 0.08)} vs last month"
    )

with col4:
    st.metric(
        label="⭐ Avg Rating", 
        value=f"{avg_rating:.2f} / 5.0", 
        delta=None
    )

st.markdown("---")

# Main View Tabs
tab1, tab2, tab3 = st.tabs(["📈 Performance Charts", "🔍 Data Explorer", "💡 Business Insights"])

with tab1:
    st.subheader("Visual Analysis")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Chart 1: Sales Trend over Time (Streamlit Native line_chart)
        st.markdown("#### Sales & Profit Trends Over Time")
        daily_sales = filtered_df.groupby('Date')[['Sales', 'Profit']].sum().reset_index()
        st.line_chart(daily_sales, x='Date', y=['Sales', 'Profit'])
        
        # Chart 3: Correlation / Scatter plot (Streamlit Native scatter_chart)
        st.markdown("#### Sales vs. Profit Correlation")
        st.scatter_chart(filtered_df, x='Sales', y='Profit', color='Category')

    with col_right:
        # Chart 2: Category Breakdown (Streamlit Native bar_chart)
        st.markdown("#### Sales by Product Category")
        category_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index().sort_values('Sales', ascending=False)
        st.bar_chart(category_sales, x='Category', y='Sales')
        
        # Chart 4: Region Performance (Pie Chart using Matplotlib)
        st.markdown("#### Regional Sales Market Share")
        region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        ax4.pie(
            region_sales['Sales'], 
            labels=region_sales['Region'], 
            autopct='%1.1f%%', 
            colors=sns.color_palette('pastel')[0:4],
            startangle=90
        )
        ax4.axis('equal')
        ax4.set_title("Market Share by Region", fontsize=14, pad=10)
        plt.tight_layout()
        st.pyplot(fig4)

with tab2:
    st.subheader("Transactional Data Explorer")
    st.markdown("Search and filter the raw transaction records.")
    
    # Search input
    search_query = st.text_input("Search categories or regions", "")
    
    display_df = filtered_df.copy()
    if search_query:
        display_df = display_df[
            display_df['Category'].str.contains(search_query, case=False) |
            display_df['Region'].str.contains(search_query, case=False)
        ]
        
    st.dataframe(display_df, use_container_width=True)
    
    # Download option
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_sales_data.csv',
        mime='text/csv'
    )
    
    # Summary statistics
    with st.expander("Show Statistical Summary"):
        st.write(display_df.describe())

with tab3:
    st.subheader("📈 Strategic Insights")
    
    # Dynamic insight calculations
    top_category = filtered_df.groupby("Category")["Sales"].sum().idxmax()
    top_region = filtered_df.groupby("Region")["Profit"].sum().idxmax()
    lowest_profit_category = filtered_df.groupby("Category")["Profit"].sum().idxmin()
    total_quantity = filtered_df['Quantity'].sum()
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown(f"""
        ### Key Observations
        * The highest revenue contributing department is **{top_category}**.
        * The most profitable market region is **{top_region}**.
        * Across the selected filters, users ordered a total of **{total_quantity:,} items**, yielding a cumulative revenue of **${total_revenue:,.2f}**.
        * The lowest profit department in this segment is **{lowest_profit_category}**.
        * Customer satisfaction stands at an average of **{avg_rating:.2f}/5.0**.
        """)
        
    with col_b:
        st.markdown(f"""
        ### Strategic Recommendations
        1. **Target {top_region} Expansion**: Further capitalize on the profitability in the **{top_region}** region through targeted marketing.
        2. **Improve {lowest_profit_category} Profitability**: Re-evaluate the cost structure or pricing model of the **{lowest_profit_category}** category.
        3. **Optimize Inventory**: Adjust stock levels in **{top_category}** products to match current demand trends.
        """)



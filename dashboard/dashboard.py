import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
merged_df = pd.read_csv('./data/merged_data.csv')
rfm = pd.read_csv('./data/rfm.csv')

# Isi
st.header('E-Commerce Dashboard')

st.subheader('by Charles Wijaya')

st.image("./E-Commerce.jpeg", use_container_width=True)

st.write("This is the dataset used for analysis")

st.write(merged_df)

tabs = st.tabs(['Customers', 'Sellers', 'Products', 'Rating & Deliveries', 'Others'])

with tabs[0]:
    st.title("Top 10 Customers by Spending")
    st.write("Here are the top 10 customers with the highest total spending:")

    # Plotting the top 10 customers by spending
    fig, ax = plt.subplots(figsize=(10, 5))
    customer_spending = merged_df.groupby("customer_unique_id")["payment_value"].sum().sort_values(ascending=False).head(10)
    sns.barplot(x=customer_spending.values, y=customer_spending.index, palette="viridis", ax=ax)
    ax.set_xlabel("Total Spending")
    ax.set_ylabel("Customer ID")
    ax.set_title("Top 10 Customers by Spending")
    st.pyplot(fig)
    
    st.title("Top 10 Customers by Orders Count")
    st.write("Here are the top 10 customers with the highest total orders count:")
    
    # Plotting the top 10 customers by orders count
    customer_orders = merged_df.groupby("customer_unique_id")["order_id"].count().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=customer_orders.values, y=customer_orders.index, palette="viridis", ax=ax)
    ax.set_xlabel("Total Orders Count")
    ax.set_ylabel("Customer ID")
    ax.set_title("Top 10 Customers by Orders Count")
    st.pyplot(fig)
    
    st.title("Segmentation of Customers")
    st.write("Segmentation of customers based on RFM analysis:")
    st.write(rfm)
    
    rfm_count = rfm.groupby("RFM_Score").size().reset_index(name="Customer Count")
    st.title("Customer Count by RFM Score")
    st.write(rfm_count)
    
    st.write("Startegi untuk beberapa segmentasi:")
    st.image("./Segmentasi.png", use_container_width=True)
    

with tabs[1]:
    st.title("Top 10 Sellers by Revenue")
    st.write("Here are the top 10 sellers with the highest total revenue:")

    # Plotting the top 10 sellers by revenue
    fig, ax = plt.subplots(figsize=(10, 5))
    seller_revenue = merged_df.groupby("seller_id")["payment_value"].sum().sort_values(ascending=False).head(10)
    sns.barplot(x=seller_revenue.values, y=seller_revenue.index, palette="viridis", ax=ax)
    ax.set_xlabel("Total Revenue")
    ax.set_ylabel("Seller ID")
    ax.set_title("Top 10 Sellers by Revenue")
    st.pyplot(fig)

    st.title("Top 10 Sellers by Orders Count")
    st.write("Here are the top 10 sellers with the highest total orders count:")
    
    # Plotting the top 10 sellers by orders count
    seller_orders = merged_df.groupby("seller_id")["order_id"].count().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=seller_orders.values, y=seller_orders.index, palette="viridis", ax=ax)
    ax.set_xlabel("Total Orders Count")
    ax.set_ylabel("Seller ID")
    ax.set_title("Top 10 Sellers by Orders Count")
    st.pyplot(fig)
    
    seller_order_counts = merged_df.groupby("seller_id")["order_id"].count()
    sellers_filter = seller_order_counts[seller_order_counts > 100].index
    seller_ratings = merged_df[merged_df["seller_id"].isin(sellers_filter)].groupby("seller_id")["review_score"].mean().sort_values(ascending=False)
    top_sellers_by_rating = seller_ratings.head(10)
    
    st.title("Top 10 Sellers by Rating")
    st.write("Here are the top 10 sellers with the highest average rating (Sales > 100):")
    
    # Plotting the top 10 sellers by rating
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y=top_sellers_by_rating.index, x=top_sellers_by_rating.values, palette="viridis")
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Seller ID")
    ax.set_title("Top 10 Sellers by Rating (Sales > 100)")
    st.pyplot(fig)

    
with tabs[2]:
    st.title("Distribution of Product Prices")
    st.write("Here is the distribution of product prices:")
    
    # Plotting the distribution of product prices
    fig,ax = plt.subplots(figsize=(10,5))
    sns.histplot(merged_df['price'], bins=50, kde=True)
    ax.set_xlim(0, 1000)
    ax.set_xlabel("Price")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribusi Harga Produk")
    st.pyplot(fig)
    
    st.title("Top 10 Products by Revenue")
    st.write("Here are the top 10 products with the highest total revenue:")
    
    # Plotting the top 10 products by revenue
    top_products = merged_df.groupby("product_category_name_english")["payment_value"].sum().sort_values(ascending=False).head(10)
    fig,ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y=top_products.index, x=top_products.values, palette='coolwarm')
    ax.set_xlabel("Total Revenue")
    ax.set_ylabel("Product Category")
    ax.set_title("10 Kategori Produk Terlaris by Revenue")
    st.pyplot(fig)
    
    st.title("Top 10 Products by Order Count")
    st.write("Here are the top 10 products with the highest total order count:")
    
    # Plotting the top 10 products by order count
    top_categories = merged_df['product_category_name_english'].value_counts().head(10)
    fig,ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y=top_categories.index, x=top_categories.values, palette='coolwarm')
    ax.set_xlabel("Total Orders")
    ax.set_ylabel("Product Category")
    ax.set_title("10 Kategori Produk Terlaris by Order Count")
    st.pyplot(fig)
    
    st.title("Top 10 Products by Rating")
    st.write("Here are the top 10 products with the highest average rating:")
    
    # Plotting the top 10 products by rating
    order_counts = merged_df.groupby("product_category_name_english")["order_id"].count()
    valid_categories = order_counts[order_counts >= 100].index
    filtered_df = merged_df[merged_df["product_category_name_english"].isin(valid_categories)]
    top_products_by_rating = (
        filtered_df.groupby("product_category_name_english")["review_score"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y=top_products_by_rating.index, x=top_products_by_rating.values, palette="coolwarm", ax=ax)
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Product Category")
    ax.set_title("10 Kategori Produk Terlaris by Rating (Min. 100 Orders)")

    st.pyplot(fig)
    
with tabs[3]:
    st.title("Rating Distribution")
    st.write("Here is the distribution of ratings:")
    
    # Plotting the distribution of ratings
    fig,ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x=merged_df['review_score'], palette='coolwarm')
    ax.set_xlabel("Review Score")
    ax.set_ylabel("Count")
    ax.set_title("Distribusi Review Score")
    st.pyplot(fig)
    
    st.title("Box Plot Delivery Delay")
    
    fig,ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(y=merged_df['delivery_delay'], color='red')
    ax.set_ylabel("Days Late")
    ax.set_title("Distribusi Keterlambatan Pengiriman")
    st.pyplot(fig)
    
    st.title("Average Delivery Time by Review Score")
    st.write("Here is the average delivery time by review score:")
    
    delivery_time_by_review = merged_df.groupby("review_score")["delivery_time"].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    delivery_time_by_review.plot(kind="bar", ax=ax)
    ax.set_title("Rata-rata Waktu Pengiriman Berdasarkan Review Score")
    ax.set_xlabel("Skor Review")
    ax.set_ylabel("Rata-rata Waktu Pengiriman (Hari)")
    st.pyplot(fig)

with tabs[4]:
    st.title("Payment Method Distribution")
    st.write("Here is the distribution of payment methods:")
    
    fig,ax = plt.subplots(figsize=(8, 5))
    sns.countplot(y=merged_df['payment_type'], order=merged_df['payment_type'].value_counts().index, palette='viridis')
    ax.set_xlabel("Count")
    ax.set_ylabel("Payment Method")
    ax.set_title("Metode Pembayaran Terbanyak")
    st.pyplot(fig)
    
    st.title('Hourly Order Distribution')
    st.write("Here is the distribution of orders by hour:")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(merged_df["hour_timestamp"], bins=24, edgecolor="black")
    ax.set_title("Distribusi Waktu Pembelian dalam Sehari")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Pesanan")
    st.pyplot(fig)
            

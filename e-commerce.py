import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

events = pd.read_csv('events.csv')
orders = pd.read_csv('orders.csv')
order_items = pd.read_csv('order_items.csv')
products = pd.read_csv('products.csv')
users = pd.read_csv('users.csv')
reviews = pd.read_csv('reviews.csv')

print('loaded successfully...')

print(orders.head())
print(orders.info())
print(orders.shape)

print(order_items.head())
print(order_items.info())
print(order_items.shape)

print(users.head())
print(users.info())
print(users.shape)

print(reviews.head())
print(reviews.info())
print(reviews.shape)

print(events.head())
print(events.info())
print(events.shape)

print(products.head())
print(products.info())
print(products.shape)

orders['orders_date'] = pd.to_datetime(orders['order_date'])
events['event_timestamp'] = pd.to_datetime(events['event_timestamp'])


sales = order_items.merge(
    orders.drop(columns=['user_id']),
    on='order_id',
    how='left'
)

sales = sales.merge(users, on='user_id', how='left')
sales = sales.merge(products, on='product_id', how='left')
print(sales.head())
print(sales.info)


best_products =(
    sales.groupby('product_name')['quantity']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print('Top 5 Best Selling Products:')
print(best_products.head(5))

worst_products = (
    sales.groupby('product_name')['quantity']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    )

print('Top 5 Worst selling Products:')
print(worst_products.tail(5))

customer_spending = (
    sales.groupby('user_id')['item_total']
    .sum()
    .sort_values(ascending=False)
    )

print(customer_spending.head(10))

avg_order_value = sales.groupby('order_id')['item_total']
print('Average Order Value:',avg_order_value)

sales['order_date'] = pd.to_datetime(sales['order_date'])
sales['month'] = sales['order_date'].dt.to_period('M')
monthly_sales = sales.groupby('month')['item_total'].sum()
print(monthly_sales)

plt.figure(figsize=(15,8))

plt.subplot(2,2,1)
best_products.plot(kind='bar', color="#4C72B0")
plt.title("Top 5 Best Selling Products", fontsize=12)
plt.xlabel('[Products')
plt.ylabel('Quantity Sold')

plt.subplot(2,2,2)
worst_products.plot(kind='bar', color="#DD8452")
plt.title('Top 5 worst Selling Products', fontsize=12)
plt.xlabel('[Products')
plt.ylabel('Quantity Sold')

plt.subplot(2,2,3)
monthly_sales.plot(kind='line', marker="o", color="#55A868")
plt.title('Monthly Sales Trend', fontsize=12)
plt.xlabel('Month')
plt.ylabel('Total sales')

plt.suptitle("E-Commerce Sales Analysis Dashboard", fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0,0,1,0.95])
plt.show()


import os
print(os.getcwd())

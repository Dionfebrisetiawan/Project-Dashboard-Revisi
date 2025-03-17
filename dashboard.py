import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from babel.numbers import format_currency
from unidecode import unidecode 

sns.set(style='dark')

st.header('Selamat Datang di Dashboard E-Commerce Public Dataset ✨')

order_payments = pd.read_csv("order_payments_dataset.csv")  
customer_dataset = pd.read_csv("customers_dataset.csv")  

st.subheader("Distribusi Tipe Pembayaran")

data = order_payments.groupby("payment_type")["payment_value"].agg(['count', 'mean']).reset_index()
data.columns = ["payment_type", "count", "average_value"]

selected_payments = st.multiselect("**Filter Perbandingan Metode Pembayaran**:", data['payment_type'].unique(), default=data['payment_type'].tolist())
filtered_data = data[data['payment_type'].isin(selected_payments)]
filtered_data = filtered_data.sort_values(by="count", ascending=False)

fig = px.bar(filtered_data, x='payment_type', y='count', text='count',
             labels={'count': 'Jumlah Transaksi'},
             hover_data=['average_value'],
             width=600, height=400)
            
st.plotly_chart(fig)
st.dataframe(filtered_data)

st.subheader("Distribusi Jumlah Customer Per Kota")

customer_counts = customer_dataset["customer_city"].value_counts().reset_index()
customer_counts.columns = ["customer_city", "count"]

customer_dataset["customer_city"] = (
    customer_dataset["customer_city"]
    .str.lower()            
    .str.strip()           
    .str.replace("ã", "a")
)

top_5_cities = customer_counts.head(5)  

selected_city = st.multiselect(
    "**Filter Perbandingan Distribusi Customer**:", top_5_cities['customer_city'], default=top_5_cities['customer_city'].tolist()
)
filtered_data = customer_counts[customer_counts['customer_city'].isin(selected_city)]
filtered_data = filtered_data.sort_values(by="count", ascending=False)

fig = px.bar(filtered_data, x='count', y='customer_city', text='count',
                 labels={'count': 'Jumlah Customer', 'customer_city': 'Kota'},
                 height=500)

st.plotly_chart(fig)
st.dataframe(filtered_data)

st.subheader("Jumlah Transaksi vs Rata-rata Nilai Transaksi Berdasarkan Metode Pembayaran")

if order_payments.empty:
    raise ValueError("Dataset order_payments kosong")

# Menghitung jumlah transaksi per metode pembayaran
payment_count = order_payments["payment_type"].value_counts().reset_index()
payment_count.columns = ["payment_type", "count"]

# Menghitung rata-rata nilai transaksi per metode pembayaran
average_transaction = order_payments.groupby("payment_type")["payment_value"].mean().reset_index()

result = pd.merge(payment_count, average_transaction, on="payment_type")

print(result.head())

fig, ax1 = plt.subplots(figsize=(12, 6))

color1 = "#72BCD4"
sns.barplot(x="payment_type", y="count", data=result, ax=ax1, color=color1, label="Total Transactions")

ax2 = ax1.twinx()
color2 = "#D97706"
sns.lineplot(x="payment_type", y="payment_value", data=result, ax=ax2, color=color2, marker="o", linewidth=2, label="Avg Transaction Value")

ax1.set_xlabel("Payment Type")
ax1.set_ylabel("Total Transactions", color=color1)
ax2.set_ylabel("Avg Transaction Value", color=color2)

ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

st.pyplot(fig)

st.write("Do you satisfied with the dashboard?")

max_value = st.slider(
    label="Adjust satisfaction level",
    min_value=0, max_value=100, value=100
)
values = (0, max_value)

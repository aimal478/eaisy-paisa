import streamlit as st
import pandas as pd
from datetime import date

# CSV file to store data
FILE_NAME = "easypaisa_daily_record.csv"

# Load or initialize DataFrame
def load_data():
    try:
        return pd.read_csv(FILE_NAME)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Total Sale', 'Total Expense', 'Profit'])

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

# Main app
st.set_page_config(page_title="Easypaisa Daily Record", layout="centered")
st.title("📱 Easypaisa Daily Record & Profit Tracker")

# Input fields
with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        entry_date = st.date_input("Date", value=date.today())
        sale = st.number_input("Total Sale (Rs)", min_value=0.0, step=100.0)
    with col2:
        expense = st.number_input("Total Expense (Rs)", min_value=0.0, step=100.0)

    submitted = st.form_submit_button("➕ Add Record")

# Process submission
df = load_data()

if submitted:
    profit = sale - expense
    new_row = {'Date': entry_date, 'Total Sale': sale, 'Total Expense': expense, 'Profit': profit}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)
    st.success(f"Record added for {entry_date}: Profit Rs. {profit:.2f}")

# Show records
st.subheader("📊 All Records")
if df.empty:
    st.info("No records yet. Start by adding a sale record above.")
else:
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)

    # Total profit summary
    st.subheader("📈 Summary")
    total_profit = df["Profit"].sum()
    total_sale = df["Total Sale"].sum()
    total_expense = df["Total Expense"].sum()
    st.metric("💰 Total Profit", f"Rs. {total_profit:.2f}")
    st.metric("🧾 Total Sale", f"Rs. {total_sale:.2f}")
    st.metric("💸 Total Expense", f"Rs. {total_expense:.2f}")

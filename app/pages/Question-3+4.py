import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import numpy as np

# Database functions
def create_connection():
    conn = sqlite3.connect('rent_data.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rent_data (
            id INTEGER PRIMARY KEY,
            city TEXT,
            date TEXT,
            rent_price REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(city, date, rent_price):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO rent_data (city, date, rent_price) VALUES (?, ?, ?)',
                   (city, date, rent_price))
    conn.commit()
    conn.close()

def get_data(city):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rent_data WHERE city = ?', (city,))
    data = cursor.fetchall()
    conn.close()
    return data

def update_data(id, city, date, rent_price):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE rent_data SET city = ?, date = ?, rent_price = ? WHERE id = ?',
                   (city, date, rent_price, id))
    conn.commit()
    conn.close()

def delete_data(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM rent_data WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Streamlit visualization
create_table()

st.title("Rent Forecasting Analysis")

# Data input
city = st.selectbox("Select a city", ["Los Angeles", "Rochester"])
date = st.date_input("Select date")
rent_price = st.number_input("Enter rent price")

if st.button("Add Data"):
    insert_data(city, str(date), rent_price)
    st.success("Data added successfully!")

# Data display with Edit and Delete buttons
rent_data = get_data(city)
df = pd.DataFrame(rent_data, columns=["ID", "City", "Date", "Rent Price"])

for index, row in df.iterrows():
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])
    with col1:
        st.write(row['City'])
    with col2:
        st.write(row['Date'])
    with col3:
        st.write(f"${row['Rent Price']:.2f}")
    with col4:
        if st.button('Edit', key=f'edit_{index}'):
            st.session_state.editing = index
    with col5:
        if st.button('Delete', key=f'delete_{index}'):
            delete_data(row['ID'])
            st.experimental_rerun()

# Edit form
if 'editing' in st.session_state:
    edit_row = df.loc[st.session_state.editing]
    with st.form(key=f'edit_form_{st.session_state.editing}'):
        new_city = st.text_input("City", value=edit_row['City'])
        new_date = st.date_input("Date", value=pd.to_datetime(edit_row['Date']))
        new_price = st.number_input("Rent Price", value=float(edit_row['Rent Price']))
        if st.form_submit_button("Save Changes"):
            update_data(edit_row['ID'], new_city, new_date, new_price)
            del st.session_state.editing
            st.experimental_rerun()

# Analysis and visualization
if st.button("Analyze Rent Distribution"):
    rent_prices = df["Rent Price"].values.reshape(-1, 1)
    
    if len(rent_prices) > 1:
        n_components = min(len(rent_prices), 3)  # Adjust n_components
        gmm = GaussianMixture(n_components=n_components, random_state=42)
        gmm.fit(rent_prices)
        
        x = np.linspace(rent_prices.min(), rent_prices.max(), 1000).reshape(-1, 1)
        y = np.exp(gmm.score_samples(x))
        
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title(f"Rent Distribution for {city}")
        ax.set_xlabel("Rent Price")
        ax.set_ylabel("Density")
        st.pyplot(fig)
        
        st.write("GMM Means:", gmm.means_.flatten())
        st.write("GMM Variances:", gmm.covariances_.flatten())
    else:
        st.warning("Not enough data for analysis. Please add more rent prices.")

# Seasonal analysis
if st.button("Analyze Seasonal Patterns"):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Season'] = df['Date'].dt.month.map({12: 'Winter', 1: 'Winter', 2: 'Winter',
                                            3: 'Spring', 4: 'Spring', 5: 'Spring',
                                            6: 'Summer', 7: 'Summer', 8: 'Summer',
                                            9: 'Fall', 10: 'Fall', 11: 'Fall'})
    
    seasonal_avg = df.groupby('Season')['Rent Price'].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots()
    seasonal_avg.plot(kind='bar', ax=ax)
    ax.set_title(f"Average Rent by Season in {city}")
    ax.set_ylabel("Average Rent Price")
    st.pyplot(fig)

# Time series analysis
if st.button("Show Rent Price Trend"):
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    fig, ax = plt.subplots()
    ax.plot(df['Date'], df['Rent Price'])
    ax.set_title(f"Rent Price Trend in {city}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Rent Price")
    plt.xticks(rotation=45)
    st.pyplot(fig)

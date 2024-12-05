import streamlit as st
import pandas as pd
import numpy as np 
import warnings
from google.cloud import storage
import matplotlib.pyplot as plt 

from statsmodels.tsa.arima.model import ARIMA
warnings.simplefilter('ignore')

st.sidebar.info("Adapted from Marcus Hartman's Question 1.")

st.header("Question 1")
st.text("Could there be a larger increase in the gap of rent between a high-income state and one that is lower? Could we see people move to other states to save the money, but work remotely?")

st.divider()

st.subheader("Interact with the Database")

progress_text = "Processing the data; please wait. This may take a few minutes to complete."

st.markdown("### Texas")
huduser_TX = pd.read_csv('gs://cse-587-huduser/huduser_TX.csv')

def updateTX():
    client = storage.Client()
    f = client.bucket("cse-587-huduser").blob("huduser_TX.csv")
    if f.exists():
        f.delete()
    huduser_TX.to_csv("gs://cse-587-huduser/huduser_TX.csv", index=False)
st.data_editor(huduser_TX, use_container_width=True, hide_index=True, on_change=updateTX)

# util
years = np.array(range(2017, 2025))

st.markdown("#### Values for ARIMA parameters")
autoregression_TX = st.number_input("Value for Autoregression", value=1, key=5)
differencing_TX = st.number_input("Value for Differencing", value=0, key=6)
moving_average_TX = st.number_input("Value for Moving Average", value=2, key=7)
process_TX = st.button("Process the Data", key=1)

if process_TX:
    bar_TX = st.progress(0, text=progress_text)
    allCounties_TX = huduser_TX["county_name"].unique()
    ARIMA_data = {}
    
    for county in allCounties_TX:
        ARIMA_data[county] = []
        percent_complete = len(ARIMA_data) / len(allCounties_TX)
        
        for year in years:
            yearData = huduser_TX.loc[(huduser_TX["county_name"] == county) & (huduser_TX["year"] == year)]
            ARIMA_data[county].append(yearData['Efficiency'].iloc[0])
            
        # predict the next 5 years
        for year in range(2025, 2031):
            # consider the order=(autoregression, differencing, moving average). 
            # this is where influence based on the past data comes into play. one index = one year
            # these values (1,0,2) were chosen because the market can be thought to be influenced by the past couple of years, rather than the average going extremely high within a year (stability).
            model = ARIMA(ARIMA_data[county], order=(autoregression_TX, differencing_TX, moving_average_TX))
            model_fit = model.fit()
            ARIMA_data[county].append(model_fit.forecast()[0])
        
        # add each to the plot below
        
        bar_TX.progress(percent_complete, text=progress_text)
        
    st.line_chart(ARIMA_data, use_container_width=True, x_label="Years after 2017", y_label="Estimated Rent")
    st.text("Note that the x axis used to be labelled by the year in Phase 2, but limitations of the framework's (streamlit) API does not have the xticks option like in matplotlib.")
    bar_TX.empty()
    st.toast("Finished Processing Data!")
    
st.divider()

st.markdown("### Minnesota")
huduser_MN = pd.read_csv('gs://cse-587-huduser/huduser_MN.csv')

def updateMN():
    client = storage.Client()
    f = client.bucket("cse-587-huduser").blob("huduser_MN.csv")
    if f.exists():
        f.delete()
    huduser_MN.to_csv("gs://cse-587-huduser/huduser_MN.csv", index=False)    
st.data_editor(huduser_MN, use_container_width=True, hide_index=True, on_change=updateMN)

st.markdown("#### Values for ARIMA parameters")
autoregression_MN = st.number_input("Value for Autoregression", value=1, key=8)
differencing_MN = st.number_input("Value for Differencing", value=0, key=9)
moving_average_MN = st.number_input("Value for Moving Average", value=2, key=10)
process_MN = st.button("Process the Data", key=2)

if process_MN:
    bar_MN = st.progress(0, text=progress_text)
    allCounties_MN = huduser_MN["county_name"].unique()
    ARIMA_data = {}
    
    for county in allCounties_MN:
        ARIMA_data[county] = []
        percent_complete = len(ARIMA_data) / len(allCounties_MN)
        
        for year in years:
            yearData = huduser_MN.loc[(huduser_MN["county_name"] == county) & (huduser_MN["year"] == year)]
            ARIMA_data[county].append(yearData['Efficiency'].iloc[0])
            
        # predict the next 5 years
        for year in range(2025, 2031):
            # consider the order=(autoregression, diferencing, moving average). 
            # this is where influence based on the past data comes into play. one index = one year
            # these values (1,0,2) were chosen because the market can be thought to be influenced by the past couple of years, rather than the average going extremely high within a year (stability).
            model = ARIMA(ARIMA_data[county], order=(autoregression_MN, differencing_MN, moving_average_MN))
            model_fit = model.fit()
            ARIMA_data[county].append(model_fit.forecast()[0])
        
        # add each to the plot below
        
        bar_MN.progress(percent_complete, text=progress_text)
        
    st.line_chart(ARIMA_data, use_container_width=True, x_label="Years after 2017", y_label="Estimated Rent")
    st.text("Note that the x axis used to be labelled by the year in Phase 2, but limitations of the framework's (streamlit) API does not have the xticks option like in matplotlib.")
    bar_MN.empty()
    st.toast("Finished Processing Data!")
    
st.divider()
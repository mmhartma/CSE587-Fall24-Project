import streamlit as st
import pandas as pd
import numpy as np 
import warnings
import matplotlib.pyplot as plt 
from google.cloud import storage
from scipy import stats


st.sidebar.info("Adapted from Marcus Hartman's Question 2.")

st.header("Question 2")
st.text("As rent continues to rise, could we see a decline of single-room rent prices to combat multi-family apartments?")

st.divider()

st.subheader("Interact with the Database")

progress_text = "Processing the data; please wait. This may take a few minutes to complete."

st.markdown("### Texas")
huduser_TX = pd.read_csv('gs://cse-587-huduser/huduser_TX2.csv')

def updateTX():
    client = storage.Client()
    f = client.bucket("cse-587-huduser").blob("huduser_TX2.csv")
    if f.exists():
        f.delete()
    huduser_TX.to_csv("gs://cse-587-huduser/huduser_TX2.csv", index=False)
st.data_editor(huduser_TX, use_container_width=True, hide_index=True, on_change=updateTX)

# util
years = np.array(range(2017, 2025))

process_TX = st.button("Process the Data", key=1)

allCounties_TX = huduser_TX["county_name"].unique()

if process_TX:
    bar_TX = st.progress(0, text=progress_text)
    ARIMA_data = {}
    countyRegressions = {}
    
    for county in allCounties_TX:
        res = huduser_TX.loc[huduser_TX["county_name"] == county]
        regressions = {}
        
        columns = ["One-Bedroom", "Two-Bedroom", "Three-Bedroom", "Four-Bedroom"]
        for column in columns:
            y = res[column].to_numpy()
            slope, intercept, _r, _p, _err = stats.linregress(years, y)
            
            # map given regression line to points that can be used for graphing
            def findValue(x):
                return slope * x + intercept
            regressions[column] = list(map(findValue, years))
            
        countyRegressions[county] = regressions
        
    bar_TX.empty()
    st.session_state["isProcessed"] = True
    st.session_state.countyRegressions = countyRegressions
    
if "isProcessed" in st.session_state and "countyRegressions" in st.session_state:
    selectedCounty = st.selectbox("Select a county to display:", allCounties_TX, key="county")
    st.line_chart(st.session_state.countyRegressions[selectedCounty], x_label="Years after 2017", y_label="Rent Price")
    
    
st.divider()

st.markdown("### Minnesota")
huduser_MN = pd.read_csv('gs://cse-587-huduser/huduser_MN2.csv')

def updateMN():
    client = storage.Client()
    f = client.bucket("cse-587-huduser").blob("huduser_MN2.csv")
    if f.exists():
        f.delete()
    huduser_MN.to_csv("gs://cse-587-huduser/huduser_MN2.csv", index=False)    
st.data_editor(huduser_MN, use_container_width=True, hide_index=True, on_change=updateMN)

process_MN = st.button("Process the Data", key=2)

allCounties_MN = huduser_MN["county_name"].unique()

if process_MN:
    bar_MN = st.progress(0, text=progress_text)
    ARIMA_data = {}
    countyRegressions = {}
    
    for county in allCounties_MN:
        res = huduser_MN.loc[huduser_MN["county_name"] == county]
        regressions = {}
        
        columns = ["One-Bedroom", "Two-Bedroom", "Three-Bedroom", "Four-Bedroom"]
        for column in columns:
            y = res[column].to_numpy()
            slope, intercept, _r, _p, _err = stats.linregress(years, y)
            
            # map given regression line to points that can be used for graphing
            def findValue(x):
                return slope * x + intercept
            regressions[column] = list(map(findValue, years))
            
        countyRegressions[county] = regressions
        
    bar_MN.empty()
    st.session_state["_isProcessed"] = True
    st.session_state._countyRegressions = countyRegressions
    
if "_isProcessed" in st.session_state and "_countyRegressions" in st.session_state:
    selectedCounty = st.selectbox("Select a county to display:", allCounties_MN, key="_county")
    st.line_chart(st.session_state._countyRegressions[selectedCounty], x_label="Years after 2017", y_label="Rent Price")
    
    
st.divider()
import streamlit as st
from predict_page import show_predict_page

st.sidebar.selectbox("Explore or Predict", ("Predict","Explore"))

show_predict_page()
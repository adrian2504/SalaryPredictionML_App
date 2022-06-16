import streamlit as st
import pickle
import numpy as numpy

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


data = load_model()

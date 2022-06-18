import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


def show_predict_page():
    st.title("Software Developer Salary Prediction")
    st.write("""### We need some information to predict the salary""")

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]


countries = (
    "United States",
    "India",
    "United Kingdom",
    "Germany",
    "Canada",
    "Brazil",
    "France",
    "Spain",
    "Australia",
    "Netherlands",
    "Poland",
    "Italy",
    "Russian Federation",
    "Sweden"
)

education = (
    "Less than a Bachelors", 
    "Bachelor’s degree",
    "Master’s degree",
    "Post Grad"
)

country = st.selectbox("Countries", countries)
education = st.selectbox("Education Level", education)
experience = st.slider("Experience Level",0 , 50, 3)

ok = st.button("Calculate Salary")

if ok:
    x = np.array([[country,education,experience]])
    x[:,0] = le_country.transform(x[:,0])
    x[:,1] = le_education.transform(x[:,1])
    x = x.astype(float)

    salary = regressor.predict(x)
    st.subheader(f"The estimated salary is ${salary[0]:.2f}")
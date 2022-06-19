import streamlit as st
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt


def shorten_categories(categories, cutoff):
    categories_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categories_map[categories.index[i]] = categories.index[i]
        else:
            categories_map[categories.index[i]] = 'Other'

    return categories_map

def clean_experience(x):
    if x=='More than 50 years':
        return 50
    if x=='Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

# to imporve performance by preventing from re executing again.
@st.cache
def load_data():
    df = pd.read_csv("csv/survey_results_public.csv")
    df = df[["Country","EdLevel","YearsCodePro","Employment","ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly":"Salary"},axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment",axis=1)
    country_map = shorten_categories(df.Country.value_counts(),400)
    df['Country'] = df['Country'].map(country_map)

    df = df[df['Salary'] <= 250000]
    df = df[df['Salary']>=10000]
    df = df[df['Country'] != 'Other']

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)

    return df

df = load_data()

def show_explore_page():

    st.title("Explore Software Engineering Salaries")
    st.write(
        """
        ### StackOverFlow Survey 2021
        """
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%",shadow=False,startangle=90, textprops={'fontsize': 5})
    ax1.axis("equal") #equal aspect ratio ensures that pie is drawn as a circle

    st.write("""### Number of Data from Different Countries """)

    st.pyplot(fig1)

    st.write("""
    ### Mean Salary based on country 
    """)

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data,height=800)

    st.write(
        """ 
        ### Mean Salary based on experience """)

    data2 = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data,height=800)


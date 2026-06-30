import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

st.title("Day 19 Exercises: Streamlit Demonstration")

st.header("1. Widgets")
name = st.text_input("Enter your name", value="Alice")
age = st.slider("Select your age", min_value=0, max_value=100, value=25)
country = st.selectbox("Select your country", options=["USA", "India", "Germany", "Japan"])
agree = st.checkbox("I agree to the terms")
hobbies = st.multiselect("Select your hobbies", options=["Coding", "Reading", "Traveling", "Gaming"])
if st.button("Submit"):
    st.write(f"Hello {name}! You are {age} years old and live in {country}.")
    if agree:
        st.write("You agreed to the terms.")
    if hobbies:
        st.write(f"Your hobbies: {', '.join(hobbies)}")

st.header("2. Charts")
np.random.seed(42)
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
st.subheader("Streamlit Native Line Chart")
st.line_chart(chart_data)

st.subheader("Matplotlib & Seaborn Chart")
fig, ax = plt.subplots()
sns.histplot(chart_data['A'], kde=True, ax=ax)
st.pyplot(fig)

st.header("3. Layout")
st.sidebar.header("Configuration Sidebar")
theme = st.sidebar.radio("Choose App Theme", options=["Light", "Dark"])

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Active Users", value="1,245", delta="+12%")
with col2:
    st.metric(label="Conversion Rate", value="2.8%", delta="-0.4%")

tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
with tab1:
    st.write("Content for Tab 1")
with tab2:
    st.write("Content for Tab 2")

with st.expander("Show Details"):
    st.write("Here is some extra detailed information that remains hidden by default.")

st.header("4. Caching")
@st.cache_data
def load_large_dataset():
    time.sleep(2)
    df = pd.DataFrame({'Product': ['A', 'B', 'C'], 'Sales': [100, 200, 150]})
    return df

st.write("Loading cached data...")
start_time = time.time()
data = load_large_dataset()
duration = time.time() - start_time
st.write(f"Data loaded in {duration:.4f} seconds!")
st.dataframe(data)

@st.cache_resource
def load_model():
    time.sleep(2)
    return "Mock ML Model"

st.write("Loading cached resource (model)...")
start_time = time.time()
model = load_model()
duration = time.time() - start_time
st.write(f"Model loaded in {duration:.4f} seconds!")
st.write(model)

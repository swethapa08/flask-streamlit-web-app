import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# Configuration
# --------------------------------------------------

API_URL = "https://flask-streamlit-web-app-1.onrender.com/"


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Student Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📊 Student Analytics Dashboard")

st.write(
    "This dashboard gets student data "
    "from the Flask REST API."
)


# --------------------------------------------------
# Get data from Flask API
# --------------------------------------------------

try:

    response = requests.get(API_URL)

    if response.status_code != 200:

        st.error("Unable to get data from Flask API.")

        st.stop()

    data = response.json()


except requests.exceptions.ConnectionError:

    st.error(
        "Flask server is not running. "
        "Please start Flask first."
    )

    st.stop()


# --------------------------------------------------
# Check whether data exists
# --------------------------------------------------

if len(data) == 0:

    st.warning(
        "No student data found. "
        "Please add students through the Flask application."
    )

    st.stop()


# --------------------------------------------------
# Convert JSON to Pandas DataFrame
# --------------------------------------------------

df = pd.DataFrame(data)


# --------------------------------------------------
# Dashboard metrics
# --------------------------------------------------

total_students = len(df)

average_marks = df["marks"].mean()

average_attendance = df["attendance"].mean()


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Students",
        total_students
    )


with col2:

    st.metric(
        "Average Marks",
        round(average_marks, 2)
    )


with col3:

    st.metric(
        "Average Attendance",
        f"{average_attendance:.2f}%"
    )


# --------------------------------------------------
# Student data
# --------------------------------------------------

st.subheader("Student Data")

st.dataframe(
    df,
    use_container_width=True
)


# --------------------------------------------------
# Department Analysis
# --------------------------------------------------

st.subheader("Students by Department")


department_count = (
    df["department"]
    .value_counts()
)


st.bar_chart(
    department_count
)


# --------------------------------------------------
# Average Marks by Department
# --------------------------------------------------

st.subheader(
    "Average Marks by Department"
)


department_marks = (
    df.groupby("department")["marks"]
    .mean()
)


st.bar_chart(
    department_marks
)


# --------------------------------------------------
# Marks Distribution
# --------------------------------------------------

st.subheader("Marks Distribution")


fig1, ax1 = plt.subplots()


ax1.hist(
    df["marks"],
    bins=5
)


ax1.set_title(
    "Distribution of Student Marks"
)


ax1.set_xlabel("Marks")


ax1.set_ylabel(
    "Number of Students"
)


st.pyplot(fig1)


# --------------------------------------------------
# Attendance vs Marks
# --------------------------------------------------

st.subheader(
    "Attendance vs Marks"
)


fig2, ax2 = plt.subplots()


ax2.scatter(
    df["attendance"],
    df["marks"]
)


ax2.set_title(
    "Attendance vs Student Marks"
)


ax2.set_xlabel(
    "Attendance (%)"
)


ax2.set_ylabel(
    "Marks"
)


st.pyplot(fig2)


# --------------------------------------------------
# Statistical Summary
# --------------------------------------------------

st.subheader(
    "Statistical Summary"
)


st.dataframe(
    df.describe(),
    use_container_width=True
)
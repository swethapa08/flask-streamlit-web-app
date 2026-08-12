import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Flask API URL
API_URL = "https://flask-streamlit-web-app-1.onrender.com/api/students"

st.set_page_config(
    page_title="Student Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Student Analytics Dashboard")

st.write(
    "This dashboard gets student data from the Flask REST API."
)

# --------------------------------------------------
# Get data from Flask API
# --------------------------------------------------

try:

    response = requests.get(
        API_URL,
        timeout=30
    )

    # Show error if Flask API does not return 200
    if response.status_code != 200:

        st.error(
            f"Flask API returned status code: "
            f"{response.status_code}"
        )

        st.code(response.text[:1000])

        st.stop()

    # Check whether response is actually JSON
    try:

        data = response.json()

    except ValueError:

        st.error(
            "Flask API did not return JSON."
        )

        st.write("Response received from Flask:")

        st.code(response.text[:1000])

        st.stop()

except requests.exceptions.RequestException as e:

    st.error(
        "Unable to connect to Flask API."
    )

    st.write(str(e))

    st.stop()


# --------------------------------------------------
# Check data
# --------------------------------------------------

if not data:

    st.warning("No student data found.")

    st.stop()


# --------------------------------------------------
# Convert JSON to DataFrame
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
# Student Data
# --------------------------------------------------

st.subheader("Student Data")

st.dataframe(
    df,
    use_container_width=True
)


# --------------------------------------------------
# Students by Department
# --------------------------------------------------

st.subheader("Students by Department")

department_count = df["department"].value_counts()

st.bar_chart(department_count)


# --------------------------------------------------
# Average Marks by Department
# --------------------------------------------------

st.subheader("Average Marks by Department")

department_marks = (
    df.groupby("department")["marks"]
    .mean()
)

st.bar_chart(department_marks)


# --------------------------------------------------
# Marks Distribution
# --------------------------------------------------

st.subheader("Marks Distribution")

fig1, ax1 = plt.subplots()

ax1.hist(
    df["marks"],
    bins=5
)

ax1.set_title("Distribution of Student Marks")

ax1.set_xlabel("Marks")

ax1.set_ylabel("Number of Students")

st.pyplot(fig1)


# --------------------------------------------------
# Attendance vs Marks
# --------------------------------------------------

st.subheader("Attendance vs Marks")

fig2, ax2 = plt.subplots()

ax2.scatter(
    df["attendance"],
    df["marks"]
)

ax2.set_title(
    "Attendance vs Student Marks"
)

ax2.set_xlabel("Attendance (%)")

ax2.set_ylabel("Marks")

st.pyplot(fig2)


# --------------------------------------------------
# Statistical Summary
# --------------------------------------------------

st.subheader("Statistical Summary")

st.dataframe(
    df.describe(),
    use_container_width=True
)
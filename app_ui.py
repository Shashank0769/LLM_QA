import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# API Base URL (update if running on a different port)
BASE_URL = "http://127.0.0.1:8000"

# Streamlit UI
st.title("🏨 Hotel Booking Analytics")
st.markdown("Query hotel booking data using AI-powered search!")

# Query Section
st.header("🔍 Ask a Question")
user_query = st.text_input("Enter your question:", "Show me the highest revenue bookings")

if st.button("Get Answer"):
    response = requests.post(f"{BASE_URL}/ask", json={"question": user_query})
    if response.status_code == 200:
        st.write(response.json()["answer"])
    else:
        st.error("Failed to fetch data. Make sure FastAPI is running!")

# Analytics Section
st.header("📊 Booking Analytics")

if st.button("Get Analytics"):
    response = requests.get("http://127.0.0.1:8000/analytics")  # Replace with your API URL
    analytics_data = response.json()

    # Display Cancellation Rate
    st.subheader("📉 Cancellation Rate")
    st.write(f"**{analytics_data['cancellation_rate']:.2f}%**")

    # Display Top Booking Countries
    st.subheader("🌍 Top Booking Countries")
    for country, percentage in analytics_data["top_countries"].items():
        st.write(f"**{country}:** {percentage:.2f}%")

    # Revenue Trends Over Time (Line Chart)
    df_revenue = pd.DataFrame(analytics_data["revenue_trends"])
    df_revenue["date"] = df_revenue["month"] + '-' + df_revenue["year"].astype(str)

    st.subheader("📈 Revenue Trends Over Time")
    plt.figure(figsize=(12, 5))
    sns.lineplot(x="date", y="revenue", data=df_revenue, marker="o")
    plt.xticks(rotation=90)
    plt.xlabel("Month-Year")
    plt.ylabel("Total Revenue (ADR)")
    plt.title("Revenue Trends Over Time")
    st.pyplot(plt)

    # Booking Lead Time Distribution (Histogram)
    st.subheader("📊 Booking Lead Time Distribution")
    plt.figure(figsize=(12, 5))
    sns.histplot(analytics_data["lead_times"], bins=30, kde=True)
    plt.xlabel("Lead Time (Days)")
    plt.ylabel("Count")
    plt.title("Booking Lead Time Distribution")
    st.pyplot(plt)


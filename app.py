import streamlit as st
import pandas as pd
import sqlite3

# ---------------- DATABASE CONNECTION ----------------
conn = sqlite3.connect("local_food_wastage.db", check_same_thread=False)

# ---------------- LOAD CSV DATA INTO DB ----------------
def load_csv_to_db():

    providers_df = pd.read_csv("/mnt/data/providers_data.csv")
    receivers_df = pd.read_csv("/mnt/data/receivers_data.csv")
    food_df = pd.read_csv("/mnt/data/food_listings_data.csv")
    claims_df = pd.read_csv("/mnt/data/claims_data.csv")

    # Clean & map columns
    providers_df = providers_df[["Provider_ID", "Name"]]
    providers_df.columns = ["id", "name"]
    providers_df.to_sql("providers", conn, if_exists="replace", index=False)

    receivers_df = receivers_df[["Receiver_ID", "Name"]]
    receivers_df.columns = ["id", "name"]
    receivers_df.to_sql("receivers", conn, if_exists="replace", index=False)

    food_df = food_df[["Food_ID", "Food_Name", "Quantity", "Provider_ID"]]
    food_df.columns = ["id", "food_name", "quantity", "provider_id"]
    food_df.to_sql("food", conn, if_exists="replace", index=False)

    claims_df = claims_df[["Claim_ID", "Food_ID", "Receiver_ID", "Status"]]
    claims_df.columns = ["id", "food_id", "receiver_id", "status"]
    claims_df.to_sql("claims", conn, if_exists="replace", index=False)


# Load data once per run
load_csv_to_db()

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="Food Wastage System", layout="wide")

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Providers", "Receivers", "Food", "Claims", "Analysis"]
)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.title("🍲 Food Wastage Management Dashboard")

    providers = pd.read_sql("SELECT COUNT(*) AS total FROM providers", conn)
    receivers = pd.read_sql("SELECT COUNT(*) AS total FROM receivers", conn)
    food = pd.read_sql("SELECT COUNT(*) AS total FROM food", conn)
    claims = pd.read_sql("SELECT COUNT(*) AS total FROM claims", conn)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Providers", providers["total"][0])
    c2.metric("Receivers", receivers["total"][0])
    c3.metric("Food Listings", food["total"][0])
    c4.metric("Claims", claims["total"][0])

# ---------------- PROVIDERS ----------------
elif page == "Providers":

    st.title("Providers Data")

    df = pd.read_sql("SELECT * FROM providers", conn)
    st.dataframe(df, use_container_width=True)

# ---------------- RECEIVERS ----------------
elif page == "Receivers":

    st.title("Receivers Data")

    df = pd.read_sql("SELECT * FROM receivers", conn)
    st.dataframe(df, use_container_width=True)

# ---------------- FOOD ----------------
elif page == "Food":

    st.title("Food Listings")

    df = pd.read_sql("SELECT * FROM food", conn)
    st.dataframe(df, use_container_width=True)

# ---------------- CLAIMS ----------------
elif page == "Claims":

    st.title("Claims Data")

    df = pd.read_sql("SELECT * FROM claims", conn)
    st.dataframe(df, use_container_width=True)

# ---------------- ANALYSIS ----------------
elif page == "Analysis":

    st.title("Data Analysis")

    option = st.selectbox("Choose Analysis", [
        "Total Food Available",
        "Top Providers"
    ])

    if option == "Total Food Available":
        df = pd.read_sql("SELECT SUM(quantity) AS total_food FROM food", conn)

    elif option == "Top Providers":
        df = pd.read_sql("""
            SELECT provider_id, SUM(quantity) AS total
            FROM food
            GROUP BY provider_id
            ORDER BY total DESC
        """, conn)

    st.dataframe(df)

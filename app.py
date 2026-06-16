import streamlit as st
import pandas as pd
from db_connection import get_connection

# ---------------- DB CONNECTION ----------------
conn = get_connection()
cursor = conn.cursor()

# ---------------- CREATE TABLES ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS receivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT,
    quantity INTEGER,
    provider_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS claims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id INTEGER,
    receiver_id INTEGER,
    status TEXT
)
""")

conn.commit()

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Food Wastage System", layout="wide")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Providers", "Receivers", "Food", "Claims", "Analysis"]
)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.title("🍲 Food Wastage Dashboard")

    providers = pd.read_sql("SELECT COUNT(*) AS total FROM providers", conn)
    receivers = pd.read_sql("SELECT COUNT(*) AS total FROM receivers", conn)
    food = pd.read_sql("SELECT COUNT(*) AS total FROM food", conn)
    claims = pd.read_sql("SELECT COUNT(*) AS total FROM claims", conn)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Providers", providers["total"][0])
    c2.metric("Receivers", receivers["total"][0])
    c3.metric("Food", food["total"][0])
    c4.metric("Claims", claims["total"][0])

# ---------------- PROVIDERS ----------------
elif page == "Providers":

    st.title("Providers")

    name = st.text_input("Provider Name")

    if st.button("Add Provider"):
        if name:
            cursor.execute("INSERT INTO providers (name) VALUES (?)", (name,))
            conn.commit()
            st.success("Provider Added")

    df = pd.read_sql("SELECT * FROM providers", conn)
    st.dataframe(df)

# ---------------- RECEIVERS ----------------
elif page == "Receivers":

    st.title("Receivers")

    name = st.text_input("Receiver Name")

    if st.button("Add Receiver"):
        if name:
            cursor.execute("INSERT INTO receivers (name) VALUES (?)", (name,))
            conn.commit()
            st.success("Receiver Added")

    df = pd.read_sql("SELECT * FROM receivers", conn)
    st.dataframe(df)

# ---------------- FOOD ----------------
elif page == "Food":

    st.title("Food Management")

    action = st.selectbox("Action", ["View", "Add"])

    if action == "View":
        df = pd.read_sql("SELECT * FROM food", conn)
        st.dataframe(df)

    elif action == "Add":

        provider_id = st.number_input("Provider ID", step=1)
        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", step=1)

        if st.button("Add Food"):

            cursor.execute("""
            INSERT INTO food (food_name, quantity, provider_id)
            VALUES (?, ?, ?)
            """, (food_name, quantity, provider_id))

            conn.commit()
            st.success("Food Added")

# ---------------- CLAIMS ----------------
elif page == "Claims":

    st.title("Claims")

    df = pd.read_sql("SELECT * FROM claims", conn)
    st.dataframe(df)

# ---------------- ANALYSIS ----------------
elif page == "Analysis":

    st.title("SQL Analysis")

    option = st.selectbox("Choose", ["Top Providers", "Total Food"])

    if option == "Total Food":
        df = pd.read_sql("SELECT SUM(quantity) AS total FROM food", conn)

    elif option == "Top Providers":
        df = pd.read_sql("""
            SELECT provider_id, SUM(quantity) AS total
            FROM food
            GROUP BY provider_id
        """, conn)

    st.dataframe(df)

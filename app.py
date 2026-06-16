import streamlit as st
import pandas as pd
import sqlite3

# ---------------- DATABASE ----------------
conn = sqlite3.connect("local_food_wastage.db", check_same_thread=False)

# ---------------- LOAD CSV ----------------
def load_csv_to_db():

    providers_df = pd.read_csv("providers_data.csv")
    receivers_df = pd.read_csv("receivers_data.csv")
    food_df = pd.read_csv("food_listings_data.csv")
    claims_df = pd.read_csv("claims_data.csv")

    providers_df.to_sql(
        "providers",
        conn,
        if_exists="replace",
        index=False
    )

    receivers_df.to_sql(
        "receivers",
        conn,
        if_exists="replace",
        index=False
    )

    food_df.to_sql(
        "food",
        conn,
        if_exists="replace",
        index=False
    )

    claims_df.to_sql(
        "claims",
        conn,
        if_exists="replace",
        index=False
    )


# Load CSV into DB
load_csv_to_db()

# ---------------- UI ----------------
st.set_page_config(
    page_title="Food Wastage Management",
    layout="wide"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Providers",
        "Receivers",
        "Food",
        "Claims"
    ]
)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.title("🍲 Food Wastage Dashboard")

    p = pd.read_sql(
        "SELECT COUNT(*) total FROM providers",
        conn
    )

    r = pd.read_sql(
        "SELECT COUNT(*) total FROM receivers",
        conn
    )

    f = pd.read_sql(
        "SELECT COUNT(*) total FROM food",
        conn
    )

    c = pd.read_sql(
        "SELECT COUNT(*) total FROM claims",
        conn
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Providers", p.iloc[0, 0])
    c2.metric("Receivers", r.iloc[0, 0])
    c3.metric("Food", f.iloc[0, 0])
    c4.metric("Claims", c.iloc[0, 0])

# ---------------- PROVIDERS ----------------
elif page == "Providers":

    st.title("Providers")

    st.dataframe(
        pd.read_sql(
            "SELECT * FROM providers",
            conn
        ),
        use_container_width=True
    )

# ---------------- RECEIVERS ----------------
elif page == "Receivers":

    st.title("Receivers")

    st.dataframe(
        pd.read_sql(
            "SELECT * FROM receivers",
            conn
        ),
        use_container_width=True
    )

# ---------------- FOOD ----------------
elif page == "Food":

    st.title("Food Listings")

    st.dataframe(
        pd.read_sql(
            "SELECT * FROM food",
            conn
        ),
        use_container_width=True
    )

# ---------------- CLAIMS ----------------
elif page == "Claims":

    st.title("Claims")

    st.dataframe(
        pd.read_sql(
            "SELECT * FROM claims",
            conn
        ),
        use_container_width=True
    )

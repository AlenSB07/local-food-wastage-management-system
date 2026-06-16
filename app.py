import streamlit as st
import pandas as pd
import sqlite3

# ---------------- DATABASE ----------------
conn = sqlite3.connect("local_food_wastage.db", check_same_thread=False)

# ---------------- LOAD CSV ----------------
def load_csv():

    pd.read_csv(
        "providers_data.csv"
    ).to_sql(
        "providers",
        conn,
        if_exists="replace",
        index=False
    )

    pd.read_csv(
        "receivers_data.csv"
    ).to_sql(
        "receivers",
        conn,
        if_exists="replace",
        index=False
    )

    pd.read_csv(
        "food_listings_data.csv"
    ).to_sql(
        "food",
        conn,
        if_exists="replace",
        index=False
    )

    pd.read_csv(
        "claims_data.csv"
    ).to_sql(
        "claims",
        conn,
        if_exists="replace",
        index=False
    )


load_csv()

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Local Food Wastage Management",
    layout="wide"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Providers",
        "Receivers",
        "Claims",
        "Manage Food",
        "SQL Analysis"
    ]
)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.title("🍲 Local Food Wastage Dashboard")

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
    c3.metric("Food Listings", f.iloc[0, 0])
    c4.metric("Claims", c.iloc[0, 0])

# ---------------- PROVIDERS ----------------
elif page == "Providers":

    st.title("Providers")

    df = pd.read_sql(
        "SELECT * FROM providers",
        conn
    )

    city = st.selectbox(
        "Filter City",
        ["All"] +
        sorted(df["city"].dropna().unique())
    )

    if city != "All":
        df = df[
            df["city"] == city
        ]

    st.dataframe(
        df,
        use_container_width=True
    )

# ---------------- RECEIVERS ----------------
elif page == "Receivers":

    st.title("Receivers")

    df = pd.read_sql(
        "SELECT * FROM receivers",
        conn
    )

    city = st.selectbox(
        "Filter City",
        ["All"] +
        sorted(df["City"].dropna().unique())
    )

    if city != "All":

        df = df[
            df["City"] == city
        ]

    st.dataframe(
        df,
        use_container_width=True
    )

# ---------------- CLAIMS ----------------
elif page == "Claims":

    st.title("Claims")

    df = pd.read_sql(
        "SELECT * FROM claims",
        conn
    )

    status = st.selectbox(
        "Status",
        ["All"] +
        sorted(df["Status"].dropna().unique())
    )

    if status != "All":

        df = df[
            df["Status"] == status
        ]

    st.dataframe(
        df,
        use_container_width=True
    )

# ---------------- MANAGE FOOD ----------------
elif page == "Manage Food":

    st.title("Manage Food")

    df = pd.read_sql(
        "SELECT * FROM food",
        conn
    )

    location = st.selectbox(
        "Location",
        ["All"] +
        sorted(df["Location"].dropna().unique())
    )

    food_type = st.selectbox(
        "Food Type",
        ["All"] +
        sorted(df["Food_Type"].dropna().unique())
    )

    meal = st.selectbox(
        "Meal Type",
        ["All"] +
        sorted(df["Meal_Type"].dropna().unique())
    )

    if location != "All":
        df = df[
            df["Location"] == location
        ]

    if food_type != "All":
        df = df[
            df["Food_Type"] == food_type
        ]

    if meal != "All":
        df = df[
            df["Meal_Type"] == meal
        ]

    st.dataframe(
        df,
        use_container_width=True
    )

# ---------------- SQL ANALYSIS ----------------
elif page == "SQL Analysis":

    st.title("SQL Analysis")

    query = st.selectbox(
        "Choose Query",
        [
            "Total Food Available",
            "Top Provider",
            "Claim Status"
        ]
    )

    if query == "Total Food Available":

        sql = """
        SELECT
        SUM(Quantity)
        AS Total
        FROM food
        """

    elif query == "Top Provider":

        sql = """
        SELECT
        Provider_ID,
        SUM(Quantity)
        AS Total

        FROM food

        GROUP BY Provider_ID

        ORDER BY Total DESC
        """

    else:

        sql = """

        SELECT

        Status,

        COUNT(*)
        AS Total

        FROM claims

        GROUP BY Status

        """

    result = pd.read_sql(
        sql,
        conn
    )

    st.dataframe(
        result,
        use_container_width=True
    )

st.divider()

st.caption(
    "Developed using Streamlit + SQLite"
)

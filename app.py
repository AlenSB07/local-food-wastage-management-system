import streamlit as st
import pandas as pd
from db_connection import get_connection
conn = get_connection()
import os

if os.path.exists("local_food_wastage.db"):
    os.remove("local_food_wastage.db")
cursor.execute("CREATE TABLE IF NOT EXISTS food (...)")
cursor.execute("CREATE TABLE IF NOT EXISTS providers (...)")
cursor.execute("CREATE TABLE IF NOT EXISTS receivers (...)")
cursor.execute("CREATE TABLE IF NOT EXISTS claims (...)")


import sqlite3

conn = sqlite3.connect("local_food_wastage.db")
cursor = conn.cursor()

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
    expiry_date TEXT,
    provider_id INTEGER,
    location TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS claims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id INTEGER,
    receiver_id INTEGER,
    status TEXT,
    claim_date TEXT
)
""")

conn.commit()
conn.close()



st.set_page_config(
    page_title="Food Wastage Management",
    layout="wide"
)

conn = get_connection()

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
if page=="Dashboard":

    st.title("🍲 Local Food Wastage Management System")

    st.markdown(
    """
    Helping reduce food waste through providers and receivers.
    """
    )

    providers=pd.read_sql(
        "SELECT COUNT(*) total FROM providers",
        conn
    )

    receivers=pd.read_sql(
        "SELECT COUNT(*) total FROM receivers",
        conn
    )

    food=pd.read_sql(
        "SELECT COUNT(*) total FROM food",
        conn
    )

    claims=pd.read_sql(
        "SELECT COUNT(*) total FROM claims",
        conn
    )

    c1,c2,c3,c4=st.columns(4)

    c1.metric(
        "Providers",
        providers.iloc[0,0]
    )

    c2.metric(
        "Receivers",
        receivers.iloc[0,0]
    )

    c3.metric(
        "Food Listings",
        food.iloc[0,0]
    )

    c4.metric(
        "Claims",
        claims.iloc[0,0]
    )

    st.divider()

# ---------------- PROVIDERS ----------------

elif page=="Providers":

    st.title("Providers")

    df=pd.read_sql(
        "SELECT * FROM providers",
        conn
    )

    city=st.selectbox(
        "Filter City",
        ["All"]+
        list(df["City"].unique())
    )

    if city!="All":
        df=df[
            df["City"]==city
        ]

    st.dataframe(
        df,
        use_container_width=True
    )

# ---------------- RECEIVERS ----------------

elif page=="Receivers":

    st.title("Receivers")

    df=pd.read_sql(
        "SELECT * FROM receivers",
        conn
    )

    city=st.selectbox(
        "Filter City",
        ["All"]+
        list(df["City"].unique())
    )

    if city!="All":

        df=df[
            df["City"]==city
        ]

    st.dataframe(
        df,
        use_container_width=True
    )

# ---------------- CLAIMS ----------------

elif page=="Claims":

    st.title("Claims")

    df=pd.read_sql(
        "SELECT * FROM claims",
        conn
    )

    status=st.selectbox(
        "Status",

        ["All"]+

        list(
            df["Status"].unique()
        )
    )

    if status!="All":

        df=df[
            df["Status"]==status
        ]

    st.dataframe(
        df,
        use_container_width=True
    )
    # ---------------- MANAGE FOOD ----------------

elif page=="Manage Food":

    st.title("Manage Food Listings")

    action = st.selectbox(
        "Select Action",
        [
            "View",
            "Add"
        ]
    )

    if action=="View":

        df=pd.read_sql(
            "SELECT * FROM food",
            conn
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    elif action=="Add":

        provider=st.number_input(
            "Provider ID",
            step=1
        )

        food=st.text_input(
            "Food Name"
        )

        quantity=st.number_input(
            "Quantity",
            step=1
        )

        if st.button(
            "Add Food"
        ):

            cur=conn.cursor()

            cur.execute(
                """
                INSERT INTO food
                (Provider_ID,Food_Name,Quantity)

                VALUES
                (%s,%s,%s)
                """,

                (
                    provider,
                    food,
                    quantity
                )
            )

            conn.commit()

            st.success(
                "Food Added Successfully"
            )
            # ---------------- SQL ANALYSIS ----------------

elif page=="SQL Analysis":

    st.title("SQL Analysis")

    query = st.selectbox(

        "Choose Query",

        [

        "Total Food Available",

        "Top Provider",

        "Claim Status"

        ]

    )

    if query=="Total Food Available":

        sql="""

        SELECT

        SUM(Quantity)

        AS Total_Food

        FROM food

        """

    elif query=="Top Provider":

        sql="""

        SELECT

        Provider_ID,

        SUM(Quantity)

        Total

        FROM food

        GROUP BY Provider_ID

        ORDER BY Total DESC

        LIMIT 10

        """

    elif query=="Claim Status":

        sql="""

        SELECT

        Status,

        COUNT(*)

        Total

        FROM claims

        GROUP BY Status

        """

    df=pd.read_sql(
        sql,
        conn
    )

    st.dataframe(
        df,
        use_container_width=True
    )
st.divider()

st.caption(
"Developed using Streamlit + MySQL"
)

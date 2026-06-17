import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px


# ===============================
# CONFIG
# ===============================

st.set_page_config(
    page_title="Local Food Wastage Management",
    page_icon="🍲",
    layout="wide"
)


# ===============================
# DATABASE
# ===============================

@st.cache_resource
def get_connection():

    return sqlite3.connect(
        "local_food_wastage.db",
        check_same_thread=False
    )


conn = get_connection()


@st.cache_data
def load_data():

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


load_data()


food = pd.read_sql(
    "SELECT * FROM food",
    conn
)

claims = pd.read_sql(
    "SELECT * FROM claims",
    conn
)

providers = pd.read_sql(
    "SELECT * FROM providers",
    conn
)

receivers = pd.read_sql(
    "SELECT * FROM receivers",
    conn
)


# ===============================
# SIDEBAR
# ===============================

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


st.sidebar.title(
"🛠️ Dashboard Control Panel"
)


city = st.sidebar.multiselect(
"📍 Filter by City Location",
sorted(food["Location"].dropna().unique())
)

provider = st.sidebar.multiselect(
"🏢 Filter by Provider Type",
sorted(food["Provider_Type"].dropna().unique())
)

meal = st.sidebar.multiselect(
"⏰ Filter by Meal Time Windows",
sorted(food["Meal_Type"].dropna().unique())
)

diet = st.sidebar.multiselect(
"🥦 Filter by Dietary Food Type",
sorted(food["Food_Type"].dropna().unique())
)


filtered = food.copy()


if city:

    filtered = filtered[
        filtered["Location"].isin(city)
    ]


if provider:

    filtered = filtered[
        filtered["Provider_Type"].isin(provider)
    ]


if meal:

    filtered = filtered[
        filtered["Meal_Type"].isin(meal)
    ]


if diet:

    filtered = filtered[
        filtered["Food_Type"].isin(diet)
    ]


filtered_claims = claims.merge(

    filtered[
        ["Food_ID"]
    ],

    on="Food_ID",

    how="inner"
)


# ===============================
# DASHBOARD
# ===============================

if page == "Dashboard":


    st.title(
    "🍲 Local Food Wastage Management Dashboard"
    )

    st.caption(
    "Production Analytical Workspace"
    )


    c1,c2,c3,c4=st.columns(4)


    c1.metric(
        "📦 Total Food Items",
        filtered["Food_ID"].nunique()
    )


    c2.metric(
        "📊 Food Quantity",
        int(
            filtered["Quantity"].sum()
        )
    )


    completed = filtered_claims[
        filtered_claims[
            "Status"
        ]=="Completed"
    ]


    c3.metric(
        "✅ Completed Claims",
        len(completed)
    )


    rate=0


    if len(filtered_claims)>0:

        rate=(
            len(completed)
            /
            len(filtered_claims)
        )*100


    c4.metric(
        "📈 Success Rate",
        f"{rate:.2f}%"
    )


    st.divider()


    left,right=st.columns(2)


    with left:

        chart=(

            filtered

            .groupby(
                "Location"
            )

            [
                "Quantity"
            ]

            .sum()

            .reset_index()

        )


        fig=px.bar(

            chart,

            x="Location",

            y="Quantity",

            color="Location"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with right:


        demand=(

            filtered_claims

            .merge(
                filtered,
                on="Food_ID"
            )

            .groupby(
                "Meal_Type"
            )

            .size()

            .reset_index(
                name="Claims"
            )

        )


        fig=px.pie(

            demand,

            names="Meal_Type",

            values="Claims",

            hole=.55

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    left2,right2=st.columns(2)


    with left2:


        group=(

            filtered

            .groupby(

                [
                    "Meal_Type",

                    "Food_Type"

                ]

            )

            .size()

            .reset_index(
                name="Count"
            )

        )


        fig=px.bar(

            group,

            x="Meal_Type",

            y="Count",

            color="Food_Type",

            barmode="group"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with right2:


        status=(

            filtered_claims

            ["Status"]

            .value_counts()

            .reset_index()

        )


        status.columns=[

            "Status",

            "Count"

        ]


        fig=px.bar(

            status,

            x="Count",

            y="Status",

            orientation="h",

            color="Status"

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.subheader(
        "🔍 Search Records"
    )


    search=st.text_input(
        "Search"
    )


    table=filtered.merge(

        filtered_claims,

        on="Food_ID",

        how="left"

    )


    if search:


        table=table[

            table

            .astype(str)

            .apply(

                lambda x:

                x.str.contains(

                    search,

                    case=False

                )

            )

            .any(
                axis=1
            )

        ]


    st.dataframe(
        table,
        use_container_width=True
    )


# ===============================
# PROVIDERS
# ===============================

elif page=="Providers":

    st.title(
        "Providers"
    )

    st.dataframe(
        providers,
        use_container_width=True
    )


# ===============================
# RECEIVERS
# ===============================

elif page=="Receivers":

    st.title(
        "Receivers"
    )

    st.dataframe(
        receivers,
        use_container_width=True
    )


# ===============================
# CLAIMS
# ===============================

elif page=="Claims":

    st.title(
        "Claims"
    )

    st.dataframe(
        claims,
        use_container_width=True
    )


# ===============================
# FOOD
# ===============================

elif page=="Manage Food":

    st.title(
        "Food Listings"
    )

    st.dataframe(
        filtered,
        use_container_width=True
    )


# ===============================
# SQL
# ===============================

elif page=="SQL Analysis":

    st.title(
        "SQL Analysis"
    )


    q=st.selectbox(

        "Query",

        [

            "Total Food",

            "Top Provider"

        ]

    )


    if q=="Total Food":

        st.metric(

            "Total",

            int(

                food[
                    "Quantity"
                ].sum()

            )

        )


    else:


        r=(

            food

            .groupby(
                "Provider_ID"
            )

            [
                "Quantity"
            ]

            .sum()

            .sort_values(
                ascending=False
            )

            .head(10)

        )


        st.bar_chart(
            r
        )


st.divider()

st.caption(
"Developed using Streamlit + SQLite"
)

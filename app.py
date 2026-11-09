import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="PIGMENT | Purchase Intelligence",
    page_icon="✦",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(135deg,#0b1020 0%,#111a2e 55%,#101827 100%);
    color: #eef2ff;
}

.block-container {
    padding-top: 2rem;
    max-width: 1400px;
}

[data-testid="stSidebar"] {
    background: #0c1425;
    border-right: 1px solid #26334c;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif;
    color: #f4f7ff;
}

.hero {
    padding: 28px 32px;
    border: 1px solid #2a3955;
    border-radius: 24px;
    background: linear-gradient(
        110deg,
        rgba(48,71,111,.55),
        rgba(23,36,59,.7)
    );
    margin-bottom: 22px;
}

.eyebrow {
    color: #a5b4fc;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 11px;
    font-weight: 700;
}

.hero-title {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1.3px;
    margin: 7px 0;
    color: #fff;
}

.hero-sub {
    color: #b8c5dc;
    font-size: 14px;
}

.metric {
    background: linear-gradient(145deg,#17243a,#111c30);
    border: 1px solid #2a3a56;
    border-radius: 18px;
    padding: 18px 20px;
}

.metric-label {
    font-size: 12px;
    color: #9aabc5;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    font-family: 'Manrope';
    font-size: 27px;
    font-weight: 800;
    color: #f8fafc;
    margin-top: 5px;
}

.metric-note {
    font-size: 11px;
    color: #8ee3cf;
    margin-top: 4px;
}

.section {
    font-family: 'Manrope';
    font-weight: 700;
    font-size: 19px;
    margin: 18px 0 10px;
    color: #e8edfa;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #293954;
    border-radius: 14px;
    overflow: hidden;
}

.stSelectbox label,
.stMultiSelect label {
    color: #c6d2e5 !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- DATA LOADING ----------------
@st.cache_data
def load_data():

    data_file = (
        Path(__file__).parent
        / "data"
        / "customer_transactions.csv"
    )

    if not data_file.exists():
        st.error(
            "Dataset not found: "
            "data/customer_transactions.csv"
        )
        st.info(
            "Upload the complete data folder "
            "to your GitHub repository."
        )
        st.stop()

    data = pd.read_csv(
        data_file,
        parse_dates=["transaction_date"]
    )

    required_columns = [
        "transaction_id",
        "customer_id",
        "transaction_date",
        "product_id",
        "product_name",
        "category",
        "quantity",
        "unit_price",
        "total_amount",
        "payment_method",
        "city"
    ]

    missing = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing:
        st.error(f"Missing dataset columns: {missing}")
        st.stop()

    return data


df = load_data()


# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## ✦ PIGMENT")
st.sidebar.caption("Purchase Intelligence | Apache Pig")
st.sidebar.markdown("---")

cities = ["All"] + sorted(df["city"].dropna().unique().tolist())

city = st.sidebar.selectbox(
    "Filter by city",
    cities
)

categories = st.sidebar.multiselect(
    "Product categories",
    sorted(df["category"].dropna().unique().tolist()),
    default=sorted(df["category"].dropna().unique().tolist())
)

date_min = df["transaction_date"].min().date()
date_max = df["transaction_date"].max().date()

date_range = st.sidebar.date_input(
    "Transaction period",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max
)


# ---------------- FILTER DATA ----------------
filtered = df[
    df["category"].isin(categories)
].copy()

if city != "All":
    filtered = filtered[
        filtered["city"] == city
    ]

if isinstance(date_range, (tuple, list)):

    if len(date_range) == 2:
        start_date, end_date = date_range

        filtered = filtered[
            filtered["transaction_date"].dt.date.between(
                start_date,
                end_date
            )
        ]

    elif len(date_range) == 1:
        filtered = filtered[
            filtered["transaction_date"].dt.date == date_range[0]
        ]

else:
    filtered = filtered[
        filtered["transaction_date"].dt.date == date_range
    ]


if filtered.empty:
    st.warning(
        "No transactions found. "
        "Please change your filters."
    )
    st.stop()


# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">

    <div class="eyebrow">
        DATA SCIENCE • BIG DATA ANALYTICS
    </div>

    <div class="hero-title">
        Customer Purchase Pattern Analysis
    </div>

    <div class="hero-sub">
        Discover what customers buy, when they buy,
        and where revenue comes from — powered by
        Apache Pig analytics.
    </div>

</div>
""", unsafe_allow_html=True)


# ---------------- KPI METRICS ----------------
revenue = filtered["total_amount"].sum()

orders = filtered["transaction_id"].nunique()

customers = filtered["customer_id"].nunique()

average_order = revenue / orders if orders else 0

cols = st.columns(4)

metrics = [
    ("TOTAL REVENUE", f"₹{revenue:,.0f}", "Filtered sales"),
    ("TOTAL ORDERS", f"{orders:,}", "Unique transactions"),
    ("CUSTOMERS", f"{customers:,}", "Unique buyers"),
    ("AVERAGE ORDER", f"₹{average_order:,.0f}", "Revenue per order")
]

for col, (label, value, note) in zip(cols, metrics):

    col.markdown(
        f"""
        <div class="metric">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- REVENUE ANALYSIS ----------------
st.markdown(
    '<div class="section">Revenue & Buying Behaviour</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.35, 1])


# Monthly revenue
monthly = (
    filtered.assign(
        month=filtered["transaction_date"]
        .dt.to_period("M")
        .astype(str)
    )
    .groupby("month", as_index=False)["total_amount"]
    .sum()
)

fig1 = px.area(
    monthly,
    x="month",
    y="total_amount",
    markers=True,
    title="Monthly Revenue",
    color_discrete_sequence=["#8b9cff"]
)

fig1.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#dbe5f5",
    margin=dict(l=10, r=10, t=50, b=10),
    xaxis_title="",
    yaxis_title="Revenue (₹)"
)

fig1.update_traces(
    fill="tozeroy",
    line_width=3
)

left.plotly_chart(
    fig1,
    use_container_width=True
)


# Category revenue
category_sales = (
    filtered.groupby("category", as_index=False)
    ["total_amount"]
    .sum()
    .sort_values("total_amount", ascending=False)
)

fig2 = px.pie(
    category_sales,
    names="category",
    values="total_amount",
    hole=0.62,
    title="Revenue by Category",
    color_discrete_sequence=[
        "#8b9cff",
        "#55d6be",
        "#ffbd69",
        "#ed8ca8"
    ]
)

fig2.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#dbe5f5",
    margin=dict(l=10, r=10, t=50, b=10),
    legend_title=""
)

fig2.update_traces(
    textposition="inside",
    textinfo="percent"
)

right.plotly_chart(
    fig2,
    use_container_width=True
)


# ---------------- PRODUCT ANALYSIS ----------------
st.markdown(
    '<div class="section">Product & Customer Insights</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)


# Top products
top_products = (
    filtered.groupby("product_name", as_index=False)
    .agg(
        units=("quantity", "sum"),
        revenue=("total_amount", "sum")
    )
    .sort_values("revenue", ascending=False)
    .head(8)
)

fig3 = px.bar(
    top_products,
    x="revenue",
    y="product_name",
    orientation="h",
    title="Top Products by Revenue",
    color="revenue",
    color_continuous_scale=[
        "#34466e",
        "#8b9cff"
    ]
)

fig3.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#dbe5f5",
    margin=dict(l=10, r=10, t=50, b=10),
    xaxis_title="Revenue (₹)",
    yaxis_title="",
    coloraxis_showscale=False
)

left.plotly_chart(
    fig3,
    use_container_width=True
)


# City sales
city_sales = (
    filtered.groupby("city", as_index=False)
    ["total_amount"]
    .sum()
    .sort_values("total_amount", ascending=False)
)

fig4 = px.bar(
    city_sales,
    x="city",
    y="total_amount",
    title="Revenue by City",
    color_discrete_sequence=["#55d6be"]
)

fig4.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#dbe5f5",
    margin=dict(l=10, r=10, t=50, b=10),
    xaxis_title="",
    yaxis_title="Revenue (₹)"
)

right.plotly_chart(
    fig4,
    use_container_width=True
)


# ---------------- TRANSACTION EXPLORER ----------------
st.markdown(
    '<div class="section">Transaction Explorer</div>',
    unsafe_allow_html=True
)

search = st.text_input(
    "Search product or customer",
    placeholder="e.g. Headphones or C014"
)

view = filtered.copy()

if search:

    view = view[
        view["product_name"].str.contains(
            search,
            case=False,
            na=False
        )
        |
        view["customer_id"].str.contains(
            search,
            case=False,
            na=False
        )
    ]


st.dataframe(
    view.sort_values(
        "transaction_date",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)


# ---------------- CSV DOWNLOAD ----------------
st.download_button(
    label="↓ Download Filtered Transactions",
    data=view.to_csv(index=False).encode("utf-8"),
    file_name="filtered_transactions.csv",
    mime="text/csv"
)


# ---------------- FOOTER ----------------
st.markdown("---")

st.caption(
    "PIGMENT | Customer Purchase Intelligence "
    "| Academic Project Demo | Apache Pig + Python"
)

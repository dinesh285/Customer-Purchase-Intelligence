import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PIGMENT | Purchase Intelligence", page_icon="✦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:linear-gradient(135deg,#0b1020 0%,#111a2e 55%,#101827 100%);color:#eef2ff;}
.block-container {padding-top:2rem;max-width:1400px;}
[data-testid="stSidebar"] {background:#0c1425;border-right:1px solid #26334c;}
h1,h2,h3 {font-family:'Manrope',sans-serif;color:#f4f7ff;}
.hero {padding:28px 32px;border:1px solid #2a3955;border-radius:24px;background:linear-gradient(110deg,rgba(48,71,111,.55),rgba(23,36,59,.7));margin-bottom:22px;}
.eyebrow {color:#a5b4fc;text-transform:uppercase;letter-spacing:2px;font-size:11px;font-weight:700;}
.hero-title {font-size:34px;font-weight:800;letter-spacing:-1.3px;margin:7px 0;color:#fff;}
.hero-sub {color:#b8c5dc;font-size:14px;}
.metric {background:linear-gradient(145deg,#17243a,#111c30);border:1px solid #2a3a56;border-radius:18px;padding:18px 20px;}
.metric-label {font-size:12px;color:#9aabc5;text-transform:uppercase;letter-spacing:1px;}
.metric-value {font-family:'Manrope';font-size:27px;font-weight:800;color:#f8fafc;margin-top:5px;}
.metric-note {font-size:11px;color:#8ee3cf;margin-top:4px;}
.section {font-family:'Manrope';font-weight:700;font-size:19px;margin:18px 0 10px;color:#e8edfa;}
div[data-testid="stDataFrame"] {border:1px solid #293954;border-radius:14px;overflow:hidden;}
.stSelectbox label,.stMultiSelect label {color:#c6d2e5!important;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    d = pd.read_csv("data/customer_transactions.csv", parse_dates=["transaction_date"])
    return d

df = load_data()
st.sidebar.markdown("## ✦ PIGMENT")
st.sidebar.caption("Purchase intelligence • Apache Pig")
st.sidebar.markdown("---")
cities = ["All"] + sorted(df["city"].unique().tolist())
city = st.sidebar.selectbox("Filter by city", cities)
categories = st.sidebar.multiselect("Product categories", sorted(df["category"].unique()), default=sorted(df["category"].unique()))
date_min, date_max = df.transaction_date.min().date(), df.transaction_date.max().date()
date_range = st.sidebar.date_input("Transaction period", (date_min, date_max), min_value=date_min, max_value=date_max)
filtered = df[df.category.isin(categories)].copy()
if city != "All":
    filtered = filtered[filtered.city == city]
if isinstance(date_range, tuple) and len(date_range)==2:
    filtered = filtered[(filtered.transaction_date.dt.date >= date_range[0]) & (filtered.transaction_date.dt.date <= date_range[1])]
if filtered.empty:
    st.warning("No transactions match the selected filters. Adjust the filters in the sidebar.")
    st.stop()

st.markdown("""
<div class="hero">
  <div class="eyebrow">DATA SCIENCE • BIG DATA ANALYTICS</div>
  <div class="hero-title">Customer Purchase Pattern Analysis</div>
  <div class="hero-sub">Discover what customers buy, when they buy, and where revenue comes from — powered by an Apache Pig analytics workflow.</div>
</div>
""", unsafe_allow_html=True)

revenue = filtered.total_amount.sum()
orders = filtered.transaction_id.nunique()
customers_n = filtered.customer_id.nunique()
avg_order = revenue/orders if orders else 0
cols=st.columns(4)
metrics=[("TOTAL REVENUE",f"₹{revenue:,.0f}","Across filtered transactions"),("ORDERS",f"{orders:,}","Unique transactions"),("CUSTOMERS",f"{customers_n:,}","Unique buyers"),("AVERAGE ORDER",f"₹{avg_order:,.0f}","Revenue per transaction")]
for c,(label,value,note) in zip(cols,metrics):
    c.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',unsafe_allow_html=True)

st.markdown('<div class="section">Revenue & buying behaviour</div>',unsafe_allow_html=True)
left,right=st.columns([1.35,1])
monthly=filtered.assign(month=filtered.transaction_date.dt.to_period("M").astype(str)).groupby("month",as_index=False).total_amount.sum()
fig1=px.area(monthly,x="month",y="total_amount",markers=True,title="Monthly revenue",color_discrete_sequence=["#8b9cff"])
fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#dbe5f5",margin=dict(l=10,r=10,t=50,b=10),xaxis_title="",yaxis_title="Revenue (₹)")
fig1.update_traces(fill="tozeroy",line_width=3)
left.plotly_chart(fig1,use_container_width=True)
cat=filtered.groupby("category",as_index=False).total_amount.sum().sort_values("total_amount",ascending=False)
fig2=px.pie(cat,names="category",values="total_amount",hole=.62,title="Revenue by category",color_discrete_sequence=["#8b9cff","#55d6be","#ffbd69","#ed8ca8"])
fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="#dbe5f5",margin=dict(l=10,r=10,t=50,b=10),legend_title="")
fig2.update_traces(textposition="inside",textinfo="percent")
right.plotly_chart(fig2,use_container_width=True)

st.markdown('<div class="section">Product & customer insights</div>',unsafe_allow_html=True)
left,right=st.columns(2)
top_products=filtered.groupby("product_name",as_index=False).agg(units=("quantity","sum"),revenue=("total_amount","sum")).sort_values("revenue",ascending=False).head(8)
fig3=px.bar(top_products,x="revenue",y="product_name",orientation="h",title="Top products by revenue",color="revenue",color_continuous_scale=["#34466e","#8b9cff"])
fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#dbe5f5",margin=dict(l=10,r=10,t=50,b=10),xaxis_title="Revenue (₹)",yaxis_title="",coloraxis_showscale=False)
left.plotly_chart(fig3,use_container_width=True)
city_sales=filtered.groupby("city",as_index=False).total_amount.sum().sort_values("total_amount",ascending=False)
fig4=px.bar(city_sales,x="city",y="total_amount",title="Revenue by city",color_discrete_sequence=["#55d6be"])
fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#dbe5f5",margin=dict(l=10,r=10,t=50,b=10),xaxis_title="",yaxis_title="Revenue (₹)")
right.plotly_chart(fig4,use_container_width=True)

st.markdown('<div class="section">Transaction explorer</div>',unsafe_allow_html=True)
search=st.text_input("Search product or customer",placeholder="e.g. Headphones or C014")
view=filtered.copy()
if search:
    view=view[view.product_name.str.contains(search,case=False,na=False)|view.customer_id.str.contains(search,case=False,na=False)]
st.dataframe(view.sort_values("transaction_date",ascending=False),use_container_width=True,hide_index=True)
st.download_button("↓ Download filtered transactions",view.to_csv(index=False).encode("utf-8"),"filtered_transactions.csv","text/csv")

st.markdown("---")
st.caption("PIGMENT • Academic project demo | Sample synthetic retail data | Analytics logic is also provided as Apache Pig scripts in the /pig folder.")

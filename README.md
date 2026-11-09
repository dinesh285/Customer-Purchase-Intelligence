# Customer Purchase Pattern Analysis Using Pig

**Project UI:** PIGMENT — Purchase Intelligence Dashboard  
**Technology:** Apache Pig, Hadoop HDFS, Python, Streamlit, Pandas, Plotly

## Overview
This academic project analyses retail transaction data to identify product performance, customer spending behaviour, category revenue, monthly sales trends, and city-wise performance.

The repository contains:
- A polished interactive Streamlit dashboard.
- A sample dataset with 1,000 synthetic retail transactions.
- Apache Pig Latin scripts for product, customer, category, and city summaries.
- Setup instructions for local demo and Hadoop/Pig execution.

> Dataset note: the included transactions are synthetic sample data created for demonstration. They are not real customer records.

## Run the dashboard locally

1. Install Python 3.9 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Start the dashboard:

```bash
streamlit run app.py
```

The app opens in your browser. Use the sidebar to filter by city, category, and date range.

## Run the Apache Pig analysis

The Pig script expects the CSV at:

`/user/cloudera/purchase/input/customer_transactions.csv`

Example HDFS commands:

```bash
hdfs dfs -mkdir -p /user/cloudera/purchase/input
hdfs dfs -put -f data/customer_transactions.csv /user/cloudera/purchase/input/
pig -x mapreduce pig/purchase_analysis.pig
```

The script writes four output folders under `/user/cloudera/purchase/output/`:
- `product_summary`
- `customer_summary`
- `category_summary`
- `city_summary`

If your Hadoop username or HDFS path differs, edit the input and output paths in `pig/purchase_analysis.pig`.

## Dashboard features
- KPI cards: total revenue, orders, unique customers, average order value.
- Monthly revenue trend.
- Revenue share by category.
- Top products by revenue.
- City-wise revenue comparison.
- Searchable transaction explorer and CSV export.
- Interactive sidebar filters.

## Repository structure

```text
Customer_Purchase_Pattern_Analysis_Using_Pig/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── customer_transactions.csv
└── pig/
    └── purchase_analysis.pig
```

## Push to GitHub

Create an empty repository on GitHub, then run these commands from this folder:

```bash
git init
git add .
git commit -m "Add customer purchase pattern analysis project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your own GitHub repository URL.

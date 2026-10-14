# Bike Shop Sales Dashboard

An end-to-end e-commerce analytics project for a cycling retailer: synthetic
order data, a pandas analysis pipeline, and an interactive Streamlit dashboard.

Built to demonstrate **Python, pandas, SQL-style aggregation thinking, and
data storytelling** on a domain I know cold — I spent two years as a cycling
expert at Curated.com ($500K+ in bike sales) and have worked bike-shop retail
and e-commerce operations (Shopify, ShipStation, Zendesk, Gorgias).

## What's inside

- `data/generate_data.py` — generates 2 years of realistic synthetic orders
  (`data/orders.csv`): seasonality, growth trend, per-category pricing and
  return behavior, online vs in-store channel mix.
- `analysis/sales_analysis.py` — core KPIs, revenue by category/brand/channel,
  return-rate analysis, top products, monthly trends; prints insights and
  writes `analysis/report.md`.
- `dashboard/app.py` — interactive Streamlit + Plotly dashboard with filters,
  KPI cards, revenue trends, and return-rate breakdowns.

## Quickstart

```bash
pip install -r requirements.txt
python data/generate_data.py      # create the dataset
python analysis/sales_analysis.py # print the insights + report.md
streamlit run dashboard/app.py    # launch the dashboard
```

## Sample findings

- Apparel drives high volume but the highest return rate (~18%) — fit/sizing
  guidance is the obvious lever.
- Revenue peaks in April–June: spring inventory and staffing should be planned
  around it.
- Bikes are low-volume, high-ticket; components and accessories are the
  high-frequency repeat-purchase engine.

## Notes

All data is synthetic (seeded, reproducible). Swap in a real order export with
the same columns to run it against live data.

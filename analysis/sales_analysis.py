"""Core sales analysis for the bike shop dashboard.

Loads data/orders.csv and prints key business insights; also writes
analysis/report.md so the findings are reviewable without running code.

Run:  python analysis/sales_analysis.py
"""
from pathlib import Path
import pandas as pd

pd.set_option("display.float_format", "{:,.2f}".format)

DATA = Path(__file__).resolve().parent.parent / "data" / "orders.csv"
REPORT = Path(__file__).resolve().parent / "report.md"


def load() -> pd.DataFrame:
    df = pd.read_csv(DATA, parse_dates=["order_date"])
    df["net_revenue"] = df["revenue"] * (1 - df["returned"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    return df


def summarize(df: pd.DataFrame) -> dict:
    kept = df[df["returned"] == 0]
    return {
        "total_orders": len(df),
        "gross_revenue": df["revenue"].sum(),
        "net_revenue": df["net_revenue"].sum(),
        "return_rate": df["returned"].mean(),
        "aov": kept["revenue"].mean(),
        "revenue_by_category": df.groupby("category")["net_revenue"].sum().sort_values(ascending=False),
        "return_rate_by_category": df.groupby("category")["returned"].mean().sort_values(ascending=False),
        "revenue_by_brand": df.groupby("brand")["net_revenue"].sum().sort_values(ascending=False).head(10),
        "revenue_by_channel": df.groupby("channel")["net_revenue"].sum(),
        "monthly": df.groupby("month")["net_revenue"].sum(),
        "top_products": df.groupby("product")["net_revenue"].sum().sort_values(ascending=False).head(10),
    }


def print_report(s: dict) -> None:
    print(f"Orders:            {s['total_orders']:,}")
    print(f"Gross revenue:     ${s['gross_revenue']:,.0f}")
    print(f"Net revenue:       ${s['net_revenue']:,.0f}")
    print(f"Return rate:       {s['return_rate']:.1%}")
    print(f"Avg order value:   ${s['aov']:,.0f}")
    print("\nNet revenue by category:")
    print(s["revenue_by_category"].apply(lambda x: f"${x:,.0f}").to_string())
    print("\nReturn rate by category:")
    print(s["return_rate_by_category"].apply(lambda x: f"{x:.1%}").to_string())
    print("\nTop 10 brands by net revenue:")
    print(s["revenue_by_brand"].apply(lambda x: f"${x:,.0f}").to_string())
    print("\nNet revenue by channel:")
    print(s["revenue_by_channel"].apply(lambda x: f"${x:,.0f}").to_string())
    print("\nTop 10 products by net revenue:")
    print(s["top_products"].apply(lambda x: f"${x:,.0f}").to_string())

    # simple insights
    worst_cat = s["return_rate_by_category"].idxmax()
    best_month = s["monthly"].idxmax()
    print(f"\nINSIGHT: '{worst_cat}' has the highest return rate "
          f"({s['return_rate_by_category'].max():.1%}) — sizing/fit guidance could cut returns.")
    print(f"INSIGHT: Peak revenue month was {best_month} "
          f"(${s['monthly'].max():,.0f}) — plan spring inventory and staffing around it.")


def write_markdown(s: dict) -> None:
    lines = [
        "# Bike Shop Sales Report",
        "",
        f"- **Orders:** {s['total_orders']:,}",
        f"- **Gross revenue:** ${s['gross_revenue']:,.0f}",
        f"- **Net revenue:** ${s['net_revenue']:,.0f}",
        f"- **Return rate:** {s['return_rate']:.1%}",
        f"- **Average order value:** ${s['aov']:,.0f}",
        "",
        "## Net revenue by category",
        "",
        s["revenue_by_category"].apply(lambda x: f"${x:,.0f}").to_markdown(),
        "",
        "## Return rate by category",
        "",
        s["return_rate_by_category"].apply(lambda x: f"{x:.1%}").to_markdown(),
        "",
        "## Top 10 brands",
        "",
        s["revenue_by_brand"].apply(lambda x: f"${x:,.0f}").to_markdown(),
    ]
    REPORT.write_text("\n".join(lines))
    print(f"\nWrote {REPORT}")


def main() -> None:
    df = load()
    s = summarize(df)
    print_report(s)
    write_markdown(s)


if __name__ == "__main__":
    main()

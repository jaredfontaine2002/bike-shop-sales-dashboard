"""Generate a synthetic 2-year e-commerce dataset for a bike shop.

Produces data/orders.csv with one row per order line:
    order_id, order_date, customer_id, product, category, brand,
    quantity, unit_price, revenue, channel, returned

Run:  python data/generate_data.py
"""
import csv
import random
from datetime import date, timedelta

SEED = 42
START = date(2024, 1, 1)
DAYS = 730  # two full years
OUTFILE = "data/orders.csv"

random.seed(SEED)

CATEGORIES = {
    "Road Bikes":   {"weight": 0.12, "price": (1200, 9500), "return_p": 0.04,
                     "brands": ["Trek", "Specialized", "Cannondale", "Giant", "Cervelo"]},
    "Mountain Bikes": {"weight": 0.10, "price": (900, 8000), "return_p": 0.04,
                     "brands": ["Trek", "Specialized", "Giant", "Santa Cruz", "Yeti"]},
    "E-Bikes":      {"weight": 0.08, "price": (1800, 6000), "return_p": 0.05,
                     "brands": ["Specialized", "Trek", "Cannondale", "Aventon"]},
    "Components":   {"weight": 0.28, "price": (25, 600), "return_p": 0.07,
                     "brands": ["Shimano", "SRAM", "Campagnolo", "Wolf Tooth"]},
    "Apparel":      {"weight": 0.22, "price": (20, 350), "return_p": 0.18,
                     "brands": ["Rapha", "Castelli", "Pearl Izumi", "Gore"]},
    "Accessories":  {"weight": 0.20, "price": (10, 250), "return_p": 0.06,
                     "brands": ["Garmin", "Lezyne", "Topeak", "Knog"]},
}

MODELS = {
    "Road Bikes": ["Emonda ALR", "Tarmac SL8", "CAAD13", "Defy Advanced", "Soloist"],
    "Mountain Bikes": ["Marlin 7", "Stumpjumper", "Talon 2", "Hightower", "SB140"],
    "E-Bikes": ["Turbo Vado", "Rail 9", "Mavaro Neo", "Level 2"],
    "Components": ["105 Groupset", "Rival AXS RD", "XT Cassette", "Dropper Post", "Carbon Wheelset"],
    "Apparel": ["Pro Jersey", "Bib Shorts", "Winter Jacket", "Gloves", "Helmet"],
    "Accessories": ["Edge 540", "Floor Pump", "Saddle Bag", "Front Light", "Multitool"],
}


def seasonal_factor(day: date) -> float:
    """Cycling retail seasonality: spring peak, winter trough."""
    m = day.month
    return {1: 0.75, 2: 0.80, 3: 1.10, 4: 1.35, 5: 1.40, 6: 1.30,
            7: 1.15, 8: 1.05, 9: 1.00, 10: 0.95, 11: 0.85, 12: 0.90}[m]


def pick_category() -> str:
    r = random.random()
    cum = 0.0
    for cat, spec in CATEGORIES.items():
        cum += spec["weight"]
        if r < cum:
            return cat
    return "Accessories"


def main() -> None:
    rows = []
    order_id = 100000
    customer_ids = list(range(1, 4001))

    for i in range(DAYS):
        day = START + timedelta(days=i)
        # gentle growth trend + seasonality + noise
        lam = 14 * (1 + 0.0009 * i) * seasonal_factor(day)
        n_orders = max(0, int(random.gauss(lam, lam ** 0.5)))
        for _ in range(n_orders):
            order_id += 1
            cat = pick_category()
            spec = CATEGORIES[cat]
            brand = random.choice(spec["brands"])
            product = f"{brand} {random.choice(MODELS[cat])}"
            qty = 1 if random.random() < 0.92 else 2
            unit_price = round(random.uniform(*spec["price"]), 2)
            channel = "Online" if random.random() < 0.62 else "In-Store"
            returned = random.random() < spec["return_p"]
            rows.append([order_id, day.isoformat(), random.choice(customer_ids),
                         product, cat, brand, qty, unit_price,
                         round(qty * unit_price, 2), channel, int(returned)])

    with open(OUTFILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["order_id", "order_date", "customer_id", "product", "category",
                    "brand", "quantity", "unit_price", "revenue", "channel", "returned"])
        w.writerows(rows)

    print(f"Wrote {len(rows):,} orders to {OUTFILE}")


if __name__ == "__main__":
    main()

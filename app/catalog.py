import csv
from pathlib import Path

PRODUCTS_CSV = Path("data/products.csv")


class Catalog:
    def __init__(self):
        self.products = self._load_products()

    def _load_products(self):
        items = []
        with open(PRODUCTS_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["business_id"] = int(row["business_id"])
                row["price"] = float(row["price"])
                row["in_stock"] = int(row["in_stock"])
                items.append(row)
        return items
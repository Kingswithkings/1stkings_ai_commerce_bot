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

    def list_categories(self, business_id: int):
        return sorted({
            p["category"]
            for p in self.products
            if p["business_id"] == business_id and p["in_stock"] == 1
        })

    def products_by_category(self, business_id: int, category: str):
        category = category.strip().lower()
        return [
            p for p in self.products
            if p["business_id"] == business_id
            and p["in_stock"] == 1
            and p["category"].lower() == category
        ]

    def search(self, business_id: int, text: str):
        text = (text or "").strip().lower()
        matches = []

        for p in self.products:
            if p["business_id"] != business_id or p["in_stock"] != 1:
                continue

            haystack = " ".join([
                p["sku"], p["name"], p["aliases"], p["category"]
            ]).lower()

            score = 0
            if text == p["name"].lower():
                score += 5
            if text in p["name"].lower():
                score += 4
            if text in p["aliases"].lower():
                score += 4
            if text in p["category"].lower():
                score += 2
            if text in haystack:
                score += 1

            if score > 0:
                matches.append((score, p))

        matches.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in matches[:10]]

    def best_match(self, business_id: int, text: str):
        results = self.search(business_id, text)
        return results[0] if results else None
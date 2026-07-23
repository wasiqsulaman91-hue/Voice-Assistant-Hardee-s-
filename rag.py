import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_MENU_PATH = os.path.join(_BASE_DIR, "Resturant", "menu.json")

with open(_MENU_PATH, "r", encoding="utf-8") as f:
    _data = json.load(f)

_currency = _data.get("currency", "")


def _format_price(item: dict) -> str:
    if "price" in item:
        return f"{item['price']} {_currency}"

    sizes = item.get("sizes")
    if sizes and isinstance(sizes[0], dict):
        parts = [f"{s['size']}: {s['price']} {_currency}" for s in sizes]
        return ", ".join(parts)

    return "price not available"


def _flatten_menu(data: dict) -> list[dict]:
    flat_items = []

    for category in data.get("categories", []):
        category_name = category.get("name", "")
        for item in category.get("items", []):
            description = item.get("description", "")
            includes = item.get("includes")
            if includes:
                description = "Includes: " + ", ".join(includes)

            flat_items.append({
                "id": item.get("id", ""),
                "name": item.get("name", ""),
                "description": description,
                "category": category_name,
                "price_text": _format_price(item),
            })

    for extra in data.get("extras", []):
        flat_items.append({
            "id": extra.get("name", ""),
            "name": extra.get("name", ""),
            "description": "Add-on / extra",
            "category": "Extras",
            "price_text": f"{extra.get('price', '')} {_currency}",
        })

    return flat_items


_menu = _flatten_menu(_data)

_menu_texts = [
    f"{item['name']} ({item['category']}): {item['description']}"
    for item in _menu
]

_menu_embeddings = _model.encode(_menu_texts, normalize_embeddings=True)


def search_menu_items(query: str, top_k: int = 3):
    query_embedding = _model.encode([query], normalize_embeddings=True)[0]
    scores = np.dot(_menu_embeddings, query_embedding)
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for i in top_indices:
        item = _menu[i]
        results.append({
            "name": item["name"],
            "description": item["description"],
            "category": item["category"],
            "price_text": item["price_text"],
            "score": float(scores[i]),
        })
    return results


def find_menu_item(name: str):
    """Find an exact-ish menu item by name for order placement."""
    name_lower = name.lower().strip()
    for item in _menu:
        if item["name"].lower() == name_lower:
            return item
    for item in _menu:
        if name_lower in item["name"].lower():
            return item
    return None
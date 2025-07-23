import requests
from config import LAZADA_API_KEY, LAZADA_API_HOST

def search_lazada_products(query):
    url = f"https://{LAZADA_API_HOST}/lazada/search/items"
    headers = {
        "X-RapidAPI-Key": LAZADA_API_KEY,
        "X-RapidAPI-Host": LAZADA_API_HOST
    }
    params = {
        "keywords": query,
        "site": "my",  # Malaysia site
        "page": 1,
        "sort": "pop",  # Sort by popularity
        "limit": 2      # Limit to 2 results
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": "Request failed", "details": str(e)}

    try:
        data = response.json()

        if "data" not in data or "items" not in data["data"]:
            return {"error": "Unexpected API structure", "raw": data}

        items = data["data"]["items"]
        if not items:
            return {"message": "No results found."}

        results = ["🛍️ *Top Lazada Search Results:*"]
        for i, item in enumerate(items, 1):
            title = item.get("title", "No title")
            price = item.get("price", "N/A")
            original_price = item.get("original_price")
            image = item.get("image")
            link = item.get("link", "#")
            shop = item.get("shop_name", "Unknown Shop")
            location = item.get("location", "Unknown Location")

            price_info = f"RM{price}"
            if original_price and original_price != price:
                price_info += f" (was RM{original_price})"

            results.append(
                f"""\n🔹 *{i}. {title}*\n💰 {price_info}\n🏪 {shop} - {location}\n🔗 [View Product]({link})"""
            )

        return {"response": "\n".join(results)}

    except ValueError:
        return {"error": "Invalid JSON response", "raw": response.text}

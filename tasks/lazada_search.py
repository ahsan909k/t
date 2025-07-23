from services.lazada_api import search_lazada_products

def search_lazada_task(params):
    query = params.get("query")
    if not query:
        return {"error": "Missing search query."}

    results = search_lazada_products(query)
    if "error" in results:
        return results

    # The API already returns formatted results
    if "results" in results:
        return results
    
    return {"message": "No products found."}

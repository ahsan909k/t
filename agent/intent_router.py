from tasks.lazada_search import search_lazada_task
from services.lazada_api import search_lazada_products

def parse_intent(message):
    message = message.lower()

    if "lazada" in message and "search" in message:
        return "search_lazada", extract_query(message)

    return None, {}

def extract_query(message):
    # crude method: get text after "search" or "for"
    tokens = message.split()
    if "search" in tokens:
        idx = tokens.index("search")
        query = " ".join(tokens[idx+1:])
    elif "for" in tokens:
        idx = tokens.index("for")
        query = " ".join(tokens[idx+1:])
    else:
        query = message
    return {"query": query.strip()}

def handle_message(message):
    # First check if it's a direct search request
    search_terms = ["show me", "find", "search for", "look for"]
    message_lower = message.lower()
    
    # Extract search query from direct requests
    search_query = None
    for term in search_terms:
        if term in message_lower:
            # Get the text after the search term
            parts = message_lower.split(term, 1)
            if len(parts) > 1:
                search_query = parts[1].strip()
                break
    
    # If no direct search term found, try to extract product type
    if not search_query:
        # Check for common product types
        product_types = ["laptop", "phone", "headphone", "camera", "tablet"]
        for product in product_types:
            if product in message_lower:
                search_query = product
                break
    
    # If we have a search query, perform the search
    if search_query:
        print(f"Searching for: {search_query}")
        results = search_lazada_products(search_query)
        
        # Check if we have a direct response from the API
        if results and "response" in results:
            return {"response": results["response"]}
            
        # Extract URLs and titles (fallback to previous behavior)
        if results and "results" in results:
            products = results["results"]
            if products:
                response = f"Here are some {search_query} products I found:\n\n"
                for i, item in enumerate(products):
                    title = item.get("title", "Product")
                    url = item.get("url", "#")
                    # Format with markdown for clickable links
                    response += f"{i+1}. [{title}]({url})\n\n"
                return {"response": response}
        
        return {"response": f"Sorry, I couldn't find any {search_query} products right now."}
    
    # Check for intent using the existing parser
    intent, params = parse_intent(message)
    
    if intent == "search_lazada":
        query = params.get("query")
        results = search_lazada_products(query)
        
        # Check if we have a direct response from the API
        if results and "response" in results:
            return {"response": results["response"]}
            
        # Extract URLs only (fallback to previous behavior)
        if results and "results" in results:
            products = results["results"]
            if products:
                response = f"Here are some {query} products I found:\n\n"
                for i, item in enumerate(products):
                    title = item.get("title", "Product")
                    url = item.get("url", "#")
                    # Format with markdown for clickable links
                    response += f"{i+1}. [{title}]({url})\n\n"
                return {"response": response}
        
        return {"response": f"Sorry, I couldn't find any {query} products right now."}
    
    # Default response
    return {"response": "I can help you search for products! Just tell me what you're looking for."}
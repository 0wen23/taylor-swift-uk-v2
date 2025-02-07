#products t swift uk


import requests # For making HTTP requests
import json     # For parsing JSON responses

# List of collection URLs to scrape
collection_urls = [
    "https://storeuk.taylorswift.com/collections/all-merch/products.json", # All merch
    "https://storeuk.taylorswift.com/collections/taylor-swift-the-eras-tour-collection/products.json", # The Eras Tour Collection
    "https://storeuk.taylorswift.com/products.json", #home page
    # Add more collection URLs here
]

# File to store product data
products_file = "taylor_swiftuk_products.json"

def fetch_all_products(url): #fetches all products from a collection URL
    """Fetch all products from a collection URL, handling pagination."""
    products = [] #list to store products
    page = 1 #start with page 1
    while True:  
        # Fetch the next page of products
        response = requests.get(f"{url}?page={page}")
        
        if response.status_code != 200:  #if the response is not successful
            print(f"Failed to fetch products from {url} on page {page}.")  #print error message
            break  #exit the loop

        # Parse the products from the response 
        new_products = response.json().get("products", [])  #get the products from the response
        if not new_products:  #if there are no new products
            break  # No more products

        # Add the new products to the list
        products.extend(new_products)  
        print(f"Fetched {len(new_products)} products from {url} (page {page}).")  #print the number of products fetched

        # Move to the next page
        page += 1  

    return products  #return the list of products

def parse_product(product):  #parses a product and extracts relevant details
    """Extract relevant details from a product."""  #function description
    name = product.get("title")  #get the product title
    handle = product.get("handle") #get the product handle
    link = f"https://storeuk.taylorswift.com/products/{handle}" #generate the product link
    image = product.get("images")[0].get("src") if product.get("images") else None #get the product image
    variants = product.get("variants", []) #get the product variants
    size_variants = {variant.get("option1"): variant.get("id") for variant in variants if variant.get("option1")} #get the size variants
    in_stock = any(variant.get("available") for variant in variants) #check if any variant is in stock

    return { #return the product details
        "id": product.get("id"),
        "name": name,
        "size_variants": size_variants,  # Dictionary of sizes and their variant IDs
        "in_stock": in_stock,
        "link": link,
        "image": image,
        "variants": variants  # Include the full variants data
    }

def save_products(products): #saves products to a JSON file
    """Save products, ensuring no duplicates by ID.""" 
    unique_products = {} #dictionary to store unique products by ID
    for product in products: #for each product
        product_id = product["id"] #get the product ID
        if product_id not in unique_products: #if the product ID is not already in the dictionary
            unique_products[product_id] = product #add the product to the dictionary
    with open(products_file, "w") as file: #open the file for writing 
        json.dump(list(unique_products.values()), file, indent=4) #write the products to the file in JSON format

def main(): #fetches all products from multiple collections and saves them to a JSON file
    """Fetch all products from multiple collections and save them to a JSON file."""
    all_products = []  #list to store
    for url in collection_urls:  #for each collection URL
        print(f"Fetching products from {url}...")  #print the URL
        products = fetch_all_products(url) #fetch all products from the URL
        all_products.extend(products) #add the products to the list
    
    parsed_products = [parse_product(product) for product in all_products] #parse the products
    save_products(parsed_products)  #save the products to the JSON file

if __name__ == "__main__":
    main()

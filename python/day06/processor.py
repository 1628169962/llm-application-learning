
def process_products(products,min_rating = 4.5,min_stock = 10):
    if products is None:
        return None
    lis =[]
    for product in products.get("products",[]):
        clean_products={}
        rating = float(product["rating"])
        stock = int(product["stock"])
        if rating >= min_rating and stock >= min_stock:
            clean_products["title"] = product["title"].strip()
            clean_products["price"] = float(product["price"])
            clean_products["rating"] =rating
            clean_products["stock"] = stock
            lis.append(clean_products)
    lis = sorted(lis,key=lambda x:x["rating"],reverse=True)
    return lis

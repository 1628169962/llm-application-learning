from api_client import APIClient
from processor import process_products

def main():
    client = APIClient("https://dummyjson.com/products")
    products = client.get_products()
    lis = process_products(products)
    print(lis)

if __name__ == "__main__":
    main()
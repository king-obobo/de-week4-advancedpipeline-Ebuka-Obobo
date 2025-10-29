from pipeline.api_client import APIClient
from pprint import pprint


if __name__ == "__main__":
    api_client = APIClient()
    all_products = api_client.get_all_products()
    # pprint(all_products)
    all_users = api_client.get_all_users()
    # pprint(all_users)
    
    pass

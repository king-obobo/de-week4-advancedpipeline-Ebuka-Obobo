from pipeline.api_client import APIClient
from pprint import pprint
from pipeline.data_enricher import DataEnricher


if __name__ == "__main__":
    api_client = APIClient()
    all_products = api_client.get_all_products()
    # pprint(all_products[:2])
    all_users = api_client.get_all_users()
    # pprint(all_users[:2])
    
    enricher = DataEnricher(all_products, all_users)
    df = enricher.enrich_data()
    pprint(df.head())
    pass

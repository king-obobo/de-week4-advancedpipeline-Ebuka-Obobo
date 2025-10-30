from pipeline.api_client import APIClient
from pprint import pprint
from pipeline.data_enricher import DataEnricher
from pipeline.data_analyzer import Analyzer


if __name__ == "__main__":
    api_client = APIClient()
    all_products = api_client.get_all_products()
    # pprint(all_products[:2])
    all_users = api_client.get_all_users()
    # pprint(all_users[:2])
    
    enricher = DataEnricher(all_products, all_users)
    df = enricher.enrich_data()
    # pprint(df.head())
    
    df_analyzer = Analyzer(df) 
    analysis = df_analyzer.perform_analysis()
    
    pprint(analysis)
    
    #Run analysis
    pass

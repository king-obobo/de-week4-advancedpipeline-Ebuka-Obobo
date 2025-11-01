from .api_client import APIClient
from .data_enricher import DataEnricher
from .data_analyzer import Analyzer
from .exporter import Exporter
from .logging_config import setup_logger



logger = setup_logger(__name__)


class Pipeline:
    
    def run(self):
        try:
            api_client = APIClient()
            all_products = api_client.get_all_products()
            all_users = api_client.get_all_users()

            # Let us enrich tghe data
            enricher = DataEnricher(all_products, all_users)
            df = enricher.enrich_data()

            # Let us run the analysis
            df_analyzer = Analyzer(df) 
            analysis = df_analyzer.perform_analysis()
            
            # We export and save
            my_exporter = Exporter(analysis)
            my_exporter.export_to_json()
            
        except Exception as e:
            logger.exception(f"An error occured: {e}")
            # print(f"An error occured: {e}")
        
        

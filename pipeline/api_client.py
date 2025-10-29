from config import ConfigManager


class APIClient:
    CONFIG_FILE = "pipeline.cfg"
    CONFIGMANAGER = ConfigManager(CONFIG_FILE)
    
    def __init__(self):
        self.base_url = APIClient.CONFIGMANAGER.get("API", "base_url")
        self.limit = int(APIClient.CONFIGMANAGER.get("PAGINATION", "limit"))
    
        
    @property    
    def get_config_settings(self):
        return APIClient.CONFIGMANAGER.settings()
        
        
api_object = APIClient()
print(api_object.get_config_settings)
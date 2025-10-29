from pipeline.config import ConfigManager


if __name__ == "__main__":
    # fake_file = "unknownfile.ini"
    file = "pipeline.cfg"
    config = ConfigManager(file)
    
    base_url = config.get("API", "base_url")
    limit = config.get("PAGINATION", "limit")
    
    print(base_url, limit)

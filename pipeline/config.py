from configparser import ConfigParser


class ConfigManager(ConfigParser):
    "A simple ConfigManager class to read my configuration file and provide easy access to the settings"
    
    def __init__(self, file_path:str) -> None:
        super().__init__()
        self.config_file = file_path
        self.read(file_path)
        
        
    def settings(self, section : str = None) -> dict:
        if section:
            if self.has_section(section):
                return dict(self[section])
            else:
                raise ValueError("f Section '{section}' not found in config file")
        else:
            return {sec: dict(self[sec]) for sec in self.sections()}
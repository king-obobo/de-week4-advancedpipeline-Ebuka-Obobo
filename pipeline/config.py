from configparser import ConfigParser
from pathlib import Path

class ConfigManager(ConfigParser):
    "A simple ConfigManager class to read my configuration file and provide easy access to the settings"
    
    def __init__(self, file_path:str) -> None:
        super().__init__()
        self.config_file = self._validate_file_path(file_path)
        self.read(self.config_file)
        
    
    def _validate_file_path(self, path:str) -> Path | None:
        """
        A helper function to validate that file infact exists
        Args:
            path (str): A path to the file containing

        Raises:
            FileNotFoundError: This is raised if the path does not exists

        Returns: A valdi path or None
            : 
        """
        path_obj = Path(path)
        if not path_obj.exists():
            raise FileNotFoundError(f"The Path to the file does not exist")
        return path_obj

    def settings(self, section : str = None) -> dict:
        if section:
            if self.has_section(section):
                return dict(self[section])
            else:
                raise ValueError(f"Section '{section}' not found in config file")
        else:
            return {sec: dict(self[sec]) for sec in self.sections()}
        
# manager = ConfigManager("pipeline.cfg")
# print(manager.settings())
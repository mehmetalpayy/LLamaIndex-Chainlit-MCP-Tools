import logging
import os
from datetime import datetime
from abc import ABC, abstractmethod


class BaseLogger(ABC):
    def __init__(self):
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        logger = logging.getLogger(self._get_logger_name())
        logger.setLevel(logging.INFO)
        
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        file_handler = logging.FileHandler(
            f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    @abstractmethod
    def _get_logger_name(self) -> str:
        pass
    
    @abstractmethod
    def info(self, message: str):
        pass
    
    @abstractmethod
    def error(self, message: str, exc_info=None):
        pass
    
    @abstractmethod
    def warning(self, message: str):
        pass
    
    @abstractmethod
    def debug(self, message: str):
        pass
    
    @abstractmethod
    def success(self, message: str):
        pass
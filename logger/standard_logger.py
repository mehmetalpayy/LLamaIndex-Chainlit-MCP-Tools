from .base import BaseLogger


class Logger(BaseLogger):
    def _get_logger_name(self) -> str:
        return 'standard_logger'
    
    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str, exc_info=None):
        self.logger.error(message, exc_info=exc_info)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def success(self, message: str):
        self.logger.info(f"SUCCESS: {message}")


standard_logger = Logger()
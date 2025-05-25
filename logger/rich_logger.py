from rich.console import Console
from rich.theme import Theme
from datetime import datetime


class RichLogger:
    def __init__(self):
        self.theme = Theme({
            "info": "cyan",
            "warning": "yellow",
            "error": "bold red",
            "debug": "dim cyan",
            "success": "bold green"
        })
        self.console = Console(theme=self.theme)
    
    def info(self, message: str):
        self.console.print(f"[info]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - INFO: {message}[/info]")
    
    def error(self, message: str, exc_info=None):
        self.console.print(f"[error]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERROR: {message}[/error]")
        if exc_info:
            self.console.print_exception()
    
    def warning(self, message: str):
        self.console.print(f"[warning]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - WARNING: {message}[/warning]")
    
    def debug(self, message: str):
        self.console.print(f"[debug]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - DEBUG: {message}[/debug]")
    
    def success(self, message: str):
        self.console.print(f"[success]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - SUCCESS: {message}[/success]")


rich_logger = RichLogger()
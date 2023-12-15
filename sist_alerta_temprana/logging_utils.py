import logging
from datetime import datetime, timedelta
import os

def setup_logging(log_level=logging.INFO):
    """
    Set up basic logging configuration.

    Parameters:
    - log_filename (str): The name of the file to log messages to.
    - log_level: The root logger level (default is logging.INFO).
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_filename_today = f"log_{current_date}.log"
    log_filename_yesterday = f"log_{(datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')}.log"
    
    if os.path.exists(log_filename_yesterday):
        os.remove(log_filename_yesterday)
        
    # Set up the basic configuration
    logging.basicConfig(filename=log_filename_today,
                        level=log_level,
                        format='%(asctime)s - %(levelname)s - %(message)s')
import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')
else:
    # Delete all files in the logs directory
    for filename in os.listdir('logs'):
        file_path = os.path.join('logs', filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)

# Generate a unique log file name based on the current date and time
log_filename = datetime.now().strftime('logs/log_%Y%m%d_%H%M%S.log')

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
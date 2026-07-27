"""
Logging Module
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("Gold Intelligence")


from modules.logger import logger

logger.info("Fetching gold rates...")
logger.warning("Duplicate prices detected.")
logger.error("API unavailable.")

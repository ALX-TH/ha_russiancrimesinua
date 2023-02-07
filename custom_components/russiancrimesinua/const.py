"""Constants for blueprint."""
from typing import Final

DOMAIN = "russiancrimesinua"
DOMAIN_DATA = f"{DOMAIN}_data"
ATTRIBUTION = "Losses of the Russian army in Ukraine"
ATTR_IMG_UA = "img_ua"
ATTR_IMG_EN = "img_en"

INTEGRATION_VERSION = "main"
PLATFORMS = ["sensor"]
REQUIRED_FILES = [
    ".translations/en.json",
    ".translations/ua.json",
    "api.py",
    "const.py",
    "manifest.json",
]
ISSUE_URL = "https://github.com/ALX-TH/ha_russiancrimesinua/issues"
OFFICIAL_SITE_ROOT = "https://www.russiancrimes.in.ua"
UPDATE_INTERVAL = 1

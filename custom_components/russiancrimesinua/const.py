"""Constants for blueprint."""

DOMAIN = "russiancrimesinua"
DOMAIN_DATA = f"{DOMAIN}_data"
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


# Client IDs
GOOGLE_ID = "google"
GEMINI_FLASH_ID = "gemini-1.5-flash"
GEMINI_PRO_ID = "gemini-1.5-pro"

ALIAS_TO_CLIENT = {
    "gemini": GEMINI_FLASH_ID,
    "g-flash": GEMINI_FLASH_ID,
    "gemini-flash": GEMINI_FLASH_ID,
    "g-pro": GEMINI_PRO_ID,
    "gemini-pro": GEMINI_PRO_ID,
    "google": GOOGLE_ID,
    "web": GOOGLE_ID
}

# Client TYPES
TYPE_GEMINI = "gemini"
TYPE_GOOGLE = "google"

CLIENT_ID_TO_TYPE = {
    GEMINI_PRO_ID: TYPE_GEMINI,
    GEMINI_FLASH_ID: TYPE_GEMINI,
    GOOGLE_ID: TYPE_GOOGLE
}




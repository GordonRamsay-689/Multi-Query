
GREEN = 34
RED = 52
DRED = 1
LRED = 196

CONFIG_FILENAME = "config.env"

# Valid Commands
VALID_COMMANDS = ["-c", "-setup", "-help"]

# Client IDs
GOOGLE_ID = "google"
GEMINI_FLASH_ID = "gemini-1.5-flash"
GEMINI_PRO_ID = "gemini-1.5-pro"

# Client Aliases
ALIAS_TO_CLIENT = {
    "gemini": GEMINI_FLASH_ID,
    "gflash": GEMINI_FLASH_ID,
    "gpro": GEMINI_PRO_ID,
    "google": GOOGLE_ID,
}

# Client TYPES
TYPE_GEMINI = "gemini"
TYPE_GOOGLE = "google"

TYPES = [TYPE_GEMINI, TYPE_GOOGLE]
REQUIRES_KEY = [TYPE_GEMINI]

CLIENT_ID_TO_TYPE = {
    GEMINI_PRO_ID: TYPE_GEMINI,
    GEMINI_FLASH_ID: TYPE_GEMINI,
    GOOGLE_ID: TYPE_GOOGLE
}

# OUTPUT STRINGS (instructions, warnings, information..)

CLI_EXAMPLE_USAGE = f'''\
Example Usage: 
msearch "query" -command client

For more details:
msearch -help'''

CLI_HELP = f'''\
This information is only relevant for running the script with arguments.

All args are optional, and except for the query (which must come first
if included) are not positional.

To update API keys run:
msearch -setup

- Doublequotes signify a query. If you wish to include doubleqoutes
in your query remember to escape them with '\\'. If the query starts
with '-' then you must escape that too. If no query is included it 
will be assumed that you wish to start a persistent chat with selected
clients.

- To select a specific client use any of the following aliases:

    ALIAS - CLIENT
    {ALIAS_TO_CLIENT}

If no client is provided the script will default to gemini-flash-1.5
    
- Commands are prepended with '-'

Some valid commands are:
    'c' // Starts a persistent chat session with all clients.
    'setup' // Update api keys.

msearch is a suggested enviroment alias, replace with python3 master.py
if running directly from script directory.
'''

ERROR_SCRIPT_DIR = "Failed to get script directory."

SCRIPT_NAME = "MSearch"
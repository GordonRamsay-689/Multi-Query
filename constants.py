
GREEN = 34
LBLUE = 26
RED = 52
DRED = 1
LRED = 196

TIMEOUT = 45

# Valid Commands
VALID_COMMANDS = ["-c", "-help", "-aliases", "-s"] 

# Client IDs
GOOGLE_ID = "google"
GEMINI_FLASH_ID = "gemini-1.5-flash"
GEMINI_PRO_ID = "gemini-1.5-pro"
GPT_3_5_TURBO_ID = "gpt-3.5-turbo"
GPT_4_ID = "gpt-4"
GPT_4_TURBO_ID = "gpt-4-turbo"
GPT_4O_ID = "gpt-4o"
GPT_4O_MINI_ID = "gpt-4o-mini"
O1_PREVIEW_ID = "o1-preview"
O1_MINI_ID = "o1-mini"
TEST_ID = "test-client"

# Client Aliases
ALIAS_TO_CLIENT = {
    GEMINI_FLASH_ID: GEMINI_FLASH_ID,
    "gemini": GEMINI_FLASH_ID,
    "gflash": GEMINI_FLASH_ID,
    GEMINI_PRO_ID: GEMINI_PRO_ID,
    "gpro": GEMINI_PRO_ID,
    GOOGLE_ID: GOOGLE_ID,
    "google": GOOGLE_ID,
    GPT_3_5_TURBO_ID: GPT_3_5_TURBO_ID,
    "turbo3.5": GPT_3_5_TURBO_ID,
    GPT_4_ID: GPT_4_ID,
    "gpt4": GPT_4_ID,
    GPT_4_TURBO_ID: GPT_4_TURBO_ID,
    "turbo": GPT_4_TURBO_ID,
    GPT_4O_ID: GPT_4O_ID,
    "gpt4o": GPT_4O_ID,
    "4o": GPT_4O_ID,
    GPT_4O_MINI_ID: GPT_4O_MINI_ID,
    "mini": GPT_4O_MINI_ID,
    O1_PREVIEW_ID: O1_PREVIEW_ID,
    "o1p": O1_PREVIEW_ID,
    "o1preview": O1_PREVIEW_ID,
    O1_MINI_ID: O1_MINI_ID,
    "o1m": O1_MINI_ID,
    "o1mini": O1_MINI_ID,
    TEST_ID: TEST_ID
}

# Client TYPES
TYPE_GEMINI = "type_gemini"
TYPE_GOOGLE = "type_google"
TYPE_OPENAI = "type_openai"
TYPE_TEST = "type_test"

TYPES = [TYPE_GEMINI, TYPE_GOOGLE, TYPE_OPENAI]

STREAM_SUPPORT = [TYPE_GEMINI]

CLIENT_ID_TO_TYPE = {
    GEMINI_PRO_ID: TYPE_GEMINI,
    GEMINI_FLASH_ID: TYPE_GEMINI,
    GOOGLE_ID: TYPE_GOOGLE,
    GPT_3_5_TURBO_ID: TYPE_OPENAI,
    GPT_4_ID: TYPE_OPENAI,
    GPT_4_TURBO_ID: TYPE_OPENAI,
    GPT_4O_ID: TYPE_OPENAI,
    GPT_4O_MINI_ID: TYPE_OPENAI,
    O1_PREVIEW_ID: TYPE_OPENAI,
    O1_MINI_ID: TYPE_OPENAI,
    TEST_ID: TYPE_TEST
}

DEFAULT_SYS_MSG = {"role": "system", "content": "You are efficient, to the point and helpful"}

# OUTPUT STRINGS (instructions, warnings, information..)

CLI_EXAMPLE_USAGE = f'''\
Example Usage: 
msearch "query" -command client

For more details:
msearch -help'''

CLI_HELP = f'''\
Set enviroment variables in bash, sh or zsh with the following command:

    export GEMINI_API=YOUR_KEY

Replacing YOUR_KEY with your Gemini API Key.

All args are optional, and except for the query (which must come first
if included) are not positional.

- Doublequotes signify a query. If you wish to include doubleqoutes
in your query remember to escape them with '\\'. If the query starts
with '-' then you must escape that too. If no query is included it 
will be assumed that you wish to start a persistent chat with selected
clients.

- To select a specific client use it's name or an alias as an argument.
For a full list of aliases use the command '-aliases'.

If no client is provided the script will default to gemini-flash-1.5
    
- Commands are prepended with '-'

Some valid commands are:
    'c' // Starts a persistent chat session with all clients.
    'setup' // Update api keys.
    'aliases' // Full list of aliases

msearch is a suggested enviroment alias, replace with python3 master.py
if running directly from script directory.
'''

ERROR_SCRIPT_DIR = "Failed to get script directory."

SCRIPT_NAME = "msearch"

TEST_RESPONSE = "This is a test response for TestClient.\n\
This is line 2 of the test response\n\
This is line 3 of the test response"
MODELS_CACHE_FILE = "models.json"

TIMEOUT = 45

SCRIPT_NAME = "search"

# 256-Color Codes
GREEN = 34
LBLUE = 26
RED = 52
DRED = 1
LRED = 196
YELLOW = 11

# Commands
CHAT_COMMAND = '-c'
HELP_COMMAND = '-help'
ALIASES_COMMAND = '-models'
STREAM_COMMAND = '-s'
SYS_COMMAND = '-sys'
NOFORMAT_COMMAND = '-noformat'
VALID_COMMANDS = [CHAT_COMMAND, HELP_COMMAND, ALIASES_COMMAND, STREAM_COMMAND, SYS_COMMAND, NOFORMAT_COMMAND] 

# Flags (during runtime, not args)
# Flags include ':' to avoid conflating with flags the user may search for
ADD_FLAG = '--add:'
REMOVE_FLAG = '--rm:'
STREAM_FLAG = '--stream:'
DISPLAY_FLAG = '--aliases:'
SYSMSG_FLAG = '--sys:'
CLEAR_FLAG = '--clear:'
FORMAT_FLAG = '--format:'
VALID_FLAGS = [ADD_FLAG, REMOVE_FLAG, STREAM_FLAG, DISPLAY_FLAG, SYSMSG_FLAG, CLEAR_FLAG, FORMAT_FLAG] 
TOGGLEABLE_FLAGS = [DISPLAY_FLAG, CLEAR_FLAG, FORMAT_FLAG]

# Client IDs
GEMINI_FLASH_ID = "gemini-1.5-flash"
TEST_ID = "test-client"

DEFAULT_MODEL = GEMINI_FLASH_ID

# Client TYPES
TYPE_GEMINI = "type_gemini"
TYPE_GOOGLE = "type_google"
TYPE_OPENAI = "type_openai"
TYPE_DEEPSEEK = "type_deepseek"
TYPE_TEST = "type_test"

DEFAULT_TYPE = TYPE_GEMINI

TYPES = [TYPE_GEMINI, TYPE_GOOGLE, TYPE_OPENAI, TYPE_DEEPSEEK, TYPE_TEST]

# TODO: use client directly instead of types
STREAM_SUPPORT = [TYPE_GEMINI, TYPE_OPENAI, TYPE_DEEPSEEK]

ALIAS_TO_CLIENT = {TEST_ID: TEST_ID}
CLIENT_ID_TO_TYPE = {DEFAULT_MODEL: DEFAULT_TYPE, TEST_ID: TYPE_TEST}

# OUTPUT STRINGS (instructions, warnings, information..)
CLI_EXAMPLE_USAGE = f'''\
Example Usage: 
search "query" -command client

For more details:
search {HELP_COMMAND}'''

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
For a full list of aliases use the command '{ALIASES_COMMAND}'.

If no client is provided the script will default to gemini-flash-1.5
    
- Commands are prepended with '-'

Some valid commands are:
    '{CHAT_COMMAND}' // Starts a persistent chat session with all clients.
    '{ALIASES_COMMAND}' // Updates and displays list of aliases > models. Cached in {MODELS_CACHE_FILE}

search is a suggested enviroment alias for running the script.
'''

ERROR_SCRIPT_DIR = "Failed to get script directory."

ERROR_MULTIPLE_SYS_MESSAGES = "You can only provide one system message at a time. \nUsing first message provided."

TEST_RESPONSE = "This is a test response for TestClient.\n\
This is line 2 of the test response\n\
This is line 3 of the test response"

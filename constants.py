TIMEOUT = 45

SCRIPT_NAME = "search"

DEFAULT_SYS_MSG = {"role": "system", "content": "You are efficient, to the point and helpful"}

# 256-Color Codes
GREEN = 34
LBLUE = 26
RED = 52
DRED = 1
LRED = 196

# Commands
CHAT_COMMAND = '-c'
HELP_COMMAND = '-help'
ALIASES_COMMAND = '-aliases'
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
VALID_FLAGS = [ADD_FLAG, REMOVE_FLAG, STREAM_FLAG, DISPLAY_FLAG, SYSMSG_FLAG, CLEAR_FLAG] 

# Client IDs
# Until o1 and o3-mini are available they have been commented out.
# Use OpenAI.models.list() to view available clients.

GOOGLE_ID = "google" # Unsupported
GEMINI_FLASH_EXP_ID = "gemini-2.0-flash-exp"
GEMINI_FLASH_ID = "gemini-1.5-flash"
GEMINI_PRO_ID = "gemini-1.5-pro"
GPT_3_5_TURBO_ID = "gpt-3.5-turbo"
GPT_4_ID = "gpt-4"
GPT_4_TURBO_ID = "gpt-4-turbo"
GPT_4O_ID = "gpt-4o"
GPT_4O_MINI_ID = "gpt-4o-mini"
#O1_ID = "o1"
O1_PREVIEW_ID = "o1-preview"
O1_MINI_ID = "o1-mini"
#O3_MINI_ID = "o3-mini"
DEEPSEEK_R1_FREE = "deepseek/deepseek-r1:free"

TEST_ID = "test-client"

# Client Aliases
ALIAS_TO_CLIENT = {
    GEMINI_FLASH_ID: GEMINI_FLASH_ID,
    "gemini": GEMINI_FLASH_ID,
    "gflash": GEMINI_FLASH_ID,
    GEMINI_FLASH_EXP_ID: GEMINI_FLASH_EXP_ID,
    "gflash2": GEMINI_FLASH_EXP_ID,
    "gexp": GEMINI_FLASH_EXP_ID,
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
    #O1_ID: O1_ID, 
    O1_PREVIEW_ID: O1_PREVIEW_ID,
    "o1p": O1_PREVIEW_ID,
    "o1preview": O1_PREVIEW_ID,
    O1_MINI_ID: O1_MINI_ID,
    "o1m": O1_MINI_ID,
    "o1mini": O1_MINI_ID,
    #O3_MINI_ID: O3_MINI_ID, 
    #"o3m": O3_MINI_ID, 
    #"o3mini": O3_MINI_ID, 
    DEEPSEEK_R1_FREE: DEEPSEEK_R1_FREE,
    "r1": DEEPSEEK_R1_FREE,
    "deepseek": DEEPSEEK_R1_FREE,
    TEST_ID: TEST_ID
}

# Client TYPES
TYPE_GEMINI = "type_gemini"
TYPE_GOOGLE = "type_google"
TYPE_OPENAI = "type_openai"
TYPE_DEEPSEEK = "type_deepseek"
TYPE_TEST = "type_test"

TYPES = [TYPE_GEMINI, TYPE_GOOGLE, TYPE_OPENAI, TYPE_DEEPSEEK]

STREAM_SUPPORT = [TYPE_GEMINI, TYPE_OPENAI, TYPE_DEEPSEEK]

CLIENT_ID_TO_TYPE = {
    GEMINI_PRO_ID: TYPE_GEMINI,
    GEMINI_FLASH_ID: TYPE_GEMINI,
    GEMINI_FLASH_EXP_ID: TYPE_GEMINI,
    GOOGLE_ID: TYPE_GOOGLE,
    GPT_3_5_TURBO_ID: TYPE_OPENAI,
    GPT_4_ID: TYPE_OPENAI,
    GPT_4_TURBO_ID: TYPE_OPENAI,
    GPT_4O_ID: TYPE_OPENAI,
    GPT_4O_MINI_ID: TYPE_OPENAI,
    O1_PREVIEW_ID: TYPE_OPENAI,
    O1_MINI_ID: TYPE_OPENAI,
    #O1_ID: TYPE_OPENAI, # Verify functionality when fully launched by OpenAI
    #O3_MINI_ID: TYPE_OPENAI, # Verify functionality when fully launched by OpenAI
    DEEPSEEK_R1_FREE: TYPE_DEEPSEEK,
    TEST_ID: TYPE_TEST
}

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
    '{ALIASES_COMMAND}' // Full list of aliases

search is a suggested enviroment alias for running the script.
'''

ERROR_SCRIPT_DIR = "Failed to get script directory."

TEST_RESPONSE = "This is a test response for TestClient.\n\
This is line 2 of the test response\n\
This is line 3 of the test response"
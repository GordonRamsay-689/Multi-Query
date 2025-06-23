MODELS_CACHE_REL_PATH = "data/cache/models.json"

TIMEOUT = 45

SCRIPT_NAME = "search"

# 256-Color Codes
GREEN = 34
LBLUE = 26
RED = 52
DRED = 1
LRED = 196
YELLOW = 11

# Runtime flags
CHAT_RUNFLAG = '--chat'
ALIASES_RUNFLAG = '--models'
HELP_RUNFLAG = '--help'
STREAM_RUNFLAG = '--stream'
SYS_RUNFLAG = '--sys-message'
NOFORMAT_RUNFLAG = '--no-format'

SHORTHAND_TO_RUNFLAG = {
    "-c": CHAT_RUNFLAG,
    "-m": ALIASES_RUNFLAG,
    "-h": HELP_RUNFLAG,
    "-s": STREAM_RUNFLAG,
    "-S": SYS_RUNFLAG, 
    "-f": NOFORMAT_RUNFLAG
}

VALID_RUNFLAGS = [CHAT_RUNFLAG, HELP_RUNFLAG, ALIASES_RUNFLAG, STREAM_RUNFLAG, SYS_RUNFLAG, NOFORMAT_RUNFLAG] 

# Prompt flags 
# Prompt flags include ':' to avoid conflating with flags the user may search for
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
search "query" --flag model

For more details:
search {HELP_RUNFLAG}'''

CLI_HELP = f'''\
NOT IMPLEMENTED
'''

ERROR_SCRIPT_DIR = "Failed to get script directory."

ERROR_MULTIPLE_SYS_MESSAGES = "You can only provide one system message at a time. \nUsing first message provided."

TEST_RESPONSE = "This is a test response for TestClient.\n\
This is line 2 of the test response\n\
This is line 3 of the test response"

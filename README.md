<h1>Multi-Query</h1>

Query LLMs from the command line. Send the same query to several different models at a time, responses being printed as they are received. Currently supports text-based models from OpenAI and Gemini.

**Disclaimer:** Token usage varies between models. No checks regarding token usage or token availability are performed before sending queries. 

### Prerequisites
- Python 3.12 or later + optional packages: `google-generativeai`, `openai`.

<h2>Setup</h2>

1. Clone this repository:
```bash
git clone https://github.com/GordonRamsay-689/Multi-Query.git
```

2. Install at least one of the following libraries (you only need the ones you plan to use):

<h3>Gemini API</h3>

1. Install [Gemini API](https://ai.google.dev/):
```bash
pip3 install google-generativeai
```

2. Generate a free API key at https://aistudio.google.com/apikey.

3. Set the following environment variable:
```bash
export GOOGLE_API_KEY=*
```

<h3>OpenAI API</h3>

1. Install [OpenAI API](https://platform.openai.com/docs)
```bash
pip3 install openai
```

2. Create a project and generate an API key at https://platform.openai.com/docs/api-reference/authentication. You may need to purchase tokens at least once to avoid RateLimitErrors.

3. Set the following environment variable:
```bash
export OPENAI_API_KEY=*
```

<h2>Usage</h2>

Tip: Create an alias for easy access: 
```bash
alias mq="python3 ../Multi-Query/master.py"
```

Multi-Query can run in *Conversation Mode* or *One-Shot Mode*. If a query is passed the program will start in One-Shot Mode. If no query is passed or if the conversation flag (`-c`) is passed the program will start in Conversation Mode.

* **One-Shot Mode:** Terminates after all responses to the query passed as argument have been received.
* **Conversation Mode:** An interface will be presented for submitting queries. To send a message in Conversation Mode, enter three newline characters in a row (press enter four times). Pasted content is supported, but if the pasted content contains three consecutive newline characters the query will be sent immediately and anything after that point will not be included in the query.

Running the script with no arguments will provide a list of model aliases. Both aliases and full names are supported when specifying models.

To submit a query:
```bash
mq "QUERY" [MODEL NAME | MODEL ALIAS] [--FLAG | -FLAG SHORTHAND]
```

The query is delimited by double quotes, and must be the first argument passed **if** provided. Other arguments are not positional, and can be mixed freely. Any number of clients can be added:
```bash
mq "QUERY" --flag CLIENT_A --flag CLIENT_B ...
```

<h4>Examples:</h4>

Submit a query, add three models, start Conversation Mode and print raw responses (no markdown formatting):
```bash
mq "Write a haiku about README.md" g1.5f -c g2.5f gpt4 --no-format
```

Start Conversation Mode with two models:
```bash
mq g2.5f gpt4
```

<h3>Flags</h3>

<h4>Runtime Flags</h4>

Runtime flags are passed as arguments on runtime.

**Available runtime flags:**
Flag | Shorthand | Function
-|-|-
`--models` | `-m` | Fetch models from providers, cache it, and print a table of supported models and their aliases.
`--chat` | `-c` | Start in Conversation Mode.
`--help` | `-h` | Detailed usage information.
`--no-format` | `-f` | Disables output formatting.
`--stream` | `-s` | Enables streamed responses for supported model. Only one model can stream at a time.
`--sys-message` | `-S` | Provide a system message to supported models. Must be followed by a message.

<h4>Prompt Flags</h4>

Prompt flags are used in Conversation Mode, prefixed with two dashes, followed by a colon and any necessary argument.
```Conversation Mode
--flag:[ARGUMENT]
```
Flags that do not require an argument will not be recognized if one is passed.

Flags will be extracted from the query (and executed) before it is sent:
```Conversation Mode
This is a --add:g2.5f --rm:gpt4 query.
```
The model (Gemini 2.5 Flash in this case) would receive the query: "This is a query."

**Available prompt flags:**
Flag | Function
-|-
`--add:` | Add a model to the conversation. Must be passed a valid model name or alias.
`--rm:` | Remove a model from the conversation. Must be passed a valid model name or alias. *Tip: Pass "all" to remove all active sessions.*
`--clear:` | Restart all active sessions.
`--dump:` | Dumps current conversation to file at `./dumps/dump_MM_DD_YYYY_HH_MM_SS.txt`.
`--format:` | Toggle response markdown formatting.
`--stream:` | Toggle streamed responses for a specific model. *
`--aliases:` | Display a table of available models and their aliases.
`--sys:` | Specifies a new system message. Must be passed a message enclosed in double quotes. *\*

*\* Only one client can have streaming enabled at any given time. Enabling streaming for a new client will disable streaming for all other clients.*

*\*\* Currently, only OpenAI models support receiving system messages mid-conversation.*

### Tips and Tricks:

Upload file contents with your initial prompt:
```bash
mq "Extract key ideas from this article: $(cat article.txt) and insert into this essay: $(cat essay.txt)."
```
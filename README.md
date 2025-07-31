<h1>Multi-Search</h1>

*Readme is outdated, pending rewrite. Software itself works however.* 

Query LLMs from the command line. You can query several models/engines at the same time, responses being printed as they are received. Multi-line queries, chat sessions and pasted content is supported. 

*Google Search integration, previously available, is currently unavailable due to a defunct API. Restoration is planned if feasible.*

**Disclaimers:** 
- Shell pasting behavior varies, often capping content around 4000 characters.
- Pasting content with more than three consecutive newline characters will send that content immediately.
- Persistent chat history is not yet implemented.

### Prerequisites
- Python 3.12.3 or later

Optional:
- Gemini API by Google
- OpenAI API by OpenAI

<h2>Setup</h2>

Install at least one of the following libraries (you only need the ones you plan to use):

<h3>Gemini API</h3>

1. Install [Gemini API](https://ai.google.dev/):
```zsh
pip3 install google-generativeai
```

2. Create a free API key at https://aistudio.google.com/apikey.

<h3>OpenAI API</h3>

1. Install [OpenAI API](https://platform.openai.com/docs)
```zsh
pip3 install openai
```

2. Create a project and generate and API key at https://platform.openai.com/docs/api-reference/authentication. You may need to provide payment information and purchase tokens at least once.

<h2>Usage</h2>

Set environment variables with the API keys for the APIs you plan to use. For bash, sh, zsh:
```zsh
export GEMINI_API=*
export OPENAI_API_KEY=*
export OPENROUTER_API=*
```

Running the script with no arguments will prompt you for necessary information,
but providing arguments is often more efficient.

If you start a chat session (default if no query is provided) an interface which allows for multi-line input is presented. To send a message, enter three  newline characters in a row (press enter four times). Pasted content is supported as long as it does not include three consecutive newline characters.

Create an alias for easy access: 
```zsh
alias search="python3 ../multi_search/master.py"
```

For detailed help, use:
```zsh
search -help
```

To query one or more clients, enter your query enclosed in double quotes followed by one or more client aliases:
```
search "query" gflash
```
or just:
```zsh
search "query" # Defaults to gemini-1.5-flash
```

You can add any number of clients to query:
```zsh
search gflash gpt4o ...
```

The query is signified by double quotes, and must be the first argument provided **if** provided. Other arguments do not rely on position, and can be mixed freely:
```zsh
search "query" -option CLIENT_A -option CLIENT_B ...
```

<h3>Options</h3>

Options are provided as arguments after the query, if provided. It does not matter if they are provided before, after or mixed with aliases.

**Available options:**
Option | Function
-|-
```-aliases``` | Provides a table of supported models and their aliases.
```-c``` | Initiate a persistent chat session.
```-help``` | Detailed usage information.
```-noformat``` | Disables output formatting.
```-s``` | Enables streamed responses (from supported models/engines).
```-sys``` | Provide a system message to supported models, ```-sys``` must be followed by the message in question.

<h3>Flags</h3>

Flags are used during runtime, prefixed with two dashes, followed by a colon and any necessary information. For example, to add Gemini 1.5 Pro to the conversation:
```
--add:gpro 
```

Flags will be extracted from the query before sending it, so this is also valid:
```
This is a --add:gpro --rm:gpt4 query.
```
The client would recieve "This is a query." and nothing else.

**Available flags:**
Flag | Function
-|-
```--add:``` | Add a model/engine to the conversation.
```--rm:``` | Remove a model/engine from the conversation. *Tip: Provide "all" to remove all active sessions.*
```--clear:``` | Reinitialize all active sessions. *Needs no argument after the colon.*
```--stream:``` | Toggle streamed responses for a specific model/engine.
```--aliases:``` | Display a table of available models/engines and their aliases. *Needs no argument after the colon.*
```--sys:``` | Specifies a new system message.

*\* Only one client can have streaming enabled at any given time. Enabling streaming for a new client will disable streaming for all other clients.*

*\*\* Currently, only OpenAI models support mid-conversation system message updates.*

### Valid client-aliases:

*FYI: You can always use the full client name as an alias (for example, ```gpt-4o``` for ```gpt-4o```).*

Run with option ```-aliases``` to view a list of all aliases. 

Using an alias for a client for which you lack the necessary libraries to use
will omit said client.

**Disclaimer:** Token usage varies between models. The script doesn't currently check token usage before sending queries. 

### Tips and Tricks:

Upload file contents with your initial prompt:
```zsh
search "$(cat path/to/file)"
```

You can submit multiple files like this, including comments:
```zsh
search "Extract key ideas from this article: $(cat article.txt) and insert into this essay: $(cat essay.txt)."
```
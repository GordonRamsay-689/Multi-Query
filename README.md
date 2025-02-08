<h1>Multi-Search</h1>

This is a simple script that lets you query LLMs (Gemini, OpenAI, DeepSeek-R1) directly from the terminal, neatly displaying the results. You can query several models/engines at the same time, responses being printed as they are received. 

Multi-line queries, chat sessions and pasted content is supported. 

*In the past searching Google was possible as well, but the required API has stopped functioning. It will be repaired in the future if maintaining it is not unreasonably tasking.*

**Disclaimers:** 
- Different shells handle pasting a bit differently, most seem to cap pasted content at around 4000 characters.
- Pasting content with more than three sequential newline characters will send that content immediately.
- There is currently no way to load conversations from previous sessions, but this will be implemented in the future.

- Currently, Google Search is unsupported as the API it relied on has stopped working. I am looking into alternatives, or the viability of fixing
the original API. The code for Google Search (GoogleClient) has not been completely removed, but it is not possible to initiate a Google session.

### Prerequisites
- Python 3.12.3 or later

Optional:
- Gemini API by Google
- OpenAI API by OpenAI

<h2>Setup</h2>

Install at least one of the following libraries (you only need the ones you plan to use):

<h3>Gemini API</h3>

1. Install [Gemini API](https://ai.google.dev/):
``` 
    pip3 install google-generativeai
```

2. Create a free API key at https://aistudio.google.com/apikey.

<h3>OpenAI API</h3>

1. Install [OpenAI API](https://platform.openai.com/docs)
```
    pip3 install openai
```

2. Create a project and generate and API key at https://platform.openai.com/docs/api-reference/authentication. You may need to provide payment information and purchase tokens at least once.

<h2>Usage</h2>

If using any of the APIs, export your API keys as environment variables. For bash, sh, zsh:
```
    export GEMINI_API=*
    export OPENAI_API_KEY=*
```

Running the script with no arguments will prompt you for necessary information, but providing information as arguments is often more efficient.

If you start a chat session (default if no query is provided) an interface which allows for multi-line input is presented. To send a message, enter three newline characters in a row (press enter four times). Pasted content is supported as long as it does not include three sequential newline characters, which is unusual.

I recommend setting an environment alias for easy access: 
```
    alias search="python3 ../multi_search/master.py"
```

For detailed help, use:
```
    search -help
```

To query one or more clients, enter your query enclosed in double quotes
followed by one or more client aliases:
```
    search "query" gflash
```
or just:
```
    search "query" // Defaults to gemini-1.5-flash
```

You can add any number of clients to query:
```
    search gflash gpt4o ...
```

The query is signified by double quotes, and must be the first argument provided **if** provided. Other arguments do not rely on position, and can be mixed freely:
```
    search "query" -command CLIENT_A -command CLIENT_B ...
```

<h3>Commands</h3>

Commands are optional and are provided as arguments after the query, if provided. Commands are signified by a preceding dash.

**Available commands:**
Commmand | Function
-|-
```-aliases``` | Provides a table of supported models and their aliases.
```-c``` | Initiate a persistent chat session.
```-help``` | Detailed usage information.
```-noformat``` | Disables output formatting (except for Google Web Search which cannot be provided without formatting).
```-s``` | Enables streamed responses (from supported models/engines).
```-sys``` | Provide a system message to supported models, ```-sys``` must be followed by the message in question.

<h3>Flags</h3>

Flags are provided during runtime. They are signified by two dashes preceding the flag, followed by a colon and any other information necessary.

If you for example want to add Gemini 1.5 Pro to the conversation, you would type this anywhere inside your query (don't worry, the flag will not be included in the query sent to the model/engine):
```
    --add:gpro 
```

**Available flags:**
Flag | Function
-|-
```--add:``` | Add a model/engine to the conversation. Needs to be followed by a client alias.
```--rm:``` | Remove a model/engine from the conversation. Needs to be followed by a client alias.
```--stream:``` | Toggle streamed responses for a specific model/engine. Needs to be followed by a client alias.* 
```--aliases:``` | Display a table of available models/engines and their aliases. Does not need to be followed by a client alias.
```--sys:``` | Specify a new system message. You can only provide one system message at a time. Needs to be followed by a system message, which must be enclosed in double quotes.**

*\* Only one client can have streaming enabled at any given time. Enabling streaming for a new client will disable streaming for all other clients.*

*\*\* Currently the only clients that support adding system messages mid conversation are OpenAI Clients.*

### Valid client-aliases:

*FYI: You can always use the full client name as an alias (for example, ```gpt-4o``` for ```gpt-4o```).*

Alias | Model/Engine
-|-
4o | gpt-4o
gemini | gemini-1.5-flash
gflash | gemini-1.5-flash
gpro | gemini-1.5-pro
gexp, gflash2 | gemini-2.0-flash-exp
turbo3.5 | gpt-3.5-turbo
gpt4 | gpt-4
turbo | gpt-4-turbo
gpt4o | gpt-4o
mini | gpt-4o-mini
o1m, o1mini | o1-mini
o1p, o1preview | o1-preview

**Disclaimer:** Some models use more tokens than others or require an API you may not have installed or access to. At the moment no checks regarding expected token use are performed before sending a query. No error will be thrown however if you provide a client alias for a client you do not have installed, it will simply be omitted.
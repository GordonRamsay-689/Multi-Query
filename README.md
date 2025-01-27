<h1>Multi-Search</h1>

_Work in progress for personal use, use at your own discretion. Feel free to modify any way you like._

This is a simple script that lets you search Google and query Gemini, OpenAI models directly from the terminal, neatly displaying the results. You can query several models/engines at once, responses being printed as they are received.

Persistent chat sessions have now been added, as well as an input function that allows for multi-line queries 
and pasted content (if no more than three newline chars **in sequence** inside the pasted content). 

**Disclaimers:** 
- Google Search will sometimes fail to return responses, if you are usinga VPN try disabling it. 
- Different shells handle pasting a bit differently, most seem to cap pasted content at around 4000 characters.
- There is currently no way to load conversations from previous sessions, but this will be implemented in the future.

### Prerequisites
- Python 3.12.3 or later (tested on macOS. Linux compatibility is unconfirmed)

Optional:
- Google-Search-API by abenassi 
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

<h3>Google Web Search</h3>

1. Install [Google Search API](https://github.com/abenassi/Google-Search-API):
```
    pip3 install git+https://github.com/abenassi/Google-Search-API
```

2. After installing googleapi you need to patch it, as it no longer works out of the box.
3. Navigate to python site-packages, on MacOS default location is ```/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/```
4. Replace ```../site-packages/googleapi/modules/standard_search.py``` with ```multi_search/for_googleapi/standard_search.py```, provided in this repo.

<h2>Usage</h2>

If using any of the APIs, export your API keys as environment variables. For bash, sh, zsh:
```
    export GEMINI_API=*
    export OPENAI_API_KEY=*
```

Running the script with no arguments will prompt you for the necessary information. This is useful when your initial query needs to be formatted, or include copy-pasted text.

I recommend setting an environment alias for easy access: 
```
    alias search="python3 ../multi_search/master.py"
```

For detailed help, use:
```
    search -help
```

To query one or more clients, enter your query enclosed in double qoutes
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

As you receive responses they will be printed, as soon as one client responds you can read that response while waiting for the other clients to respond.

Requests will time out after 45 seconds.

<h3>Commands</h3>

Commands are optional and are provided as arguments after the query, if provided. Commands are signified by a preceding dash.

**Available commands:**
Commmand | Function
-|-
```-aliases``` | Provides a table of supported models and their aliases.
```-c``` | Initiate a persistent chat session.
```-help``` | Detailed usage information.
```-noformat``` | Disables output formatting (except for Google Web Search which cannot be provided without formatting).
```-s``` | Enables streamed responses (from supported models/egnines).
```-sys``` | Provide a system message to supported models, ```-sys``` must be followed by the message in question.

<h3>Flags</h3>

Flags are provided during runtime. They are signified by two dashes preceding the flag, followed by a colon and any other information necessary.

If you for example want to add Gemini 1.5 Pro to the conversation, you would type this anywhere inside your query (don't worry, the flag will not be included in the query sent to the model/engine):
```
    --add:gpro 
```

**Available flags:**
Flag         | Function
-|-
```--add:``` | Add a model/engine to the conversation. Needs to be followed by a client alias.
```--rm:``` | Remove a model/engine from the conversation. Needs to be followed by a client alias.
```--stream:``` | Toggle streamed responses for a specific model/engine. Needs to be followed by a client alias. (Only one client can have streaming enabled at one given time. Enabling streaming for a new client will disable streaming for all other clients.)
```--aliases:``` | Display a table of available models/engines and their aliases. Does not need to be followed by a client alias.
```--sys:``` | Specify a new system message, added to conversation if a client/model supports insertion of system messages mid conversation (currently, only Gemini does not support this). You can only provide one system message at a time. Needs to be followed by a system message, which must be enclosed in doubleqoutes.

### Valid client-aliases:

*FYI: You can always use the full client name as an alias (for example, ```gpt-4o``` for ```gpt-4o```).*

Alias | Model/Engine
-|-
4o | gpt-4o
gemini | gemini-1.5-flash
gflash | gemini-1.5-flash
gpro | gemini-1.5-pro
gexp, gflash2 | gemini-2.0-flash-exp
google | google
turbo3.5 | gpt-3.5-turbo
gpt4 | gpt-4
turbo | gpt-4-turbo
gpt4o | gpt-4o
mini | gpt-4o-mini
o1m, o1mini | o1-mini
o1p, o1preview | o1-preview

**Disclaimer:** Some models use more tokens than others or require an API you do not have installed or access to. At the moment no checks regarding expected token use are performed before sending a query. No error will be thrown however if you provid a client alias for a client you do not have installed, it will simply be omitted.
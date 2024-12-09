<h1>Multi-Search</h1>

_Work in progress for personal use, use at your own discretion. Feel free to modify any way you like._

This is a simple script that lets you search Google and query Gemini directly from the terminal, neatly displaying the results. You can query several models/engines at once, responses being printed as they are received.

Persistent chat has now been added, as well as an input function that allows for multi-line queries 
and pasted content (if no more than three newline chars **in sequence** inside the pasted content). 

**Disclaimers:** 
- Google Search will often fail to return responses. I will look into porting parts of the API as it is unreliable at the 
moment.
- Different shells handle pasting a bit differently, and some seem to cap the pasted content at about 4000 characters.

### Prerequisites
- Python 3.12.3 (tested on macOS. Linux compatibility is unconfirmed)

Optional:
- Google-Search-API by abenassi 
- Google's Gemini API 

<h2>Setup</h2>

1. Install at least one of the following libraries (you only need the ones you plan to use):

<h3>Gemini API</h3>
1. Install [Gemini API](https://ai.google.dev/) and get a free API key:
``` 
    pip3 install google-generativeai
```

<h3>Google Web Search</h3>
1. Install [Google Search API](https://github.com/abenassi/Google-Search-API)
```
    pip3 install git+https://github.com/abenassi/Google-Search-API
```
2. After installing googleapi you need to patch it, as it no longer works:
3. Navigate to python site-packages, on MacOS default location is ```/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/googleapi/modules/```
4. Replace 'standard_search.py' with ```multi_search/for_googleapi/standard_search.py```

<h2>Usage</h2>

Export your API keys as environment variables. For bash, sh, zsh:
```
    export GEMINI_API=key
```

Running the script with no arguments will prompt you for necessary information.

For detailed information, use:
```
    msearch -help
```

I recommend setting an environment alias for easy access: 
```
    alias msearch="python ~/path/to/script/script.py"
```

To query one or more clients, enter your query enclosed in double qoutes
followed by one or more client aliases:
```
    msearch "query" gflash
```
or just:
```
    msearch "query" // Defaults to gemini-flash
```

You can add any number of clients to query:
```
    msearch gflash gpro ...
```

The query is signified by double quotes, and must be the first argument provided **if** provided. Other arguments do not rely on position, and can be mixed freely:
```
    msearch "query" -command CLIENT_A -command CLIENT_B ...
```

Use `-c` to start a persistent chat session.  This is also the default behavior if no query is provided.

As you receive responses they will be printed, as soon as one client responds you can read that response while waiting for the other clients to respond.

Requests will time out after 45 seconds.

### Valid client-aliases:

Client Alias | Model/Engine
-|-
gemini, gflash | Gemini 1.5 Flash
gpro         | Gemini 1.5 Pro
google       | Google Web Search


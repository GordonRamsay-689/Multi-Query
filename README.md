<h1>Multi-Search</h1>

_Work in progress for personal use, use at your own discretion. Feel free to modify any way you like._

This is a simple script that lets you search Google and query Gemini directly in terminal, neatly displaying the results. You can query several models/engines at once, responses being printed as they are received.

The current implementation will only send the query you provided as an argument when running the script, but I have tested persistent chats, and will be adding 
a client where you can keep a conversation going (or several conversations at once) for as long as you like.

### Prerequisites
- Python 3.12.3 (tested on macOS. Linux compatibility is unconfirmed)
- Google-Search-API by abenassi
- Google's Gemini API

<h2>Setup</h2>

1. Install [Google Search API](https://github.com/abenassi/Google-Search-API)
```
    pip3 install git+https://github.com/abenassi/Google-Search-API
```
3. After installing googleapi you need to patch it, as it no longer works:
4. Navigate to python site-packages, on MacOS default location is ```/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/googleapi/modules/```
5. Replace 'standard_search.py' with the file with the same name provided in the repository inside folder "for_googleapi"
6. Install [Gemini API](https://ai.google.dev/) and get a free API key
``` 
    pip3 install google-generativeai
```
7. Run the setup to store your API keys in a local env file:
``` 
    msearch -setup
```
**This is not being encrypted in any way, so modify it yourself if you don't feel comfortable storing your keys locally without encryption.**

<h2>Usage</h2>

I recommend setting an enviroment alias for easy access: 
```
    alias msearch="python ~/path/to/script/script.py"
```
Run the module with the following command, replacing ```CLIENT``` with a valid alias (see bottom of readme):
```
    msearch "query" CLIENT
```
or just:
```
    msearch "query" // Defaults to gemini-flash
```

You can add any number of clients to query:
```
    msearch "query" CLIENT_A CLIENT_B ...
```
As you receive responses they will be printed, so as soon as one client responds you can read the response while waiting for the other clients to respond.

There is no timeout feature implemented, so you can simply use CTRL + C to interrupt the script.

### Valid client-aliases:
- "gemini" or "gflash": Gemini 1.5 Flash
- "gpro": Gemini 1.5 Pro
- "google": Google Web Search

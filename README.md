This is a simple script that lets you search Google and query Gemini directly in terminal, neatly displaying the results. More engines and models will be
added when _I_ feel like it, but it should be fairly easy to add your own if _you_ feel like it. 

The current implementation will only send the query you provided as an argument when running the script, but I have tested persistent chats, and will be adding 
a client where you can keep a conversation going (or several conversations) for as long as you like. I didn't include that functionality when directly running
the module with arguments because I didn't need it.

<h2>Setup</h2>

You must first run the setup to store your API keys in a local env file.

    msearch -setup

**This is not being encrypted in any way, so modify it yourself if you don't feel comfortable storing your keys locally without encryption.**

<h2>Usage</h2>

I recommend setting an enviroment alias for easy access: 

    alias msearch="python3 ~/path/to/script/script.py"

At the moment you can run the module request_handler.py directly in terminal by simply typing:

    msearch "query" CLIENT

or just:

    msearch "query" // Defaults to gemini-flash

You can add any number of clients to query:

    msearch "query" CLIENT_A CLIENT_B ...

As you receive responses they will be printed, so as soon as one client responds you can read the response while waiting for the other clients to respond.

There is no timeout feature implemented, so you can simply use CTRL + C to interrupt the script.

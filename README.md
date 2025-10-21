# One-Off-Projects

LLM generated one off projects that are only scripts or some little sites or something alike that
will automate some task for me. Very sloppy, ...

## pdftonote

- get annotations from a pdf file for paper reviews of mine
- gets all kinds of annotations and outputs them slightly markdown formatted into stdout
- **droped** on favour of _pdfannots_

## icsgen

- generates ics cal files from a text file or cli arguments

## ics mcp (idea 🚧)

- uses the same functionality as icsgen to
  - generate ics files and import them to my calendar application
  - or only download them?
- events can then be generated with human language in claude desktop directly imported with the tool
- ics files can for example be written to `/tmp/mcp-ics` and open from there with `open`

## prompt manager

- manage and pre-write prompts for coding agents
- input them via Tmux into the window where your agent is currently running
- for the best experience assign a keymap in your `tmux.conf`

## stdioproxy (idea 🚧)

- so I want to run MCP servers on my pi and I want to use them from my mac and Claude code
- the goal is to create an MCP proxy that is one stdio MCP server that can talk to multiple http MCP
  servers and forward their messages
- that way I can use free tier of Claude and use multiple servers that run on the local network

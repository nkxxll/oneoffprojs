# Kairos v2

So why Kairos v2...because while making the very interesting mcp connection from a pi to my mac that
can take my times I recognized that the constant connection between the mac and the pi is unstable
because I move the mac a lot and thus the mcp connection dies. This could be handled with retries
and better error handling but the main problem is that MCP is a stateful protocol which is a problem
for my use case.

Solution: I can just run `timew` scripts from the command line with `ssh` very old but very good
script that works. And I can expose a limited set of the api for an mcp with and mcp server that
translates to the stateless invocation of one command via `ssh`. Very simple solution that makes me
really sad because my complicated solution with `claude desktop -> stdio/http mcp proxy -> pi http mcp
server` and with CLI options via `REST -> pi REST/MCP proxy -> pi http mcp server` is now really
dump and obsolete and does not work.

But in the end of it all I want to have a working very easy time taking tool which I can use from
all my computers. Yes ssh setup is a bit more tricky with `ssh-copy-id`. But this is a one off cost
that I have payed already and will happily pay every time I get a new computer (hopefully not in the
next year or five).

## New architecture

```
CLI -> SSH -> TIMEW
CLAUDE DESKTOP -> MCP -> SSH -> TIMEW
```

Very easy can be really easily done with `bun`.

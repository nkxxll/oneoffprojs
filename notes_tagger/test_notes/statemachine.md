---
tags:
- compilers
- cli-tools
- functional
---

# Statemachine (yes it is a state machine but this state machine is a tokenizer or a lexer)

A state machine is a computer science concept that consists of **inputs**, **rules** and **state**.
Rules define how the system transitions between states. There is also an initial state and a final
state as well as some kind of input that triggers a transition.  
The state machine I want to closer look at is a _Deterministic Finite State Machine_.
State machines are used in lexical analysis of compilers, network protocols, as well as, frontend.
component state management.

## Link parser

```
<a href="url">link text</a>
```

This parse should find all links in an html site.

### Language

Let's write that in Zig ... because we want to learn Zig.
Construct:

- make a struct for the state machine
- define an enum for the states
- make a while-true-loop for the state transitions break if state finished occurs
- step one char at a time through a string
- change the state if necessary

Works like a charm.

### Lessons Learned

I use the following construct:

```zig
fn step() void {
  position += 1;
  if (position >= buffer.len) {
    return;
  }
}
```

...which then morphed into:

```zig
fn step() bool {
  position += 1;
  if (position >= buffer.len) {
    return false;
  }
  return true;
}
```

The problem is the step function should look like this:

```zig
fn step() ?char {
  self.position += 1;
  if (position >= buffer.len) {
    return null;
  }
  return self.buffer[self.position];
}
```

Why? This is similar to the iterator pattern that is omnipresent in Zig and it enables me to check
for null in the outer scope and adjust the state accordingly. With the `bool` I have to get the char
every time afterwards (code duplication) and I have to check for the `bool` and `break` if
necessary. This look a bit funny and does not work as well as using the iterator pattern which is
much more elegant (see [here](https://github.com/ziglang/zig/blob/dbc886fd04328391598880c8d5abe8443b514a02/lib/std/mem.zig#L3008-L3079).

## Zig state maching in the zig compiler

- there is a state machine in the zig compiler code [here](https://github.com/ziglang/zig/blob/master/lib/std/zig/tokenizer.zig)
- they have some important things
- there is no allocation
- there is no peek

The token looks like this :D

```zig
pub const Token = struct {
    tag: Tag,
    loc: Loc,

    pub const Loc = struct {
        start: usize,
        end: usize,
    };
...
};
```

and the tokenizer looks like this

```zig
pub const Tokenizer = struct {
    buffer: [:0]const u8,
    index: usize,
...

    pub fn next() Token {
        pub fn next(self: *Tokenizer) Token {
        var result: Token = .{
            .tag = undefined,
            .loc = .{
                .start = self.index,
                .end = undefined,
            },
        };
        state: switch (State.start) {
             if (self.index == self.buffer.len) {
                 return .{
                     .tag = .eof,
                     .loc = .{
                         .start = self.index,
                         .end = self.index,
                     },
                 };
             } else {
                 continue :state .invalid;
             }
            ...
            'a'...'z', 'A'...'Z', '_' => {
                result.tag = .identifier;
                continue :state .identifier; // go up again
                // if we don't go up we stop and...
            }
        }
        result.loc.end = self.index;
        return result;
    }
}
```

That is great I want to build all my tokenizers like this how can I take this and make a calculator
out of this.

Note (31.1.2026): I dont know how often I have copied the zig tokenizer from the compiler code. It is so cute to see my younger self have struggles with patterns from tokenizers. Which is just an afterthought for me now.

Interesting notes:
- [mitchell hashimoto on the zig tokenizer](https://mitchellh.com/zig/tokenizer)
- [zig tokenizer in the compiler](https://codeberg.org/ziglang/zig/src/branch/master/lib/std/zig/tokenizer.zig)
- [odin tokenizer](https://github.com/odin-lang/Odin/blob/f7901cffc9f4983259586241d5b336cdb6377b9c/core/odin/tokenizer/tokenizer.odin#L1)

## Related Notes
- [[Chat GPT test examn 2019/2020]]
- [[Golang]]

# Sun 01 Feb 2026

- [x] dsm: papers lesen project root
- [x] some typing tests: 91 at max

---

- [ ] virtualbadge.io:
  - docu
  - make system architecture (todo)
  - make the documentation (todo)
  - think of what to do in the workflow presentation (todo)
  - make a lessons learned (wip)
- [ ] blog: einen blog cleanen
- [ ] read up: ist stoizismus entspannend und sind entspannte leute erfolgreicher
- [ ] blog idea: opus 4.5 with a skill can transpile jai to odin and odin to jai what are these guys doing
- [ ] look at: memalloc
- [ ] jc 69, 70, 71: lesen vllt ein bischen llm zusammenfassen
  - 71 we are here:
- [ ] https://registerspill.thorstenball.com/p/joy-and-curiosity-71#:~:text=Ben%20Thompson%20on,hundreds%20of%20years
- [ ] rading: makingsoftware.com
  - is there a compiler section
  - is there a garbage collector section
  - is there a inter process communication section
- [ ] matklat: blog read
- [ ] blog: why do you need an orchestra when you can have all instruments at the click of a button on
- [ ] you computer

# Sat 31 Jan 2026

- [x] https://mike.tech/blog/death-of-software-development?utm_source=nodeland&utm_medium=email&utm_campaign=the-human-in-the-loop
- [x] projects: update old github projects
- [x] thorsten ball: email turing machine???
  - not gonna write it is too inimportant
- [x] look at: how to extract stuff from this note file how to make other notes that are connected to this
- [x] file but keep the simplicity of one file
  - note taking considerations that keep the simplicity in the workflow but make it more searchable
- [x] reading: memory allocation strats ...
- [x] https://www.gingerbill.org/series/memory-allocation-strategies/
  - part 1 done
  - basically motivation what is memory management and why
  - what are basic memory management strategies short show
  - why does the compiler do not cut it
  - where do languages such as rust and cpp with smart pointer go wrong
- [x] blog: maybe blog about the memory management strats
- [x] look at: semantic embeddings write down a little note
- [x] blog: write apps that you would have written without ai (tag, analyze, link)

# Fri 30 Jan 2026

- [x] monkeytype:
  - best 96
- [x] wif:
  - highlights done
  - fixes done
- [x] ebk:
  - repeat
  - independent set problem

# Thu 29 Jan 2026

- [x] sean godecky:
  - https://www.seangoedecke.com/predators
  - https://www.seangoedecke.com/party-tricks
  - https://www.seangoedecke.com/impressing-people
- [x] conti: app activieren
- [x] netlight:
  - good
  - focus on self development
  - focus on client impact
  - focus on good work
  - focus on learning
  - new technologies
  - in foot reach of f m hbf
  - bad
  - salary
  - career chances at netlight

# Wed 28 Jan 2026

- [x] qtaks: case insensitive
  - can now search tags case insensitive
- [x] qtaks: perf improvements
  - use a thread pool instead of serial reading of the files
  - most of the time is spend waiting for file I/O
  - one thread per file is too much overhead
  - serial is too slow
  - nbio would be perfect but is not in the current odin version
  - so I have settled with thread pool with a variable size of workers default 4
- [x] virtualbadge:
  - make system architecture (todo)
  - make the max model approach be the new backend (done)
  - make the documentation (todo)
  - make a lessons learned (wip)
  - think of what to do in the workflow presentation (todo)
  - think of the economical implications (done)
  - usage metrics: (done)

```
result = await Runner.run(agent, "What's the weather in Tokyo?")
usage = result.context_wrapper.usage

print("Requests:", usage.requests)
print("Input tokens:", usage.input_tokens)
print("Output tokens:", usage.output_tokens)
print("Total tokens:", usage.total_tokens)
```

- docu: https://openai.github.io/openai-agents-python/usage/

# Tue 27 Jan 2026

- [x] monkeytype: 3 tests 90 avg
- [x] odin: continue garbage collector
  - read rc improvement ideas
- [x] skifahren: entscheiden
- [x] ebk: P vs NP
  - P is the class of problems that can be solved in polynomial time
- [x] sean godecky: how i estimate time as a staff engineer
  - estimations are always wrong
  - you cannot have a problem and through the forest of solutions choose the one that will immediately stick
  - what you need is multiple plans and to give options with risks to the management
  - then the management can choose their plan
  - and you can adjust the software choices to the time you have
- [x] > We tackle X Y Z directly, which might all go smoothly but if it blows out we’ll be here for a month
- [x] > We bypass Y and Z entirely, which would introduce these other risks but possibly allow us to hit the deadline
- [x] > We bring in help from another team who’s more familiar with X and Y, so we just have to focus on Z
  - first you need an estimate, then you can make the software in that estimate or close to it
  - other way around does not work
  - do pragmatic estimates that are not: "it is impossible in this time" and not "I can do it in one
- [x] week" (not delivering)
- [x] > When I estimate, I extract the range my manager is looking for, and only then do I go through the
- [x] > code and figure out what can be done in that time. I never come back with a flat “two weeks”
- [x] > figure. Instead, I come back with a range of possibilities, each with their own risks, and let my
- [x] > manager make that tradeoff.
  - banger sentence:
  - find out what management is willing to spend
  - then give options how the product with this time could look like and come out as
- [x] sean godecky: Crypto grifters are recruiting open-source AI developers
  - there is a crypto scheme that looks like this:
  - open-source developer has project
  - someone other does a crypto coin in his name
  - the this someone does pay the open-source developer
  - the open source developer promotes the coin with his name
  - the coin gets traction
  - someone is happy
  - someone is rug pulling the crypto coin from under the users gets the money
  - open-source dev is either naive or he gets profit too from the coin rug pulling game
  - wild blog would never build a crypto coin or buy it
- [x] jc71: "What Does a Database for SSDs Look Like?"
  - gpt: If you rewrote a database in 2025:
  - You'd use modern hardware and networks to make distributed durability, replication, and consistency foundational.
  - You'd ditch some older local-storage optimizations (like traditional WALs) and redesign around SSD performance profiles and cloud scaling.
- [x] odin hat kein ffi generator built-in wie jai sad but true
- [x] look at: odin core library
  - heruntergeladen in git/odin
  - was sollte man sich hier anschauen:
  - core/odin
  - core/socket
- [x] image opener in neovim autocommand:
- [x] https://github.com/laytan/dotfiles/blob/main/nvim/.config/nvim/lua/laytan/autocommands.lua
- [x] wif: abgabe fertig machen sind noch so 2h arbeit aber muessen gemacht werden
  - ist fuer review an papa
  - highlights muessen noch gemacht/gesichtet werden

# Mon 26 Jan 2026

- [x] vid: be so calm it makes people nervous
  - 4 - 7 - 8 breathing: 4 in 7 hold 8 out
  - confident posture: 10% tilt head forward -- still no movement
  - eye contact
  - silence is a power move 3 seconds
  - don't tap into emotions
  - don't tap into any emotion for that matter just stay calm
  - alisa is uncomfy --> I am uncomfy too: mirror
  - but I am chilled alisa chilled to
  - kenny exited because I am exited that is the same thing like
  - malte exited - I uncomfy: both uncomfy
  - malte exited - I calm: both chill
  - exercises: breath, mirror watch yourself into the eyes, posture, (?visualisation?)
  - calm -- stoic taps into your pre-frontal cortex which makes you more rational
  - nervous makes you fight or flight which makes you dumber
  - hate those self improvement vids but some thing I already knew but they have to be remembered and
- [x] this does make me remember things that I just did and that I did with a lot of calm and they
- [x] worked
  - balls pay of what is the worst thing that could happen
- [x] feedly: add this rss https://jvns.ca/atom.xml
- [x] feedly: add this rss https://danluu.com/atom.xml
- [x] blog: sean has a cool website for his blog
- [x] CERN: bewerbung muss raus **PRIO** (done)
- [x] EBK: lernplan machen was muss ich noch verstehen?
  - turing machine
  - non-deterministic turing machine
  - i have written a visualization for tms in the browser
  - amp did it it was easy
- [x] odin: build a garbage collector
- [x] laufen und emam
  - easy run
  - pull up, push up, sit up, stand up (squat)

# Sun 25 Jan 2026

- mount command `sudo mount -t cifs //192.168.2.166/home /mnt/synology -o username=nkxxll,uid=$(id -u),gid=$(id -g)`
- [x] jc 71: inside ai by tommy falkowski: https://www.youtube.com/watch?v=RNGJNQrA-tU&list=PLmdnOV1KOWd6EBJYCAd1lZgSaRpOc7XTn
  - wild conversation between thorsten ball and tommy
  - they talk about the future of ai
  - but also the economical implications that building software is not a 90% margin trait any more
  - that you have to be able to do the work by hand but you dont have to do it
  - you have to understand everything but you do not have to type anything anymore
  - tools are not that important anymore
  - programming language is not important anymore
  - using the **best model** first to be able to tell what the **best possible outcome** is is important only
- [x] then you can think of **scaling down**
  - models dont grow their capabilities in a linear fashion they can be totally different from version
- [x] to version
- [x] sean godecky: I am adicted to being useful: https://www.seangoedecke.com/addicted-to-being-useful/
  - as a swe you should be **adicted to being useful**
  - which means doing the right work to get the company forward
  - helping people
  - solving problems
  - this all should be second nature and make you happy instead of being a chore
  - this is what makes you not burn out
  - though keep private and work live separated
  - dont put all your emotional happiness into work
  - further read:
  - https://www.seangoedecke.com/predators
  - https://www.seangoedecke.com/party-tricks
  - https://www.seangoedecke.com/impressing-people

# Sat 24 Jan 2026

- [x] nothing wild
- [x] breakfast with the handballers
- [x] running
- [x] trump being trump
- [x] some blog reading
- [x] odin qtaks version works like a charm
- [x] very nice
- [x] learned a lot of odin which is basically jai light with go influence
- [x] found out that it works astonishingly good with llms

# Fri 23 Jan 2026

- [x] jc69: continue

# Thu 22 Jan 2026

- [x] jc69: https://blog.ezyang.com/2026/01/the-gap-between-a-helpful-assistant-and-a-senior-engineer/
  - this might be a good point about where the gap is between an agent and an software engineer
  - but it is too much on the surface for my taste
  - a senior software engineer does not only better understand the entire context (company user etc.)
  - a senior engineer also write better abstractions code that can be better maintained and when the
- [x] alarm rings at 2 oclock you rather want to fix the code of a senior than an llm even if the llm
- [x] could write it slightly faster in the first place
  - there is a place for agents but it wont replace anything it'll augment at the most
  - the steps we take in llm are baby steps at the moment we dont make leaps in quality it is an slow
- [x] incremental advance to more useful but not fundamentally changing workflows
- [x] jc69: agent native architectures
  - interesting to reread with the polotno agent in mind but I am not capable of that now
  - it is about how to use agents right
  - what agents are good at what you should and shouldn't let the agent do
  - how you should structure tools to play into the strengths of the llm
  - way too long though
- [x] continue here: https://registerspill.thorstenball.com/p/joy-and-curiosity-69#:~:text=From%20the%20same%20thought%2Duniverse%3A%20Rijnard
- [x] jc69: the code-only agent
  - the question is what if we only had one tool for your agents
  - what if the agent was not only able but enforced to use code to express its interactions with the
- [x] outer world
  - the code only tool enables the agent to use code to do anything:
  - read files
  - edit files
  - search files etc
  - you as a user can deterministically validate that the agent was doing the right thing
  - the agent and you can iterate on the code it wrote
  - my thoughts are split
  - this might be a similar thing to jais metaprogramming at compile time you can metaprogram you
- [x] program with an agent that writes the metaprogram to write the program
  - but what is the gain here
  - when you have multiple tools each tool best for what it was meant to do the tools are faster than
- [x] writing code they can do less but they are way faster give way better feedback and always give
- [x] expectable feedback to the agent
  - if you go code-only agent then you dont know what the agent will do next when you ask it to search
- [x] the file system will it use rg which is very fast or will it open all files in an async os walk
- [x] and search line by line taking up to 5 min on a big code base that it should work on then you see
- [x] ohh cool it is dump but deterministically dump but what does that help you isn't that reinventing
- [x] the wheel too much
  - my question is and I already thought about that might the code-only agent have a witness but the
- [x] witnessing makes the whole thing terribly slow?
  - might have to dabble on my own
- [x] jc 69: fly has build sprites
  - sprites are super fast sandboxes or cloud computers with checkpoints made for coding agents
- [x] jc 69: martin fowler
  - has spoken about how you can use agents to do tdd
  - red cycle green cycle
  - some of my prof are very red-green pilled
  - this leads to rather good outcomes good feedback loops
  - if you could tell the agents all the requirements at the start the agent would be able to build it
- [x] all
  - but since when do we know all the requirements at the start?
  - well we dont this is the problem we are facing right now
  - this is the problem some of the other blogs talk about
  - a good developer is not the man or woman that can code it all in every language possible
  - a good developer is the one that can steer 10 agents into the abyss while understanding what the
- [x] customer wants and how this is still making revenue
  - damn the new world is going to shit all the things that you work hard to be good at can be done by
- [x] agents
  - can they though
  - can you tell a 5 year old savant (fly blog) what to do when you don't know your own shit
  - I hardly think so
  - I still think being a good coder is a skill worth learning and a skill that is marketable even
- [x] more in the 20th century germany because when the germans start using ai to its fulles potentials
- [x] the others dont event touch an ide for 10 decades
  - damn do we even know stuff
  - are you not just a problem solving machine and the interesting part is what problems to solve with
- [x] what tool that makes us better than monkeys but at the heart we are still monkeys that code or let
- [x] an computer with a matrix on it code or we say hey you dont even have to code any more but why are
- [x] we all doing this funny game of this is the progress of the world
  - the day an agent saves a live is the day I think this is all not a huge game of some kind of crazy
- [x] people that think that all this matrix multiplication comes without a cost
  - agents dont build high performance games
  - they dont build durable reliable software humans do and whether they build something with a
- [x] screwdriver or a power tool they have to know how the wall and the hole works how to make the
- [x] screw stick and what screw to choose does it change the world? I am in an existential mood right
- [x] now!

# Thu 22 Jan 2026

- [x] CERN:
  - transkript is da
  - letter is bald da hoffentlich
  - texte sind angefangen fast fertig
- [x] dsm: Jai interpreter would stand the studenleistung part 2 and part 1 test
- [x] wif: fix the things that where mentioned in the feedback

- [ ] reading:
  - jc69: start
  - sean godecky read will be done
  - sean godecky next read out

```
siemens:
- Java Training
- Mathematics Course
- Cloud Storage and Virtualization (2022)
- Digitization
- Product Lifecycle Management
- SAP Client Training (2021–2024)
```

```
Virtual Badge intern
I interned as a software engineer at VirtualBadge.io, where I built an LLM agent that automatically creates certificates as an extension to the Certificate Editor.
```

```
Multi-agent, Storage-Systems, Distributed Systems, High-performance computing
Please elaborate briefly your experience of the chosen domain/s. Note you can also develop further in your CV and/or motivation letter. We also recommend you to include the specific skills (programming languages, hardware, databases etc.) that you have acquired in the previous page “Education” and “Experience” in order to increase your chances of being selected.(max 1440 chars) *
- I am particularly interested in high-performance computing
  - here I am learning about memory management strategies in different programming languges and how
to use them to get the best performance out of your programs
  - programming languages I particularly work with here are Rust, C, Jai, Odin, Zig
  - the languges provide a lot of power to the programmer and teach you how higher level languages
like python use cpu, gpu and memory under the hood
- in storage systems
  - i am familiar with a lot of data bases on a basic level
  - postgresql
  - mysql
  - oracle db
  - are all databases I worked with in a company setting
  - Most experience I have with sqlite3 from side project which are on my github (github.com/nkxxll)
  - aside from that I have build my own redis like database a key value store
  - an I have build my own in memory file storage once to understand how such an application would
work
- Distributed system
  - in university but also in my experience in the industry Distributed systems have always played a
roll
  - Eviden/atos applied the microservice architecture to lots of application which I learned to know
in my practical placements in the company
  - deutsche bank of course need to manage a lot of customer and transaction data which are
organized in microservice over the entire company
  - how to use these Distributed systems to increase performance (increase throughput and decrease latency) and decrease coupling
  - in my bachlors thesis I improved the performance of a system by scaling it vertically through docker containers
  - in the process I found out that the system even though it was build to scale vertically couldn't use the resources exhaustively
- in ai I am particularly interested in the role that coding agents will play in software
engineering and how to use agents of all kinds to actually make the most impact with them
- I really try to stay up to date with the latest developements and try to push the agents to their
boudaries
- it is interesting to me how those agents with shape the software industry and computers science in
the future
```

# Wed 21 Jan 2026

- [x] CERN: bewerbung
  - What is your motivation for applying for this job? (max. 1440 char.) \*
  - I want to come back to CERN learn more collaborate more
  - I have a strong interest in how things work because I believe that if you really understand how
- [x] things work then you can make the best out of it.
  - computers are a realm in which you can build everything.
  - sadly most software is not challenging to build not really there are challenges like
- [x] maintainability understanding the requirements of people right building the right thing
- [x] maintaining some quality standard in your project etc.
  - CERN has the unique mixture of very smart people and very hard problems to solve and I want to
- [x] grow on those hard problems
  - With the age of ai much software will not be written by humans any more but these hard problems
- [x] are still worth solving by hand and you can only solve them by hand
  - Storage technologies, high performance computing, multi-agent systems
  - Please elaborate briefly your experience of the chosen domain/s. Note you can also develop further in your CV and/or motivation letter. We also recommend you to include the specific skills (programming languages, hardware, databases etc.) that you have acquired in the previous page "Education" and "Experience" in order to increase your chances of being selected.(max 1440 chars) \*
  - I like to know how databases work on the inside as a matter of fact I built my own redis like
- [x] database and my own in memory file storage once
  - I am also very interested in performance oriented programming languages
  - at the moment I am working with JAI I am part of the closed beta it is very I opening how the
- [x] memory management is simplified in contrast to C or C++ while still maintaining very fast compile
- [x] times in contrast to Rust
  - any major operating system Windows, but especially MacOS and Linux
  - gaming computer building (hardware)
  - von neuman architecture computers
  - raspberry pi
  - Please give details of any interest (and ideally, experience) in specific topics (such as data acquisition, triggers, detector building, simulations, machine learning, quantum technologies...) or CERN experiments. (max 1440 chars) \*
  - several lectures in machine learing
  - I have build my own simple simulations with graphics libraries such as sdl2
  - I am highly interested in performant data acquisition and data processing
  - With which programming languages and operating systems are you familiar with? \*
  - I am familiar with most programming languages you dont have to get me up to speed in any
- [x] particular languages I will have to learn specific things for the job but syntax is not a problem
  - ... fill in all the languages i have worked with ...
  - With which databases are you familiar with? \*
  - mostly sqlite3 but also mysql, postgres, mongo, oracle
  - Please indicate your preferred dates of internship. Since lectures and workshops take place in July and August it is highly recommended to include these whole two months in your preferred dates. \*
  - whenever it fits most

```
I love computers and I love computer science. I want to work with people who care deeply about their field and who are motivated by learning, collaboration, and improving their work.

During my two weeks at CERN in the CBI A3 program, I experienced this environment firsthand. I learned a lot, but more importantly, I worked alongside students and researchers who were genuinely curious, open, and collaborative. That experience confirmed for me that CERN is the kind of place where I want to develop my skills.

The Summer Student Programme represents exactly what I am looking for: the opportunity to work on real technical problems, learn from experts in a team environment, and contribute meaningfully while continuing to grow as a computer scientist and software developer.
```

- [x] virtualbadge.io: abschlussmeeting ausmachen mit kenny
  - 29.1
  - um 4 auch den 4ten .2
  - ===> 4.2. 16 Uhr
- [x] reading:
  - jc68: finish (done)

# Tue 20 Jan 2026

- [x] jai: continue on the interpreter
- [x] vpn: eva.th-mannheim.de

# Mon 19 Jan 2026

- [x] dsm: papers lesen project root
  - hab das hoerbuch gehoert
- [x] jai:
  - look at modules/ImGui/generate.jai
  - look at modules/d3d11/generate.jai
  - for better generate examples

# Sun 18 Jan 2026

- https://registerspill.thorstenball.com/p/joy-and-curiosity-68#:~:text=I%20personally%20found%20this%20post%20by%20Ivan%20Zhao%2C%20CEO%20of%20Notion%2C%20very%2C%20very%20interesting.%20Yes%2C%20long%2Dform%20Twitter%20posts%20have%20a%20certain%20patina%20to%20them%20that%E2%80%99s%20hard%20to%20overcome%2C
- [x] Steam, Steel, and Infinite Minds
  - x post by Ivan Zhao CEO of Notion
  - link: https://x.com/ivanhzhao/status/2003192654545539400
  - interesting compares ai to the invention of the steam engine and the invention of steal and the
- [x] invention of the car
  - he sais we are still in the water mill phase (steam engine metaphor)
  - he has a 10x engineer (if those are real) which is now a 30x - 40x engineer because he
- [x] orchestrates 3 to 4 ai agents at the time
  - he can asynchronously make them do work when he is not there or sleeping or whatever
  - I like the metaphors but I dont like the background
  - he is ceo of notion
  - if notion misses the ai phase they die
  - they have to go full ai now or they might just miss the train
  - he speaks of workflows that are made for humans but we have to think of workflows made for ai
  - the problem the workflows are made for humans for a reason we have to think about the things to
- [x] understand them
  - we have to talk to each other to be up to speed if an ai agent holds another ai agent up to speed
- [x] the human still does not know that is going on
  - what I mean is yes there might be a bright future where we can use ai to its full potential but
- [x] ai is and will never do some things that humans have to do it can just relieve us of the pesky small
- [x] decisions that we have to face not the big ones not the design not the keeping each other in the
- [x] loop
  - at some point we will be limited by the capacity of the human that has to make the decision
  - that sucks but we cannot hand over all the things we do to the ai agents and hope they will build
- [x] cities without guidance that we want to have
  - the good thing is we need people with a vision for the future
  - one of those visions might be real but I think like always in the past 99% will fall hard
  - I want to be a very good programmer one of the best building products for people
  - I want to be able to solve tricky problems
  - doing the easy things good
  - being able to do the hard things
  - I have to learn to walk before I can jump into a car
  - good point from thosten 1 person startup vs even larger cooperations which ivan said in his post
- [x] rope:
  - rope impl in c is kind of finished
  - rope impl needs some cleaning up but I kind of dont want to do this in c I want to write jai at
- [x] least because it is way easier
- [x] jai rope: started
  - rope works but we have to also implement it in jai this is in c right now because I still have a
- [x] fear of writing jai on my mac
- [x] blog: writing to learn
- [x] blog: writing is a skill that dies with ai

# Sat 17 Jan 2026

- [x] jc 68: https://www.makingsoftware.com/chapters/shaders
  - what is a shader
- [x] > a shader is a type of program designed to run in parallel on the GPU
  - a shader just figures out what color a pixel should be
  - https://www.makingsoftware.com/chapters/shaders#:~:text=happen%20in%20sequence.-,How%20a%20GPU%20works,-Because%20shaders%20run
- [x] continue here
  - finished reading the shader blog very good did not get all the things right away but you can go
- [x] through it and piece by piece write a shader along side or many partial shaders
  - write a simple shader in jai? should be easy because it is made for this with opengl and so on

# Fri 16 Jan 2026

- [x] joy&curiosity 68: fertig
  - https://austinhenley.com/blog/canceledbookdeal.html canceling my first book deal
  - cool very nice break down of the writing process
  - interesting what a publisher wants in a book and why I would rather read blogs
  - they wanted to reduce the personality of the writer ... why this is why I read from this writer
- [x] not because of the content this is what I can get from any writer the personality the personal
- [x] insights into the topic
  - https://austinhenley.com/blog/challengingprojects.html uhhhh this is a banger
  - some of these project are perfect for jai
  - I kind of want to write an editor
  - editor in jai?
  - rope
  - gap buffer
  - piece table
- [x] rope:
  - the rope is a binary tree
  - the nodes have weights, left and right node
  - the leafs have strings which is the weight
  - the nodes store the weight of the left subtree why
  - because the weight is there to easily index into the tree
  - if you are at the top of the tree and you want to do something at index 5 you look at the weight
- [x] and say is it greater or less than 5 if it is not you go down to the left else you go to the right
  - if the total length is 11 split into 2 then you go to the right because the weight of the top node
- [x] is 5 so the index is not smaller the right holds the string from index 5-10 the left holds the
- [x] index from 0-4
  - example "Hallo Welt":

```
                        [ 6 ]
                       /      \
                  [ 4 ]        [ 2 ]
                 /     \      /     \
            [ 2 ]     [ O_ ] [ We ]  [ It ]
           /     \
        [ Ha ]   [ ll ]
```

- index(i) at node with weight w:
- if i < w → go left
- else → go right with index (i - w)
- Start at \[6\], index = 5
- [x] 1. 5 < 6 → go left
- [x] 2. At \[4\], index = 5
- [x] 3. 5 ≥ 4 → go right, index = 5 - 4 = 1
- [x] 4. At \[ O\_ \]
- [x] 5. return 'O\_'\[1\] i.e. space character
  - we have other operations
  - concatenate i.e. new parent node -> balence
  - split i.e. new parent node left and right from index
  - insert: split concate concate
  - delete: split -> right, delete_left; split(delete_left): right, delete, left; concate(right,
- [x] left)
  - to_string: in order traversal and string retrieval
  - for an editor you have to read the file that you want to edit
  - then you have to make a rope with n-length leafs (what should n be? I dont know)
- [x] joy&curiosity 69: start
- [x] jai: 4\*\* reading
- [x] jai: scope
  - the scope directives are the three following
  - scope_file
  - scope_export
  - scope_module
  - scope_file means the following functions are only visible inside the file scope
  - scope_export this is the default scope everything is visible in the global scope
  - scope_module this function is only visible inside the current modules scope if someone imports the
- [x] module she will not see the functions in this scope only other files inside the module that load
- [x] the module with `#load`

  - other imports also are only valid inside the scope e.g.

  ```jai
  #import "Basic";

  some_func :: () {
    print("hello");
  }
  // other file.jai
  #import,file "first_file.jai";
  some_func();
  print("hello");
  ^^^^^
  Error because print is not in scope!
  ```

- [x] -> qtaks: treesitter dependency
  - I learned something new you can generate bindings for c libs with `generate_bindings(...)`
  - look at `modules/Bindings_Generator/examples/first.jai` for docu have to look at this to make
- [x] binds for tree-sitter or work on the tree-sitter binds by `overlord-systems/jai-tree-sitter`

# Thu 15 Jan 2026

- [x] jai 400: build system
  - the jai build system is in jai
  - it is just a meta program that defines workspaces
  - a workspace is a thing that gets some options
  - optimization
  - whether its a dll or an executable
  - after the source code has been added to the workspace the compilation starts and options must not
- [x] be changed
- [x] mars: marc meeting 12 Uhr
  - questions wann is es zu ende? nach der praesi eigentlich
  - was ist das deliverable? praesi und bericht
  - willst du bei meiner end praesi dabei sein? ja
  - abgabe am schluss wird auch ein teil sein ^^
- [x] uni: studiengebueren (done)
- [x] syn linux:
  - damn you cannot mount the syn easy with the file manager that is sad
  - normal mounting is the thing it is just the linux way with the command line
- [x] qtaks:
  - realtive path works now
  - snapshot testing set up
  - more file types
  - tests
- [x] blog: ai blog needs to be done I think
  - or maybe not just write it down then decide
  - ai is a powerful thing and this is the funny thing about it
  - people how want to get better at it will get better at it they wont know everything that they do
  - but they dont have to because they know that they dont know everything
  - they will elide some things
  - and it wont matter because at their skill level it is just a matter of time then they could have
- [x] done it themselves
  - they still know what a good pattern is and what a bad pattern is because they have written it
- [x] 10000 times
  - when you dont know what a good pattern is and the pattern occurs maybe it is a pattern but not a
- [x] good one
  - you can't make a desertion you just take it and say that is good code it works and then you have
- [x] to explain to someone why you can figure out what is wrong with the codebase
  - and you search an error and the ai cant find the error and there is the problem you still have to
- [x] understand
  - this is why people say that ai is bad because they understand the code that it writes and they
- [x] know they could do better they can differentiate
  - so is ai a massive help
  - yes but you cannot hold the thing right when you cannot do the thing yourself
  - you can only make things faster you cannot hope that it will take all you decisions from you
  - it just makes the unimportant ones faster because it has seen the pattern it has ingrained them
  - it still makes big decisions wrong
  - you have to be the boss of the ai and this means like when you have a junior that is good you have
- [x] to give it direction in the bigger picture you have more important context it just has a lot of
- [x] context
  - you can give you decisions weight and reason it cant it does not know the bussiness it does not
- [x] know a lot of good software trades
  - it read the std lib of zig and gives it the same importance like toms super json
  - you can recognise that zig stdlib is one of the best pieces of software that there is to read
- [x] blog: build a snapshot framework with a stupid shell script
  - started that and it needs to be finished now
- [x] CERN: bewerbung
  - motivation:
  - I was at cern 2 week and it changed my life this sounds placative but it changed my life 5%
- [x] maybe but this is as much as 2 weeks can change your life. I see CERN as a big club of poeple that
- [x] love what they do. And that want to change something in the research in the world. And I love
- [x] computers I love working with computers and I want to learn from and with those people that love
- [x] their field as much as I love computer science.
  - I was at CERN 2 weeks and I loved it. I learned a lot and more important I meat a lot of people
- [x] just like me. That wanted to learn more, that love their field of work of reaserch and that want
- [x] to change something real do something siginficant and get better at what they do change the
- [x] field.
  - I was at CERN 2 weeks I became to know Richard. Who cofounded the web something that I work with
- [x] every day all day. And I learned more about the web and the start of network computing than in 2
- [x] months at university. I want to be at an institution that does those things I want to take part
- [x] in inventing the next web. I want to take part in the next thing that changes the world with my
- [x] knowledge in my field.
  - I love computers. I love Computer Science. I want to work with people who love what they do as
- [x] much as I do and who love to learn as much as I do. I know that they do because I had the chance
- [x] to see it for 2 weeks in the cbi a3 program. Since then I wanted to get a chance to come back.
- [x] blog: jai what does the programming language do that others dont
  - jai get just out of the way
  - jai is what c could have been if it was better and more developer focused
  - jai has a stdlib that is as good as zigs you can just read it from top to bottom and it makes
- [x] sense
  - no build system pain
  - dependencies are just there
- [x] wif: fix the things that where mentioned in the feedback
  - iso fuer maintainability (is es nicht weil das nur generelle metriken sind nicht exakte metriken)
  - language agnostic instead of independent
  - vllt eher der whitney u test wegen minmierung von bias der programmierer
  - fuer einen test entscheiden
- [x] embed neovim or an agent in the browser to code on the toilet (too risky security wise)
  - but if that thing was sandboxed and only could make prs to the repo
  - this would be very nice some thing in a virtual machine that can download anything and make prs
  - uff

# Wed 14 Jan 2026

- [x] gewerbe: Frau Haenel anrufen wegen dem Antrag tel: 06236 – 41 82 325 (done) papa hat angerufen
- [x] virtualbadge.io: meeting kenny irgendwann zeigen was gerade so laeuft
  - look at the todo.md in the project
  - we have a new direction or we have a direction
  - we can work to a goal now
  - the goal as always is to sell a workflow

# Tue 13 Jan 2026

- [x] pkv: rueckerstattung
  - rechnungsapp der continentale
  - rechnungsapp tan angefragt
- [x] geschenk: jani: pasta ostmann
- [x] qtaks: walk the file tree
  - zig version done
- [x] blog: was lsp the right choice (started)
- [x] gewerbe anmelden
  - bogen ausgefuellt und heruntergeladen
  - aber muss fuer beide bezahlen
  - hab deswegen noch nicht fertig gemacht
- [x] dsm:
  - expression koennen kein error werfen die machen nur null
  - statements: sind fuer control flow keonnen errors werfen
- [x] the overnight student:
  - writeup is comming here
  - this is a video about a book called the overnight student
  - it is about how to learn and understand things
  - write notes with pencils not with the computer
  - because you cannot type as fast as the teacher is speaking but you cannot spell that fast by hand
  - show relationship with the writing you are doing
  - stand up
  - your mind work faster if you stand up (is that a thing I dont know) @todo look that up
  - little by little teaching yourself the points on the notes that you have taken
  - byte by byte
  - read one atomic thing then turn around then teach an imaginary class about the thing you have just
- [x] read
  - out loud
  - because what you teach other people you understand
  - and the thing will be that you cant not put that into words
  - teaching others brings you into another mid state
  - if you forget something you look back but you will always start from the start of the byte side
- [x] portion
  - there are perls of wisdom of every page
  - the book is called the overnight student and it is about 5 bucks (euros hehe)
  - question: does the overnight student book have something to do with The Feynman Technique https://chatgpt.com/c/69668993-d258-8328-8459-7069f0ba0331
  - the overnight student is the base concept
  - the Feynman Technique is a specific technique an implementation of the concept
  - the common core is deep understanding makes you learn faster and it is easier to keep the
- [x] concepts in mind
  - you learn better by understanding rather than by memorizing
  - the Feynman technique is about writing a concept down in a simple to understand way as if you
- [x] would teach something @incomplete read the paper with doi: https://doi.org/10.32871/rmrj2109.02.06
  - what I think is: can you do the same thing with ai can you learn by thinking about a topic with an
- [x] imaginary partner that seams to know everything
  - you can test your understanding of the topic with ai because it either tells you you are wrong or
- [x] it tells you you are right at which point you wonder am i right because the ai is not always
- [x] correct
  - do really good people in programming become so good at it because they are writing about it event
- [x] though they don't always publish all their writing
  - is there a problem of writing in English compared to German when German is my mother tongue
  - is there a similarity in writing and programming do you get better in programming because you have
- [x] to explain a problem to the computer in a way that it understands
- [x] Jai: interfacing into c code study: https://github.com/copilot/c/c4fc51e7-03f6-47c0-ae63-899c9f154ef6

- [ ] qtaks: walk the file tree
- [ ] qtaks: jai: uppercase the tag; only take comments; only take specifc tags; file path relative to
  - focus on the jai version for now

# Mon 12 Jan 2026

- [x] rich hicky on ai: https://gist.github.com/richhickey/ea94e3741ff0a4e3af55b9fe6287887f
  - what a legend
  - what if we build a home and the second flour is built on cardboard
  - ai could be that cardboard glue that makes this possible but what if we need to go back to the
- [x] cardboard to build a stable house well we need to learn it any ways should you have to type
- [x] everything out, no. But where is the border to the land where you miss out on some learnings that
- [x] are important. How would you know what you dont know.
- [x] jc 68: damn i read this made no notes
  - https://chadnauseam.com/coding/random/calculator-app
  - build a calculator app should not be that hard but wait... you want to make a real calculator not
- [x] some middle school project in python (though python has bigints built in haha -- first step done)
  - very interesting solving strategy for big numbers and very cool that it is written in a way that
- [x] a non mathematician can understand
- [x] jc 68: mergiraf and on that note difftastic
- [x] jc 68: https://www.scd31.com/posts/programming-on-the-subway
  - coding on the subway what a post very cool
  - looking forward to the split keyboard glasses setup
- [x] running devcontainers with neovim: https://cadu.dev/running-neovim-on-devcontainers/
  - interesting but way too much work to do this
  - this should work out of the box nvim can be served as a remote session this should be possible
- [x] from the def container and the config should be able to live on the host machine
- [x] jc 68: ring buffers https://www.snellman.net/blog/archive/2016-12-13-ring-buffers/
  - ok you always waist an element
  - never wrote a ring buffer in prod myself
  - why not just add one field empty (and you don't have to the buffer indices tell you)
  - nobody knows
- [x] jc 68: https://andreasfragner.com/writing/three-ways-to-solve-problems
  - three ways to solve a problem
  - yes there are
  - but most of the people use 2 and 3 for not 90% of problems but the full 100% of all their problems
  - the perk is: there are no problems any more and nothing changes
  - so make it you have to use 2 and 3 for 80 to 90 percent of problems not more not less
  - and the choosing of what is to solve with 2 or 3 is not trivial in fact it is the hardest thing
- [x] there is
  - and this is the reason most startups fail because it is hard to find the right problems
  - it is very very hard in live to find the right problems to solve
- [x] jai: first program a doxygen like document parser:
  - parses only comments of a specific format like `// @<note type> (optional note)`
  - has the comment strings for different languages
  - parses the comments to a quickfix style, and or emacs compiler style list with line and file
  - can be used for sorted todo lists that can be reloaded and dynamically computed
  - can be used to add taged notes in all your programs and jump to them easily
  - either with grep `\/\/ @\w+ .*$` or with the list tool
  - mvp:
  - jai, c, c++, java, javascript, ... style //-comments
  - define tags
  - add option to sort -s/--sort by e.g. group "todo" or filetree and file line depth
  - add vim quickfix output format
- [x] fix the deploy of my website
  - fixed it jj messed up everything delete it with `rm -rf .jj`
  - reset the git log with `git reset --hard HEAD~2`
  - pushed force like we do it here
  - amp: buddy can you redo the font change
  - amp: yes of course
  - and changed the code theme
- [x] blog: why zig is for ai
- [x] laufen... 1:40 ca.
- [x] uni: eval swq
- [x] qtaks: basic zig and jai version for one file

# Sun 11 Jan 2026

- [x] jai: 100_polymorphic_procedures.jai
- [x] jai: 110_polymorphic_arguments.jai
- [x] jai: 115_auto_bakes.jai
- [x] jai: 120_polymorphic_structs.jai (nicht wirklich angeschaut aber ist denke ich intuitiv)
- [x] jai: 160_type_restrictions.jai (auch geskippet weil nicht so wichtig)
- [x] jai: 170_modify.jai
- [x] tree-sitter: built a simple c api example of the treesitter program that gets the main function from
- [x] a main.c file
- [x] jai: look at some examples

# Sat 10 Jan 2026

- [x] cv: udpaten fuer cern bewerbung
- [x] jai: 090_how_typechecking_works.jai
- [x] jai: 093_operator_overloading.jai
- [x] jai: 094_array_operators.jai
- [x] jai: 095_static_if.jai
- [x] jai: idea:
  - the ai helper cli
  - you can fzf a file with the fzf lib
  - you can then fzf the symbols in the file with treesitter
  - you can then get the file name and the range like this
  - `file @<path from project root> in symbol <symbol> from line <start> to line <end>`
  - `@<path from project root>`
  - `@<path from project root> lines <start> to <end>`
  - you can open the editor at the symbol
  - you can search symbols in the whole project
  - you can search only functions in the project
  - you can add custom treesitter querys in the config (nice to have)
  - you can copy to the clipboard (with #if cross platform)
  - basically an enhanced readline for the coding agents that copies to the clipboard
  - libs
  - readline
  - fzf or fzy or sk
  - treesitter
  - you can use an areana for the strings in the search because you can clear those directly after you
- [x] search and you search possibly multiple times in the workflow

# Fri 09 Jan 2026

- [x] jc 67: McCarthy: read the article about McCarthy https://www.smithsonianmag.com/arts-culture/two-years-cormac-mccarthys-death-rare-access-to-personal-library-reveals-man-behind-myth-180987150/
- [x] tree-sniffer: halstead metric einbauen (done)
- [x] jai: 85 default values
- [x] tree-sniffer: look at ratatui and crossterm for terminal applications in rust

# Thu 08 Jan 2026

- [x] wif:
  - cedric:
  - microservices
  - ist die datenverarbeitung cpu bound
  - kann man mit der ms architecture parallelisieren
  - ist das ziel performance?
  - implementierung
  - was sind die anforderungen
  - wie kann man das implementieren (was ist das artefakt was hier raus kommt)
  - horizontal scalieren
  - python muss ja nicht langsam sein
  - vergleich
  - etl mit nicht python monolitisch
  - e-t-l sind in einem job
  - latency
  - und durchsatz (bessere lastenverteilung)
  - methodik
  - expertengespraech
  - architektur entwicklung
  - lokaler test
  - mit syntetischen test daten
  - kann man validieren ob die daten repraesentativ sind
  - zero
  - probleme
  - transparenz
  - begriffe
  - Nutzerverifizierung
  - visualisierung
  - ux kann man einfacher verstehen
  - rq
- [x] 1. technische korektheit wie kann man mit llm daten (verarbeiten?)
- [x] 2. wie kann man die sicherheit der daten verbessern? visualisierung
- [x] 3. wie gut sind die visualisierungen von dem model
  - koennen korrekt sein aber nichts bringen
- [x] -
- [x] 4. wie koenne wir dem nutzer weis machen, dass bestimmte daten nicht vertrauenswuerdig sind
  - experten interview
  - user study
  - nasty
  - wie kann man tourismus daten nach aussen freigeben in universalen apis
  - herterogene bezeichnungen -> nlp?
  - es gibt schon beispiele aber mit verschiedenen daten formaten
  - orte problem genauigkeit
  - schlechte docu -> llms?
  - city sdk ist eine standartisierung in der eu
  - ohne echtzeit -> was macht den google aka crowd sourced
  - smart city gibt es schon aber nicht fuer tourismus
  - rest mit openapi
  - kann man aber auch graphql nutzen
  - bronze sliver gold layer architecture
  - wie bekommt man es hin dass man das fuer mehrere staedte zu machen ohne viele handarbeit
  - das ziel ist also eine api nicht wie man an die daten kommt differenzierung?
  - user tests? aber es gibt doch standards
- [x] ttykata: start and finish

# Wed 07 Jan 2026

- [x] ttykata: started with ttykata
  - started not tested just some vibe coding
- [x] lots of python programming today feels very unproductive
- [x] wif: Vortrag geuebt und paper noch mal gelesen
- [x] mars|vb: look at the docs that I wrote make a technical documentation like document not with all the
- [x] stuff but some that was important that were decisions that I took for reasons
- [x] vb: send image to model create certifcates that look like image
- [x] vb: make the tool suite for the agent
  - done that dont know which tool suite is better I dont know
- [x] vb: think of a way to make the comparison of the different tool suites and the models
  - I am just making it by hand right now
- [x] vb: meet with kenny
  - kenny is on vacation
  - meet with daniel he might also have an idea how to continue
  - daniel does not want to meet

# Tue 06 Jan 2026

- [x] keygli.de: very funny helix golf game
- [x] tree-sniffer: look what is still todo
  - used pprof-rs to profile the applicaton
  - found out that the query creation is a major problem and can be cached
  - performance is through the roof
  - adjusted the display of the table
  - found that cc is way to high for match statements in functional languages
- [x] wif: finish presentation
  - been there done the llm part have to write some things down
  - done
- [x] blog: write about how ai makes me feel
  - **note** didn't write that
  - makes me feel stupid as fuck
  - makes me feel smart as fuck at the same time
  - makes me feel confident makes me start makes me work harder longer
  - makes me care about one layer up of decisions
  - makes me care about the price of software
  - makes me care about developer tooling and what the future of that is
- [x] salad: research
  - oil nvim is the thing that I use
  - mini files is the base of the architecture
  - chat gpt worked out the requirements that would be fine here are mine:
  - open dir in a simulated normal mode
  - walk dir with
  - enter goes into a dir
  - "-" goes out of a dir i.e. one dir up
  - "i" goes into insert mode i.e. open the editor of choid on the current dir
  - if the editor is closed the file actions are synced
  - the file tool is back in normal mode
  - have to be able to move the file tree and change dirs then move further
  - thought: is this the right thing to do?
  - thought: shouldn't that be built into your editor?

# Mon 05 Jan 2026

- [x] dsm: studienleistung ist done
  - lief gut bissel gechocked by den kleinigkeiten
  - hx lief gut
  - works just out of the box with ocaml wild
  - could move easily in the file
  - soll darueber nachdenken wie man eine interne api benutzen kann um weniger code im compiler zu benutzen
- [x] mars: write marc about meeting(done)
- [x] mars: write meeting notes for mars meeting
  - bisher
  - requirements geklaert
  - architecture ausgearbeitet
  - documentiert siehe pdfs markdowns in repo
  - frontend fuer testing geschrieben
  - backend fuer frontend geschrieben
  - mcp fuer llm in backend geschrieben
  - getested ob das moeglich waere
  - dann
  - backend neu geschreiben in python
  - backend mit openai agent sdk ausgestattet
  - agent geschrieben erst mit komplizierter architecture jetzt einfacher
  - frontend mit chat interface angepasst
  - websocket communication between frontend and backend
  - tools fuer das veraendern von json strukturen geschrieben
  - jetzt
  - plan
  - tools anpassen
  - tools sind zu klein jeder tool call ist ein round trip wir haben gerade ein sehr
- [x] teures aber funktionierendes model
  - groessere tools schreiben vllt das llm auch direkt json structuren schreiben lassen und nur die
- [x] validierung auslagern in ein tool
  - vergleichen wie "gut" die changes sind
  - ein actinable berichtartiges document schreiben ueber, das was ich gelernt hab
- [x] The Feynman Technique: How to learn anything https://abhishekpathak.substack.com/p/the-feynman-technique-how-to-learn
  - you have to be able to explain it in simple words to a non subject native
  - if you can't you havn't understand it
  - so to learn something you have to write down all the knowledge you gained as if you wanted
- [x] to explain it to someone
  - then try to explain it to a 6 year old
  - or try to explain it in front of a mirror
  - where you go into jargon
- [x] helix tutor:
  - very interesting
  - i like the mulicursors
  - i like the mnemonic of the default keymaps
  - i also like that the keymaps are not a tree of multiple possibilities but as flat as possible
  - i like the snappy feel
  - I will have to unlearn a lot of muskle memory with the editor but a lot will stick like
  - hjkl
  - c-w mode
  - select delete line also when it is with xd now
  - what wont be easy will be
  - G -> ge
  - c-^ -> ga
  - file picker
  - delete lines
  - delete char from x to d
  - remove selection this is something i wouldn't have to think about
  - I have to give it some time one or two weeks
  - I wont loose anything in the mean time
  - most of the typing is still typing like normal
  - most of the moveing is still moving like normal
  - feels snappy feels fast makes fun
  - have to learn new strategies now

# Sun 04 Jan 2026

- [x] joy & curiosity 68
  - been reading Kent beck on changing the context of code review
  - very insightful lots of truths there async does slow you down
  - the context gets lost it is not going with the time
  - code rabbit as fast reviewer is interesting
  - pair programming might be even a better form of review also right now
  - industrialization of Software:
  - new kind of software: software created with no durable expectation of ownership, maintenance, or long-term understanding.
  - but this is software not only of low cost but also of low value
  - what tends to get lost is that the running cost of a machine is low
  - the running cost of ai is high
  - you can’t maintain
  - you have low quality (without good engineering which is not industrial any more)
  - paints an interesting picture though why swe might go into just another level of productivity and not into junk and boutique software

# Sat 03 Jan 2026

- [x] tree-sniffer: interactive mode display
- [x] vortrag: Prasentation Ihres Themas
  - Basierend auf Ihrem Expose
  - Initiales Expose geschrieben
  - Feedback von Betreuendem erhalten
  - Feedback eingearbeitet
  - Diskussion (nach Prasentation)
  - Feedback von Prof. Leuchter und Prof. Nagel
  - Feedback von Ihren Kommilitonen
  - 4-5 Teilnehmende pro Woche. Pflicht fur alle. Aufbau Seminar
  - Vorstellung (10 Minuten)
  - Thema / Motivation
  - Fragestellung / Forschungsfrage
  - Literatur / Stand der Wissenschaft
  - Methodik (u.a. Auswahl und Begrundung, Passung, Planung, Auswertung)
  - Zusammenfassung
  - Diskussion (5 Minuten)
  - Insgesamt: 15 Minuten
- [x] wif: name the contribution
- [x] seangoedecke: blog https://www.seangoedecke.com/2025-wrapup/
  - interesting
  - the blog is becoming expensive
  - he is paying for statistics on his blog
  - 60$ a year on https://plausible.io/ plausible
  - and a 6$ netlify plan because of the traffic his blog gets
- [x] netlify.com seams nice
  - there is a free plan with 300 "credits"
  - which is enough for a blog that nobody reads like mine
  - there is excellent astro support -> I like
- [x] sidequest... annotating stuff
  - https://chatgpt.com/c/69599e90-21f4-8329-b85c-563642426e1f
  - because of the McCarthy blog about his home and lots of books with _annotations_
- [x] joy & curiosity 68
  - got stuck with McCarthy here https://www.smithsonianmag.com/arts-culture/two-years-cormac-mccarthys-death-rare-access-to-personal-library-reveals-man-behind-myth-180987150/#:~:text#genius%20with%20schizophrenia.

# Fri 02 Jan 2026

- [x] dsm:
  - finsish second part of requirement (done)
  - email for test (done)
- [x] die gruene neuhofen

- [ ] tree-sniffer funcitonal:
  - need to test with ocaml or haskell projects
  - fixed the tree-sniffer ocaml plugin shows that the complexity of a big project is lower than big
- [ ] c project
- [ ] wif: read feedback
  - feedback read
- [ ] > A very ambitious and interesting project. In my opinion, R1 is not an a research question but a way to contribute to answering R2.

- [ ] > For the methodological step E (empirical evaluation) there is no external criterion on
- [ ] > maintainability, as far as I understand: You select software systems and apply your newly developed
- [ ] > tooling which indicates some maintainability issues. But there is no "ground truth" about the
- [ ] > maintainability of the selected software systems that you can relate your findings to.
  - main point here is what is the right name for the contribution of the master thesis

# Thu 01 Jan 2026

- [x] tree-sniffer: display
  - tested smart mode on display
  - smart mode seams to be not that smart
  - disclosure I am using rust
  - I am giving it very strict requirements to work with
  - I am not leaving it room for self exploration
  - it seams not as sharp as free mode actually with good requirements
  - maybe I have to leave it off the leash
- [x] tree-sniffer: refactor
  - queries
  - metrics computation
  - internal data structure for metrics (hashmap by file -> hashmap by function)
- [x] tree-sniffer: validation script
- [x] NUC: Next Unit of Computing i.e. mini pc fuer hans
  - asus hat intel nucs
  - geekom hat amd und intel nucs
  - hp hat auch welche
  - dreamquest
  - preis ist so 400 - open (ca. 1000)
- [x] home assistant is the software for this fun
  - you can set timers with it
  - it is offline
  - it can control smart home devices
  - it can be installed on a raspberry pi (should be 4 though)
  - you need a microphone
  - you dont need ai if the sentences are stable
  - if you want intent detection you need to run a model on the pi or in the cloud

# Wed 31 Dec 2025

- [x] added function stats (done that)
  - code
  - blank
  - comment (does not work: test sqlite3.c)
- [x] started to work on cyclomatic complexity

# Tue 30 Dec 2025

- [x] analytical philosophy: https://chatgpt.com/c/69507e4b-5430-832f-af31-9ac62b133ff2 look at the
- [x] literature list
- [x] tree-sniffer: display
- [x] tree-sniffer: add new metrics
  - look at average line of code per function
  - look at other common metrics
  - add the most common
- [x] tree-sniffer: add functional language like ocaml
  - added haskell and ocaml

# Mon 29 Dec 2025

- [x] tree-sniffer: display
  - display research
  - metrics choice
- [x] jai next chapters

# Sun 28 Dec 2025

- [x] tree-sniffer: find functions
  - done with the query: "(function_definition) @function"
- [x] tree-sniffer: parse c file
  - also done was harder than expected rust types and so
- [x] tree-sniffer: download repo
  - done with some help of gemini which gets pretty easy stuff but make some dump errors does not
- [x] "think for itself" like amp
  - repos can be downloaded with depth one and files are computed
- [x] muscm: read lua interpreter code (partial understanding)
- [x] did tweak some more neovim stuff (dup line, dup line comment)
- [x] continue here now in how_to/042_using.jai:1:1 (done)

- [ ] # Fri Dec 2025
- [ ] 027_if_case.jai
  - done
- [ ] 030_any.jai
  - done
- [ ] newtype datastructure trees in arrays with indexes matklat - have to look into that: looking into
- [ ] that https://matklad.github.io/2018/06/04/newtype-index-pattern.html
  - done was fun is now part of the muscm interpreter
  - is a very cool pattern for rust cyclic data structures
  - additionally all the structures are in one place which makes the caching more efficient
- [ ] lua interperter full implementation and test
  - did I learn something here ... no
  - was it fun ... maybe
  - lua interpreter can now run the ascii art demo
  - this was easier than expected
  - interpreter improvements
- [ ] newtype linked list implementation
- [ ] compilecommand for rust
- [ ] amp.nvim
  - interesting for selections but are selection so much better than what I have right now
- [ ] vim compiler and makeprg investigation
- [ ] set cargo check as make prog for rust
- [ ] tree-sniffer
  - master thesis pre project to see how it works
  - uses anyhow, clap, tree-sitter, tree-sitter-c (for now), url, git2
  - goal is to be able to give it an URL and it goes downloads the repo either to temp or persistent
- [ ] storage and measures code metrics
- [ ] started to look into analytical philosophy

  - https://chatgpt.com/c/69507e4b-5430-832f-af31-9ac62b133ff2

- [ ] # Fri Dec 2025
- [ ] look at svgs
  - yes
  - you can js in that thing
  - you can make pictures in that thing
  - you can change the way e.g. excalidraw svgs look in that thing
  - you can do everything in that thing and pdf can render it
- [ ] nvim config made the makeprg automation that I wanted all the time
  - mm make ml make local make prg mp make global make prg
  - ta add a todo to the todo.txt that has a filename:line:col
  - tt load the todo.txt to the qflist
- [ ] jai
  - 020_type_info.jai
  - 022_if.jai
  - 025_ifx.jai
  - 027_if_case.jai
  - partially noted point down in todo

# Wed Dec 24 2025

- [x] toad
  - an cli app ai integration for the command line that works with several coding agents and lets you
- [x] run full tui applications while talking to an agent very cool
- [x] codebase from an agent for an agent https://ampcode.com/by-an-agent-for-an-agent
- [x] DVTUI
  - basically what I wanted to do with the shader application that I wrote with PPMs
- [x] write to escape the default settings https://kupajo.com/write-to-escape-your-default-setting/
  - very good article about writing
  - should I write about me myself and I
- [x] https://friendlybit.com/python/writing-justhtml-with-coding-agents/ just html
  - lessons learned from writing an html parser with agents
- [x] some more work on the lua nom parser
- [x] some nvim telescope grep stuff
- [x] newtype datastructure trees in arrays with indexes matklat
  - have to look into that
  - the rust version: https://matklad.github.io/2018/06/04/newtype-index-pattern.html
  - the zig version: https://matklad.github.io/2025/12/23/zig-newtype-index-pattern.html

# Wed Dec 24 2025

- [x] look at mermaid
  - very cool very easy to use for e.g. flow charts
  - similar to plant uml
- [x] look at treesitter
  - initial look
  - you can include either the library to a c compatible program or you can use the treesitter cli
  - should start to play with the treesitter cli some day for the master thesis
- [x] jai 015, 018, 080, 094
- [x] klimmies
- [x] look at itertools rust
- [x] https://www.youtube.com/watch?v#utyBNDj7s2w
- [x] https://www.seangoedecke.com/nobody-knows-how-software-products-work/
- [x] nom tokenizer for lua
- [x] nom parser for lua
  - nom parser for lua started little problem currently with the implementation of the Input trait for
- [x] `&[Token]` because my input is not `&str`
- [x] fix fucking telescope issue

# Mon Dec 23 2025

- [x] jai 010 - 015
  - enums are basic use #specify to have to use ints for save serialization
  - jai's temp storage basically a mem arena for small bits of memory great feature
  - love the mem management of jai so far
  - context is a beast where you can change out the allocator, temp storage, logger
  - it is passed to every scope
  - you can modify it and push a new context with #context_push <new> {}
- [x] jai Preload
- [x] look at Printercow
  - basically a raspi os for printing
- [x] look at nom rust
  - initially looked at nom did not really do some things my self amp took over
  - very similar to angstrom

# Mon Dec 22 2025

- [x] jai 007
- [x] adventskalender day 23
- [x] adventskalender day 24
- [x] jai 008 - 010

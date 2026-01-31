"""Default configuration for notes tagger."""

import json
from pathlib import Path
from typing import Optional

from notes_tagger.models import Config, ModelType

DEFAULT_CONFIG = Config(
    topics={
        "programming": "Writing code in Go, Rust, Zig, or Python. Debugging issues and refactoring code to use better patterns. Software development and coding projects.",
        "compilers": "Building compilers, lexers, and tokenizers. State machines for lexical analysis. Parsing, ASTs, and code generation. Language implementation in Zig or C.",
        "algorithms": "Implementing algorithms and data structures. Sorting, searching, graphs, trees, and hash tables. Big O complexity and optimization techniques.",
        "concurrency": "Multithreading, async/await, and parallel programming. Race conditions, mutexes, channels, and synchronization. Goroutines, Tokio, or threading libraries.",
        "testing": "Writing unit tests, integration tests, and end-to-end tests. Test-driven development and mocking. pytest, Jest, or Go testing patterns.",
        "cli-tools": "Building command-line tools and scripts. Argument parsing, terminal output, and shell scripting. CLI applications in Python, Go, or Rust.",
        "graphics": "Computer graphics, rendering, and game development. OpenGL, WebGL, shaders, and game engines. 2D and 3D graphics programming.",
        "embedded": "Embedded systems and microcontroller programming. Arduino, Raspberry Pi, and bare-metal code. Hardware interfaces and low-level C.",
        "functional": "Functional programming patterns and concepts. Immutability, pure functions, monads, and composition. Haskell, Elixir, or functional style in other languages.",
        "web-dev": "Building frontend applications with React, Vue, or Svelte. Working with HTML, CSS, and JavaScript. Browser APIs, DOM manipulation, and responsive design.",
        "backend": "Building server applications and REST APIs. Working with Node.js, Django, FastAPI, or Express. Authentication, middleware, and GraphQL endpoints.",
        "full-stack": "End-to-end application development connecting frontend to backend. Deploying full applications and integrating all layers of the stack.",
        "mobile": "Building mobile apps for iOS or Android. Using React Native, Flutter, Swift, or Kotlin. Touch interfaces and responsive mobile design.",
        "systems": "Operating systems, kernels, and low-level programming. Memory management, processes, threads, and scheduling. File systems and device drivers.",
        "networking": "Network protocols like TCP/IP, HTTP, and DNS. Socket programming and distributed systems. Understanding latency, bandwidth, and network architecture.",
        "databases": "Working with SQL and NoSQL databases. Query optimization, indexing, and transactions. Data modeling with PostgreSQL, SQLite, or other databases.",
        "security": "Cryptography, encryption, and hashing. Authentication and authorization systems. Finding vulnerabilities and writing secure code.",
        "machine-learning": "Training neural networks and deep learning models. Working with embeddings, transformers, and NLP. Classification, inference, and model optimization.",
        "theory": "Turing machines and complexity classes like P and NP. NP-complete problems like SAT and Clique. Polynomial reductions, decidability, and Rice's theorem. Automata and formal languages.",
        "architecture": "Designing scalable systems with microservices. Load balancing, caching strategies, and API design. Software design patterns and system architecture.",
        "devops": "Setting up CI/CD pipelines and containerization. Working with Docker and Kubernetes. Infrastructure, deployment, monitoring, and observability.",
        "finance": "Budgeting, accounting, and financial planning. Tracking revenue, expenses, and costs. Financial forecasts and money management.",
        "meeting": "Meeting notes with attendees, agenda items, and action items. Discussions, decisions made, and follow-up tasks.",
        "ideas": "Brainstorming new ideas and creative proposals. Things to explore later, project ideas, and innovative thoughts.",
        "research": "Reading academic papers and investigating topics. Running experiments and analyzing results. Literature review and research notes.",
        "planning": "Creating roadmaps and project plans. Scheduling, prioritization, and setting milestones. Future plans and task organization.",
        "learning": "Studying for exams and taking courses. Klausur preparation and practice problems. Tutorials, educational content, and knowledge acquisition.",
    },
    threshold=0.25,
    max_tags=3,
    model_name=ModelType.MPNET,
    cache_dir=str(Path(__file__).parent.parent / "cache"),
    device=None,
)


def load_config(path: Optional[str] = None) -> Config:
    """Load config from JSON file or use defaults."""
    if path is None:
        return DEFAULT_CONFIG
    
    with open(path) as f:
        data = json.load(f)
    return Config(**data)

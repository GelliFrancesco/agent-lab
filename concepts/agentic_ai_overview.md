# Agentic AI — Concepts Overview

> A mental model for understanding what AI agents are, how they work, and how to build with them.

---

## 1. What is an AI agent?

A traditional language model interaction is a single exchange: you send a prompt, the model replies. That's it.

An **AI agent** is different. It's a system where the model can:
- **take actions** (run code, call APIs, read files, browse the web)
- **observe results** from those actions
- **reason** about what to do next
- **loop** until the task is complete

The key insight is that the model isn't just generating text — it's participating in a process with real-world consequences. The model becomes the "brain" of a system that can actually do things.

A useful mental model: think of an agent as an employee who receives a task, has access to certain tools and information, and is trusted to figure out the steps needed to get it done — rather than being told exactly what to do at each turn.

---

## 2. The agent loop

Most agentic systems follow a core loop, sometimes called a **ReAct loop** (Reason + Act):

```
┌─────────────────────────────────────┐
│                                     │
│   1. Receive task / observe state   │
│              ↓                      │
│   2. Reason: what should I do?      │
│              ↓                      │
│   3. Act: call a tool or respond    │
│              ↓                      │
│   4. Observe the result             │
│              ↓                      │
│   5. Loop back to step 2            │
│      (or finish if task is done)    │
│                                     │
└─────────────────────────────────────┘
```

Each cycle through this loop is sometimes called a **turn** or a **step**. The number of steps an agent needs is variable — some tasks take one, others take dozens.

---

## 3. Tool use (function calling)

The primary mechanism by which agents act on the world is **tool use** (also called function calling).

Here's how it works at a high level:

1. You define tools as JSON schemas — name, description, input parameters
2. You include those definitions in your API call
3. The model decides whether to call a tool, and if so, which one and with what arguments
4. Your code executes the tool and returns the result
5. You send the result back to the model, which continues reasoning

Example tools you might give a Claude agent:
- `search_web(query)` — returns search results
- `read_file(path)` — returns file contents
- `run_python(code)` — executes code and returns output
- `send_email(to, subject, body)` — sends an email
- `query_database(sql)` — runs a SQL query

The model never directly executes tools — **your code does**. The model just says "call this tool with these arguments," and you handle the actual execution. This keeps you in control.

---

## 4. The context window

Everything the model knows about the current task lives in its **context window** — the input it receives on each API call.

For agentic tasks, the context window typically contains:
- The **system prompt** — instructions, persona, constraints, available tools
- The **conversation history** — all prior messages and tool results
- The **current task** or user message

Context windows have limits (measured in tokens — roughly ¾ of a word each). For long-running agentic tasks, you need to think about how you manage context: what to keep, what to summarize, what to drop.

Claude's context window is very large (up to 200K tokens for some models), which helps, but context management is still an important design concern for complex agents.

---

## 5. Memory types

Agents can have several kinds of "memory":

| Type | What it is | Example |
|---|---|---|
| **In-context** | Information in the current context window | Conversation history, tool results |
| **External (retrieval)** | A database the agent can search | A vector store of documents |
| **In-weights** | Knowledge baked into the model | Claude's training data |
| **In-cache** | Saved computation for repeated prompts | KV cache for static system prompts |

For most applications, you'll work with in-context memory and external retrieval. Understanding the difference matters because in-context memory is temporary (gone when the session ends) while external memory persists.

---

## 6. Orchestration patterns

As you build more complex systems, you'll encounter different ways of arranging agents:

### Single agent
One model, one loop. Good for most tasks. Simple to build and debug.

```
User → [Claude] → Tool calls → Result → User
```

### Agent with subagents
A primary "orchestrator" agent delegates to specialized subagents. The orchestrator decides what to do; subagents handle specific capabilities.

```
User → [Orchestrator] → delegates to → [Researcher Agent]
                                    → [Coder Agent]
                                    → [Writer Agent]
```

### Parallel agents
Multiple agents work simultaneously on independent subtasks, then results are combined.

```
Task → [Agent A] ──┐
     → [Agent B] ──┼→ [Combine] → Result
     → [Agent C] ──┘
```

### Pipeline (sequential)
Each agent's output is the next agent's input. Good for structured workflows.

```
[Data Collector] → [Analyzer] → [Summarizer] → [Formatter] → Output
```

Each pattern has trade-offs. Single agents are easiest to reason about. Multi-agent systems can be more powerful but introduce coordination complexity.

---

## 7. Prompt engineering for agents

Agents are sensitive to how they're instructed. A few principles that matter more in agentic settings than in simple Q&A:

**Be explicit about the task and goal.** The model needs to know what "done" looks like, not just what to do next.

**Define the scope of authority.** What tools can it use? What decisions can it make autonomously vs. pause and ask for? What should it never do?

**Specify output format.** If the agent produces structured output (JSON, markdown, etc.), say so clearly.

**Include examples for edge cases.** Agentic tasks often encounter unexpected situations. A few examples of how to handle them goes a long way.

**Think about failure modes.** What should the agent do if a tool fails? If it's uncertain? If it reaches a decision point it wasn't prepared for?

---

## 8. Safety and control

Giving an AI agent the ability to take actions introduces real risks. A few principles:

**Minimal footprint** — give the agent only the tools and permissions it actually needs. Don't give it database write access if it only needs to read.

**Human in the loop** — for high-stakes or irreversible actions, build in a confirmation step before the agent proceeds.

**Logging and observability** — record every tool call and result. You need to be able to see what happened if something goes wrong.

**Sandboxing** — when agents run code, run it in an isolated environment (a container, a VM) so it can't affect your production systems.

**Prompt injection awareness** — agents that read external content (web pages, files, emails) can be manipulated by adversarial content embedded in that content. Be aware of this attack vector.

Anthropic publishes guidelines on agentic safety here: https://docs.anthropic.com/en/docs/build-with-claude/agentic-systems

---

## 9. Where to go from here

Once you have the basics down, interesting areas to explore:

- **Retrieval-Augmented Generation (RAG)** — giving agents access to large knowledge bases by searching at query time
- **Code execution** — agents that write and run code as a first-class capability
- **Multi-modal agents** — agents that can see images, read PDFs, process audio
- **Long-horizon tasks** — managing state across very long tasks that span hours or days
- **Model Context Protocol (MCP)** — Anthropic's open standard for connecting agents to tools and data sources

See `resources/learning_resources.md` for specific links on all of these.

---

*Next: check out `glossary.md` for quick definitions of the terms used here.*

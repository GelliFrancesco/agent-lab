# Learning Resources

A curated collection of links for going deeper on Claude, the Claude API, and agentic AI. Organized from foundational to advanced.

---

## Official Anthropic documentation

The primary source of truth. Well-written and regularly updated.

| Resource | URL | Notes |
|---|---|---|
| Anthropic docs home | https://docs.anthropic.com | Start here |
| Claude models overview | https://docs.anthropic.com/en/docs/about-claude/models/overview | Current model names, context windows, pricing links |
| API reference | https://docs.anthropic.com/en/api | Full REST API spec |
| Quickstart guide | https://docs.anthropic.com/en/docs/quickstart | Get a working API call in under 5 minutes |
| Messages API | https://docs.anthropic.com/en/api/messages | The core API endpoint |
| Prompt engineering overview | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview | How to write effective prompts |
| Tool use (function calling) | https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview | The main guide for giving Claude tools |
| Agentic systems guide | https://docs.anthropic.com/en/docs/build-with-claude/agentic-systems | Orchestration, safety, best practices |
| Vision (image input) | https://docs.anthropic.com/en/docs/build-with-claude/vision | Sending images to Claude |
| Extended thinking | https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking | Claude's deep reasoning mode |
| Streaming | https://docs.anthropic.com/en/docs/api-features/streaming | Getting token-by-token output |

---

## API console and account

| Resource | URL |
|---|---|
| Anthropic Console | https://console.anthropic.com |
| Get an API key | https://console.anthropic.com/settings/keys |
| Usage and billing | https://console.anthropic.com/settings/billing |
| Rate limits | https://docs.anthropic.com/en/api/rate-limits |

---

## SDKs

Anthropic maintains official SDKs so you don't have to hand-craft HTTP requests.

| SDK | URL |
|---|---|
| Python SDK | https://github.com/anthropics/anthropic-sdk-python |
| TypeScript/Node SDK | https://github.com/anthropics/anthropic-sdk-typescript |
| Python SDK on PyPI | https://pypi.org/project/anthropic/ |

Install the Python SDK:
```bash
pip install anthropic
```

---

## Model Context Protocol (MCP)

MCP is Anthropic's open standard for connecting AI agents to tools and data sources. Worth learning once you're comfortable with basic tool use.

| Resource | URL |
|---|---|
| MCP official site | https://modelcontextprotocol.io |
| MCP specification | https://spec.modelcontextprotocol.io |
| MCP GitHub | https://github.com/modelcontextprotocol |
| Anthropic's MCP announcement | https://www.anthropic.com/news/model-context-protocol |
| MCP Python SDK | https://github.com/modelcontextprotocol/python-sdk |

---

## Key papers

Research papers behind core concepts. You don't need to read all of these — but skimming them gives you a deeper understanding of why things work the way they do.

| Paper | What it covers |
|---|---|
| [Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762) | The Transformer architecture that underlies all modern LLMs |
| [ReAct: Synergizing Reasoning and Acting in LLMs (2022)](https://arxiv.org/abs/2210.03629) | The foundational agent loop pattern (Reason + Act) |
| [Toolformer (2023)](https://arxiv.org/abs/2302.04761) | Teaching LLMs to use tools via self-supervised learning |
| [Constitutional AI (2022)](https://arxiv.org/abs/2212.08073) | Anthropic's approach to training helpful, harmless AI — the basis for Claude |
| [Retrieval-Augmented Generation (2020)](https://arxiv.org/abs/2005.11401) | Foundational RAG paper from Meta AI |
| [Chain-of-Thought Prompting (2022)](https://arxiv.org/abs/2201.11903) | Getting models to reason step-by-step |

---

## Anthropic blog posts and announcements

| Post | URL |
|---|---|
| Introducing Claude | https://www.anthropic.com/news/introducing-claude |
| Claude's model card | https://www.anthropic.com/claude/model-card |
| Anthropic's core views | https://www.anthropic.com/research/core-views-on-ai-safety |
| Building effective agents | https://www.anthropic.com/research/building-effective-agents |

---

## Prompt engineering — deeper reading

| Resource | URL |
|---|---|
| Anthropic's prompt library | https://docs.anthropic.com/en/prompt-library/library |
| Prompt engineering guide | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview |
| Few-shot prompting | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-examples |
| Chain of thought | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought |

---

## Example repos and cookbooks

| Resource | URL |
|---|---|
| Anthropic Cookbook | https://github.com/anthropics/anthropic-cookbook |
| Claude quickstarts | https://github.com/anthropics/anthropic-quickstarts |
| Tool use examples | https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use |
| MCP servers (official) | https://github.com/modelcontextprotocol/servers |

The Anthropic Cookbook is especially useful — it's a collection of Jupyter notebooks showing real patterns for RAG, tool use, multi-agent systems, and more.

---

## Community and support

| Resource | URL |
|---|---|
| Anthropic developer forum | https://forum.anthropic.com |
| Anthropic on X/Twitter | https://x.com/AnthropicAI |
| Claude subreddit | https://reddit.com/r/ClaudeAI |
| Stack Overflow (anthropic tag) | https://stackoverflow.com/questions/tagged/anthropic |

---

## Recommended learning order (beginner)

1. Read the [Quickstart guide](https://docs.anthropic.com/en/docs/quickstart) — get something running
2. Understand [prompt engineering basics](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
3. Work through [tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) — the foundation of agents
4. Explore the [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) for real examples
5. Read [Building effective agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic's own guidance on agent design
6. Try the [Agentic systems guide](https://docs.anthropic.com/en/docs/build-with-claude/agentic-systems) for orchestration patterns
7. Explore MCP when you're ready to build something real

---

*Last updated: April 2026. Anthropic's docs evolve quickly — always check the official site for the latest.*

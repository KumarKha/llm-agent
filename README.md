# Local Autonomous AI Agent (Edge-Hub Architecture)

An enterprise-grade, distributed AI agent framework that implements a true autonomous **Perception-Action Loop** utilizing local LLMs. The architecture is split across a low-power edge node (Raspberry Pi) handling lightweight intent classification and an optimized hardware hub (RTX 5070 Desktop) executing multi-step reasoning, dynamic tool selection, and local API orchestration.

Rather than relying on bloated wrapper libraries, this system was engineered from the ground up using native Python primitives to maximize performance, control context inflation, and maintain local data privacy.

---

## Architecture Overview

```
[ Raspberry Pi Edge ] --- (POST /api/orchestrate) ---> [ Desktop Hub Gateway ]
 (Llama 3.2 1B / 3B)                                          │ (FastAPI)
  • Intent Routing                                            ▼
  • Budget Allocation                             [ Core Perception Loop ]
                                                    (Qwen 2.5 7B / Llama 3)
                                                              │
                                        ┌─────────────────────┴─────────────────────┐
                                        ▼                                           ▼
                            [ Custom Memory Stream ]                       [ Extensible Toolkit ]
                               • Sliding-Window JSONL                       • Brave Context API
                               • Token VRAM Protection                      • Google Calendar/Tasks (OAuth)
```

---

## Core Features

- **Autonomous Perception-Action Loop:** Replaces rigid linear inference pipelines with a continuous `while True` execution loop, empowering the model to evaluate tool results, self-correct, and chain actions recursively.
- **Edge-Hub Distributed Compute:** Offloads raw triage to an always-on Raspberry Pi. Complex workloads dynamically spin up heavy local LLM context windows on an RTX 5070 desktop hub, gracefully flushing graphics card VRAM upon completion.
- **VRAM-Optimized Memory Stream:** Implements a sliding-window message-turn extraction system utilizing a custom JSONL layout. Includes tool-role filtering and metadata state tracking (`tool_call_id`) to keep deep history contexts lightning fast.
- **Zero-Dependency Network Engineering:** Built using Python's native `urllib` library to completely eliminate overhead. Manually handles raw Gzip binary compression signature hooks (`0x8b`) and macOS-specific SSL verification layers.
- **Ollama Modelfile Isolation:** Decouples core logic from prompt strings by baking identities, strict deterministic system boundaries (`temperature 0.0`), and parameters directly into the local Ollama engine.

---

## Detailed Project Structure

```
llm-agent/
├── config/                  # Ollama Modelfiles & YAML configuration boundaries
├── data/                    # Local session isolation files (.jsonl format)
├── src/
│   ├── agents/
│   │   ├── assistant.py     # Master Conductor executing the Perception-Action loop
│   │   └── router.py        # Edge routing & dynamic compute budget allocator
│   ├── memory/
│   │   ├── __init__.py      # Package import namespace insulation layer
│   │   └── chat_history.py  # Sliding-window context filter & persistence mechanics
│   ├── tools/
│   │   ├── __init__.py      # Standardized tool schema registry and function map
│   │   ├── calendar_tool.py # Google Calendar automation bindings
│   │   ├── google_auth.py   # Unified OAuth 2.0 background token refresh helper
│   │   └── search_tool.py   # Optimized Brave LLM Context extraction tool
│   └── main.py              # Lightweight FastAPI web gateway layer
└── requirements.txt         # Minimalist direct-dependency manifest
```

---

## Technical Stack & Infrastructure

- **Languages & Frameworks:** Python, FastAPI, Pydantic
- **Local LLM Ecosystem:** Ollama (Qwen 2.5 7B/14B, Llama 3.1 8B, Llama 3.2 Edge models)
- **APIs & Protocols:** Brave Search (LLM Context Endpoint), Google Calendar/Tasks (OAuth 2.0)
- **Tooling:** Neovim (LazyVim), Pyright LSP, Python Virtual Environments

---

## Development Roadmap

- [x] **Phase 1: Architecture Core** – Continuous perception loops, `max_iterations` safety brakes, and absolute/relative import path synchronization.
- [x] **Phase 2: Data & Networking** – Streamlined JSONL session recording, failsafe magic-bytes Gzip decompression, and custom tool schema registry tracking.
- [ ] **Phase 3: Real-World Integrations** – Finalize Google API authentication routines (`token.json` disk persistence) and active Calendar scheduling.
- [ ] **Phase 4: Distributed Gateway** – Expose the hub terminal endpoints via FastAPI and deploy the lightweight routing agent onto the Raspberry Pi hardware node.

---

## License

This project is open-source and available under the [MIT License](LICENSE).

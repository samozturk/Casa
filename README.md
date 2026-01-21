# Casa – Voice‑Enabled Home Assistant

> **Casa** (Spanish for *house*) is a small prototype that demonstrates how to build a voice‑driven home‑assistant with LangChain, LangGraph, and a handful of other modern Python libraries.  
> It can **read notes from an Obsidian vault**, **control smart lights** (via MQTT), **search the web**, and **chat** in a single conversational flow.

> ⚠️ **This is a demo/learning project** – it’s not production‑ready.  Some features are simplified or stubbed for clarity.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Demo](#running-the-demo)
- [Using the Assistant from Code](#using-the-assistant-from-code)
- [Extending the Assistant](#extending-the-assistant)
- [License](#license)

---

## Features

| Feature | What it does | Where it lives |
|---------|--------------|----------------|
| **Intent Classification** | Determines whether the user wants to *search*, *read*, *control*, or *chat*. | `src/tools.py` (`classify_intent`) & `src/prompts.py` (`INTENT_PROMPT`) |
| **Smart Reading** | Picks the most relevant note from an Obsidian vault and returns its content. | `src/prompts.py` (`READ_FILE_SELECTION_PROMPT`, `READ_NOTE_PROMPT`) |
| **Smart Control** | Interprets a command like “turn on the kitchen lights” and emits a JSON that can be passed to an MQTT client. | `src/prompts.py` (`CONTROL_PARAMETER_PROMPT`) |
| **Web Search** | Uses `duckduckgo-search` to answer factual questions. | *Not yet exposed in the demo notebook, but ready for a LangGraph node.* |
| **Speech Recognition** | `openai-whisper` or `paddleocr` can be used for voice‑to‑text or OCR. | *Dependencies listed in `pyproject.toml`* |
| **Audio I/O** | `sounddevice` + `webrtcvad` can capture, detect voice activity, and play responses. | *Available for future expansion.* |

---

## Project Structure

```text
casa/
├── .python-version          # Python 3.12
├── README.md                # ← This file
├── pyproject.toml           # Project metadata & dependencies
├── src/
│   ├── __init__.py
│   ├── demo.ipynb           # Jupyter demo
│   ├── main.py              # (Not shown) The LangGraph/FastAPI entry point
│   ├── prompts.py           # Prompt definitions
│   ├── tools.py             # Helper functions / LLM wrappers
│   └── models.py            # Pydantic models (e.g., Rooms)
└── ...
```

---

## Prerequisites

| Component | Version | Why |
|-----------|---------|-----|
| Python | 3.12+ | Required by `pyproject.toml` (`requires-python = ">=3.12"`) |
| Poetry | 1.8+ | Used for dependency management (`pyproject.toml`) |
| An LLM provider | e.g., OpenAI, Ollama, Anthropic | The project uses `langchain`‑LLMs.  You need a key / local model. |
| MQTT broker | e.g., Mosquitto | Required for the *control* feature. |
| Obsidian vault | Any folder | The assistant reads notes from a path you provide. |

> **Tip:** The demo notebook only uses the LLM and file system – it does **not** need MQTT or speech libraries to run.

---

## Installation

```bash
# Clone the repo
git clone https://github.com/your-username/casa.git
cd casa

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.\.venv\Scripts\activate     # Windows

# Install dependencies
poetry install
```

> Poetry will read `pyproject.toml` and pull all required packages.  
> If you prefer `pip`, you can run `pip install -e .` after creating the venv.

---

## Configuration

| Variable | Default / Example | Notes |
|----------|-------------------|-------|
| `LLM_MODEL` | `gpt-4o-mini` | Set to your chosen LLM name (OpenAI, Anthropic, etc.). |
| `OBSIDIAN_VAULT_PATH` | `/Users/sam/Documents/Obsidian Vault/Casa` | Override in `demo.ipynb` or in an `.env` file. |
| `MQTT_BROKER_URL` | `mqtt://localhost:1883` | Used by the *control* node (if you extend it). |
| `MQTT_CLIENT_ID` | `casa-agent` | Optional. |

Create a `.env` file at the project root if you want to keep these settings out of code:

```dotenv
LLM_MODEL=gpt-4o-mini
OBSIDIAN_VAULT_PATH=/path/to/obsidian
MQTT_BROKER_URL=mqtt://localhost:1883
```

Then load it in your Python code with `python-dotenv`.

---

## Running the Demo

The Jupyter notebook `src/demo.ipynb` shows a minimal usage example.

```bash
# Start Jupyter (or open the file in VS Code)
jupyter notebook src/demo.ipynb
```

1. The notebook imports `app` from `main.py` (the LangGraph/FastAPI graph).  
2. It sends a single `HumanMessage` asking the assistant to “Read the notes and bring the grocery list.”  
3. The result is printed to the console.

> **NOTE:** If you haven’t added a `main.py` yet, you can run the following minimal example instead:

```python
# src/main.py
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage
from tools import classify_intent

def main():
    # Dummy graph that just calls intent classification
    state = {"messages": [HumanMessage(content="Read the notes")], "intent": None}
    result = classify_intent(state)
    print(result)

if __name__ == "__main__":
    main()
```

Run it with:

```bash
python src/main.py
```

---

## Using the Assistant from Code

The public API is the `app.invoke` method (defined in `main.py`).

```python
from main import app
from langchain_core.messages import HumanMessage

response = app.invoke(
    {
        "messages": [HumanMessage(content="Turn on the living room lights.")],
        "intent": None,   # The graph will infer intent
    }
)

print(response)
```

`app.invoke` returns a dictionary that contains the final `messages` and any node‑specific outputs (e.g., MQTT commands, file paths, search results).

---

## Extending the Assistant

| Where to add | How |
|--------------|-----|
| **New nodes** | Edit `src/main.py` – add a new function that receives `State` and returns a new `State`.  Then add it to the graph. |
| **Prompt changes** | Edit `src/prompts.py`.  Add or modify `SystemMessage` instances. |
| **New tools** | Add a function to `src/tools.py` and register it in the graph. |
| **Speech support** | Use `openai-whisper` or `paddleocr` to turn audio into text.  Feed the text to the graph as a `HumanMessage`. |
| **MQTT integration** | Add a node that publishes the JSON from `CONTROL_PARAMETER_PROMPT` to the broker. |

---

## License

MIT © 2026 Sam

---

### Want to Contribute?

Feel free to open issues or pull requests.  All contributions that help improve the demo, add documentation, or extend functionality are welcome!
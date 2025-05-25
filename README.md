<h1 align="center"><strong>LLamaIndex-Chainlit-MCP-Tools <strong></h1>

A powerful chatbot application built with Chainlit and LlamaIndex, featuring multiple LLM integrations, conversation history management, and various tools.

## Features

- 🤖 Multiple LLM Support
  - Google Gemini
  - OpenAI GPT (ready to integrate)
  - Anthropic Claude (ready to integrate)

- 🛠️ Built-in Tools
  - Mathematical Operations (sum, average, square root)
  - PDF File Analysis
  - More tools can be easily added

- 📝 Advanced Logging
  - Rich Console Output
  - File-based Logging
  - Daily Log Rotation

- 💾 Conversation History
  - Session-based Storage
  - JSON Format
  - Persistent Storage in Local Files

- ⚙️ Customizable Settings
  - LLM Model Selection
  - Temperature Control
  - Greeting Message Toggle

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mehmetalpayy/LLamaIndex-Chainlit-MCP-Tools.git
cd LLamaIndex-Chainlit-MCP-Tools
```

2. Install uv (if not already installed):
```bash
# Windows (PowerShell)
python -m pip install uv

# Linux/MacOS
python -m pip install uv
```

3. Create and activate virtual environment, then install dependencies:
```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/MacOS

# Install dependencies using uv
uv pip install .
```

4. Create `.env` file and add your API key:
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Or manually create .env file with:
# GEMINI_API_KEY=your_api_key_here
```

<h2>📁 Project Structure</h2>

<pre>
LLamaIndex-Chainlit-MCP-Tools/
├── llms/
│   ├── __init__.py
│   ├── base.py
│   ├── gemini.py
│   ├── openai.py
│   └── claude.py
│
├── tools/
│   ├── __init__.py
│   └── math.py
│
├── logger/
│   ├── __init__.py
│   ├── logging.py
│   └── rich_logger.py
│
├── history/
│   ├── __init__.py
│   ├── local_memory.py
│   └── sessions/
│       └── {session_id}/
│           └── messages.json
│
├── logs/
│   └── YYYY-MM-DD.log
│
└── main.py
</pre>


## Usage

1. Start the application:
```bash
chainlit run main.py
```

2. Access the web interface at `http://localhost:8000`

3. Features:
   - Chat with the AI assistant
   - Upload and analyze PDF files
   - Use mathematical tools
   - Customize settings through the UI

## Configuration

### LLM Settings
- Model: Choose between different Gemini models
- Temperature: Adjust response creativity (0.0 - 1.0)
- Greeting: Toggle welcome message

### Logging
- Console: Rich formatted output
- Files: Daily log files in `logs/` directory

### History
- Sessions: Unique ID for each chat session
- Storage: JSON files in `history/sessions/` directory

## Development

### Adding New Tools
1. Create a new file in `tools/`
2. Define your function with `@cl.step(type="tool")`
3. Add to tool list in `main.py`

### Adding New LLMs
1. Create new file in `llms/`
2. Implement using `base.LLMConfig`
3. Add to LLM selection in settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
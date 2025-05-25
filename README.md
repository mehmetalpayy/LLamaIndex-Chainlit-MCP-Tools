# MCP-Chainlit

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
git clone https://github.com/mehmetalpayy/MCP-Chainlit.git
cd MCP-Chainlit
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file and add your API key:
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Or manually create .env file with:
# GEMINI_API_KEY=your_api_key_here
```

## Project Structure

MCP-Chainlit/
├── llms/ # LLM integrations
│ ├── init.py
│ ├── base.py # Base LLM configuration
│ └── gemini.py # Google Gemini integration
├── tools/ # Tool implementations
│ ├── init.py
│ └── math.py # Mathematical operations
├── logger/ # Logging functionality
│ ├── init.py
│ ├── logging.py # Standard logging
│ └── rich_logger.py # Rich console logging
├── history/ # Conversation history
│ ├── init.py
│ └── local_memory.py # Local storage implementation
└── main.py # Main application


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
# AI Website Builder

An interactive web application that uses AI to generate websites based on natural language descriptions. Features a real-time preview, version history, and a draggable interface.

## Features

- 🤖 AI-powered website generation using OpenAI's API
- 🔑 Bring your own OpenAI API key
- 🎯 Multiple AI model options:
  - GPT-4o Mini
  - GPT-4o
  - GPT-4
  - GPT-3.5
  - O1 Mini
  - O1 Preview
- 🖥️ Real-time preview
- 📝 Version history with restore points
- 🔄 Copy generated HTML code
- 🌐 Publish and share generated websites
- 🖱️ Draggable interface
- ⚡ Fast and responsive
- 🔒 Multi-user support with session management
- 💾 Persistent storage using pickle with file locking

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.7+
- pip (Python package manager)
- An OpenAI API key (get one at https://platform.openai.com/api-keys)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/BonifacioCalindoro/ai-website-builder
    cd ai-website-builder
    ```

2. Create a virtual environment (recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate # On Windows: .venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the server:
    ```bash
    python main.py
    ```
    Or alternatively:
    ```bash
    uvicorn main:app --reload --port 8001
    ```

2. Open your browser and navigate to:
    ```
    http://localhost:8001
    ```

## How to Use

### Getting Started
1. Enter your OpenAI API key in the input field
2. Select your preferred AI model from the dropdown
3. Type your website description
4. Click "Generate" or press Enter
5. Watch as your website appears in the preview window


### Generating a Website

1. Type your website description in the input field at the top of the screen
2. Click "Generate" or press Enter
3. Watch as your website appears in the preview window below

Example prompts:
- "Create a landing page for a coffee shop with a dark theme"
- "Make a personal portfolio with three sections: About, Projects, and Contact"
- "Build a simple blog homepage with recent posts"

You can continue editing the website by clicking "Generate" with a new prompt.

### Using Version History

1. Click the "Chat History" dropdown in the prompt panel
2. View your previous prompts with timestamps
3. Click "Restore" next to any version to revert to that design
4. The active version is highlighted in blue
5. Use "Clear History" to start fresh

### Publishing Your Website

1. Click the "Publish" button when you're happy with your design
2. Copy the generated URL from the modal
3. Share the URL with others to view your website

### Interface Controls

- **API Key**: Enter your OpenAI API key (required for generation)
- **Model Selection**: Choose your preferred AI model
- **Drag & Drop**: Click and drag the prompt panel header to move it
- **Minimize**: Click the "-" button to collapse the prompt panel
- **Copy HTML**: Click the "Copy HTML" button to copy the generated code
- **Preview**: Updates automatically with each generation or restoration
- **Show/Hide API Key**: Toggle visibility of your API key

## Technical Details

- Backend: FastAPI (Python)
- AI Models: Multiple OpenAI models with optimizations
- Frontend: Vanilla JavaScript
- Session Management: Cookie-based with pickle storage
- Real-time updates using iframe refresh
- File locking for concurrent access
- Persistent sessions across server restarts

## Limitations

- Requires OpenAI API key
- Different models have different capabilities and speeds
- API costs vary by model choice

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.



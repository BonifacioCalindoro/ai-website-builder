# AI Website Builder

An interactive web application that uses AI to generate websites based on natural language descriptions. Features a real-time preview, version history, and a draggable interface.

## Features

- 🤖 AI-powered website generation
- 🖥️ Real-time preview
- 📝 Version history with restore points
- 🔄 Copy generated HTML code
- 🖱️ Draggable interface
- ⚡ Fast and responsive

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.7+
- pip (Python package manager)

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

4. Create a `.env` file based on the `.env.example` template:
    ```bash
    cp .env.example .env
    ```

5. Add your OpenAI API key to the `.env` file:
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    ```

## Running the Application

1. Run the application:
    ```bash
    python main.py
    ```

2. Open your browser and navigate to:
    ```bash
    http://localhost:8001
    ```


## How to Use

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

### Interface Controls

- **Drag & Drop**: Click and drag the prompt panel header to move it around the screen
- **Minimize**: Click the "-" button to collapse the prompt panel
- **Copy HTML**: Click the "Copy HTML" button in the bottom-right to copy the generated code
- **Preview**: The preview updates automatically with each generation or restoration

### Tips

1. Be specific in your descriptions for better results
2. Use the version history to go back to a previous design
3. Copy the HTML code to use it in your own projects
4. Minimize the prompt panel if you need a clearer view of the preview

## Technical Details

- Backend: FastAPI (Python)
- AI Model: GPT-4o-mini
- Frontend: Vanilla JavaScript
- Real-time updates using iframe refresh
- In-memory version history storage

## Limitations

- Version history is not persistent (clears on server restart)
- Single user support (no authentication)

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.



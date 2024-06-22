# Nutrition Chatbot

This is a Nutrition Chatbot built using FastAPI and OpenAI's GPT-4 model. The chatbot provides accurate information about nutrition, dietary advice, meal planning, and healthy eating habits. It can only respond to nutrition-related questions.

## Features

- Provides nutritional advice and meal planning tips.
- Maintains a chat log to track the conversation history.
- Interactive chat interface using WebSocket for real-time communication.
- Generates images based on user input.

## Getting Started

### Prerequisites

- Python 3.7 or later
- OpenAI API key

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/khushbu-kumari295/chatbot.git
    cd chatbot
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables:
    - Create a `.env` file in the root directory of the project.
    - Add your OpenAI API key to the `.env` file:
      ```env
      OPENAI_API_KEY=your_openai_api_key_here
      ```

### Running the Application

1. Start the FastAPI server:
    ```bash
    uvicorn nutrition:app --reload
    ```

2. Open your web browser and navigate to `http://localhost:8000` to interact with the chatbot.

### API Endpoints

- **GET /**: Renders the home page with the chat interface.
- **POST /**: Handles form submissions for chat messages.
- **WebSocket /ws**: Manages real-time chat communication.
- **GET /image**: Renders the image generation page.
- **POST /image**: Generates images based on user input.

### Example Usage

- **Chat Interface**: 
    - Open the home page and start a conversation by typing your nutrition-related question and pressing "Send".
    - The bot will respond with appropriate nutritional advice.
- **Image Generation**:
    - Navigate to the image generation page.
    - Enter a prompt for the image you want to generate and submit the form.
    - The generated image URL will be displayed on the page.

### Code Overview

- **main.py**:
    - Initializes the FastAPI app and sets up Jinja2 templates.
    - Defines the chat log with initial system message.
    - Implements the WebSocket and form handling for chat messages.
    - Provides endpoints for chat and image generation.

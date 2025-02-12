# AI Pediatrician Chatbot

An intelligent chatbot system designed to provide preliminary pediatric health assessments and recommendations. This project implements three different workflow approaches, from simple to production-ready implementations.

⚠️ **IMPORTANT DISCLAIMER**: This chatbot is for educational and demonstration purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## Features

- Interactive conversation flow for gathering symptoms and patient information
- Structured diagnostic assessments
- Treatment recommendations with pharmacy locator
- Product recommendations with affiliate links
- Comprehensive medical history collection
- Asynchronous processing capabilities
- Production-ready data validation

## Workflows Description

**Workflow #1** is ideal for simpler applications where a conversational loop and a final summary report are sufficient. It is straightforward, synchronous, and relies on minimal data structuring.

**Workflow #2** is designed for more complex, production-ready scenarios. Its modular, asynchronous approach coupled with robust data validation using Pydantic makes it highly extensible. It not only manages a comprehensive diagnostic process but also integrates additional features like product recommendations with affiliate links.

**Workflow #3** captures the intent, functionality, and behavior of both original workflows while combining the best parts of each approach into one coherent, asynchronous design.

## Project Structure

The project contains three implementation approaches:

1. **Simple Application** (`workflows/1-simple-application.py`)
   - Basic synchronous implementation
   - Ideal for prototypes and simple use cases
   - Straightforward conversation flow

2. **Production Ready** (`workflows/2-production-ready-scenario.py`)
   - Advanced implementation with Pydantic models
   - Structured data validation
   - Product recommendations with affiliate links
   - Comprehensive error handling

3. **Asynchronous Workflow** (`workflows/3-asynchronous-workflow.py`)
   - Combines best practices from both approaches
   - Asynchronous processing
   - Enhanced error handling
   - Modular design

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chatbot-ai-pediatrician.git
   cd chatbot-ai-pediatrician
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Choose the workflow implementation that best suits your needs:

1. Simple Application:
   ```bash
   python workflows/1-simple-application.py
   ```

2. Production Ready:
   ```bash
   python workflows/2-production-ready-scenario.py
   ```

3. Asynchronous Workflow:
   ```bash
   python workflows/3-asynchronous-workflow.py
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security

- Never commit your `.env` file or expose your API keys
- Always use environment variables for sensitive data
- Keep your dependencies updated

## Support

If you find this tool helpful, consider making a donation to support its development. 
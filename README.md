# text-summarizer

## Overview
The Text Summarizer project is a Django-based web application that leverages AI to generate concise summaries of long texts. It uses the Facebook BART model for high-quality text summarization, ensuring that key information is preserved while reducing the overall length of the input text.

## Features
- **Web Interface**: A user-friendly interface to input text and view summaries.
- **AI-Powered Summarization**: Utilizes the `transformers` library and the BART model for accurate and efficient text summarization.
- **API Support**: Provides an API endpoint for programmatic access to the summarization functionality.
- **Customizable Model**: Includes a pre-trained model that can be fine-tuned or replaced with other summarization models.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd text-summarizer
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/`.

## Usage

### Web Interface
1. Navigate to the home page.
2. Paste your text into the input box.
3. Click "Generate Summary" to view the summarized text.

### API
- Endpoint: `/api/summarize/`
- Method: POST
- Payload: `{ "text": "Your text here" }`
- Response: `{ "summary": "Summarized text" }`

## Project Structure
- `summarizer/`: Contains Django project settings and configurations.
- `text/`: Main app for text summarization, including views, templates, and services.
- `my_summarizer_model/`: Directory for the pre-trained summarization model.
- `templates/`: HTML templates for the web interface.

## Model Details
The project uses the `facebook/bart-large-cnn` model from Hugging Face's Transformers library. The model is downloaded and saved locally for efficient reuse.

## License
This project is licensed under the MIT License.

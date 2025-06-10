# AI Therapist Application

A supportive and empathetic AI therapist application that provides a safe space for users to express their thoughts and feelings. The application uses OpenAI's GPT-3.5 model to generate thoughtful, compassionate responses while maintaining appropriate therapeutic boundaries.

## Features

- Clean, modern, and calming user interface
- Real-time chat interaction with AI therapist
- Empathetic and supportive responses
- Safe and confidential environment
- Responsive design that works on all devices

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://localhost:5000`

## Important Notes

- This application is not a replacement for professional mental health services
- The AI therapist is designed to provide emotional support and guidance
- For serious mental health concerns, please consult with a licensed mental health professional
- All conversations are processed through OpenAI's API and are subject to their privacy policy

## Security and Privacy

- The application does not store any conversation history
- All communication is handled through secure HTTPS connections
- Your OpenAI API key should be kept confidential and never shared

## Contributing

Feel free to submit issues and enhancement requests! 
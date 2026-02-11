# 🤖 Django AI Data Chat Dashboard

A powerful Django web application that allows users to upload CSV data and interact with it using AI-powered natural language queries. The application generates visualizations using Chart.js and can answer data-related questions using pandas operations.

## ✨ Features

- **CSV Upload**: Upload your own CSV files or use sample data
- **Data Display**: View uploaded data in a beautiful HTML table
- **AI-Powered Analysis**: LLM analyzes your data and generates column descriptions automatically
- **Interactive Chat**: Ask questions in natural language about your data
- **Chart Generation**: Automatically generates charts (bar, line, pie, scatter, etc.) using Chart.js
- **Pandas Integration**: Executes pandas code to answer complex data queries
- **Modern UI**: Beautiful dark theme with gradient effects and smooth animations

## 🚀 Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd d:\myprojects\dashbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Google API Key**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.env` file in the project root
   - Add your API key:
     ```
     GOOGLE_API_KEY=your_actual_api_key_here
     ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Open your browser**
   Navigate to: `http://127.0.0.1:8000/`

## 📋 Requirements

The application requires the first 5 rows of your CSV data to generate column descriptions. This happens automatically when you upload a file or use sample data.

### Query Examples

**Chart Queries:**
- "Show me a bar chart of salary by department"
- "Create a pie chart showing city distribution"
- "Display a line chart of ages"

**Data Queries:**
- "What is the average salary?"
- "How many people are in each department?"
- "What is the maximum age?"

## 🎨 UI Flow

1. **Upload Section**: Choose a CSV file or use sample data
2. **Loading State**: Shows "Loading chatbot..." while LLM processes the data
3. **Data Table**: Displays your uploaded data in a styled HTML table
4. **Chat Interface**: Ask questions and receive answers or visualizations

## 🛠️ Technology Stack

- **Backend**: Django 5.0+
- **AI**: Google Gemini (gemini-pro)
- **Data Processing**: Pandas
- **Visualization**: Chart.js
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with modern gradients and animations

## 📁 Project Structure

```
dashbot/
├── chat/                      # Main Django app
│   ├── templates/
│   │   └── chat/
│   │       └── index.html    # Main UI template
│   ├── views.py              # Backend logic
│   └── urls.py               # URL routing
├── dashbot/                  # Project settings
│   ├── settings.py          # Django settings
│   └── urls.py              # Main URL configuration
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
└── README.md               # This file
```

## 🔧 Configuration

The application uses session storage to maintain data state. In production, consider using:
- Django's database-backed sessions
- Redis for session management
- PostgreSQL for data persistence

## 🎯 How It Works

1. **Upload**: User uploads CSV or uses sample data
2. **Processing**: 
   - CSV is converted to pandas DataFrame
   - First 5 rows are sent to Gemini LLM
   - LLM generates column descriptions in JSON format
3. **Display**: Data is shown in an HTML table
4. **Chat**: 
   - User asks a question
   - Question + column descriptions sent to LLM
   - LLM generates pandas code or chart configuration
   - Results displayed as text or Chart.js visualization

## 🔐 Security Notes

- Never commit your `.env` file with real API keys
- Use environment variables for sensitive data
- In production, use proper CSRF protection
- Consider rate limiting for API calls

## 📝 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

Feel free to fork, modify, and use this project as a template for your own AI-powered data dashboards!

## 📧 Support

For issues or questions, please create an issue in the repository.

---

**Happy Data Chatting! 🎉**

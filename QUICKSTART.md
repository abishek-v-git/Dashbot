# 🚀 Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google API Key (from Google AI Studio)

## Setup Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Your Google API Key
1. Get your API key from: https://makersuite.google.com/app/apikey
2. Open the `.env` file in the project root
3. Replace the example key with your actual key:
   ```
   GOOGLE_API_KEY=your_actual_google_api_key_here
   ```

### 3. Run Database Migrations
```bash
python manage.py migrate
```

### 4. Start the Development Server
```bash
python manage.py runserver
```

### 5. Open Your Browser
Navigate to: http://127.0.0.1:8000/

## Usage

### Upload Data
1. Click "Choose CSV File" to upload your own data, or
2. Click "Use Sample Data" to try the demo

### Wait for Loading
The system will:
- Convert CSV to DataFrame
- Send first 5 rows to LLM
- Generate column descriptions
- Display "Loading chatbot..." message

### Start Chatting
Once loaded, you'll see:
- Your data in a table
- A chat interface below

### Example Queries

**For Charts:**
- "Show me a bar chart of salary by department"
- "Create a pie chart of city distribution"
- "Display a line chart of ages"

**For Data Analysis:**
- "What is the average salary?"
- "How many people work in IT?"
- "What's the highest salary in the Finance department?"

## Troubleshooting

### API Key Issues
- Make sure your `.env` file has the correct API key
- Restart the server after changing the `.env` file

### No Data Showing
- Ensure your CSV file is properly formatted
- Check browser console for errors

### Charts Not Displaying
- Check that Chart.js is loading properly
- Ensure the query clearly requests a chart

## Features Overview

✅ CSV Upload or Sample Data  
✅ Automatic column description generation  
✅ Interactive data table display  
✅ AI-powered chat interface  
✅ Chart generation with Chart.js  
✅ Pandas-based data analysis  
✅ Modern, responsive dark theme UI  

## Next Steps

- Customize the sample data in `views.py`
- Modify the UI theme in `index.html`
- Add more chart types
- Implement data export features
- Add user authentication

---

**Enjoy your AI Data Chat Dashboard! 🎉**

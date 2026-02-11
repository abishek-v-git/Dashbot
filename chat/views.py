import json
import pandas as pd
import io
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', 'YOUR_API_KEY_HERE')
genai.configure(api_key=GOOGLE_API_KEY)

# Store session data (in production, use Django session or database)
session_data = {}


def index(request):
    """Render the main page"""
    return render(request, 'chat/index.html')


@csrf_exempt
def upload_csv(request):
    """Handle CSV upload and generate column descriptions using LLM"""
    if request.method == 'POST':
        try:
            # Check if CSV file is uploaded
            if 'csv_file' in request.FILES:
                csv_file = request.FILES['csv_file']
                
                # Read CSV into DataFrame
                df = pd.read_csv(csv_file)
                
            elif 'use_sample' in request.POST:
                # Create sample data
                df = pd.DataFrame({
                    'Name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana', 'Eve', 'Frank'],
                    'Age': [25, 30, 35, 28, 42, 31, 27, 38],
                    'City': ['New York', 'London', 'Paris', 'Tokyo', 'Sydney', 'Berlin', 'Toronto', 'Mumbai'],
                    'Salary': [50000, 60000, 75000, 55000, 90000, 62000, 58000, 72000],
                    'Department': ['IT', 'HR', 'Finance', 'IT', 'Marketing', 'HR', 'IT', 'Finance']
                })
            else:
                return JsonResponse({'error': 'No file uploaded or sample data requested'}, status=400)
            
            # Store the full dataframe in session
            session_id = request.session.session_key or request.session.create()
            session_data[session_id] = {
                'df': df,
                'columns': df.columns.tolist()
            }
            
            # Get first 5 rows for LLM context
            first_5_rows = df.head(5)
            
            # Generate column descriptions using LLM
            prompt = f"""
            You are a data analyst assistant. Given the following CSV data (first 5 rows), 
            generate a JSON description of each column including its name, data type, and a brief description.
            
            Data:
            {first_5_rows.to_string()}
            
            Return ONLY a valid JSON object (no markdown, no code blocks) in this exact format:
            {{
                "columns": [
                    {{"name": "column1", "type": "string", "description": "description of column1"}},
                    {{"name": "column2", "type": "number", "description": "description of column2"}}
                ]
            }}
            """
            
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            
            # Clean the response text using regex
            import re
            response_text = response.text.strip()
            match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if match:
                response_text = match.group(0)
            
            # Remove markdown code blocks if still present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
            
            response_text = response_text.strip()
            
            try:
                column_descriptions = json.loads(response_text)
            except json.JSONDecodeError:
                response_text = response_text.replace("'", '"')
                column_descriptions = json.loads(response_text)
            
            # Store column descriptions in session
            session_data[session_id]['column_descriptions'] = column_descriptions
            
            # Convert dataframe to HTML table
            table_html = df.to_html(classes='data-table', index=False)
            
            return JsonResponse({
                'success': True,
                'table_html': table_html,
                'column_descriptions': column_descriptions,
                'session_id': session_id
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def chat_query(request):
    """Handle chat queries and generate pandas code or charts"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '')
            session_id = request.session.session_key
            
            if not session_id or session_id not in session_data:
                return JsonResponse({'error': 'No data loaded. Please upload a CSV first.'}, status=400)
            
            # Get session data
            df = session_data[session_id]['df']
            column_descriptions = session_data[session_id]['column_descriptions']
            
            # Generate pandas code using LLM
            prompt = f"""
            You are a data analysis assistant. The dataframe is loaded as 'df'.
            Column Info: {json.dumps(column_descriptions, indent=2)}
            
            User Query: {query}
            
            You cannot see the full data. You MUST generate Python/Pandas code to compute the answer.
            
            Return valid JSON with these fields:
            
            For Text Answers:
            {{
                "type": "answer",
                "code": "result = 'The average age is ' + str(round(df['Age'].mean(), 2))"
            }}
            
            For Charts:
            {{
                "type": "chart",
                "chart_type": "bar",
                "chart_title": "Title",
                "code": "data = df['City'].value_counts(); result = {{ 'labels': data.index.tolist(), 'datasets': [{{ 'label': 'Count', 'data': data.values.tolist(), 'backgroundColor': 'rgba(75, 192, 192, 0.2)' }}] }}"
            }}
            
            IMPORTANT:
            1. The code MUST define a variable named 'result' containing the final output.
            2. For charts, 'result' must be a dictionary with 'labels' and 'datasets' keys in Chart.js format.
            3. For answers, 'result' must be a string or number.
            4. Do not include markdown formatting in the JSON.
            """
            
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            
            # Clean response using regex to find JSON block
            import re
            response_text = response.text.strip()
            
            match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if match:
                response_text = match.group(0)
            
            # Clean up potential markdown
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
            
            response_text = response_text.strip()
            
            try:
                result_json = json.loads(response_text)
            except json.JSONDecodeError:
                response_text = response_text.replace("'", '"')
                result_json = json.loads(response_text)
            
            # Execute pandas code
            if 'code' in result_json:
                local_vars = {'df': df, 'pd': pd}
                try:
                    exec(result_json['code'], {}, local_vars)
                    execution_output = local_vars.get('result', 'No result generated')
                    
                    if result_json['type'] == 'answer':
                        result_json['result'] = str(execution_output)
                    elif result_json['type'] == 'chart':
                        result_json['chart_data'] = execution_output
                        
                except Exception as e:
                    result_json['result'] = f"Error executing code: {str(e)}"
                    # Setup fallback for chart error
                    if result_json['type'] == 'chart':
                        result_json['type'] = 'answer'
            
            return JsonResponse({
                'success': True,
                'result': result_json
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

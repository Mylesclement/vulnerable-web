# Vulnerable Flask Application

This project is a Flask web application designed with intentional security vulnerabilities for educational purposes.

## Setup and Run

- Install dependencies: `pip install -r requirements.txt`
- Run the application: `python app.py`

## Vulnerabilities Included

1. **SQL Injection**
   - Access via: `http://127.0.0.1:8000/search?name=<name>`
   - Example: `http://127.0.0.1:8000/search?name=' OR '1'='1`

2. **Cross-Site Scripting (XSS)**
   - Access via: `http://127.0.0.1:8000/welcome?username=<script>alert('XSS')</script>`

3. **Insecure Direct Object Reference (IDOR)**
   - Access via: `http://127.0.0.1:8000/file?file_name=filename`
   - Example: Place a file in the `static` directory and access it via the URL.

## Disclaimer

This application is for educational purposes only and should not be used in production environments.
 
"# vulnerable-website" 

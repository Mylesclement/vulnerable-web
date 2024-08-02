from flask import Flask, request, render_template_string

app = Flask(__name__)

# Hardcoded credentials (for demonstration purposes)
USER = "admin"
PASSWORD = "password123"

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Vulnerable Web App</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; }
                h1, h2 { color: #333; }
                a { color: #5D76DB; text-decoration: none; }
                form { margin-top: 20px; }
                input, button { padding: 8px; margin-top: 5px; }
                ul { list-style-type: none; }
                li { margin: 10px 0; }
            </style>
        </head>
        <body>
            <h1>Welcome to the Vulnerable Web Application!</h1>
            <p>Please use the links below to navigate to different tests:</p>
            <ul>
                <li><a href="/about">About Page</a></li>
                <li><a href="/search_form">Test SQL Injection</a></li>
                <li><a href="/xss_form">Test Cross-Site Scripting (XSS)</a></li>
                <li><a href="/idor_form">Test Insecure Direct Object Reference (IDOR)</a></li>
                <li><a href="/login_form">Test Hardcoded Credentials</a></li>
            </ul>
        </body>
    </html>
    """

@app.route('/about')
def about():
    return """
    <html>
        <body>
            <h1>About Page</h1>
            <p>This is the about page of a deliberately vulnerable web application.</p>
            <p><a href="/">Home</a></p>
        </body>
    </html>
    """

@app.route('/search_form')
def search_form():
    return """
    <html>
        <body>
            <h1>SQL Injection Test</h1>
            <form action="/search" method="get">
                <input type="text" name="name" placeholder="Enter name to search" />
                <button type="submit">Search</button>
            </form>
            <p><a href="/">Home</a></p>
        </body>
    </html>
    """

@app.route('/search')
def search():
    user_input = request.args.get('name', '')
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    return f"""
    <html>
        <body>
            <h1>Query Executed</h1>
            <p>{query}</p>
            <p><a href="/search_form">Back to Search</a></p>
            <p><a href="/">Home</a></p>
        </body>
    </html>
    """

@app.route('/xss_form')
def xss_form():
    return """
    <html>
        <body>
            <h1>XSS Test</h1>
            <form action="/welcome" method="get">
                <input type="text" name="username" placeholder="Enter username" />
                <button type="submit">Greet</button>
            </form>
            <p><a href="/">Home</a></p>
        </body>
    </html>
    """

@app.route('/welcome')
def welcome():
    user_name = request.args.get('username', 'Guest')
    return render_template_string(f"""
    <html>
        <body>
            <h1>Welcome, {user_name}!</h1>
            <p><a href="/xss_form">Test another username</a></p>
            <p><a href="/">Home</a></p>
        </body>
    </html>
    """)

@app.route('/idor_form')
def idor_form():
    return """
    <html>
        <body>
            <h1>IDOR Test</h1>
            <form action="/file" method="get">
                <input type="text" name="file_name" placeholder="Enter filename to access" required />
                <button type="submit">Access File</button>
            </form>
            <p><a href="/">Home</a></p>
        </body>
    </html>
    """

@app.route('/file')
def file():
    file_name = request.args.get('file_name')
    file_path = f"static/{file_name}"
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            return f"""
            <html>
                <body>
                    <h1>File Content</h1>
                    <pre>{content}</pre>
                    <p><a href="/idor_form">Try another file</a></p>
                    <p><a href="/">Home</a></p>
                </body>
            </html>
            """
    except FileNotFoundError:
        return """
        <html>
            <body>
                <h1>File not found.</h1>
                <p><a href="/idor_form">Try another file</a></p>
                <p><a href="/">Home</a></p>
            </body>
        </html>
        """

@app.route('/login_form')
def login_form():
    return """
    <html>
        <body>
            <h1>Login Test</h1>
            <form action="/login" method="post">
                <input type="text" name="username" placeholder="Username" required />
                <input type="password" name="password" placeholder="Password" required />
                <button type="submit">Login</button>
            </form>
            <p><a href="/">Home</a></p>
        </body>
    </html>
    """

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == USER and password == PASSWORD:
        return "<h1>Login successful!</h1><p><a href='/login_form'>Back to login</a></p>"
    else:
        return "<h1>Login failed!</h1><p>Incorrect credentials. Please try again.</p><p><a href='/login_form'>Back to login</a></p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

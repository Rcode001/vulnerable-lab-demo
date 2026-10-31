from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Intentional vulnerability 1: Hardcoded secret key / credential
API_KEY = "super_secret_api_key_12345"

@app.route("/")
def home():
    return "Welcome to the Security Playground! Check the routes."

# Intentional vulnerability 2: Reflected Cross-Site Scripting (XSS)
@app.route("/greet")
def greet():
    username = request.args.get("name", "Guest")
    # Unsafe rendering of user input directly into HTML
    template = f"<h1>Hello, {username}!</h1>"
    return render_template_string(template)

# Intentional vulnerability 3: SQL Injection
@app.route("/search")
def search():
    query = request.args.get("q", "")
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE items (name TEXT)")
    cursor.execute("INSERT INTO items VALUES ('Flag{example_flag}')")
    
    # Unsafe string formatting in SQL query
    sql = f"SELECT * FROM items WHERE name = '{query}'"
    result = cursor.execute(sql).fetchall()
    return str(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    

from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

# Получение секретов из файлов
def get_secret(path, default=None):
    try:
        with open(path) as f:
            return f.read().strip()
    except FileNotFoundError:
        return default

SECRET_KEY = get_secret(os.getenv('SECRET_KEY_FILE', ''), 'default_secret_key')
DB_PASSWORD = get_secret(os.getenv('DB_PASSWORD_FILE', ''), 'password123')

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'testdb')

@app.route('/')
def index():
    return jsonify({"message": "Hello, World!", "secret_key": SECRET_KEY})

@app.route('/db')
def test_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        return jsonify({"status": "Connected to database!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

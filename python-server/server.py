import os
import random
import string
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

from flask import Flask, jsonify  # noqa: E402
from config.connections import connections  # noqa: E402
from config.queries import queries  # noqa: E402
from db import mysql as mysql_runner  # noqa: E402
from db import mssql as mssql_runner  # noqa: E402

app = Flask(__name__)
PORT = int(os.getenv('PYTHON_PORT', '8080'))


@app.post('/init-mysql')
def init_mysql():
    conn = connections['holiday_gifts_mysql']
    try:
        mysql_runner.run_query(conn, """
            CREATE TABLE IF NOT EXISTS UserPrincipal (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        username = 'user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        mysql_runner.run_query(conn, f"INSERT INTO UserPrincipal (username) VALUES ('{username}')")
        return jsonify({'message': 'UserPrincipal table ready', 'inserted': username})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.get('/datasets/<name>')
def get_dataset(name):
    query_def = queries.get(name)
    if not query_def:
        return jsonify({'error': f"Dataset '{name}' not found"}), 404

    conn_config = connections.get(query_def['connection'])
    if not conn_config:
        return jsonify({'error': f"Connection '{query_def['connection']}' not configured"}), 500

    try:
        if conn_config['type'] == 'mysql':
            results = mysql_runner.run_query(conn_config, query_def['sql'])
        elif conn_config['type'] == 'mssql':
            results = mssql_runner.run_query(conn_config, query_def['sql'])
        else:
            return jsonify({'error': f"Unsupported connection type '{conn_config['type']}'"}), 500
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)

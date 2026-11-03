"""Synthetic catalog for isolated security-tool evaluation. Not for production."""
import os
import sqlite3
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_file

ROOT = Path(__file__).resolve().parent


def create_app():
    app = Flask(__name__)
    app.config['FILES_DIR'] = ROOT / 'sample_files'

    def database():
        connection = sqlite3.connect(':memory:')
        connection.row_factory = sqlite3.Row
        connection.execute('CREATE TABLE products (id INTEGER, name TEXT, price INTEGER)')
        connection.executemany('INSERT INTO products VALUES (?, ?, ?)', [
            (1, 'Keyboard', 30), (2, 'Mouse', 15), (3, 'Monitor', 150)
        ])
        return connection

    @app.get('/health')
    def health():
        return jsonify(status='ok')

    @app.get('/products/search')
    def search():
        query = request.args.get('q', '')
        connection = database()
        try:
            rows = connection.execute(
                "SELECT id, name, price FROM products WHERE name LIKE '%" + query + "%'"
            ).fetchall()
            return jsonify([dict(row) for row in rows])
        except sqlite3.Error:
            abort(400)
        finally:
            connection.close()

    @app.get('/products/filter')
    def filter_products():
        query = request.args.get('q', '')
        connection = database()
        try:
            rows = connection.execute(
                'SELECT id, name, price FROM products WHERE name LIKE ?',
                ('%' + query + '%',)
            ).fetchall()
            return jsonify([dict(row) for row in rows])
        finally:
            connection.close()

    @app.get('/files/download')
    def download():
        filename = request.args.get('name', 'welcome.txt')
        target = Path(app.config['FILES_DIR']) / filename
        if not target.is_file():
            abort(404)
        return send_file(target, as_attachment=True)

    return app


if __name__ == '__main__':
    create_app().run(host=os.environ.get('APP_HOST', '127.0.0.1'), port=5000, debug=False)

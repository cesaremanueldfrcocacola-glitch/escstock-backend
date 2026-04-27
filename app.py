from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")

def db():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

@app.route("/")
def home():
    return jsonify({"status": "ESCStock Online"})

@app.route("/productos", methods=["GET"])
def productos():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT id, codigo, nombre, stock FROM productos ORDER BY id ASC;")
    data = cur.fetchall()
    conn.close()

    result = []
    for row in data:
        result.append({
            "id": row[0],
            "codigo": row[1],
            "nombre": row[2],
            "stock": row[3]
        })

    return jsonify(result)

@app.route("/agregar", methods=["POST"])
def agregar():
    data = request.json

    conn = db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO productos (codigo, nombre, stock) VALUES (%s,%s,%s)",
        (data["codigo"], data["nombre"], data["stock"])
    )

    conn.commit()
    conn.close()

    return jsonify({"ok": True})

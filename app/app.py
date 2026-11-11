import os, re, time, hashlib
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from flask import Flask, request, jsonify

app = Flask(__name__)

def make_pool():
    for _ in range(30):                      # wait for Postgres on startup
        try:
            return ThreadedConnectionPool(
                1, 10,
                host=os.environ["DB_HOST"], dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"], password=os.environ["DB_PASSWORD"])
        except Exception:
            time.sleep(2)
    raise RuntimeError("database unavailable")

pool = make_pool()

def init_db():
    conn = pool.getconn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY, patient_id INT, text TEXT,
                created_at TIMESTAMPTZ DEFAULT now())""")
            cur.execute("SELECT count(*) FROM notes")
            if cur.fetchone()[0] < 200:
                for i in range(200):
                    cur.execute("INSERT INTO notes (patient_id, text) VALUES (%s, %s)",
                                (i % 20, "Patient reports mild pain, BP 120/80, prescribed rest. " * 20))
    finally:
        pool.putconn(conn)

init_db()

@app.route("/")
def index():
    return "App is running\n"

# CPU-oriented: read notes, tokenise and hash them repeatedly
@app.route("/patients/notes/process/")
def process_notes():
    n = min(int(request.args.get("n", 50)), 200)
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT text FROM notes ORDER BY id DESC LIMIT %s", (n,))
            rows = cur.fetchall()
    finally:
        pool.putconn(conn)
    total = 0
    for (text,) in rows:
        words = re.findall(r"[a-zA-Z]+", text.lower())
        digest = text.encode()
        for _ in range(150):                 # tune this to control CPU cost
            digest = hashlib.sha256(digest).digest()
        total += len(words)
    return jsonify(notes=len(rows), words=total)

# I/O-oriented: GET reads recent notes, POST writes one
@app.route("/patients/notes/", methods=["GET", "POST"])
def notes():
    conn = pool.getconn()
    try:
        with conn, conn.cursor() as cur:
            if request.method == "POST":
                body = request.get_json(silent=True) or {}
                cur.execute("INSERT INTO notes (patient_id, text) VALUES (%s, %s)",
                            (body.get("patient_id", 1), body.get("text", "note")))
            cur.execute("SELECT id, patient_id, left(text, 40) FROM notes ORDER BY id DESC LIMIT 50")
            rows = cur.fetchall()
    finally:
        pool.putconn(conn)
    return jsonify(count=len(rows))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
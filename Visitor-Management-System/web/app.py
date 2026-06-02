from flask import Flask, request, jsonify, render_template
import psycopg2
import redis

app = Flask(__name__)

# PostgreSQL Connection
db = psycopg2.connect(
    host="postgres",
    database="visitors",
    user="admin",
    password="admin123"
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS visitors (
    id SERIAL PRIMARY KEY,
    visitor_id VARCHAR(50),
    name VARCHAR(100),
    purpose VARCHAR(200)
)
""")

db.commit()

# Redis Connection
r = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/visits")
def visits():
    count = r.incr("homepage_visits")
    return jsonify({"visits": count})

@app.route("/api/visitor", methods=["POST"])
def add_visitor():
    data = request.json

    cursor.execute(
        "INSERT INTO visitors (visitor_id, name, purpose) VALUES (%s, %s, %s)",
        (data["visitor_id"], data["name"], data["purpose"])
    )
    db.commit()

    return jsonify({"message": "Visitor Added Successfully"})

@app.route("/api/visitor", methods=["GET"])
def get_visitors():
    cursor.execute("SELECT * FROM visitors")
    visitors = cursor.fetchall()

    result = []
    for visitor in visitors:
        result.append({
            "id": visitor[0],
            "visitor_id": visitor[1],
            "name": visitor[2],
            "purpose": visitor[3]
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

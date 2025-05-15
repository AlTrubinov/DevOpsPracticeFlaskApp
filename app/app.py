from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import mysql.connector
import os

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint"]
)


@app.before_request
def before_request():
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()


@app.route("/")
def index():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="db",
            user="root",
            password=os.getenv("MYSQL_ROOT_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        )
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        return jsonify({"tables": tables})
    except mysql.connector.Error as err:
        return jsonify({"error": f"MySQL connector error: {err}"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if connection:
            connection.close()


@app.route("/ping")
def ping():
    return jsonify({"message": "ping"})


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=5000, debug=os.environ.get("FLASK_ENV") == "development"
    )

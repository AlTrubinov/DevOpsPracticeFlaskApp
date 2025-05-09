from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

@app.route('/')
def index():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='db',
            user='root',
            password=os.getenv('MYSQL_ROOT_PASSWORD'),
            database=os.getenv('MYSQL_DB_NAME')
        )
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        return jsonify({"tables": tables})
    except mysql.connector.Error as err:
        return jsonify({"error": f"MySQL error: {err}, MYSQL_ROOT_PASSWORD: {os.getenv('MYSQL_ROOT_PASSWORD')}, MYSQL_DB_NAME: {os.getenv('MYSQL_DB_NAME')}"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if connection:
            connection.close()

@app.route('/ping')
def ping():
    return jsonify({"message": "ping"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=os.environ.get("FLASK_ENV") == "development")

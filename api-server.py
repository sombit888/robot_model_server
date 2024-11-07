from flask import Flask, jsonify, request

app = Flask(__name__)

# Define a simple route
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World!"})

# Another route that takes a parameter
@app.route('/api/greet/<name>', methods=['GET'])
def greet(name):
    return jsonify({"message": f"Hello, {name}!"})

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

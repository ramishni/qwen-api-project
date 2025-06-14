from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify(message="Hello World from Flask!")

@app.route('/call', methods=['POST'])
def handle_call():
    try:
        data = request.get_json(silent=True)
        name = data.get('name', 'World') if data else 'World'
        return jsonify(message=f"Hello {name} from Flask!")
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

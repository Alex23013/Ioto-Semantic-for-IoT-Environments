from flask import Flask, jsonify, request

app = Flask(__name__)

meassures = []


@app.route('/meassures')
def get_meassures():
    return jsonify(meassures)


@app.route('/meassures', methods=['POST'])
def add_meassure():
    meassures.append(request.get_json())
    return 'meassure received', 201

@app.route("/")
def welcome_message():
    return "Hello, from smart building!"


if __name__ == '__main__':
    app.run(port=5000)
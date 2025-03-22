from flask import Flask, jsonify, request, render_template
from bot import send_request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/receptionist', methods=['GET'])
def chat_with_receptionist():
    return send_request(request.args.get('message'))

if __name__ == '__main__':
    app.run(debug=True)
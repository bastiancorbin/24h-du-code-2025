from flask import Flask, jsonify, request, render_template, send_from_directory
from bot import send_request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/receptionist', methods=['GET'])
def chat_with_receptionist():
    return send_request(request.args.get('message'))

# New route to serve the Three.js animation
@app.route('/animation')
def animation():
    return render_template('animation.html')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)

if __name__ == '__main__':
    app.run(debug=True)
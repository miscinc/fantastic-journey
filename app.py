from flask import Flask, request, jsonify
import os, json, uuid, random
from datetime import datetime

app = Flask(__name__)

# Ensure the json directory exists
os.makedirs('json', exist_ok=True)

def generate_unique_filename():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))

@app.route('/new', methods=['GET'])
def new_chat():
    unique_id = generate_unique_filename()
    file_path = f'json/{unique_id}.json'
    data = {
        "meta": {
            "label": "",
            "name": "",
            "contact_info": {}
        },
        "chats": []
    }
    with open(file_path, 'w') as file:
        json.dump(data, file)
    return jsonify({"unique_id": unique_id})

@app.route('/save', methods=['POST'])
def save_chat():
    content = request.json
    unique_id = content['unique_id']
    message = content['message']
    sender = content.get('from', 'user')  # Default sender is 'user'
    file_path = f'json/{unique_id}.json'
    
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    with open(file_path, 'r+') as file:
        data = json.load(file)
        data['chats'].append({
            "timestamp": datetime.now().isoformat(),
            "from": sender,
            "message": message
        })
        file.seek(0)
        json.dump(data, file, indent=4)
    return jsonify({"success": True})

@app.route('/chat', methods=['GET'])
def get_chat():
    unique_id = request.args.get('unique_id')
    file_path = f'json/{unique_id}.json'
    
    if not os.path.exists(file_path):
        return jsonify({"error": "Not found"}), 404
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

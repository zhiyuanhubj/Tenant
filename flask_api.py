from flask import Flask, request, jsonify

app = Flask(__name__)


from chatgpt_tenant import Tenant_ask  # Import your Tenant_ask class from your existing code

@app.route('/generate_tenant_data', methods=['POST'])
def generate_tenant_data():
    try:
        data = request.json  # Assuming you send JSON data in the request
        dialogue_history = data.get('dialogue_history', '')

        tenant_communication = Tenant_ask(dialogue_history)
        result = tenant_communication.generation()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
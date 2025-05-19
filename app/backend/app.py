from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, origins=app.config['CORS_ORIGINS'], methods=app.config['CORS_METHODS'])
    
    # Register routes
    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            data = request.get_json()
            print(data)

            return {"response": f"This is a simulated response to: {data['message']}"}
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    
    return app
import warnings
import json
import asyncio
from datetime import datetime
from flask import Flask, request, jsonify
from crew import AgenteGerenciador

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = Flask(__name__)

@app.route("/", methods=["POST"])
async def index():
    data = request.get_json()
    user_planning_text = data.get("planning")
    if not user_planning_text:
        return jsonify({"error": "No planning provided"}), 400
    inputs = {'user_planning_text': user_planning_text}
    
    
    result = AgenteGerenciador().crew().kickoff(inputs=inputs)   
    return str(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)

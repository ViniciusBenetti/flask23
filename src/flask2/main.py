import sys 
import os
import warnings
from datetime import datetime
from crewai import LLM
from crew import CybersecurityProject
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

os.environ["GROQ_API_KEY"] = "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"  


llm = LLM(
    model="groq/gemma2-9b-it",  
    api_key=os.environ.get("GROQ_API_KEY")
)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run(msg=None):
    """Executa as funções sequencialmente, uma por vez"""
    try:
        scam_result = check_scam(msg)
        print(scam_result)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def check_scam(user_story: str):
    """Executa apenas a tarefa de verificação de golpe"""
    inputs = {
        'topic': user_story,
        'current_year': str(datetime.now().year),
        'task_type': 'check_scam'
    }
    
    try:
        result = CybersecurityProject(llm=llm).crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while checking for scam: {e}")
    

@app.route('/',methods=['POST'])
def checkScam():
    if request.method == 'POST':
        try:
            input = request.get_json()
            mensagem = input.get('mensagem')
        
            result = run(mensagem)
            print('sucesso')
            return jsonify({"resposta":result}),200
        except Exception as e:
            print(e)
            return jsonify({"resposta":"erro interno"}),500

if __name__ == "__main__":
    app.run(debug=True)

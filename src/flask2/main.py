import os
import sys
import warnings
from datetime import datetime
from crewai import LLM
from crew import CybersecurityProject
import os
import signal
from flask import Flask, jsonify, request
from flask_cors import CORS
from pyngrok import ngrok, conf

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
        
def start_ngrok():
    conf.get_default().auth_token = "2yPVGVqqzKuw7ix1b06J6ttR8GT_2FAoFo8pFgYmQP48n5ea"
    tunnel = ngrok.connect(5000, "http")
    print(f"URL pública do ngrok: {tunnel.public_url}")
    return tunnel

def signal_handler(sig, frame):
    ngrok.disconnect(ngrok.get_tunnels()[0].public_url)
    print("\nNgrok e Flask encerrados.")
    sys.exit(0)



if __name__ == "__main__":
    # Iniciar o ngrok
    tunnel = start_ngrok()
    # Capturar Ctrl+C para encerrar graceful
    signal.signal(signal.SIGINT, signal_handler)
    app.run(host='0.0.0.0',port=5000,debug=True)

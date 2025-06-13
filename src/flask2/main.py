import sys
import warnings
from datetime import datetime
from crewai import LLM
from crew import CybersecurityProject
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import socket


app = Flask(__name__)
CORS(app)

# Configurar a chave da API
os.environ["GROQ_API_KEY"] = "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"

# Inicializar o LLM
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
        return scam_result
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

@app.route('/', methods=['POST'])
def checkScam():
    if request.method == 'POST':
        try:
            input_data = request.get_json()
            mensagem = input_data.get('mensagem')
            if not mensagem:
                return jsonify({"resposta": "Mensagem não fornecida"}), 400
            result = run(mensagem)
            print('Sucesso na verificação de golpe')
            return jsonify({"resposta": str(result)}), 200
        except Exception as e:
            print(f"Erro na rota /: {e}")
            return jsonify({"resposta": "Erro interno no servidor"}), 500

def is_port_in_use(port):
    """Verifica se a porta está em uso"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if __name__ == "__main__":

    if is_port_in_use(5000):
        print("Erro: A porta 5000 já está em uso. Encerrando processos existentes ou escolha outra porta.")
        sys.exit(1)

    try:
        print("Iniciando servidor Flask...")
        app.run(host='0.0.0.0', port=5000, debug=False)  
    except Exception as e:
        print(f"Erro ao iniciar o Flask: {e}")
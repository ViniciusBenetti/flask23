import sys
import warnings
from datetime import datetime
from crew import CybersecurityProject
import flask
import os


os.environ = ['OPEN']

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Executa as funções sequencialmente, uma por vez"""
    try:
        scam_result = check_scam("gerente da empresa A2FBR LTDA que fala que tem uma licença formal e informa o CNPJ e procura blogueiros de qualidade para trabalhar com eles e paga adiantado e envia um link no instagram que da em um numero no whatsapp para saber mais")
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
        result = CybersecurityProject().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while checking for scam: {e}")

if __name__ == "__main__":
    result = run()
    print(result)

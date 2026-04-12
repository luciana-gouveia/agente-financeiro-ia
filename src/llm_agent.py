from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def responder(pergunta, contexto=""):
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um assistente financeiro simples e direto."},
            {"role": "user", "content": f"{contexto}\nPergunta: {pergunta}"}
        ]
    )
    return resposta.choices[0].message.content
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def responder(pergunta, contexto):
    try:
        model = genai.GenerativeModel('gemini-3.1-flash-image-preview')
        
        prompt = f"""
        Você é um consultor financeiro pessoal de 2026. 
        Analise os dados abaixo e responda de forma curta, útil e amigável.

        DADOS DO USUÁRIO:
        {contexto}

        PERGUNTA:
        {pergunta}

        Se houver gastos altos, sugira uma economia específica.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        if "429" in str(e):
            return "Limite de requisições atingido. Tente novamente em 1 minuto."
        return f"Erro na IA: {e}"

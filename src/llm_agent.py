import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega a chave da API do arquivo .env
load_dotenv()

# Configura a conexão com o Google
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def responder(pergunta, contexto):
    try:
        # Usando o modelo da sua lista (ajustado para 2026)
        model = genai.GenerativeModel('gemini-3.1-flash-image-preview')
        
        prompt = f"""
        Você é um consultor financeiro pessoal de 2026. 
        Analise os dados abaixo e responda de forma curta, útil e amigável.
        
        DADOS DO USUÁRIO:
        {contexto}
        
        PERGUNTA:
        {pergunta}
        
        Dica: Se o usuário estiver gastando muito, sugira uma economia específica.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        # Tratamento amigável para o erro de cota (429)
        if "429" in str(e):
            return "O Google pausou as requisições gratuitas por 60 segundos. Respire fundo e tente de novo em um minuto! ☕"
        return f"Erro na IA: {e}"
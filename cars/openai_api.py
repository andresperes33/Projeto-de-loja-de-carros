import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def get_car_ai_bio(model, brand, year):
    prompt = f"Crie uma descrição de venda curta e atraente para o carro {brand} {model} {year} com no máximo 200 caracteres. Fale sobre qualidade e oportunidade."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
             max_tokens=100,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro na API OpenAI: {e}")
        return f"Este {brand} {model} {year} está em excelente estado. Uma ótima oportunidade para você!"

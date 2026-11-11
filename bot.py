import os
import requests
from google import genai
from google.genai import types

# 1. Configurar credenciales desde los secretos de GitHub Actions
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "@ParleyVIPIA"

def generar_parley():
    # Inicializar el cliente oficial de Gemini
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = (
        "Actúa como un tipster experto en apuestas de fútbol de categoría prémium. "
        "Genera un pronóstico combinado tipo Bet Builder de exactamente 5 partidos de fútbol para hoy. "
        "Reglas estrictas:\n"
        "1. Cuotas altas y atractivas en cada selección.\n"
        "2. PROHIBIDO incluir mercados de 'Ambos marcan: No' o variantes similares.\n"
        "3. Usa mercados de ganadores, más de 2.5 goles, tiros de esquina o combinaciones lógicas de Bet Builder.\n"
        "4. Presenta el mensaje listo para publicar en un canal de Telegram, con un diseño profesional, emojis llamativos, cuotas estimadas por partido y la cuota total combinada."
    )
    
    # Llamada al modelo utilizando gemini-2.5-flash
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    return response.text

def enviar_a_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("¡Parley enviado con éxito a Telegram!")
    else:
        print(f"Error al enviar a Telegram: {response.text}")

if __name__ == "__main__":
    print("Generando parley con Gemini...")
    texto_parley = generar_parley()
    print("Enviando a Telegram...")
    enviar_a_telegram(texto_parley)

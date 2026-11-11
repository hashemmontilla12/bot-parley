import os
import requests
from google import genai

API_KEY_GEMINI = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "@ParleyVIPIA"

print("⚽ 1. Obteniendo partidos de fútbol de hoy...")
url_api_futbol = "https://site.api.espn.com/apis/site/v2/sports/soccer/all/scoreboard"

try:
    respuesta = requests.get(url_api_futbol)
    datos = respuesta.json()
    eventos = datos.get('events', [])
    partidos_encontrados = ""
    
    if not eventos:
        partidos_encontrados = "- No se detectaron partidos principales programados."
    else:
        lista_juegos = []
        for i, evento in enumerate(eventos[:12], 1):
            liga = evento.get('season', {}).get('slug', 'Fútbol')
            nombre_partido = evento.get('name', 'Partido')
            lista_juegos.append(f"- Juego {i} [{liga.upper()}]: {nombre_partido}")
        partidos_encontrados = "\n".join(lista_juegos)
        
    print(f"✅ Partidos detectados:\n{partidos_encontrados}\n")

except Exception as e:
    print(f"⚠️ Error al conectar con ESPN: {e}")
    partidos_encontrados = "- Real Madrid vs PSG\n- Chelsea vs Roma"

print("🤖 2. Generando pronósticos optimizados para 5 partidos...")
client = genai.Client(api_key=API_KEY_GEMINI)

prompt = f"""
Eres un analista experto en apuestas deportivas y creador de apuestas compuestas (Bet Builder / Mismo Partido).
Aquí tienes la lista de partidos de fútbol reales de hoy:

{partidos_encontrados}

Tu tarea:
1. Selecciona los 5 mejores partidos de la lista.
2. Para CADA uno de los 5 partidos, diseña una apuesta combinada de un mismo partido (Creación de Apuesta). 
   - REGLA ESTRICTA: **Quedan prohibidas las selecciones de tipo "Ambos marcan: No"** o porterías a cero arriesgadas. 
   - Enfócate en combinaciones lógicas de alto rendimiento como: 
     * "Gana [Equipo] y Ambos equipos marcan (Sí)"
     * "Gana [Equipo] y Más de 2.5 goles"
     * "Empate o Gana [Equipo] y Más de 1.5 goles"
3. Incluye una justificación técnica breve de por qué se combinan ambos sucesos.
4. Al final, arma un boleto resumen tipo parley con las 5 selecciones y una cuota total estimada alta.
5. IMPORTANTE PARA EL FORMATO: Usa exclusivamente etiquetas HTML de Telegram para dar formato (ejemplo: <b>Texto en negrita</b>, <i>cursiva</i>). NUNCA uses asteriscos (**). Utiliza emojis atractivos (⚽, 📊, 🎯, 🔥, 💰).
"""

response = client.models.generate_content(
    model='gemini-3.8-flash',
    contents=prompt,
)

parley_final = response.text

print("📲 3. Enviando el parley de 5 partidos al canal de Telegram...")

url_telegram = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": parley_final,
    "parse_mode": "HTML"
}

resultado = requests.post(url_telegram, json=payload)

if resultado.status_code == 200:
    print("\n🎉 ¡ÉXITO TOTAL! El parley de 5 partidos ya fue publicado en tu canal.")
else:
    print(f"\n❌ Error al enviar a Telegram: {resultado.text}")

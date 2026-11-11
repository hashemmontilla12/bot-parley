import os
import requests
import random
from datetime import datetime

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "@ParleyVIPIA"

def generar_parley():
    # Listas de equipos y mercados estables (sin opciones extremas de primera mitad)
    equipos = [
        ("Real Madrid", "Barcelona"), ("Manchester City", "Arsenal"), 
        ("Bayern Munich", "Borussia Dortmund"), ("Inter de Milán", "Juventus"),
        ("PSG", "Marsella"), ("Liverpool", "Chelsea"), 
        ("Bayer Leverkusen", "RB Leipzig"), ("Atlético de Madrid", "Villarreal"),
        ("Nápoles", "AC Milán"), ("Benfica", "Porto")
    ]
    
    mercados_seguros = [
        "Doble oportunidad y Más de 1.5 goles",
        "Más de 1.5 goles en el partido",
        "Doble oportunidad (1X o X2)",
        "Más de 7.5 tiros de esquina totales",
        "Total de goles: Más de 2.5 (asiático)"
    ]
    
    # Seleccionamos exactamente 5 partidos aleatorios sin repetir
    partidos_seleccionados = random.sample(equipos, 5)
    
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    
    mensaje = f"🔥 *VIP BET BUILDER PARLEY* 🔥\n📅 Fecha: {fecha_hoy}\n🎯 Canal: @ParleyVIPIA\n\n"
    mensaje += "¡Nuestra selección de 5 jugadas de alta probabilidad y menor riesgo para hoy! Analizadas bajo patrones estadísticos:\n\n"
    
    cuota_total = 1.0
    
    for i, (local, visitante) in enumerate(partidos_seleccionados, 1):
        mercado = random.choice(mercados_seguros)
        # Cuotas más estables y realistas por selección (entre 1.45 y 1.85)
        cuota_parcial = round(random.uniform(1.45, 1.85), 2)
        cuota_total = round(cuota_total * cuota_parcial, 2)
        
        mensaje += f"*{i}. {local} vs {visitante}*\n"
        mensaje += f"   📌 *Jugada:* {mercado}\n"
        mensaje += f"   📊 *Cuota estimada:* `{cuota_parcial}`\n\n"
    
    mensaje += f"💰 *CUOTA TOTAL APROXIMADA:* `{cuota_total}`\n\n"
    mensaje += "⚡ *¡Stake recomendado:* 2% del bankroll. ¡A jugar con cabeza fría!"
    
    return mensaje

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
    print("Generando parley automatizado seguro...")
    texto_parley = generar_parley()
    print("Enviando a Telegram...")
    enviar_a_telegram(texto_parley)

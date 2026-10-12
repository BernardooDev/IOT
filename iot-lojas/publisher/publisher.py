"""Simula 14 sensores de temperatura de câmaras frias (1 por loja)."""
import json
import os
import random
import time

import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_HOST", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
INTERVALO = float(os.getenv("INTERVALO", "2"))           # 60 em produção
ANOMALIA_APOS = float(os.getenv("ANOMALIA_APOS", "180"))  # segundos até a anomalia
LOJA_ANOMALA = "loja07"
LOJAS = [f"loja{i:02d}" for i in range(1, 15)]
TOPIC = "varejo/{loja}/camara-fria/temperatura"           # topic tree da Parte A.3.c

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="simulador-lojas")
client.connect(BROKER, PORT)
client.loop_start()

temps = {loja: random.uniform(3.5, 6.5) for loja in LOJAS}
inicio = time.time()

while True:
    anomalia = (time.time() - inicio) > ANOMALIA_APOS
    for loja in LOJAS:
        if anomalia and loja == LOJA_ANOMALA:
            temps[loja] = min(temps[loja] + 0.5, 12.0)  # sobe até 12 °C
        else:
            temps[loja] = max(2.0, min(8.0, temps[loja] + random.uniform(-0.3, 0.3)))
        payload = {"loja": loja, "temperatura": round(temps[loja], 2)}
        client.publish(TOPIC.format(loja=loja), json.dumps(payload))
    time.sleep(INTERVALO)

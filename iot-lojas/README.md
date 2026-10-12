# Monitoramento de temperatura – 14 lojas (MQTT → Telegraf → InfluxDB → Grafana)

## Pré-requisitos
Docker + Docker Compose v2, Python 3.9+.

## Subir a stack "do zero"
```bash
git clone <URL-DO-REPOSITORIO> && cd iot-lojas
docker compose up -d
docker compose ps        # aguardar os 4 serviços em "healthy" (~30 s)
```

| Serviço   | Endereço                | Credenciais            |
|-----------|-------------------------|------------------------|
| Mosquitto | localhost:1883          | anônimo (lab)          |
| InfluxDB  | http://localhost:8086   | admin / admin12345     |
| Grafana   | http://localhost:3000   | admin / admin          |

O datasource InfluxDB do Grafana já é provisionado automaticamente.

## Rodar o simulador (14 lojas)
```bash
cd publisher
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python publisher.py
```
Variáveis opcionais: `INTERVALO` (padrão 2 s), `ANOMALIA_APOS` (padrão 180 s), `MQTT_HOST`.

## Verificar mensagens
```bash
docker exec -it mosquitto mosquitto_sub -t 'varejo/#' -v
```

## Topic tree
`varejo/<loja01..loja14>/camara-fria/temperatura` — payload `{"loja":"loja07","temperatura":5.2}`

## Derrubar
```bash
docker compose down        # mantém dados
docker compose down -v     # apaga dados
```

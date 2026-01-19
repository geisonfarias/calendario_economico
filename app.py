from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

# =========================
# CONFIGURAÇÕES DE CACHE
# =========================
CACHE_DATA = None
CACHE_TIME = None
CACHE_TTL = 600  # 10 minutos (em segundos)

# =========================
# ROTA HOME (TESTE)
# =========================
@app.route("/")
def home():
    return "API Calendário Econômico rodando 🚀"

# =========================
# FUNÇÃO QUE BUSCA DADOS
# (com cache)
# =========================
def buscar_calendario():
    global CACHE_DATA, CACHE_TIME

    agora = datetime.utcnow()

    # Se cache ainda é válido
    if CACHE_DATA and CACHE_TIME and (agora - CACHE_TIME).seconds < CACHE_TTL:
        print("⚡ Usando cache")
        return CACHE_DATA

    print("🌐 Buscando dados externos...")

    tz_br = pytz.timezone("America/Sao_Paulo")
    hoje = datetime.now(tz_br).date()
    fim = hoje + timedelta(days=7)

    url = f"https://api.tradingeconomics.com/calendar/country/all/{hoje}/{fim}?c=guest:guest"

    r = requests.get(url, timeout=15)
    dados = r.json()

    eventos = []

    for e in dados:
        impacto = e.get("Importance", 0)

        # impacto mínimo = 1
        if impacto >= 1:
            eventos.append({
                "data": e.get("Date"),
                "pais": e.get("Country"),
                "evento": e.get("Event"),
                "impacto": impacto,
                "atual": e.get("Actual", ""),
                "previsto": e.get("Forecast", ""),
                "anterior": e.get("Previous", "")
            })

    # Atualiza cache
    CACHE_DATA = eventos
    CACHE_TIME = agora

    return eventos

# =========================
# ROTA DO CALENDÁRIO
# =========================
@app.route("/calendario")
def calendario():
    try:
        dados = buscar_calendario()
        return jsonify(dados)

    except Exception as erro:
        return jsonify({"erro": str(erro)})

# =========================
# START
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

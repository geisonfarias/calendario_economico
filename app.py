from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

@app.route("/")
def home():
    return "API Calendário Econômico rodando 🚀"

@app.route("/calendario")
def calendario():
    tz_br = pytz.timezone("America/Sao_Paulo")

    hoje = datetime.now(tz_br).date()
    fim = hoje + timedelta(days=7)

    url = f"https://api.tradingeconomics.com/calendar/country/all/{hoje}/{fim}?c=guest:guest"

    try:
        r = requests.get(url, timeout=10)
        dados = r.json()

        eventos = []
        for e in dados:
            impacto = e.get("Importance", 0)
            if impacto >= 1:  # impacto mínimo
                eventos.append({
                    "data": e.get("Date"),
                    "pais": e.get("Country"),
                    "evento": e.get("Event"),
                    "impacto": impacto,
                    "atual": e.get("Actual"),
                    "previsto": e.get("Forecast"),
                    "anterior": e.get("Previous")
                })

        return jsonify(eventos)

    except Exception as erro:
        return jsonify({"erro": str(erro)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

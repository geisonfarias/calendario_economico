from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

TZ_BR = pytz.timezone("America/Sao_Paulo")

@app.route("/")
def home():
    return "API Calendário Econômico OK"

@app.route("/calendario")
def calendario():
    impacto_min = int(request.args.get("impacto", 1))
    dias = int(request.args.get("dias", 7))

    hoje = datetime.now(TZ_BR).date()

    eventos = []
    for i in range(dias + 1):
        dia = hoje + timedelta(days=i)
        eventos.append({
            "data": dia.strftime("%Y-%m-%d"),
            "hora": "09:00",
            "moeda": "USD",
            "evento": f"Evento teste dia {i}",
            "impacto": impacto_min
        })

    return jsonify(eventos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


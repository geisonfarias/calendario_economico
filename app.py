from flask import Flask, jsonify, request
import requests
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://br.investing.com/economic-calendar/",
}

@app.route("/")
def home():
    return "API Calendário Econômico rodando 🚀"

@app.route("/calendario")
def calendario():
    impacto_min = int(request.args.get("impacto", 1))

    tz_br = pytz.timezone("America/Sao_Paulo")
    hoje = datetime.now(tz_br)
    fim = hoje + timedelta(days=7)

    url = "https://www.investing.com/economic-calendar/Service/getCalendarFilteredData"

    payload = {
        "dateFrom": hoje.strftime("%Y-%m-%d"),
        "dateTo": fim.strftime("%Y-%m-%d"),
        "timeZone": "55",      # Brasil
        "timeFilter": "timeRemain",
        "currentTab": "custom",
        "limit_from": 0
    }

    r = requests.post(url, data=payload, headers=HEADERS, timeout=15)
    data = r.json()

    eventos = []

    for e in data.get("data", []):
        impacto = e.get("importance", 0)
        if impacto < impacto_min:
            continue

        data_evento = datetime.fromtimestamp(
            int(e["timestamp"]),
            tz=pytz.utc
        ).astimezone(tz_br)

        eventos.append({
            "data": data_evento.strftime("%Y-%m-%d %H:%M"),
            "pais": e.get("country"),
            "evento": e.get("event"),
            "impacto": impacto,
            "atual": e.get("actual"),
            "previsto": e.get("forecast"),
            "anterior": e.get("previous")
        })

    return jsonify(eventos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

@app.route("/")
def home():
    return "API Calendário Econômico MQL5 rodando 🚀"

@app.route("/calendario")
def calendario():
    url = "https://www.mql5.com/pt/economic-calendar"

    r = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    tz_br = pytz.timezone("America/Sao_Paulo")
    hoje = datetime.now(tz_br).date()
    fim = hoje + timedelta(days=7)

    eventos = []

    linhas = soup.select("div.ec-event")

    for l in linhas:
        try:
            data_str = l.get("data-time")
            if not data_str:
                continue

            # timestamp vem em segundos
            data_evento = datetime.fromtimestamp(
                int(data_str), tz=pytz.utc
            ).astimezone(tz_br)

            if not (hoje <= data_evento.date() <= fim):
                continue

            impacto = l.select_one(".ec-importance")
            impacto_txt = impacto.get_text(strip=True) if impacto else ""

            impacto_n = (
                3 if "Alto" in impacto_txt else
                2 if "Médio" in impacto_txt else
                1
            )

            eventos.append({
                "data": data_evento.strftime("%Y-%m-%d %H:%M"),
                "pais": l.select_one(".ec-country").get_text(strip=True),
                "evento": l.select_one(".ec-event-name").get_text(strip=True),
                "impacto": impacto_n
            })

        except:
            continue

    return jsonify(eventos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

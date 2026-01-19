from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "pt-BR,pt;q=0.9"
}

@app.route("/")
def home():
    return "API Calendário Econômico rodando 🚀"

@app.route("/calendario")
def calendario():
    impacto_min = int(request.args.get("impacto", 1))

    tz_br = pytz.timezone("America/Sao_Paulo")
    hoje = datetime.now(tz_br).date()
    fim = hoje + timedelta(days=7)

    url = "https://br.investing.com/economic-calendar/"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    eventos = []

    linhas = soup.select("tr.js-event-item")

    for l in linhas:
        try:
            data_str = l.get("data-event-datetime")
            if not data_str:
                continue

            data_evento = datetime.fromisoformat(data_str.replace("Z", "+00:00")).astimezone(tz_br)

            if not (hoje <= data_evento.date() <= fim):
                continue

            estrelas = len(l.select(".grayFullBullishIcon"))
            if estrelas < impacto_min:
                continue

            eventos.append({
                "data": data_evento.strftime("%Y-%m-%d %H:%M"),
                "pais": l.get("data-country"),
                "evento": l.select_one(".event").get_text(strip=True),
                "impacto": estrelas
            })

        except:
            continue

    return jsonify(eventos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

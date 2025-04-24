"""Simple Flask app for **Alertas Urbanos** _SEM MongoDB_
-------------------------------------------------------------------------------
Objetivo: demonstrar o fluxo CI/CD no Azure com uma aplicação funcional, mas
sem dependências externas de banco‐de‐dados. Todos os dados ficam em memória
(durante o ciclo de vida do container).

Funcionalidades
• Tela web inicial lista alertas cadastrados.
• Formulário para upload de um arquivo **CSV** (colunas: descricao,categoria,latitude,longitude).
  Cada linha vira um alerta com status "Pendente".
• API REST:
  –   GET  /api/alertas            → lista JSON
  –   PATCH /api/alertas/<id>      → altera status (Pendente│Em andamento│Resolvido)
-------------------------------------------------------------------------------
Como rodar localmente
$ docker compose up --build   # ou python app.py
Depois abra http://localhost:5000
-------------------------------------------------------------------------------
"""

import csv
from datetime import datetime
from io import TextIOWrapper
from typing import List, Dict

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template_string,
    request,
    url_for,
)

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Dados em memória -----------------------------------------------------------
# ---------------------------------------------------------------------------
Alert = Dict[str, object]
alertas: List[Alert] = []  # será preenchido em runtime

STATUS = {"Pendente", "Em andamento", "Resolvido"}

# ---------------------------------------------------------------------------
# Templates HTML (string inline para simplicidade) ---------------------------
# ---------------------------------------------------------------------------
TPL_INDEX = """
<!doctype html>
<title>Alertas Urbanos</title>
<h1>Alertas Urbanos (Demo sem BD)</h1>
<p><a href="{{ url_for('index') }}">Atualizar lista</a></p>
<form action="{{ url_for('upload_csv') }}" method="post" enctype="multipart/form-data">
  <h3>Enviar arquivo CSV</h3>
  <input type="file" name="file" accept="text/csv" required>
  <button type="submit">Enviar</button>
</form>
{% if alertas %}
<table border="1" cellpadding="4" cellspacing="0">
  <tr><th>ID</th><th>Descrição</th><th>Categoria</th><th>Status</th><th>Data</th></tr>
  {% for a in alertas %}
  <tr>
    <td>{{ a['id'] }}</td>
    <td>{{ a['descricao'] }}</td>
    <td>{{ a['categoria'] }}</td>
    <td>{{ a['status'] }}</td>
    <td>{{ a['created_at'].strftime('%d/%m %H:%M') }}</td>
  </tr>
  {% endfor %}
</table>
{% else %}<p>Nenhum alerta cadastrado.</p>{% endif %}
"""

# ---------------------------------------------------------------------------
# Rotas Web ------------------------------------------------------------------
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template_string(TPL_INDEX, alertas=alertas)


@app.route("/upload", methods=["POST"])
def upload_csv():
    """Recebe CSV e converte em alertas."""
    file = request.files.get("file")
    if not file or file.filename == "":
        return "Arquivo não enviado", 400

    reader = csv.DictReader(TextIOWrapper(file, encoding="utf-8"))
    required_cols = {"descricao", "categoria", "latitude", "longitude"}
    if not required_cols.issubset(reader.fieldnames or {}):
        return f"CSV deve conter colunas: {', '.join(required_cols)}", 400

    next_id = (alertas[-1]["id"] + 1) if alertas else 1
    for row in reader:
        alertas.append(
            {
                "id": next_id,
                "descricao": row["descricao"],
                "categoria": row["categoria"],
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
                "status": "Pendente",
                "created_at": datetime.utcnow(),
            }
        )
        next_id += 1

    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# API -----------------------------------------------------------------------
# ---------------------------------------------------------------------------
@app.route("/api/alertas", methods=["GET"])
def get_alertas():
    return jsonify(alertas)


@app.route("/api/alertas/<int:alert_id>", methods=["PATCH"])
def patch_alert(alert_id):
    body = request.json or {}
    new_status = body.get("status")
    if new_status not in STATUS:
        return {"error": "Status inválido"}, 400

    for a in alertas:
        if a["id"] == alert_id:
            a["status"] = new_status
            return {"message": "ok"}
    return {"error": "alerta não encontrado"}, 404


# ---------------------------------------------------------------------------
# Main ----------------------------------------------------------------------
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import os

    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

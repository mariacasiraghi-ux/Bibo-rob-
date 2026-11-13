from flask import Flask, jsonify, request
from threading import Lock

app = Flask(__name__)
ORIGENS_PERMITIDAS = {
    "http://127.0.0.1:5500", "http://127.0.0.1:5501",
    "http://localhost:5500", "http://localhost:5501"
}

@app.after_request
def permitir_rosto_local(resposta):
    origem = request.headers.get("Origin")
    if origem in ORIGENS_PERMITIDAS:
        resposta.headers["Access-Control-Allow-Origin"] = origem
        resposta.headers["Vary"] = "Origin"
    return resposta

estado_bibo = {
    "expressao": "calmo", "direcao": "centro",
    "status": "DISPONIVEL", "piscada_id": 0
}
bloqueio = Lock()

@app.get("/estado")
def consultar_estado():
    with bloqueio:
        return jsonify(estado_bibo.copy())

@app.post("/estado")
def atualizar_estado():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({"erro": "JSON invalido"}), 400
    with bloqueio:
        for campo in ("expressao", "direcao", "status"):
            if campo in dados:
                estado_bibo[campo] = dados[campo]
        if dados.get("piscar") is True:
            estado_bibo["piscada_id"] += 1
        return jsonify(estado_bibo.copy())

if __name__ == "__main__":
    print("Servidor do BIBOU iniciado!")
    app.run(host="127.0.0.1", port=5000, debug=False)

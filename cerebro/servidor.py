
from flask import Flask, jsonify, request
from threading import Lock

app = Flask(__name__)


@app.after_request
def permitir_rosto_local(resposta):
    resposta.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5500"
    return resposta


estado_bibo = {
    "expressao": "normal",
    "direcao": "centro",
    "status": "DISPONIVEL"
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
        return jsonify({"erro": "JSON inválido"}), 400

    with bloqueio:
        for campo in ("expressao", "direcao", "status"):
            if campo in dados:
                estado_bibo[campo] = dados[campo]

        return jsonify(estado_bibo.copy())


if __name__ == "__main__":
    print("Servidor do BIBO iniciado!")
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )

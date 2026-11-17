
from flask import Flask, request, jsonify
from flask_cors import CORS
from conversa import ConversaBibo

app = Flask(__name__)

# Enderecos autorizados durante o desenvolvimento
ORIGENS_PERMITIDAS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5501",
    "http://localhost:5501"
]

# Configurar CORS para a API
CORS(
    app,
    origins=ORIGENS_PERMITIDAS,
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"]
)

# Inicializar o cerebro
bibo = ConversaBibo()


@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "online": True,
        "nome": "BIBO",
        "sistema": "Cerebro Python"
    })


@app.route("/api/conversar", methods=["POST"])
def conversar():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie um JSON valido."
        }), 400

    mensagem = dados.get("mensagem")

    if not isinstance(mensagem, str):
        return jsonify({
            "erro": "A mensagem precisa ser um texto."
        }), 400

    if len(mensagem) > 2000:
        return jsonify({
            "erro": "Mensagem muito longa."
        }), 400

    resposta = bibo.responder(mensagem)

    return jsonify(resposta)


if __name__ == "__main__":
    print("=" * 40)
    print("BIBO - API DO CEREBRO")
    print("=" * 40)
    print("Servidor iniciado!")
    print("Porta: 5001")
    print("CORS configurado para desenvolvimento local")

    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )



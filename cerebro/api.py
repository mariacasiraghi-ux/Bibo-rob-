
import sys
import threading
import uuid
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS

# Permitir imports estáveis tanto ao iniciar api.py quanto ao importar app.
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
PASTA_CEREBRO = Path(__file__).resolve().parent
for caminho in (str(RAIZ_PROJETO), str(PASTA_CEREBRO)):
    if caminho not in sys.path:
        sys.path.insert(0, caminho)

from conversa import ConversaBibo
from controlador import ControladorBibo

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
controlador = ControladorBibo()
controle_lock = threading.RLock()
sessao_controle_ativa = None
geracao_controle = 0
sequencia_controle = 0
DIRECOES_PERMITIDAS = {"frente", "tras", "esquerda", "direita"}


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


@app.route("/api/controle/parar", methods=["POST"])
def parar():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um JSON valido."}), 400

    if dados.get("comando") != "parar":
        return jsonify({"erro": "Comando invalido. Envie comando=parar."}), 400

    ordenado = set(dados) == {
        "comando", "sessao", "geracao", "sequencia"
    }
    legado = set(dados) == {"comando"}
    if not ordenado and not legado:
        return jsonify({"erro": "Dados de parada invalidos."}), 400

    global sessao_controle_ativa, geracao_controle, sequencia_controle

    with controle_lock:
        if ordenado:
            if not isinstance(dados["sessao"], str):
                return jsonify({"erro": "Sessao invalida."}), 400
            if type(dados["geracao"]) is not int or type(dados["sequencia"]) is not int:
                return jsonify({"erro": "Geracao ou sequencia invalida."}), 400
            if (
                dados["sessao"] != sessao_controle_ativa
                or dados["geracao"] != geracao_controle
                or dados["sequencia"] <= sequencia_controle
            ):
                return jsonify({"erro": "Comando antigo ou fora de ordem."}), 409
            sequencia_controle = dados["sequencia"]
        else:
            # Compatibilidade com clientes antigos; invalida movimentos pendentes.
            sessao_controle_ativa = None
            geracao_controle += 1
            sequencia_controle = 0

        try:
            resultado = controlador.enviar_comando(
                {"sistema": "motores", "acao": "parar"},
                sincronizar_estado=legado
            )
        except Exception as erro:
            print("[API] Falha ao parar no ESP32 virtual:", type(erro).__name__)
            return jsonify({"erro": "Nao foi possivel confirmar a parada."}), 502

        if not isinstance(resultado, dict) or not resultado.get("sucesso"):
            mensagem = (
                resultado.get("mensagem", "Nao foi possivel confirmar a parada.")
                if isinstance(resultado, dict)
                else "Nao foi possivel confirmar a parada."
            )
            return jsonify({"erro": mensagem}), 502

        return jsonify({
            "sucesso": True,
            "estado": resultado["estado"],
            "rodas": resultado["rodas"]
        })


@app.route("/api/controle/sessao", methods=["POST"])
def iniciar_sessao_controle():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict) or set(dados) != {"sessao"}:
        return jsonify({"erro": "Envie um identificador de sessao valido."}), 400

    if not isinstance(dados["sessao"], str):
        return jsonify({"erro": "Sessao invalida."}), 400
    try:
        sessao = str(uuid.UUID(dados["sessao"]))
    except (ValueError, TypeError, AttributeError):
        return jsonify({"erro": "Sessao invalida."}), 400

    if controlador.comunicacao.modo != "virtual":
        return jsonify({"erro": "Somente o ESP32 virtual esta habilitado."}), 503

    global sessao_controle_ativa, geracao_controle, sequencia_controle
    with controle_lock:
        if sessao_controle_ativa is not None:
            try:
                parada = controlador.enviar_comando(
                    {"sistema": "motores", "acao": "parar"},
                    sincronizar_estado=False
                )
            except Exception as erro:
                print("[API] Falha ao preparar nova sessao:", type(erro).__name__)
                return jsonify({"erro": "Nao foi possivel parar a sessao anterior."}), 502
            if not isinstance(parada, dict) or not parada.get("sucesso"):
                return jsonify({"erro": "Nao foi possivel confirmar a parada anterior."}), 502

        geracao_controle += 1
        sessao_controle_ativa = sessao
        sequencia_controle = 0
        return jsonify({"sucesso": True, "sessao": sessao, "geracao": geracao_controle})


@app.route("/api/controle/movimento", methods=["POST"])
def movimento():
    dados = request.get_json(silent=True)
    campos = {"comando", "sessao", "geracao", "sequencia"}
    if not isinstance(dados, dict) or set(dados) != campos:
        return jsonify({"erro": "Dados de movimento invalidos."}), 400

    comando = dados["comando"]
    if not isinstance(comando, str) or comando not in DIRECOES_PERMITIDAS:
        return jsonify({"erro": "Direcao nao permitida."}), 400
    if (
        not isinstance(dados["sessao"], str)
        or type(dados["geracao"]) is not int
        or type(dados["sequencia"]) is not int
        or dados["sequencia"] <= 0
    ):
        return jsonify({"erro": "Sessao, geracao ou sequencia invalida."}), 400

    global sequencia_controle
    with controle_lock:
        if (
            controlador.comunicacao.modo != "virtual"
            or dados["sessao"] != sessao_controle_ativa
            or dados["geracao"] != geracao_controle
        ):
            return jsonify({"erro": "Sessao inativa ou modo virtual indisponivel."}), 409
        if dados["sequencia"] <= sequencia_controle:
            return jsonify({"erro": "Comando antigo ou fora de ordem."}), 409

        sequencia_controle = dados["sequencia"]
        try:
            resultado = controlador.enviar_comando(
                {"sistema": "motores", "acao": comando},
                sincronizar_estado=False
            )
        except Exception as erro:
            print("[API] Falha no movimento virtual:", type(erro).__name__)
            return jsonify({"erro": "Falha de comunicacao com o simulador."}), 502

        if not isinstance(resultado, dict) or not resultado.get("sucesso"):
            return jsonify({
                "erro": (resultado or {}).get(
                    "mensagem", "Movimento nao confirmado pelo simulador."
                ) if isinstance(resultado, dict) else "Movimento nao confirmado pelo simulador."
            }), 502

        return jsonify({"sucesso": True, "estado": resultado["estado"]})


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



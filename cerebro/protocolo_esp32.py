
import json
from datetime import datetime, timezone


class ProtocoloESP32:
    VERSAO = "1.0"

    @staticmethod
    def criar_comando(sistema, acao, parametros=None):
        if not isinstance(sistema, str) or not sistema.strip():
            raise ValueError("Sistema invalido")

        if not isinstance(acao, str) or not acao.strip():
            raise ValueError("Acao invalida")

        if parametros is None:
            parametros = {}

        if not isinstance(parametros, dict):
            raise ValueError("Parametros invalidos")

        return {
            "versao": ProtocoloESP32.VERSAO,
            "dispositivo": "BIBO",
            "tipo": "comando",
            "sistema": sistema,
            "acao": acao,
            "parametros": parametros,
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat()
        }

    @staticmethod
    def converter_json(mensagem):
        return json.dumps(
            mensagem,
            ensure_ascii=False
        )

    @staticmethod
    def ler_json(texto):
        return json.loads(texto)

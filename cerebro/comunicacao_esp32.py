
from config_esp32 import obter_configuracao
from protocolo_esp32 import ProtocoloESP32


class ComunicacaoESP32:
    def __init__(self):
        self.configuracao = obter_configuracao()
        self.modo = self.configuracao["modo"]
        self.conectado = self.modo == "virtual"

    def enviar(self, comando):
        if not isinstance(comando, dict):
            return {
                "sucesso": False,
                "mensagem": "Comando deve ser um dicionario"
            }

        try:
            mensagem = ProtocoloESP32.criar_comando(
                sistema=comando.get("sistema"),
                acao=comando.get("acao"),
                parametros=comando.get("parametros")
            )
        except ValueError as erro:
            return {
                "sucesso": False,
                "mensagem": str(erro)
            }

        if self.modo == "virtual":
            print("[ESP32 VIRTUAL] Mensagem preparada:")
            print(ProtocoloESP32.converter_json(mensagem))

            return {
                "sucesso": True,
                "modo": "virtual",
                "mensagem": "Comando preparado para simulacao",
                "dados": mensagem
            }

        if self.modo == "fisico":
            return {
                "sucesso": False,
                "modo": "fisico",
                "mensagem": "Conexao fisica ainda nao implementada"
            }

        return {
            "sucesso": False,
            "mensagem": "Modo ESP32 desconhecido"
        }

    def verificar_conexao(self):
        return {
            "conectado": self.conectado,
            "modo": self.modo
        }

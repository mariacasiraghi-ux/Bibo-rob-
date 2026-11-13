
from busca_base import BuscaBase


class EncaixeBase:
    def __init__(self):
        self.busca = BuscaBase()
        self.alinhado = False

    def verificar_alinhamento(self):
        distancia = self.busca.estacao.distancia_cm

        if distancia > 5:
            return {
                "alinhado": False,
                "mensagem": "BIBO ainda esta longe da base"
            }

        if not self.alinhado:
            return {
                "alinhado": False,
                "mensagem": "Ajuste de alinhamento necessario"
            }

        return {
            "alinhado": True,
            "mensagem": "BIBO alinhado com a base"
        }

    def encaixar(self):
        verificacao = self.verificar_alinhamento()

        if not verificacao["alinhado"]:
            return {
                "sucesso": False,
                "mensagem": verificacao["mensagem"]
            }

        return self.busca.estacao.conectar()

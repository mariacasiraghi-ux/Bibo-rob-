
from encaixe_base import EncaixeBase


class RecargaBateria:
    def __init__(self):
        self.encaixe = EncaixeBase()
        self.nivel = 20
        self.taxa_recarga = 10

    def iniciar(self):
        conexao = self.encaixe.busca.estacao.verificar_conexao()

        if not conexao["conectado"]:
            return {
                "sucesso": False,
                "mensagem": "BIBO nao esta conectado a base"
            }

        return {
            "sucesso": True,
            "mensagem": "Recarga virtual iniciada",
            "bateria": self.nivel
        }

    def carregar_passo(self):
        conexao = self.encaixe.busca.estacao.verificar_conexao()

        if not conexao["conectado"]:
            return {
                "sucesso": False,
                "mensagem": "Recarga interrompida: base desconectada"
            }

        self.nivel = min(
            100,
            self.nivel + self.taxa_recarga
        )

        return {
            "sucesso": True,
            "bateria": self.nivel,
            "completa": self.nivel == 100
        }

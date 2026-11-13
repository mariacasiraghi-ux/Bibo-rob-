
from gerenciador_sensores import GerenciadorSensores
from ciclo_recarga import CicloRecarga


class GerenciadorEnergia:
    def __init__(self):
        self.sensores = GerenciadorSensores()
        self.ciclo = CicloRecarga()
        self.estado = "DISPONIVEL"

    def verificar(self):
        diagnostico = self.sensores.consultar()

        bateria = diagnostico["leituras"]["bateria"]
        energia = diagnostico["energia"]

        return {
            "nivel": bateria["nivel"],
            "carregando": bateria["carregando"],
            "estado": energia["estado"],
            "acao": energia["acao"]
        }

    def executar_recarga(self):
        situacao = self.verificar()

        if situacao["carregando"]:
            return {
                "sucesso": False,
                "estado": "JA_CARREGANDO"
            }

        if situacao["estado"] == "NORMAL":
            return {
                "sucesso": True,
                "estado": "RECARGA_DESNECESSARIA"
            }

        if situacao["estado"] == "CRITICO":
            self.estado = "AGUARDANDO_AJUDA"
            return {
                "sucesso": False,
                "estado": "BATERIA_CRITICA"
            }

        self.estado = "BUSCANDO_BASE"

        resultado = self.ciclo.executar(
            bateria=situacao["nivel"]
        )

        if resultado["sucesso"]:
            self.sensores.sensores.bateria = (
                resultado["bateria"]
            )
            self.sensores.sensores.carregando = False
            self.estado = "RECARGA_CONCLUIDA"
        else:
            self.estado = "FALHA_RECARGA"

        return resultado


from controle_descanso import ControleDescanso
from saida_base import SaidaBase


class AutonomiaBibo:
    def __init__(self):
        self.controle = ControleDescanso()
        self.saida = SaidaBase()

        # Todos usam a mesma estacao virtual
        estacao = self.controle.energia.ciclo.recarga.encaixe.busca.estacao

        self.controle.energia.ciclo.aproximacao.busca.estacao = estacao
        self.saida.estacao = estacao

    def executar(self, bateria=15):
        # Configurar bateria virtual inicial
        self.controle.energia.sensores.sensores.bateria = bateria

        # Buscar base, encaixar, descansar e recarregar
        recarga = self.controle.executar()

        if not recarga["sucesso"]:
            return {
                "sucesso": False,
                "estado": recarga["estado"],
                "historico": recarga["historico"]
            }

        # Sem necessidade de recarga
        if recarga["estado"] == "DISPONIVEL":
            return {
                "sucesso": True,
                "estado": "DISPONIVEL",
                "bateria": bateria,
                "mensagem": "BIBO nao precisa recarregar"
            }

        # Verificar saida da base
        nivel = recarga["bateria"]
        saida = self.saida.executar(nivel)

        if not saida["sucesso"]:
            return {
                "sucesso": False,
                "estado": "AGUARDANDO_SAIDA",
                "bateria": nivel,
                "motivo": saida["motivo"]
            }

        return {
            "sucesso": True,
            "estado": "DISPONIVEL",
            "bateria": nivel,
            "mensagem": "BIBO recarregou e saiu da base virtual!"
        }

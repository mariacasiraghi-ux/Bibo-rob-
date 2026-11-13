
from gerenciador_sensores import GerenciadorSensores
from modo_descanso import ModoDescanso
from esp32.estacao_virtual import EstacaoVirtual


class SaidaBase:
    def __init__(self):
        self.sensores = GerenciadorSensores()
        self.descanso = ModoDescanso()
        self.estacao = EstacaoVirtual()

    def verificar_saida(self, bateria):
        if bateria < 100:
            return {
                "permitido": False,
                "motivo": "Bateria ainda nao esta completa"
            }

        diagnostico = self.sensores.consultar()

        if not diagnostico["analise"]["seguro_para_mover"]:
            return {
                "permitido": False,
                "motivo": "Saida bloqueada pelos sensores",
                "alertas": diagnostico["analise"]["alertas"]
            }

        if not self.estacao.conectado:
            return {
                "permitido": False,
                "motivo": "BIBO nao esta conectado a base"
            }

        return {
            "permitido": True,
            "motivo": "Saida virtual autorizada"
        }

    def executar(self, bateria):
        verificacao = self.verificar_saida(bateria)

        if not verificacao["permitido"]:
            return {
                "sucesso": False,
                "estado": "AGUARDANDO_SAIDA",
                "motivo": verificacao["motivo"]
            }

        self.estacao.desconectar()
        self.descanso.acordar()
        self.descanso.ficar_disponivel()

        return {
            "sucesso": True,
            "estado": "DISPONIVEL",
            "mensagem": "BIBO saiu da base virtual!"
        }

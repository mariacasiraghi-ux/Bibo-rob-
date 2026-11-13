
from busca_base import BuscaBase
from gerenciador_sensores import GerenciadorSensores


class AproximacaoBase:
    def __init__(self):
        self.busca = BuscaBase()
        self.sensores = GerenciadorSensores()

    def executar(self, bateria=15):
        historico = []

        for etapa in range(30):
            decisao = self.busca.verificar(bateria)

            if decisao["estado"] != "APROXIMACAO":
                return {
                    "resultado": decisao,
                    "historico": historico
                }

            diagnostico = self.sensores.consultar()

            if not diagnostico["analise"]["seguro_para_mover"]:
                return {
                    "resultado": {
                        "estado": "BLOQUEADO",
                        "acao": "parar",
                        "alertas": diagnostico["analise"]["alertas"]
                    },
                    "historico": historico
                }

            distancia_atual = self.busca.estacao.distancia_cm

            nova_distancia = max(
                5,
                distancia_atual - 10
            )

            self.busca.estacao.distancia_cm = nova_distancia

            historico.append({
                "etapa": etapa + 1,
                "distancia_anterior": distancia_atual,
                "distancia_atual": nova_distancia
            })

        return {
            "resultado": {
                "estado": "LIMITE_ATINGIDO",
                "acao": "parar"
            },
            "historico": historico
        }

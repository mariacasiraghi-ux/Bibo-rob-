
class MonitorBateria:
    def __init__(self):
        self.limite_baixo = 20
        self.limite_critico = 10

    def verificar(self, nivel, carregando=False):
        if nivel < 0 or nivel > 100:
            raise ValueError("Nivel de bateria invalido")

        if carregando:
            return {
                "estado": "CARREGANDO",
                "acao": "aguardar_recarga"
            }

        if nivel <= self.limite_critico:
            return {
                "estado": "CRITICO",
                "acao": "parar_e_solicitar_recarga"
            }

        if nivel <= self.limite_baixo:
            return {
                "estado": "BAIXO",
                "acao": "procurar_base"
            }

        return {
            "estado": "NORMAL",
            "acao": "continuar"
        }

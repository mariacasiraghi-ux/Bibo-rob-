
class SensoresVirtuais:
    def __init__(self):
        self.distancia_cm = 100
        self.inclinacao = 0
        self.bateria = 100
        self.velocidade = 0

    def ler_distancia(self):
        return self.distancia_cm

    def ler_movimento(self):
        return {
            "inclinacao": self.inclinacao,
            "velocidade": self.velocidade
        }

    def ler_bateria(self):
        return {
            "nivel": self.bateria,
            "carregando": False
        }

    def ler_todos(self):
        return {
            "distancia_cm": self.ler_distancia(),
            "movimento": self.ler_movimento(),
            "bateria": self.ler_bateria()
        }

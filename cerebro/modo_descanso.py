
class ModoDescanso:
    def __init__(self):
        self.estado = "DISPONIVEL"
        self.carregando = False

    def descansar(self):
        self.estado = "DESCANSANDO"

        return {
            "estado": self.estado,
            "expressao": "dormindo",
            "mensagem": "Estou descansando um pouquinho... Zzz"
        }

    def iniciar_carregamento(self):
        self.estado = "CARREGANDO"
        self.carregando = True

        return {
            "estado": self.estado,
            "expressao": "dormindo",
            "mensagem": "Recarregando minhas energias!"
        }

    def acordar(self):
        self.estado = "ACORDANDO"
        self.carregando = False

        return {
            "estado": self.estado,
            "expressao": "feliz",
            "mensagem": "Bom dia! Estou cheio de energia!"
        }

    def ficar_disponivel(self):
        self.estado = "DISPONIVEL"

        return {
            "estado": self.estado,
            "expressao": "normal",
            "mensagem": "Estou pronto para brincar!"
        }

    def verificar(self):
        return {
            "estado": self.estado,
            "carregando": self.carregando,
            "pode_movimentar": self.estado == "DISPONIVEL",
            "pode_conversar": True
        }

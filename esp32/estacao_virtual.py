
class EstacaoVirtual:
    def __init__(self):
        self.disponivel = True
        self.distancia_cm = 150
        self.conectado = False

    def localizar(self):
        if not self.disponivel:
            return {
                "encontrada": False,
                "mensagem": "Base indisponivel"
            }

        return {
            "encontrada": True,
            "distancia_cm": self.distancia_cm,
            "mensagem": "Base localizada"
        }

    def verificar_conexao(self):
        return {
            "conectado": self.conectado,
            "carregando": self.conectado
        }

    def conectar(self):
        if not self.disponivel:
            return {
                "sucesso": False,
                "mensagem": "Base indisponivel"
            }

        if self.distancia_cm > 5:
            return {
                "sucesso": False,
                "mensagem": "BIBO ainda esta longe da base"
            }

        self.conectado = True

        return {
            "sucesso": True,
            "mensagem": "BIBO conectado a base virtual"
        }

    def desconectar(self):
        self.conectado = False

        return {
            "sucesso": True,
            "mensagem": "BIBO desconectado da base"
        }

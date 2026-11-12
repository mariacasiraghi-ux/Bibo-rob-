
class ContextoBibo:
    def __init__(self):
        self.assunto = None
        self.humor = "normal"
        self.ultima_mensagem = ""

    def atualizar(self, mensagem, humor="normal", assunto=None):
        self.ultima_mensagem = mensagem
        self.humor = humor

        if assunto is not None:
            self.assunto = assunto

    def consultar(self):
        return {
            "assunto": self.assunto,
            "humor": self.humor,
            "ultima_mensagem": self.ultima_mensagem
        }

    def limpar(self):
        self.assunto = None
        self.humor = "normal"
        self.ultima_mensagem = ""


    def identificar_assunto(self, mensagem):
        import unicodedata

        texto = mensagem.lower().strip()
        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(
            letra for letra in texto
            if unicodedata.category(letra) != "Mn"
        )

        assuntos = {
            "escola": [
                "escola", "prova", "estudar",
                "professor", "aula", "trabalho escolar"
            ],
            "projetos": [
                "projeto", "programacao", "codigo",
                "robo", "esp32", "python"
            ],
            "atividades": [
                "passeio", "jogo", "brincar",
                "filme", "musica", "viajar"
            ],
            "emocoes": [
                "feliz", "triste", "cansado",
                "animado", "preocupado"
            ]
        }

        for assunto, palavras in assuntos.items():
            if any(palavra in texto for palavra in palavras):
                return assunto

        return None

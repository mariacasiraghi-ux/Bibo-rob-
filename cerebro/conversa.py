
from personalidade import PersonalidadeBibo
from inteligencia import InteligenciaBibo


class ConversaBibo:
    def __init__(self):
        self.personalidade = PersonalidadeBibo()
        self.inteligencia = InteligenciaBibo()

    def responder(self, mensagem):
        mensagem = mensagem.strip()

        if not mensagem:
            return {
                "texto": "Pode me dizer alguma coisa?",
                "expressao": "normal"
            }

        resposta = self.personalidade.responder(mensagem)

        if resposta["texto"].startswith(
            "Ainda estou aprendendo a conversar!"
        ):
            try:
                resposta = self.inteligencia.responder(mensagem)
            except Exception:
                resposta = {
                    "texto": "Minha inteligência está temporariamente indisponível.",
                    "expressao": "normal"
                }

        return resposta

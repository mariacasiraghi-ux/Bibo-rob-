
from personalidade import PersonalidadeBibo
from inteligencia import InteligenciaBibo


class ConversaBibo:
    def __init__(self):
        self.personalidade = PersonalidadeBibo()
        self.inteligencia = InteligenciaBibo()

        # Historico temporario da conversa
        self.historico = []
        self.limite_historico = 12

    def responder(self, mensagem):
        mensagem = mensagem.strip()

        if not mensagem:
            return {
                "texto": "Pode me dizer alguma coisa?",
                "expressao": "calmo"
            }

        # Consultar personalidade
        resposta = self.personalidade.responder(mensagem)

        # Quando necessario, consultar o Gemini
        if resposta["texto"].startswith(
            "Ainda estou aprendendo a conversar!"
        ):
            try:
                resposta = self.inteligencia.responder(
                    mensagem,
                    historico=self.historico
                )
            except Exception as erro:
                print(
                    "[BIBOU] Erro na conversa:",
                    type(erro).__name__
                )

                resposta = {
                    "texto": (
                        "Minha inteligencia esta "
                        "temporariamente indisponivel."
                    ),
                    "expressao": "calmo"
                }

        # Guardar a mensagem do usuario
        self.historico.append({
            "role": "user",
            "texto": mensagem
        })

        # Guardar a resposta do BIBOU
        self.historico.append({
            "role": "model",
            "texto": resposta["texto"]
        })

        # Manter apenas as mensagens mais recentes
        self.historico = self.historico[
            -self.limite_historico:
        ]

        return resposta

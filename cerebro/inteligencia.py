
import os
import sys
import unicodedata

from dotenv import load_dotenv

# Localizar a pasta principal
PASTA_PRINCIPAL = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PASTA_PRINCIPAL not in sys.path:
    sys.path.insert(0, PASTA_PRINCIPAL)

from config import (
    MODO_IA,
    MODELO_IA,
    MAX_CARACTERES_PERGUNTA,
    MAX_TOKENS_RESPOSTA,
    TIMEOUT_IA
)

try:
    from .ia_gemini import IAGeminiBibo
except ImportError:
    from ia_gemini import IAGeminiBibo

load_dotenv(
    os.path.join(PASTA_PRINCIPAL, ".env")
)


class InteligenciaBibo:
    def __init__(self):
        self.nome = "BIBO"
        self.modo = MODO_IA
        self.ia_gemini = None

        if self.modo == "gemini":
            self.ia_gemini = IAGeminiBibo()

        self.respostas_simuladas = {
            "por que o ceu e azul": (
                "O céu parece azul porque a luz do Sol "
                "se espalha na atmosfera!"
            ),
            "o que e inteligencia artificial": (
                "Inteligência artificial é uma tecnologia "
                "que permite aos computadores reconhecer "
                "padrões e responder perguntas!"
            ),
            "o que e um robo": (
                "Um robô é uma máquina programada para "
                "realizar tarefas!"
            ),
            "por que a lua brilha": (
                "A Lua não produz luz própria! "
                "Ela reflete a luz do Sol."
            )
        }

    def normalizar(self, texto):
        texto = texto.lower().strip("!?., ")
        texto = unicodedata.normalize("NFD", texto)

        texto = "".join(
            letra for letra in texto
            if unicodedata.category(letra) != "Mn"
        )

        return " ".join(texto.split())

    def responder(self, pergunta, historico=None):
        pergunta = pergunta.strip()

        if not pergunta:
            return {
                "texto": "Pode me fazer uma pergunta?",
                "expressao": "normal"
            }

        if len(pergunta) > MAX_CARACTERES_PERGUNTA:
            return {
                "texto": "Sua pergunta ficou muito longa!",
                "expressao": "normal"
            }

        if self.modo == "simulacao":
            return self.responder_simulacao(pergunta)

        if self.modo == "gemini":
            return self.ia_gemini.responder(
        pergunta,
        historico=historico
    )

        return {
            "texto": "Meu modo de inteligência não foi reconhecido.",
            "expressao": "normal"
        }

    def responder_simulacao(self, pergunta):
        pergunta_normalizada = self.normalizar(pergunta)

        if pergunta_normalizada in self.respostas_simuladas:
            return {
                "texto": self.respostas_simuladas[
                    pergunta_normalizada
                ],
                "expressao": "feliz"
            }

        return {
            "texto": (
                "Ainda estou no modo de simulação! "
                "Quando minha IA online estiver conectada, "
                "poderei responder perguntas novas."
            ),
            "expressao": "normal"
        }

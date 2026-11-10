
import os

from dotenv import load_dotenv
from openai import OpenAI

from pathlib import Path


# Pasta principal do projeto
PASTA_PRINCIPAL = Path(__file__).resolve().parent.parent

# Carregar o arquivo privado
load_dotenv(PASTA_PRINCIPAL / ".env")


class IAOnlineBibo:
    def __init__(
        self,
        modelo="gpt-4.1-mini",
        max_tokens=150,
        timeout=20
    ):
        self.modelo = modelo
        self.max_tokens = max_tokens
        self.timeout = timeout

        self.chave = os.getenv("OPENAI_API_KEY")
        self.pronta = bool(self.chave)

    def responder(self, pergunta):
        # Impedir chamadas sem chave
        if not self.pronta:
            return {
                "texto": "Minha IA online ainda não foi configurada.",
                "expressao": "normal"
            }

        try:
            cliente = OpenAI(
                api_key=self.chave,
                timeout=self.timeout,
                max_retries=0
            )

            resposta = cliente.responses.create(
                model=self.modelo,
                instructions=(
                    "Você é BIBO, um pequeno robô "
                    "companheiro, curioso e amigável. "
                    "Responda em português brasileiro, "
                    "com linguagem natural e clara. "
                    "Prefira respostas curtas. "
                    "Não invente informações. "
                    "Não afirme que realizou movimentos "
                    "ou ações físicas."
                ),
                input=pergunta,
                max_output_tokens=self.max_tokens,
                store=False
            )

            texto = resposta.output_text.strip()

            if not texto:
                texto = "Não consegui responder agora."

            return {
                "texto": texto,
                "expressao": "feliz"
            }

        except Exception as erro:
            print(
                "[IA ONLINE] Erro:",
                type(erro).__name__
            )

            return {
                "texto": (
                    "Não consegui acessar minha "
                    "inteligência artificial agora."
                ),
                "expressao": "normal"
            }


import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


PASTA_PRINCIPAL = Path(__file__).resolve().parent.parent

load_dotenv(PASTA_PRINCIPAL / ".env")


class IAGeminiBibo:
    def __init__(self):
        self.nome = "BIBO"
        self.modelo = "gemini-2.5-flash-lite"

        self.chave = os.getenv("GEMINI_API_KEY")
        self.pronta = bool(self.chave)

    def responder(self, pergunta):
        pergunta = pergunta.strip()

        if not pergunta:
            return {
                "texto": "Pode me fazer uma pergunta?",
                "expressao": "normal"
            }

        if len(pergunta) > 500:
            return {
                "texto": "Sua pergunta ficou muito longa!",
                "expressao": "normal"
            }

        if not self.pronta:
            return {
                "texto": (
                    "Minha inteligência Gemini ainda "
                    "não possui uma chave configurada."
                ),
                "expressao": "normal"
            }

        try:
            cliente = genai.Client(api_key=self.chave)

            resposta = cliente.models.generate_content(
                model=self.modelo,
                contents=pergunta,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "Você é BIBO, um pequeno robô "
                        "companheiro, amigável e curioso. "
                        "Responda em português brasileiro. "
                        "Use linguagem simples e natural. "
                        "Prefira respostas curtas. "
                        "Não afirme que realizou movimentos "
                        "ou ações físicas."
                    ),
                    max_output_tokens=150,
                    temperature=0.7
                )
            )

            texto = (resposta.text or "").strip()

            if not texto:
                texto = "Não consegui responder agora."

            return {
                "texto": texto,
                "expressao": "feliz"
            }

        except Exception as erro:
            print(
                "[GEMINI] Erro:",
                type(erro).__name__
            )

            return {
                "texto": (
                    "Não consegui acessar minha "
                    "inteligência artificial agora."
                ),
                "expressao": "normal"
            }

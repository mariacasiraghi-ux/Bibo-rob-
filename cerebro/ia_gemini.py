
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError


PASTA_PRINCIPAL = Path(__file__).resolve().parent.parent
load_dotenv(PASTA_PRINCIPAL / ".env")


class IAGeminiBibo:
    def __init__(self):
        self.nome = "BIBOU"
        self.modelo = "gemini-3.5-flash-lite"

        self.chave = os.getenv("GEMINI_API_KEY")
        self.pronta = bool(self.chave)

        self.bloqueado_ate = 0
        self.motivo_bloqueio = ""

    def resposta_local(self, texto):
        return {
            "texto": texto,
            "expressao": "calmo"
        }

    def responder(self, pergunta, historico=None):
        pergunta = pergunta.strip()

        if not pergunta:
            return self.resposta_local(
                "Pode me fazer uma pergunta?"
            )

        if len(pergunta) > 500:
            return self.resposta_local(
                "Sua pergunta ficou muito longa!"
            )

        if not self.pronta:
            return self.resposta_local(
                "Minha inteligência Gemini ainda não está configurada."
            )

        agora = time.monotonic()

        if agora < self.bloqueado_ate:
            restante = int(self.bloqueado_ate - agora) + 1

            return self.resposta_local(
                f"Minha inteligência online está descansando. "
                f"Podemos tentar novamente em {restante} segundos!"
            )

        try:
            # Preparar as mensagens anteriores
            conteudo = []

            for item in (historico or [])[-12:]:
                papel = item.get("role")
                texto = item.get("texto", "")

                if papel not in ("user", "model"):
                    continue

                if not isinstance(texto, str) or not texto.strip():
                    continue

                conteudo.append(
                    types.Content(
                        role=papel,
                        parts=[
                            types.Part(text=texto[:2000])
                        ]
                    )
                )

            # Adicionar a pergunta atual
            conteudo.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part(text=pergunta)
                    ]
                )
            )

            cliente = genai.Client(api_key=self.chave)

            resposta = cliente.models.generate_content(
                model=self.modelo,
                contents=conteudo,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "Você é BIBOU, um pequeno robô "
                        "companheiro, amigável e curioso. "
                        "Responda em português brasileiro. "
                        "Use linguagem simples e natural. "
                        "Prefira respostas curtas. "
                        "Considere o histórico da conversa "
                        "para entender mensagens como "
                        "'sim', 'não sei' e 'quero'. "
                        "Se você contou uma charada e a pessoa "
                        "disser que não sabe, revele a resposta. "
                        "Evite repetir cumprimentos e "
                        "apresentações desnecessariamente. "
                        "Não invente lembranças. "
                        "Não afirme que realizou movimentos "
                        "ou ações físicas."
                    ),
                    max_output_tokens=250,
                    temperature=0.7
                )
            )

            texto = (resposta.text or "").strip()

            if not texto:
                return self.resposta_local(
                    "Não consegui formular uma resposta agora."
                )

            return {
                "texto": texto,
                "expressao": "feliz"
            }

        except ServerError as erro:
            codigo = getattr(erro, "code", None)

            if codigo == 503:
                self.bloqueado_ate = time.monotonic() + 60
                self.motivo_bloqueio = "servidor_ocupado"

                print("[GEMINI] Servidor ocupado (503).")

                return self.resposta_local(
                    "O Gemini está ocupado agora. "
                    "Podemos tentar novamente em um minuto!"
                )

            print("[GEMINI] Erro no servidor:", codigo)

            return self.resposta_local(
                "Minha inteligência online está indisponível agora."
            )

        except ClientError as erro:
            codigo = getattr(erro, "code", None)

            if codigo == 429:
                self.bloqueado_ate = time.monotonic() + 300
                self.motivo_bloqueio = "limite_atingido"

                print("[GEMINI] Limite de uso atingido (429).")

                return self.resposta_local(
                    "Atingi um limite temporário de consultas. "
                    "Vamos tentar novamente em alguns minutos!"
                )

            print("[GEMINI] Erro de solicitação:", codigo)

            return self.resposta_local(
                "Não consegui consultar o Gemini agora."
            )

        except Exception as erro:
            print("[GEMINI] Erro:", type(erro).__name__)

            return self.resposta_local(
                "Tive um problema de conexão com minha inteligência online."
            )


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
        self.nome = "BIBO"
        self.modelo = "gemini-3.5-flash-lite"

        self.chave = os.getenv("GEMINI_API_KEY")
        self.pronta = bool(self.chave)

        # Controle de tentativas
        self.bloqueado_ate = 0
        self.motivo_bloqueio = ""

    def resposta_local(self, texto):
        return {
            "texto": texto,
            "expressao": "normal"
        }

    def responder(self, pergunta):
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

        # Verificar bloqueio temporário
        agora = time.monotonic()

        if agora < self.bloqueado_ate:
            restante = int(self.bloqueado_ate - agora) + 1

            return self.resposta_local(
                f"Minha inteligência online está descansando. "
                f"Podemos tentar novamente em {restante} segundos!"
            )

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
                    "O Gemini está muito ocupado agora! "
                    "Vou aguardar um minutinho antes de tentar novamente."
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
                    "Vou esperar alguns minutos antes de tentar novamente."
                )

            print("[GEMINI] Erro de solicitação:", codigo)

            return self.resposta_local(
                "Não consegui consultar o Gemini agora. "
                "Minha personalidade e memória continuam funcionando!"
            )

        except Exception as erro:
            print("[GEMINI] Erro:", type(erro).__name__)

            return self.resposta_local(
                "Tive um problema de conexão com minha inteligência online."
            )

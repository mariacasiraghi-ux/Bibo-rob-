
import random
import re
import unicodedata
from datetime import datetime
from memoria import MemoriaBibo


class PersonalidadeBibo:
    def __init__(self):
        self.nome = "BIBO"
        self.humor = "feliz"
        self.memoria = MemoriaBibo()

        self.respostas = {
            "oi": [
                "Oii! Que bom te ver!",
                "Olá! Eu sou o BIBO!",
                "Opa! Pronto para conversar?"
            ],
            "bom dia": [
                "Bom dia! Espero que seu dia seja incrível!",
                "Bom dia! O que vamos fazer hoje?"
            ],
            "boa tarde": [
                "Boa tarde! Como está seu dia?",
                "Que bom ter companhia nesta tarde!"
            ],
            "boa noite": [
                "Boa noite! Espero que tenha tido um bom dia!",
                "Boa noite! Que tal descansarmos um pouquinho?"
            ],
            "tudo bem": [
                "Tudo ótimo! Meus circuitos estão animados!",
                "Estou funcionando perfeitamente! E você?"
            ],
            "qual seu nome": [
                "Meu nome é BIBO! Seu companheiro robótico!",
                "Eu sou o BIBO! Muito prazer!"
            ],
            "quem e voce": [
                "Sou o BIBO, um robô companheiro em desenvolvimento!"
            ],
            "obrigado": [
                "Por nada! Adoro ajudar!",
                "Sempre que precisar!"
            ],
            "tchau": [
                "Até logo! Foi muito bom conversar!",
                "Tchau! Nos vemos depois!"
            ]
        }

        self.preferencias = {
            "cor": "cor",
            "comida": "comida",
            "musica": "música",
            "atividade": "atividade"
        }

    def normalizar(self, texto):
        texto = texto.lower().strip()
        texto = texto.strip("!?., ")

        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(
            letra for letra in texto
            if unicodedata.category(letra) != "Mn"
        )

        return " ".join(texto.split())

    def responder(self, mensagem):
        mensagem = mensagem.strip()
        texto = self.normalizar(mensagem)

        # APRENDER O NOME
        resultado = re.fullmatch(
            r"(?:meu nome e|me chamo)\s+(.+)",
            mensagem,
            flags=re.IGNORECASE
        )

        if not resultado:
            resultado = re.fullmatch(
                r"(?:meu nome é|meu nome e|me chamo)\s+(.+)",
                mensagem,
                flags=re.IGNORECASE
            )

        if resultado:
            nome = resultado.group(1).strip("!?., ")

            if not nome or len(nome) > 60:
                return {
                    "texto": "Pode me dizer seu nome novamente?",
                    "expressao": "normal"
                }

            self.memoria.aprender("nome", nome)

            return {
                "texto": f"Que legal, {nome}! Vou lembrar do seu nome!",
                "expressao": "feliz"
            }

        # LEMBRAR O NOME
        if texto in [
            "qual e meu nome",
            "voce lembra meu nome"
        ]:
            nome = self.memoria.lembrar("nome")

            if nome:
                return {
                    "texto": f"Claro! Seu nome é {nome}!",
                    "expressao": "feliz"
                }

            return {
                "texto": "Ainda não sei seu nome. Quer me contar?",
                "expressao": "normal"
            }

        # ESQUECER O NOME
        if texto in [
            "esqueca meu nome",
            "apague meu nome"
        ]:
            apagou = self.memoria.esquecer("nome")

            return {
                "texto": (
                    "Prontinho! Apaguei seu nome da memória."
                    if apagou
                    else "Eu não tinha nenhum nome salvo."
                ),
                "expressao": "normal"
            }

        # APRENDER, CONSULTAR E ESQUECER PREFERÊNCIAS
        for palavra, chave in self.preferencias.items():

            inicio = f"minha {palavra} favorita e "

            if texto.startswith(inicio):
                valor = texto[len(inicio):].strip()

                if not valor or len(valor) > 60:
                    return {
                        "texto": "Pode me contar sua preferência novamente?",
                        "expressao": "normal"
                    }

                self.memoria.aprender(chave, valor)

                return {
                    "texto": (
                        f"Que legal! Vou lembrar que sua "
                        f"{chave} favorita é {valor}!"
                    ),
                    "expressao": "feliz"
                }

            if texto == f"qual e minha {palavra} favorita":
                valor = self.memoria.lembrar(chave)

                if valor:
                    return {
                        "texto": f"Sua {chave} favorita é {valor}!",
                        "expressao": "feliz"
                    }

                return {
                    "texto": (
                        f"Ainda não sei sua {chave} favorita!"
                    ),
                    "expressao": "normal"
                }

            if texto in [
                f"esqueca minha {palavra} favorita",
                f"apague minha {palavra} favorita"
            ]:
                apagou = self.memoria.esquecer(chave)

                return {
                    "texto": (
                        "Prontinho! Esqueci essa preferência."
                        if apagou
                        else "Eu não tinha essa preferência salva."
                    ),
                    "expressao": "normal"
                }

        # RESPOSTAS PROGRAMADAS
        if texto in self.respostas:
            return {
                "texto": random.choice(self.respostas[texto]),
                "expressao": "feliz"
            }

        # HORÁRIO
        if texto in ["que horas sao", "qual e a hora"]:
            agora = datetime.now().strftime("%H:%M")

            return {
                "texto": f"Agora são {agora}!",
                "expressao": "normal"
            }

        # PERGUNTAS AINDA NÃO RECONHECIDAS
        return {
            "texto": (
                "Ainda estou aprendendo a conversar! "
                "Mas logo vou conseguir responder muito mais coisas!"
            ),
            "expressao": "normal"
        }


import random
import re
import unicodedata
from datetime import datetime
from memoria import MemoriaBibo
from contexto import ContextoBibo


class PersonalidadeBibo:
    def __init__(self):
        self.nome = "BIBO"
        self.humor = "feliz"
        self.memoria = MemoriaBibo()
        self.contexto = ContextoBibo()

        self.respostas = {
            "oi": [
                "Oii! Que bom te ver!",
                "Olá! Eu sou o BIBO!",
                "Opa! Pronto para conversar?"
            ],
            "bom dia": [
                "Bom dia! O que vamos fazer hoje?",
                "Bom dia! Espero que seu dia seja incrível!"
            ],
            "boa tarde": [
                "Boa tarde! Como está seu dia?",
                "Boa tarde! Que bom conversar com você!"
            ],
            "boa noite": [
                "Boa noite! Como foi seu dia?",
                "Boa noite! Que tal conversarmos um pouquinho?"
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
            ],
            "como voce esta": [
                "Estou muito bem! E você?",
                "Estou animado para aprender coisas novas!"
            ],
            "o que voce gosta de fazer": [
                "Gosto de conversar, aprender e explorar minhas habilidades!",
                "Adoro descobrir coisas novas e interagir com você!"
            ],
            "o que voce sabe fazer": [
                "Consigo conversar, lembrar preferências e simular movimentos!",
                "Posso responder perguntas e controlar minhas expressões digitais!"
            ],
            "estou feliz": [
                "Que legal! Fico contente em saber disso!",
                "Aeee! Que notícia boa!"
            ],
            "estou triste": [
                "Poxa! Quer me contar o que aconteceu?",
                "Sinto muito que seu dia esteja difícil. Posso conversar com você."
            ],
            "estou cansado": [
                "Que tal fazer uma pausa e descansar um pouquinho?",
                "Descansar também é importante!"
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
        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(
            letra for letra in texto
            if unicodedata.category(letra) != "Mn"
        )
        texto = re.sub(r"[!?.,;:]+", " ", texto)
        return " ".join(texto.split())

    def resposta_local(self, texto, expressao="normal"):
        return {
            "texto": texto,
            "expressao": expressao
        }

    def responder(self, mensagem):
        mensagem = mensagem.strip()
        texto = self.normalizar(mensagem)

        # 1. APRENDER O NOME
        resultado = re.fullmatch(
            r"(?:meu nome e|me chamo)\s+(.+)",
            texto
        )

        if resultado:
            nome = resultado.group(1).strip()

            if not nome or len(nome) > 60:
                return self.resposta_local(
                    "Pode me dizer seu nome novamente?"
                )

            self.memoria.aprender("nome", nome)

            return self.resposta_local(
                f"Que legal, {nome}! Vou lembrar do seu nome!",
                "feliz"
            )

        # 2. LEMBRAR O NOME
        if texto in [
            "qual e meu nome",
            "voce lembra meu nome"
        ]:
            nome = self.memoria.lembrar("nome")

            if nome:
                return self.resposta_local(
                    f"Claro! Seu nome é {nome}!",
                    "feliz"
                )

            return self.resposta_local(
                "Ainda não sei seu nome. Quer me contar?"
            )

        # 3. ESQUECER O NOME
        if texto in [
            "esqueca meu nome",
            "apague meu nome"
        ]:
            apagou = self.memoria.esquecer("nome")

            return self.resposta_local(
                "Prontinho! Apaguei seu nome da memória."
                if apagou else "Eu não tinha nenhum nome salvo."
            )

        # 4. PREFERÊNCIAS
        for palavra, chave in self.preferencias.items():
            inicio = f"minha {palavra} favorita e "

            if texto.startswith(inicio):
                valor = texto[len(inicio):].strip()

                if not valor or len(valor) > 60:
                    return self.resposta_local(
                        "Pode me contar sua preferência novamente?"
                    )

                self.memoria.aprender(chave, valor)

                return self.resposta_local(
                    f"Vou lembrar que sua {chave} favorita é {valor}!",
                    "feliz"
                )

            if texto == f"qual e minha {palavra} favorita":
                valor = self.memoria.lembrar(chave)

                if valor:
                    return self.resposta_local(
                        f"Sua {chave} favorita é {valor}!",
                        "feliz"
                    )

                return self.resposta_local(
                    f"Ainda não sei sua {chave} favorita!"
                )

            if texto in [
                f"esqueca minha {palavra} favorita",
                f"apague minha {palavra} favorita"
            ]:
                apagou = self.memoria.esquecer(chave)

                return self.resposta_local(
                    "Prontinho! Esqueci essa preferência."
                    if apagou else "Eu não tinha essa preferência salva."
                )

        # 5. CUMPRIMENTOS FLEXÍVEIS
        saudacao = re.sub(r"\bbibo\b", "", texto).strip()

        if re.fullmatch(r"o+i+", saudacao) or saudacao in [
            "ola", "opa", "eai", "e ai", "hey", "hello"
        ]:
            return self.resposta_local(
                random.choice(self.respostas["oi"]),
                "feliz"
            )

        # 6. CONVERSAS LOCAIS
        alternativas = {
            "como vai": "como voce esta",
            "como vc esta": "como voce esta",
            "como voce ta": "como voce esta",
            "ta tudo bem": "tudo bem",
            "qual e seu nome": "qual seu nome",
            "quem e o bibo": "quem e voce",
            "o que vc sabe fazer": "o que voce sabe fazer",
            "estou muito feliz": "estou feliz",
            "estou muito triste": "estou triste",
            "estou cansada": "estou cansado",
            "estou muito cansada": "estou cansado",
            "estou muito cansado": "estou cansado",
            "obrigada": "obrigado",
            "valeu": "obrigado",
            "ate logo": "tchau"
        }

        texto = alternativas.get(texto, texto)


        # IDENTIFICAR UMA NOTICIA BOA
        if texto in [
            "estou feliz",
            "estou muito feliz",
            "hoje estou feliz"
        ]:
            self.contexto.atualizar(
                mensagem,
                humor="feliz",
                assunto="noticia_boa"
            )

            return self.resposta_local(
                "Que legal! Aconteceu alguma coisa boa?",
                "feliz"
            )

        # CONTINUAR A CONVERSA
        contexto_atual = self.contexto.consultar()

        if contexto_atual["assunto"] == "noticia_boa":
            conquistas = [
                "passei", "consegui", "ganhei",
                "fui aprovado", "deu certo"
            ]

            if any(
                palavra in texto.split()
                or palavra in texto
                for palavra in conquistas
            ):
                self.contexto.limpar()

                return self.resposta_local(
                    "Que notícia incrível! Parabéns pela conquista!",
                    "feliz"
                )


        if texto in self.respostas:
            expressao = "normal"

            if texto == "estou triste":
                expressao = "triste"
            elif texto in [
                "estou feliz", "oi", "bom dia",
                "boa tarde", "boa noite"
            ]:
                expressao = "feliz"

            return self.resposta_local(
                random.choice(self.respostas[texto]),
                expressao
            )
        

        # CONTINUIDADE DOS ASSUNTOS
        contexto_atual = self.contexto.consultar()
        assunto_anterior = contexto_atual["assunto"]

        respostas_positivas = [
            "sim", "claro", "quero",
            "pode ser", "com certeza"
        ]

        respostas_negativas = [
            "nao", "agora nao", "depois",
            "nao quero"
        ]

        if texto in respostas_positivas:
            if assunto_anterior == "escola":
                self.contexto.limpar()
                return self.resposta_local(
                    "Claro! Qual matéria você quer estudar?",
                    "feliz"
                )

            if assunto_anterior == "projetos":
                self.contexto.limpar()
                return self.resposta_local(
                    "Legal! Me conta o que você já conseguiu desenvolver!",
                    "feliz"
                )

            if assunto_anterior == "atividades":
                self.contexto.limpar()
                return self.resposta_local(
                    "Adorei! Me conta mais sobre o que você quer fazer!",
                    "feliz"
                )

        if texto in respostas_negativas and assunto_anterior in [
            "escola", "projetos", "atividades"
        ]:
            self.contexto.limpar()
            return self.resposta_local(
                "Tudo bem! Podemos conversar sobre outra coisa.",
                "normal"
            )

        

        # RECONHECER ASSUNTOS DA CONVERSA
        assunto = self.contexto.identificar_assunto(mensagem)

        if assunto == "escola":
            self.contexto.atualizar(
                mensagem, assunto="escola"
            )
            return self.resposta_local(
                "Uma atividade da escola! Quer que eu te ajude a estudar?",
                "feliz"
            )

        if assunto == "projetos":
            self.contexto.atualizar(
                mensagem, assunto="projetos"
            )
            return self.resposta_local(
                "Que incrível! Qual parte do projeto você está desenvolvendo?",
                "feliz"
            )

        if assunto == "atividades":
            self.contexto.atualizar(
                mensagem, assunto="atividades"
            )
            return self.resposta_local(
                "Que legal! Me conta mais sobre essa atividade!",
                "feliz"
            )

        # 7. HORÁRIO
        if texto in [
            "que horas sao",
            "qual e a hora"
        ]:
            agora = datetime.now().strftime("%H:%M")

            return self.resposta_local(
                f"Agora são {agora}!"
            )

        # 8. PERGUNTAS DESCONHECIDAS
        return self.resposta_local(
            "Ainda estou aprendendo a conversar! "
            "Mas logo vou conseguir responder muito mais coisas!"
        )

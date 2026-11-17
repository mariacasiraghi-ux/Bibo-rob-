
from comandos import interpretar_comando
from controlador import ControladorBibo
from personalidade import PersonalidadeBibo
from inteligencia import InteligenciaBibo
from config import MODO_IA

# Monitoramento automatico da bateria
from monitor_segundo_plano import MonitorSegundoPlano


# ==========================================
# INICIALIZACAO DO BIBOU
# ==========================================

bibo = ControladorBibo()
personalidade = PersonalidadeBibo()
inteligencia = InteligenciaBibo()

monitor = MonitorSegundoPlano()

EXPRESSOES = (
    "feliz",
    "triste",
    "surpreso",
    "calmo",
    "carinho",
    "sono",
    "curioso",
    "animado",
)

print("=" * 45)
print("         BIBOU - SISTEMA CENTRAL")
print("=" * 45)

print("\nBIBOU iniciado com sucesso!")

print("\nMovimentos:")
print("frente, tras, esquerda, direita, parar")
print("acenar, dancar")

print("\nExpressoes:")
print(", ".join(EXPRESSOES))
print("piscar")

print("\nConversacao:")
print("Personalidade e memoria ativadas!")

print("\nInteligencia artificial:")

if MODO_IA == "gemini":
    print("Gemini online ativado!")
else:
    print("Modo de simulacao ativado.")


# ==========================================
# INICIAR MONITORAMENTO
# ==========================================

monitor.iniciar()

print("\nMonitoramento virtual da bateria ativado!")
print("\nDigite 'sair' para encerrar.")


# ==========================================
# CONVERSACAO PRINCIPAL
# ==========================================

try:
    while True:

        try:
            entrada = input("\nVocê: ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\nBIBOU: Ate logo!")
            break

        if not entrada:
            continue

        comando_digitado = entrada.lower()

        if comando_digitado == "sair":
            print("\nBIBOU: Ate logo!")
            break

        # 1. Controlar expressoes originais do BIBOU OS
        if comando_digitado in EXPRESSOES or comando_digitado == "normal":

            expressao = (
                "calmo"
                if comando_digitado == "normal"
                else comando_digitado
            )

            bibo.atualizar_servidor({
                "expressao": expressao
            })

            print(
                f"\nBIBOU: Expressao alterada para {expressao}!"
            )
            continue

        # 2. Fazer o BIBOU piscar
        if comando_digitado == "piscar":

            bibo.atualizar_servidor({
                "piscar": True
            })

            print("\nBIBOU: Piscando!")
            continue

        # 3. Verificar comandos de movimento
        comando = interpretar_comando(entrada)

        if comando:
            bibo.enviar_comando(comando)
            continue

        # 4. Consultar personalidade e memoria
        resposta = personalidade.responder(entrada)

        # 5. Perguntas desconhecidas vao para a IA
        if resposta["texto"].startswith(
            "Ainda estou aprendendo a conversar!"
        ):

            print(
                "\n[BIBOU] Consultando inteligencia artificial..."
            )

            try:
                resposta = inteligencia.responder(entrada)

            except Exception as erro:
                print(
                    "[BIBOU] Erro na inteligencia:",
                    type(erro).__name__
                )

                resposta = {
                    "texto": (
                        "Minha inteligencia artificial esta "
                        "temporariamente indisponivel."
                    ),
                    "expressao": "calmo"
                }

        # 6. Exibir resposta
        print("\nBIBOU:", resposta["texto"])

        # 7. Atualizar o rosto digital
        expressao_resposta = resposta.get(
            "expressao", "calmo"
        )

        if expressao_resposta not in EXPRESSOES:
            expressao_resposta = "calmo"

        bibo.atualizar_servidor({
            "expressao": expressao_resposta
        })

finally:
    # Encerrar monitoramento ao sair
    monitor.parar()

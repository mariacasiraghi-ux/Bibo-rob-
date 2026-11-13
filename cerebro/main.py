
from comandos import interpretar_comando
from controlador import ControladorBibo
from personalidade import PersonalidadeBibo
from inteligencia import InteligenciaBibo
from config import MODO_IA

# Monitoramento automatico da bateria
from monitor_segundo_plano import MonitorSegundoPlano


# ==========================================
# INICIALIZACAO DO BIBO
# ==========================================

bibo = ControladorBibo()
personalidade = PersonalidadeBibo()
inteligencia = InteligenciaBibo()

monitor = MonitorSegundoPlano()


print("=" * 45)
print("          BIBO - SISTEMA CENTRAL")
print("=" * 45)

print("\nBIBO iniciado com sucesso!")

print("\nMovimentos:")
print("frente, tras, esquerda, direita, parar")
print("acenar, dancar")

print("\nExpressoes:")
print("feliz, triste")

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
            print("\nBIBO: Até logo!")
            break

        if not entrada:
            continue

        if entrada.lower() == "sair":
            print("\nBIBO: Até logo!")
            break

        # 1. Verificar comandos do robo
        comando = interpretar_comando(entrada)

        if comando:
            bibo.enviar_comando(comando)
            continue

        # 2. Consultar personalidade e memoria
        resposta = personalidade.responder(entrada)

        # 3. Perguntas desconhecidas vao para a IA
        if resposta["texto"].startswith(
            "Ainda estou aprendendo a conversar!"
        ):

            print(
                "\n[BIBO] Consultando inteligencia artificial..."
            )

            try:
                resposta = inteligencia.responder(entrada)

            except Exception as erro:
                print(
                    "[BIBO] Erro na inteligencia:",
                    type(erro).__name__
                )

                resposta = {
                    "texto": (
                        "Minha inteligencia artificial esta "
                        "temporariamente indisponivel."
                    ),
                    "expressao": "normal"
                }

        # 4. Exibir resposta
        print("\nBIBO:", resposta["texto"])

        # 5. Atualizar rosto digital
        bibo.atualizar_servidor({
            "expressao": resposta.get(
                "expressao", "normal"
            )
        })

finally:
    # Encerrar monitoramento ao sair
    monitor.parar()

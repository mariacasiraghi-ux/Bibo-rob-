
from comandos import interpretar_comando
from controlador import ControladorBibo
from personalidade import PersonalidadeBibo
from inteligencia import InteligenciaBibo
from config import MODO_IA


# ==========================================
# INICIALIZAÇÃO DO BIBO
# ==========================================

bibo = ControladorBibo()
personalidade = PersonalidadeBibo()
inteligencia = InteligenciaBibo()


print("=" * 45)
print("          BIBO - SISTEMA CENTRAL")
print("=" * 45)

print("\nBIBO iniciado com sucesso!")

print("\nMovimentos:")
print("frente, tras, esquerda, direita, parar")
print("acenar, dancar")

print("\nExpressões:")
print("feliz, triste")

print("\nConversação:")
print("Personalidade e memória ativadas!")

print("\nInteligência artificial:")

if MODO_IA == "gemini":
    print("Gemini online ativado!")
else:
    print("Modo de simulação ativado.")

print("\nDigite 'sair' para encerrar.")


# ==========================================
# CONVERSAÇÃO PRINCIPAL
# ==========================================

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

    # 1. Verificar comandos do robô
    comando = interpretar_comando(entrada)

    if comando:
        bibo.enviar_comando(comando)
        continue

    # 2. Consultar personalidade e memória
    resposta = personalidade.responder(entrada)

    # 3. Perguntas desconhecidas vão para a IA
    if resposta["texto"].startswith(
        "Ainda estou aprendendo a conversar!"
    ):

        print("\n[BIBO] Consultando inteligência artificial...")

        try:
            resposta = inteligencia.responder(entrada)

        except Exception as erro:
            print(
                "[BIBO] Erro na inteligência:",
                type(erro).__name__
            )

            resposta = {
                "texto": (
                    "Minha inteligência artificial está "
                    "temporariamente indisponível."
                ),
                "expressao": "normal"
            }

    # 4. Exibir resposta
    print("\nBIBO:", resposta["texto"])

    # 5. Atualizar rosto digital
    bibo.atualizar_servidor({
        "expressao": resposta.get("expressao", "normal")
    })

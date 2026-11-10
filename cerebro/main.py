
from comandos import interpretar_comando
from controlador import ControladorBibo
from personalidade import PersonalidadeBibo
from inteligencia import InteligenciaBibo


bibo = ControladorBibo()
personalidade = PersonalidadeBibo()
inteligencia = InteligenciaBibo()


print("=" * 45)
print("          BIBO - SISTEMA CENTRAL")
print("=" * 45)

print("BIBO iniciado com sucesso!")

print("\nMovimentos:")
print("frente, tras, esquerda, direita, parar")
print("acenar, dancar")

print("\nExpressões:")
print("feliz, triste")

print("\nConversação:")
print("Você pode conversar e ensinar preferências!")

print("\nInteligência artificial:")
print("Modo de simulação ativado.")

print("\nDigite 'sair' para encerrar.")


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

    # 2. Consultar a personalidade e a memória
    resposta = personalidade.responder(entrada)

    # 3. Se não reconhecer, consultar a IA simulada
    if resposta["texto"].startswith(
        "Ainda estou aprendendo a conversar!"
    ):
        resposta = inteligencia.responder(entrada)

    # 4. Exibir a resposta
    print("\nBIBO:", resposta["texto"])

    # 5. Atualizar o rosto digital
    bibo.atualizar_servidor({
        "expressao": resposta["expressao"]
    })

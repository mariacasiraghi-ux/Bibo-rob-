from comandos import interpretar_comando
from controlador import ControladorBibo


bibo = ControladorBibo()

print("=" * 40)
print("         BIBO - SISTEMA CENTRAL")
print("=" * 40)

print("BIBO iniciado com sucesso!")
print("\nComandos disponíveis:")
print("frente, tras, esquerda, direita")
print("parar, acenar, dancar")
print("feliz, triste, falar, carregar")
print("\nDigite 'sair' para encerrar.")

while True:

    entrada = input("\nVocê: ").strip().lower()

    if entrada == "sair":
        print("\nBIBO: Até logo!")
        break

    comando = interpretar_comando(entrada)

    if comando:
        bibo.enviar_comando(comando)
    else:
        print("[BIBO] Comando não reconhecido.")
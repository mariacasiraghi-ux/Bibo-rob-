
# CONFIGURACAO DE COMUNICACAO DO BIBO

# Modos disponiveis:
# "virtual" - ESP32 simulado
# "fisico"  - ESP32 real (futuramente)

MODO_ESP32 = "virtual"

# Configuracoes futuras do ESP32 fisico
ESP32_IP = None
ESP32_PORTA = 8080


def obter_configuracao():
    return {
        "modo": MODO_ESP32,
        "ip": ESP32_IP,
        "porta": ESP32_PORTA
    }

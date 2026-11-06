import json
import sys
from pathlib import Path

# Localiza a pasta principal do projeto.
RAIZ = Path(__file__).resolve().parent.parent

# Permite importar o simulador da pasta esp32.
sys.path.insert(0, str(RAIZ))

from esp32.esp32_virtual import ESP32Virtual


class ControladorBibo:

    def __init__(self):
        self.estado = "DISPONIVEL"
        self.esp32 = ESP32Virtual()

    def enviar_comando(self, comando):

        mensagem = {
            "dispositivo": "BIBO",
            "comando": comando
        }

        print("\n[CÉREBRO] Enviando comando...")

        print(json.dumps(
            mensagem,
            indent=4,
            ensure_ascii=False
        ))

        # Comunicação simulada.
        resposta = self.esp32.receber(mensagem)

        self.estado = resposta["estado"]

        print("\n[CÉREBRO] Resposta do ESP32:")

        print(json.dumps(
            resposta,
            indent=4,
            ensure_ascii=False
        ))
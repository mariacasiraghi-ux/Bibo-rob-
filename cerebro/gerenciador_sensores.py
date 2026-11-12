
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from esp32.sensores_virtuais import SensoresVirtuais
from analise_sensores import AnaliseSensores
from monitor_bateria import MonitorBateria


class GerenciadorSensores:
    def __init__(self):
        self.sensores = SensoresVirtuais()
        self.analisador = AnaliseSensores()
        self.monitor_bateria = MonitorBateria()

    def consultar(self):
        leituras = self.sensores.ler_todos()
        analise = self.analisador.analisar(leituras)

        bateria = leituras["bateria"]

        energia = self.monitor_bateria.verificar(
            nivel=bateria["nivel"],
            carregando=bateria["carregando"]
        )

        return {
            "leituras": leituras,
            "analise": analise,
            "energia": energia,
            "modo": "simulacao"
        }

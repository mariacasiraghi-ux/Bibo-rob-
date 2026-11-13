
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from esp32.estacao_virtual import EstacaoVirtual
from monitor_bateria import MonitorBateria


class BuscaBase:
    def __init__(self):
        self.estacao = EstacaoVirtual()
        self.monitor = MonitorBateria()

    def verificar(self, bateria, carregando=False):
        energia = self.monitor.verificar(
            bateria, carregando
        )

        if energia["estado"] == "CARREGANDO":
            return {
                "estado": "CARREGANDO",
                "acao": "aguardar_recarga"
            }

        if energia["estado"] == "CRITICO":
            return {
                "estado": "BATERIA_CRITICA",
                "acao": "parar_e_solicitar_recarga"
            }

        if energia["estado"] == "NORMAL":
            return {
                "estado": "SEM_NECESSIDADE",
                "acao": "continuar"
            }

        localizacao = self.estacao.localizar()

        if not localizacao["encontrada"]:
            return {
                "estado": "BASE_NAO_ENCONTRADA",
                "acao": "aguardar"
            }

        distancia = localizacao["distancia_cm"]

        if distancia > 5:
            return {
                "estado": "APROXIMACAO",
                "acao": "planejar_aproximacao",
                "distancia_cm": distancia
            }

        return {
            "estado": "PRONTO_PARA_ENCAIXE",
            "acao": "verificar_alinhamento",
            "distancia_cm": distancia
        }

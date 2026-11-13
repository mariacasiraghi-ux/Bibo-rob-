
import time

from autonomia_bibo import AutonomiaBibo


class MonitorAutomatico:
    def __init__(self):
        self.bibo = AutonomiaBibo()
        self.intervalo = 2
        self.ativo = False

    def verificar(self):
        sensores = self.bibo.controle.energia.sensores
        diagnostico = sensores.consultar()

        bateria = diagnostico["leituras"]["bateria"]["nivel"]
        energia = diagnostico["energia"]

     

        if energia["estado"] == "BAIXO":
            print("[BIBO] Bateria baixa! Iniciando recarga virtual...")

            resultado = self.bibo.executar(bateria)

            print("[BIBO] Resultado:", resultado["estado"])
            return resultado

        if energia["estado"] == "CRITICO":
            print("[BIBO] Bateria critica! Preciso de ajuda.")
            return {
                "sucesso": False,
                "estado": "BATERIA_CRITICA"
            }

        return {
            "sucesso": True,
            "estado": energia["estado"]
        }

    def iniciar(self, ciclos=5):
        self.ativo = True

        for _ in range(ciclos):
            if not self.ativo:
                break

            self.verificar()
            time.sleep(self.intervalo)

        self.ativo = False

    def parar(self):
        self.ativo = False

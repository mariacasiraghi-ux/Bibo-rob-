import math
import threading
import time

from esp32.movimentos import MovimentosBibo


class ESP32Virtual:
    WATCHDOG_TIMEOUT_SECONDS = 1.5
    MOVIMENTOS_VALIDOS = {"frente", "tras", "esquerda", "direita"}

    def __init__(self, timeout_watchdog=WATCHDOG_TIMEOUT_SECONDS):
        if not isinstance(timeout_watchdog, (int, float)) or not math.isfinite(timeout_watchdog) or timeout_watchdog <= 0:
            raise ValueError("O timeout do watchdog deve ser um numero positivo")

        self.timeout_watchdog = float(timeout_watchdog)
        self._condition = threading.Condition()
        self._estado = "DISPONIVEL"
        self.expressao = "normal"
        self.bateria = 100
        self.movimentos = MovimentosBibo()
        self._prazo_movimento = None

        # Uma única thread por instância; ela permanece adormecida sem movimento.
        self._watchdog = threading.Thread(
            target=self._executar_watchdog,
            name="ESP32VirtualWatchdog",
            daemon=True
        )
        self._watchdog.start()

    @property
    def estado(self):
        with self._condition:
            return self._estado

    def consultar_estado(self):
        with self._condition:
            return {
                "estado": self._estado,
                "roda_esquerda": self.movimentos.roda_esquerda,
                "roda_direita": self.movimentos.roda_direita
            }

    def _executar_watchdog(self):
        with self._condition:
            while True:
                if self._prazo_movimento is None:
                    self._condition.wait()
                    continue

                restante = self._prazo_movimento - time.monotonic()
                if restante > 0:
                    self._condition.wait(timeout=restante)
                    continue

                # O prazo expirou: parar e limpar o prazo impede reinício automático.
                self.movimentos.mover_rodas("parar")
                self._estado = "DISPONIVEL"
                self._prazo_movimento = None
                print("[ESP32 VIRTUAL] Watchdog expirou; rodas paradas.")
                self._condition.notify_all()

    def receber(self, mensagem):
        if not isinstance(mensagem, dict):
            return {"dispositivo": "BIBO", "status": "erro", "estado": self.estado}

        comando = mensagem.get("comando", {})
        if not isinstance(comando, dict):
            return {"dispositivo": "BIBO", "status": "erro", "estado": self.estado}

        sistema = comando.get("sistema")
        acao = comando.get("acao")

        with self._condition:
            print("\n[ESP32] Comando recebido!")

            if sistema == "motores":
                if acao == "parar":
                    self.movimentos.mover_rodas("parar")
                    self._estado = "DISPONIVEL"
                    self._prazo_movimento = None
                    self._condition.notify_all()
                elif acao in self.MOVIMENTOS_VALIDOS:
                    self.movimentos.mover_rodas(acao)
                    self._estado = "MOVIMENTANDO"
                    # Cada comando válido renova o prazo de segurança.
                    self._prazo_movimento = time.monotonic() + self.timeout_watchdog
                    self._condition.notify_all()
                else:
                    print("[ERRO] Movimento desconhecido")

            elif sistema == "bracos":
                if acao == "acenar":
                    self.movimentos.acenar()

            elif sistema == "corpo":
                if acao == "dancar":
                    self.movimentos.dancar()

            elif sistema == "rosto":
                self.expressao = acao
                print(f"[ROSTO] Expressão: {acao}")

            elif sistema == "audio":
                print("[ÁUDIO] BIBO:", comando.get("texto", ""))

            elif sistema == "energia":
                self.movimentos.mover_rodas("parar")
                self._prazo_movimento = None
                self._condition.notify_all()
                self._estado = "PROCURANDO_BASE"
                print("[ENERGIA] Retorno à base solicitado")
                print("[SIMULAÇÃO] Navegação ainda não implementada")

            else:
                print("[ERRO] Comando desconhecido")

            return {
                "dispositivo": "BIBO",
                "status": "simulado",
                "estado": self._estado
            }

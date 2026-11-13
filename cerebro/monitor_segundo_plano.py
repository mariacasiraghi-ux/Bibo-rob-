
import threading

from monitor_automatico import MonitorAutomatico


class MonitorSegundoPlano:
    def __init__(self):
        self.monitor = MonitorAutomatico()
        self.thread = None
        self.parar_evento = threading.Event()

    def _executar(self):
        while not self.parar_evento.is_set():
            try:
                self.monitor.verificar()
            except Exception as erro:
                print("[BIBO] Erro no monitor:", erro)

            self.parar_evento.wait(
                self.monitor.intervalo
            )

    def iniciar(self):
        if self.thread and self.thread.is_alive():
            print("[BIBO] Monitor ja esta ativo.")
            return

        self.parar_evento.clear()

        self.thread = threading.Thread(
            target=self._executar,
            daemon=True
        )

        self.thread.start()
        print("[BIBO] Monitor iniciado em segundo plano.")

    def parar(self):
        self.parar_evento.set()

        if self.thread:
            self.thread.join(timeout=5)

        print("[BIBO] Monitor encerrado.")

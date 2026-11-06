from esp32.movimentos import MovimentosBibo


class ESP32Virtual:

    def __init__(self):
        self.estado = "DISPONIVEL"
        self.expressao = "normal"
        self.bateria = 100

        self.movimentos = MovimentosBibo()

    def receber(self, mensagem):
        comando = mensagem.get("comando", {})
        sistema = comando.get("sistema")
        acao = comando.get("acao")

        print("\n[ESP32] Comando recebido!")

        if sistema == "motores":
            self.movimentos.mover_rodas(acao)

            if acao == "parar":
                self.estado = "DISPONIVEL"
            else:
                self.estado = "MOVIMENTANDO"

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
            self.estado = "PROCURANDO_BASE"
            print("[ENERGIA] Retorno à base solicitado")
            print("[SIMULAÇÃO] Navegação ainda não implementada")

        else:
            print("[ERRO] Comando desconhecido")

        return {
            "dispositivo": "BIBO",
            "status": "simulado",
            "estado": self.estado
        }

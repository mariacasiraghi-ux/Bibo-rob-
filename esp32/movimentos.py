class MovimentosBibo:

    def __init__(self):
        self.roda_esquerda = 0
        self.roda_direita = 0

        self.cabeca_horizontal = 90
        self.cabeca_vertical = 90

        self.braco_esquerdo = 90
        self.braco_direito = 90

    def mover_rodas(self, direcao):
        movimentos = {
            "frente": (50, 50),
            "tras": (-50, -50),
            "esquerda": (-40, 40),
            "direita": (40, -40),
            "parar": (0, 0)
        }

        if direcao not in movimentos:
            print("[ERRO] Movimento desconhecido")
            return

        esquerda, direita = movimentos[direcao]

        # Valores apenas simulados, não são sinais elétricos.
        self.roda_esquerda = esquerda
        self.roda_direita = direita

        print(f"[RODA ESQUERDA] {esquerda}")
        print(f"[RODA DIREITA] {direita}")

    def mover_cabeca(self, horizontal=90, vertical=90):
        self.cabeca_horizontal = max(0, min(180, horizontal))
        self.cabeca_vertical = max(0, min(180, vertical))

        print(
            "[CABEÇA]",
            self.cabeca_horizontal,
            self.cabeca_vertical
        )

    def mover_braco(self, lado, angulo):
        angulo = max(0, min(180, angulo))

        if lado == "esquerdo":
            self.braco_esquerdo = angulo

        elif lado == "direito":
            self.braco_direito = angulo

        else:
            print("[ERRO] Braço desconhecido")
            return

        print(f"[BRAÇO {lado.upper()}] {angulo} graus")

    def acenar(self):
        print("[BIBO] Acenando!")

        self.mover_braco("direito", 45)
        self.mover_braco("direito", 120)
        self.mover_braco("direito", 45)
        self.mover_braco("direito", 90)

    def dancar(self):
        print("[BIBO] Dançando!")

        self.mover_cabeca(60, 90)
        self.mover_braco("esquerdo", 45)
        self.mover_braco("direito", 135)

        self.mover_cabeca(120, 90)
        self.mover_braco("esquerdo", 135)
        self.mover_braco("direito", 45)

        self.mover_cabeca(90, 90)
        self.mover_braco("esquerdo", 90)
        self.mover_braco("direito", 90)

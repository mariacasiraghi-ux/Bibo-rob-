
class AnaliseSensores:
    def analisar(self, dados):
        alertas = []
        acoes = []

        distancia = dados["distancia_cm"]
        bateria = dados["bateria"]["nivel"]
        inclinacao = dados["movimento"]["inclinacao"]
        carregando = dados["bateria"]["carregando"]

        if distancia < 20:
            alertas.append("Obstaculo proximo")
            acoes.append("parar")

        if bateria <= 20 and not carregando:
            alertas.append("Bateria baixa")
            acoes.append("procurar_base")

        if abs(inclinacao) >= 30:
            alertas.append("Inclinacao elevada")
            if "parar" not in acoes:
                acoes.append("parar")

        return {
            "alertas": alertas,
            "acoes_sugeridas": acoes,
            "seguro_para_mover": "parar" not in acoes
        }

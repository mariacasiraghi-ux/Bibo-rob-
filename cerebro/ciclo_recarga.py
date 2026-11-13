
from aproximacao_base import AproximacaoBase
from recarga_bateria import RecargaBateria


class CicloRecarga:
    def __init__(self):
        self.recarga = RecargaBateria()
        self.aproximacao = AproximacaoBase()

        # Compartilhar a mesma estacao virtual
        self.aproximacao.busca.estacao = (
            self.recarga.encaixe.busca.estacao
        )

    def executar(self, bateria=15):
        historico = []

        # 1. Verificar a necessidade de recarga
        decisao = self.aproximacao.busca.verificar(bateria)

        historico.append({
            "etapa": "verificacao",
            "resultado": decisao
        })

        if decisao["estado"] == "SEM_NECESSIDADE":
            return {
                "sucesso": True,
                "estado": "RECARGA_DESNECESSARIA",
                "historico": historico
            }

        if decisao["estado"] != "APROXIMACAO":
            return {
                "sucesso": False,
                "estado": decisao["estado"],
                "historico": historico
            }

        # 2. Simular a aproximacao
        movimento = self.aproximacao.executar(bateria)

        historico.append({
            "etapa": "aproximacao",
            "resultado": movimento["resultado"],
            "passos": len(movimento["historico"])
        })

        if movimento["resultado"]["estado"] != "PRONTO_PARA_ENCAIXE":
            return {
                "sucesso": False,
                "estado": movimento["resultado"]["estado"],
                "historico": historico
            }

        # 3. Simular confirmacao de alinhamento
        self.recarga.encaixe.alinhado = True

        encaixe = self.recarga.encaixe.encaixar()

        historico.append({
            "etapa": "encaixe",
            "resultado": encaixe
        })

        if not encaixe["sucesso"]:
            return {
                "sucesso": False,
                "estado": "FALHA_NO_ENCAIXE",
                "historico": historico
            }

        # 4. Iniciar a recarga virtual
        self.recarga.nivel = bateria

        inicio = self.recarga.iniciar()

        if not inicio["sucesso"]:
            return {
                "sucesso": False,
                "estado": "FALHA_NA_RECARGA",
                "historico": historico
            }

        # 5. Carregar ate 100%
        while self.recarga.nivel < 100:
            resultado = self.recarga.carregar_passo()

            if not resultado["sucesso"]:
                return {
                    "sucesso": False,
                    "estado": "RECARGA_INTERROMPIDA",
                    "historico": historico
                }

            historico.append({
                "etapa": "carregamento",
                "bateria": resultado["bateria"]
            })

        return {
            "sucesso": True,
            "estado": "RECARGA_CONCLUIDA",
            "bateria": self.recarga.nivel,
            "historico": historico
        }

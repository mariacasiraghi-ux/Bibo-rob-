
from gerenciador_energia import GerenciadorEnergia
from modo_descanso import ModoDescanso


class ControleDescanso:
    def __init__(self):
        self.energia = GerenciadorEnergia()
        self.descanso = ModoDescanso()

    def executar(self):
        situacao = self.energia.verificar()
        nivel = situacao["nivel"]
        historico = []

        historico.append({
            "etapa": "verificar_bateria",
            "nivel": nivel
        })

        if situacao["estado"] == "NORMAL":
            return {
                "sucesso": True,
                "estado": "DISPONIVEL",
                "bateria": nivel,
                "historico": historico
            }

        if situacao["estado"] == "CRITICO":
            return {
                "sucesso": False,
                "estado": "AGUARDANDO_AJUDA",
                "historico": historico
            }

        # 1. Localizar e aproximar da base virtual
        aproximacao = self.energia.ciclo.aproximacao.executar(nivel)

        historico.append({
            "etapa": "aproximacao",
            "resultado": aproximacao["resultado"]
        })

        if aproximacao["resultado"]["estado"] != "PRONTO_PARA_ENCAIXE":
            return {
                "sucesso": False,
                "estado": aproximacao["resultado"]["estado"],
                "historico": historico
            }

        # 2. Compartilhar a estacao com o sistema de encaixe
        estacao = self.energia.ciclo.aproximacao.busca.estacao
        recarga = self.energia.ciclo.recarga
        recarga.encaixe.busca.estacao = estacao

        # Alinhamento confirmado apenas na simulacao
        recarga.encaixe.alinhado = True
        encaixe = recarga.encaixe.encaixar()

        if not encaixe["sucesso"]:
            return {
                "sucesso": False,
                "estado": "FALHA_NO_ENCAIXE",
                "historico": historico
            }

        historico.append({
            "etapa": "encaixe",
            "resultado": encaixe
        })

        # 3. Entrar em descanso antes de carregar
        historico.append({
            "etapa": "descansar",
            "resultado": self.descanso.descansar()
        })

        historico.append({
            "etapa": "iniciar_carregamento",
            "resultado": self.descanso.iniciar_carregamento()
        })

        # 4. Carregar enquanto permanece em descanso
        recarga.nivel = nivel

        while recarga.nivel < 100:
            resultado = recarga.carregar_passo()

            if not resultado["sucesso"]:
                return {
                    "sucesso": False,
                    "estado": "RECARGA_INTERROMPIDA",
                    "historico": historico
                }

            historico.append({
                "etapa": "carregando",
                "bateria": resultado["bateria"],
                "modo": self.descanso.estado
            })

        # 5. Atualizar bateria virtual
        self.energia.sensores.sensores.bateria = recarga.nivel

        # 6. Acordar
        historico.append({
            "etapa": "acordar",
            "resultado": self.descanso.acordar()
        })

        return {
            "sucesso": True,
            "estado": self.descanso.estado,
            "bateria": recarga.nivel,
            "historico": historico
        }

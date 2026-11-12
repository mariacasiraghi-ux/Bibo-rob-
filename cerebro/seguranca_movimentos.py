
from gerenciador_sensores import GerenciadorSensores


class SegurancaMovimentos:
    def __init__(self):
        self.gerenciador = GerenciadorSensores()

    def verificar(self, comando):
        diagnostico = self.gerenciador.consultar()
        analise = diagnostico["analise"]

        if not isinstance(comando, dict):
            return {
                "permitido": False,
                "motivo": "Comando invalido"
            }

        sistema = comando.get("sistema")
        acao = comando.get("acao")

        # Parar sempre deve ser permitido
        if acao == "parar":
            return {
                "permitido": True,
                "motivo": "Parada permitida"
            }

        # Verificar comandos de locomocao
        
        if sistema in ["rodas", "movimento", "base", "motores"]:
            if not analise["seguro_para_mover"]:
                return {
                    "permitido": False,
                    "motivo": "Movimento bloqueado pelos sensores",
                    "alertas": analise["alertas"]
                }

        return {
            "permitido": True,
            "motivo": "Comando autorizado na simulacao"
        }

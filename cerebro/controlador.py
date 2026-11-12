from seguranca_movimentos import SegurancaMovimentos
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from esp32.esp32_virtual import ESP32Virtual
from comunicacao_esp32 import ComunicacaoESP32


class ControladorBibo:
    def __init__(self):
        self.estado = "DISPONIVEL"
        self.esp32 = ESP32Virtual()
        self.comunicacao = ComunicacaoESP32()
        self.seguranca = SegurancaMovimentos()



    def atualizar_servidor(self, dados):
        endereco = "http://127.0.0.1:5000/estado"

        requisicao = Request(
            endereco,
            data=json.dumps(dados).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urlopen(requisicao, timeout=2) as resposta:
                if resposta.status == 200:
                    print("[SERVIDOR] Estado atualizado!")
        except (URLError, TimeoutError):
            print("[SERVIDOR] Não foi possível conectar ao servidor.")

    def enviar_comando(self, comando):

        verificacao = self.seguranca.verificar(comando)

        if not verificacao["permitido"]:
            print("\n[BIBO] Movimento bloqueado!")
            print("[SEGURANCA]", verificacao["motivo"])

            for alerta in verificacao.get("alertas", []):
                print("[ALERTA]", alerta)

            return

        mensagem = {
            "dispositivo": "BIBO",
            "comando": comando
        }

        print("\n[CÉREBRO] Enviando comando...")
        print(json.dumps(mensagem, indent=4, ensure_ascii=False))

                # Registrar o comando na comunicacao virtual
        confirmacao = self.comunicacao.enviar(comando)

        if not confirmacao["sucesso"]:
            print("[CÉREBRO] Falha na comunicação com ESP32.")
            return

        resposta = self.esp32.receber(mensagem)
        self.estado = resposta["estado"]

        print("\n[CÉREBRO] Resposta do ESP32:")
        print(json.dumps(resposta, indent=4, ensure_ascii=False))

        dados = {"status": self.estado}

        if comando.get("sistema") == "rosto":
            dados["expressao"] = comando.get("acao", "normal")

        self.atualizar_servidor(dados)

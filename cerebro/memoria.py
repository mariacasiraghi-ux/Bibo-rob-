
import json
from pathlib import Path


class MemoriaBibo:
    def __init__(self):
        self.arquivo = Path(__file__).parent / "dados_memoria.json"
        self.dados = self.carregar()

    def carregar(self):
        if self.arquivo.exists():
            try:
                with open(self.arquivo, "r", encoding="utf-8") as arquivo:
                    dados = json.load(arquivo)
                    if isinstance(dados, dict):
                        return dados
            except (json.JSONDecodeError, OSError):
                print("[MEMÓRIA] Não foi possível ler os dados.")

        return {}

    def salvar(self):
        with open(self.arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(
                self.dados,
                arquivo,
                indent=4,
                ensure_ascii=False
            )

    def lembrar(self, chave):
        return self.dados.get(chave)

    def aprender(self, chave, valor):
        self.dados[chave] = valor
        self.salvar()

    def esquecer(self, chave):
        if chave in self.dados:
            del self.dados[chave]
            self.salvar()
            return True

        return False

    def apagar_tudo(self):
        self.dados.clear()
        self.salvar()

def interpretar_comando(texto):
    texto = texto.lower().strip()

    comandos = {
        "frente": {
            "sistema": "motores",
            "acao": "frente"
        },

        "tras": {
            "sistema": "motores",
            "acao": "tras"
        },

        "esquerda": {
            "sistema": "motores",
            "acao": "esquerda"
        },

        "direita": {
            "sistema": "motores",
            "acao": "direita"
        },

        "parar": {
            "sistema": "motores",
            "acao": "parar"
        },

        "acenar": {
            "sistema": "bracos",
            "acao": "acenar"
        },

        "dancar": {
            "sistema": "corpo",
            "acao": "dancar"
        },

        "feliz": {
            "sistema": "rosto",
            "acao": "feliz"
        },

        "triste": {
            "sistema": "rosto",
            "acao": "triste"
        },

        "falar": {
            "sistema": "audio",
            "acao": "falar",
            "texto": "Olá! Eu sou o BIBO!"
        },

        "carregar": {
            "sistema": "energia",
            "acao": "retornar_base"
        }
    }

    return comandos.get(texto)
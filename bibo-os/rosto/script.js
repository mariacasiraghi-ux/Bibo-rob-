
const olhos = document.getElementById("olhos");
const statusTexto = document.getElementById("status");

const SERVIDOR = "http://127.0.0.1:5000/estado";

let expressaoAtual = "normal";
let direcaoAtual = "centro";
let piscando = false;

let ultimaDirecaoServidor = 0;

const expressoes = [
    "normal",
    "feliz",
    "triste",
    "surpreso"
];

const direcoes = [
    "esquerda",
    "direita",
    "cima",
    "baixo",
    "centro"
];

function atualizarRosto() {
    if (!olhos) return;

    olhos.className = "olhos";

    if (expressaoAtual !== "normal") {
        olhos.classList.add(expressaoAtual);
    }

    olhos.classList.add("olhar-" + direcaoAtual);

    if (piscando) {
        olhos.classList.add("piscando");
    }

    if (statusTexto) {
        statusTexto.textContent =
            "Expressão: " + expressaoAtual +
            " | Olhando: " + direcaoAtual;
    }
}

function mudarExpressao(expressao) {
    if (!expressoes.includes(expressao)) return;

    expressaoAtual = expressao;
    atualizarRosto();
}

function olhar(direcao) {
    if (!direcoes.includes(direcao)) return;

    direcaoAtual = direcao;
    atualizarRosto();
}

function piscar() {
    if (piscando) return;

    piscando = true;
    atualizarRosto();

    setTimeout(() => {
        piscando = false;
        atualizarRosto();
    }, 180);
}

// Movimento automatico dos olhos
function movimentarOlhos() {
    // Prioriza comandos recentes do servidor
    if (Date.now() - ultimaDirecaoServidor < 3000) {
        return;
    }

    const direcaoAleatoria =
        direcoes[Math.floor(Math.random() * direcoes.length)];

    olhar(direcaoAleatoria);
}

// Consultar o cerebro do BIBO
async function consultarServidor() {
    try {
        const resposta = await fetch(SERVIDOR);

        if (!resposta.ok) {
            throw new Error("Servidor indisponivel");
        }

        const dados = await resposta.json();

        if (expressoes.includes(dados.expressao)) {
            mudarExpressao(dados.expressao);
        }

        if (
            direcoes.includes(dados.direcao) &&
            dados.direcao !== "centro"
        ) {
            ultimaDirecaoServidor = Date.now();
            olhar(dados.direcao);
        }

    } catch (erro) {
        console.log("[BIBO] Aguardando servidor...");
    }
}

// Piscar automaticamente
setInterval(piscar, 4000);

// Movimentar olhos automaticamente
setInterval(movimentarOlhos, 2500);

// Consultar servidor a cada segundo
setInterval(consultarServidor, 1000);

atualizarRosto();
consultarServidor();

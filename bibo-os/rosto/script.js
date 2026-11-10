
const olhos = document.getElementById("olhos");
const statusTexto = document.getElementById("status");

const SERVIDOR = "http://127.0.0.1:5000/estado";

let expressaoAtual = "normal";
let direcaoAtual = "centro";
let piscando = false;

const expressoes = ["normal", "feliz", "triste", "surpreso"];
const direcoes = ["esquerda", "direita", "cima", "baixo", "centro"];

function atualizarRosto() {
    olhos.className = "olhos";

    if (expressaoAtual !== "normal") {
        olhos.classList.add(expressaoAtual);
    }

    olhos.classList.add("olhar-" + direcaoAtual);

    if (piscando) {
        olhos.classList.add("piscando");
    }

    statusTexto.textContent =
        "Expressão: " + expressaoAtual +
        " | Olhando: " + direcaoAtual;
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

// Consultar o cérebro do BIBO
async function consultarServidor() {
    try {
        const resposta = await fetch(SERVIDOR);

        if (!resposta.ok) {
            throw new Error("Servidor indisponível");
        }

        const dados = await resposta.json();

        if (expressoes.includes(dados.expressao)) {
            mudarExpressao(dados.expressao);
        }

        if (direcoes.includes(dados.direcao)) {
            olhar(dados.direcao);
        }

    } catch (erro) {
        console.log("[BIBO] Aguardando servidor...");
    }
}

// Piscadas automáticas
setInterval(piscar, 4000);

// Consultar o servidor a cada segundo
setInterval(consultarServidor, 1000);

atualizarRosto();
consultarServidor();

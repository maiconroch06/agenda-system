let profissional = JSON.parse(localStorage.getItem("profissional")) || [];
console.log(profissional)

/*  ===========================================================
    UTILITÁRIOS
    =========================================================== */

function definirErroCodigo(msg){
    const campos = document.querySelectorAll(".codigo");
    campos.forEach(campo => {
        campo.classList.add("invalido");
    });

    document.getElementById("erro-codigo").textContent = msg;
}

function limparErroCodigo(){
    const campos = document.querySelectorAll(".codigo");
    campos.forEach(campo => {
        campo.classList.remove("invalido");
    });

    document.getElementById("erro-codigo").textContent = "";
}

function proximoCampo(input) {
    input.value = input.value.replace(/[^a-zA-Z0-9]/g, "");

    if (input.value.length === 1) {
        const proximo = input.nextElementSibling;

        if (proximo && proximo.classList.contains("codigo")) {
            proximo.focus();
        }
    }
}

function voltarCampo(input, evento) {
    if (evento.key === "Backspace" && input.value === "") {
        const anterior = input.previousElementSibling;

        if (anterior && anterior.classList.contains("codigo")) {
            anterior.focus();
        }
    }
}

function aplicarCodigoValidacao() {
    const campos = document.querySelectorAll(".codigo");

    campos.forEach(campo => {
        campo.oninput = function () {
            proximoCampo(this);
        };

        campo.onkeydown = function (evento) {
            voltarCampo(this, evento);
        };
    });
}

function obterCodigoValidacao() {
    let codigo = "";
    document.querySelectorAll(".codigo").forEach(campo => {
        codigo += campo.value;
    });

    return codigo;
}

aplicarCodigoValidacao();

function codigoCompleto() {
    const camposCodigo = document.querySelectorAll(".codigo");

    for (let campo of camposCodigo) {
        if (campo.value === "") {
            return false;
        }
    }

    return true;
}

function voltar() {
    window.location.href = "cadastroProfissional.html"
}

function vincular() {
    //codicoImput = document.getElementById("").value.trim();

    const codigo = obterCodigoValidacao();

    if(codigo.length !== 8){
        definirErroCodigo("Digite os 8 caracteres.");
        return;
    }

    limparErroCodigo();

    window.location.href = "painelProfissional.html"
}
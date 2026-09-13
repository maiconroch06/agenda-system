let empresa = JSON.parse(localStorage.getItem("empresa")) || {
    nome: "",
    categoria: "",
    cnpj: "",
    abertura: "",
    fechamento: "",
    dias: []
}

/* ============================================================
   UTILITÁRIOS
   ============================================================ */

function limparErro(inputId, erroId) {
    const input = document.getElementById(inputId);
    const erro = document.getElementById(erroId);
    if (input) input.classList.remove("invalido");
    if (erro) erro.textContent = "";
}

function definirErro(inputId, erroId, msg) {
    const input = document.getElementById(inputId);
    const erro = document.getElementById(erroId);
    if (input) input.classList.add("invalido");
    if (erro) erro.textContent = msg;
}

function mostrarAviso(msg) {
    const el = document.getElementById("aviso");
    el.textContent = msg;
    el.classList.add("visivel");
    setTimeout(() => el.classList.remove("visivel"), 2500);
}

/* ============================================================
   MÁSCARA CNPJ
   ============================================================ */
   
function aplicarMascaraCnpj(input) {
    input.addEventListener("input", () => {
        let v = input.value.replace(/\D/g, "").slice(0, 14);
        v = v.replace(/^(\d{2})(\d)/, "$1.$2");
        v = v.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
        v = v.replace(/\.(\d{3})(\d)/, ".$1/$2");
        v = v.replace(/(\d{4})(\d)/, "$1-$2");
        input.value = v;
    });
}

aplicarMascaraCnpj(document.getElementById("emp-cnpj"));

/* ============================================================
   DIAS DA SEMANA
   ============================================================ */
   
const botoesDia = document.querySelectorAll(".dia-btn");

document.querySelectorAll(".dia-btn").forEach(btn => {
    btn.addEventListener("click", () => btn.classList.toggle("ativo"));
});

/* ============================================================
   TELA 3: DADOS DA EMPRESA
   ============================================================ */

function salvarEmpresa() {
    const nome = document.getElementById("emp-nome").value.trim();
    const categoria = document.getElementById("emp-categoria").value;
    const cnpj = document.getElementById("emp-cnpj").value.trim();
    const abertura = document.getElementById("emp-abertura").value;
    const fechamento = document.getElementById("emp-fechamento").value;

    if (!nome) { mostrarAviso("Informe o nome da empresa"); return; }
    if (!categoria) { mostrarAviso("Selecione uma categoria"); return; }
    if (!cnpj) { mostrarAviso("Informe o CNPJ"); return; }

    const diasAtivos = [...document.querySelectorAll(".dia-btn.ativo")].map(b => b.dataset.dia);

    const empresa = {
        nome: nome,
        categoria: categoria,
        cnpj: cnpj,
        abertura: abertura,
        fechamento: fechamento,
        dias: diasAtivos
    }

    localStorage.setItem("empresa", JSON.stringify(empresa));
    window.location.href = "cadastroServicos.html";
}

function voltar() {
    window.location.href = "tipoUsuario.html"
}

/* ============================================================
   ESTADO SERVIÇOS
   ============================================================ */

let profissional = JSON.parse(localStorage.getItem("profissional")) || [];
console.log(profissional)
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

function lerArquivoBase64(input) {
    return new Promise((resolve) => {
        const arquivo = input.files[0];
        if (!arquivo) { resolve(null); return; }
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.readAsDataURL(arquivo);
    });
}

function gerarIdUnico() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
}

/* ============================================================
   MÁSCARA TELEFONE
   ============================================================ */
   
function aplicarMascaraTelefone(input) {
    input.addEventListener("input", () => {
        let v = input.value.replace(/\D/g, "").slice(0, 11);

        v = v.replace(/^(\d{2})(\d)/, "($1) $2");
        v = v.replace(/(\d{5})(\d)/, "$1-$2");

        input.value = v;
    });
}

aplicarMascaraTelefone(document.getElementById("pro-telefone"));

/* ============================================================
   TELA 5: PROFISSIONAIS (cadastro)
   ============================================================ */

function voltar() {
    window.location.href = "tipoUsuario.html";
}

async function salvarProfissional() {
    //MostrarAviso("Acesso de funcionário será desenvolvido em breve");
    const fotoInput = document.getElementById("pro-foto");
    const tel = document.getElementById("pro-telefone").value.trim();
    const cargo = document.getElementById("pro-cargo").value.trim();
    const exp = document.getElementById("experiencia").value;

    let valido = true;

    limparErro("pro-telefone", "erro-prof-tel");
    limparErro("pro-cargo", "erro-prof-cargo");

    const telefoneLimpo = tel.replace(/\D/g, "");

    if (telefoneLimpo.length !== 11) {
        definirErro("pro-telefone", "erro-prof-tel", "Telefone inválido");
        valido = false;
    }

    if (!cargo) {
        definirErro("pro-cargo", "erro-prof-cargo", "Preencha seu cargo");
        valido = false;
    }

    if (!valido) { return; }

    const foto = await lerArquivoBase64(fotoInput);

    profissional = { // Isso vai causar algum erro?
        foto: foto,
        telefone: tel,
        cargo: cargo,
        experiencia: exp
    }

    localStorage.setItem("profissional", JSON.stringify(profissional));
    window.location.href = "vinculacaoEmpresa.html"
}

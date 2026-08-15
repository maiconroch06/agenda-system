/* ============================================================
   ESTADO AUTENICAÇÃO
   ============================================================ */

let usuario = JSON.parse(localStorage.getItem("usuario")) || {
    nome: "",
    senha: "",
    email: "",
    tipo: ""
};

console.log(usuario)
console.log(JSON.parse(localStorage.getItem("empresa")))

/*  ===========================================================
    UTILITÁRIOS
    =========================================================== */

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

/* ============================================================
   ABAS DE AUTH
   ============================================================ */

document.querySelectorAll(".auth-aba").forEach(aba => {
    aba.addEventListener("click", () => {
        document.querySelectorAll(".auth-aba").forEach(a => a.classList.remove("ativa"));
        aba.classList.add("ativa");

        const qual = aba.dataset.aba;
        document.getElementById("form-login").hidden = qual !== "login";
        limparErro("login-usuario", "erro-login-usuario");
        limparErro("login-senha", "erro-login-senha");
        document.getElementById("form-cadastro").hidden = qual !== "cadastro";
        ["cad-nome","cad-email","cad-senha","cad-confirmar"].forEach((id, i) => {
            limparErro(id, ["erro-cad-nome","erro-cad-email","erro-cad-senha","erro-cad-confirmar"][i]);
        });
    });
});

/* ============================================================
   TELA 1: LOGIN
   ============================================================ */

function fazerLogin() {
    const login = document.getElementById("login-usuario").value.trim();
    const senha = document.getElementById("login-senha").value;

    let valido = true;

    limparErro("login-usuario", "erro-login-usuario");
    limparErro("login-senha", "erro-login-senha");

    console.log(usuario)


    if (!usuario) {
        definirErro("login-usuario", "erro-login-usuario", "Digite o nome de usuário ou e-mail.");
        definirErro("login-senha", "erro-login-senha", "Digite uma senha.");
        return;
    }

    if (login !== usuario.nome && login !== usuario.email) {
        definirErro("login-usuario", "erro-login-usuario", "Usuário ou e-mail incorreto.");
        valido = false;
    }

    if (senha !== usuario.senha) {
        definirErro("login-senha", "erro-login-senha", "Senha incorreta.");
        valido = false;
    }

    if (!valido) return;

    if (usuario.tipo == "admin") {
        window.location.href = "painelAdministrativo.html";
        return;
    }
    if (usuario.tipo == "profissional") {
        window.location.href = "painelProfissional.html";
    }
}

/* ============================================================
   TELA 1: CADASTRO
   ============================================================ */

function fazerCadastro() {
    const nome = document.getElementById("cad-nome").value.trim();
    const email = document.getElementById("cad-email").value.trim();
    const senha = document.getElementById("cad-senha").value;
    const confirmar = document.getElementById("cad-confirmar").value;

    let valido = true;

    ["cad-nome","cad-email","cad-senha","cad-confirmar"].forEach((id, i) => {
        limparErro(id, ["erro-cad-nome","erro-cad-email","erro-cad-senha","erro-cad-confirmar"][i]);
    });

    if (nome.length < 3) {
        definirErro("cad-nome", "erro-cad-nome", "Nome deve ter ao menos 3 caracteres");
        valido = false;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        definirErro("cad-email", "erro-cad-email", "Informe um e-mail válido");
        valido = false;
    }

    if (senha.length < 6) {
        definirErro("cad-senha", "erro-cad-senha", "Senha deve ter ao menos 6 caracteres");
        valido = false;
    }

    if (senha !== confirmar || confirmar == "") {
        definirErro("cad-confirmar", "erro-cad-confirmar", "As senhas não coincidem");
        valido = false;
    }

    if (!valido) return;

    const usuario = {
        nome: nome,
        email: email,
        senha: senha
    };

    localStorage.setItem("usuario", JSON.stringify(usuario));

    window.location.href = "tipoUsuario.html";
}

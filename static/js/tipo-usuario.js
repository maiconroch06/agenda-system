
const usuario = JSON.parse(localStorage.getItem("usuario"));

if (usuario) {
    document.getElementById("nome-boas-vindas").textContent = usuario.nome;
}

/* ============================================================
   TELA 2: TIPO DE USUÁRIO
   ============================================================ */

function escolherTipo(tipo) {
    if (tipo === "admin") {
        usuario.tipo = "admin";
        localStorage.setItem("usuario", JSON.stringify(usuario));
        
        window.location.href = "cadastroEmpresa.html"
    } else {
        usuario.tipo = "profissional";
        localStorage.setItem("usuario", JSON.stringify(usuario));
        
        window.location.href = "cadastroProfissional.html"
    }
}
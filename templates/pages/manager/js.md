/* ============================================================
   ESTADO SERVIÇOS
   ============================================================ */

let usuario = JSON.parse(localStorage.getItem("usuario")) || {
    nome: "",
    senha: "",
    email: ""
};

console.log(usuario)
console.log(usuario.tipo)

let servicos = JSON.parse(localStorage.getItem("servicos")) || [];
let profissionais = JSON.parse(localStorage.getItem("profissionais")) || [];

gerarCodigo();

sincronizarPainel();

window.onload = preencherPainel; 
//preencherPainel();

/* ============================================================
   UTILITÁRIOS
   ============================================================ */

function mostrarAviso(msg) {
    const el = document.getElementById("aviso");
    el.textContent = msg;
    el.classList.add("visivel");
    setTimeout(() => el.classList.remove("visivel"), 2500);
}

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
   TELA 6: PAINEL
   ============================================================ */

function gerarCodigoAcesso() {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890";
    let codigo = "";
    for (let i = 0; i < 8; i++) {
        if (i === 4) codigo += "-";
        codigo += chars[Math.floor(Math.random() * chars.length)];
    }
    return codigo;
}

function gerarCodigo() {
    codigoAcesso = gerarCodigoAcesso();
    localStorage.setItem("codigoAcesso", codigoAcesso);
    document.getElementById("codigo-acesso").textContent = codigoAcesso;
    mostrarAviso("Novo código gerado!");
}

function copiarCodigo() {
    if (!codigoAcesso) return;
    navigator.clipboard.writeText(codigoAcesso)
        .then(() => mostrarAviso("Código copiado!"))
        .catch(() => mostrarAviso("Não foi possível copiar automaticamente"));
}

function preencherPainel() {
    let emp = JSON.parse(localStorage.getItem("empresa"))
    
    if (!emp) return;

    document.getElementById("sidebar-nome-empresa").textContent = emp.nome;
    document.getElementById("perfil-nome").textContent = emp.nome;
    document.getElementById("perfil-categoria").textContent = emp.categoria;
    document.getElementById("perfil-cnpj").textContent = emp.cnpj;
    document.getElementById("perfil-expediente").textContent = `${emp.abertura} – ${emp.fechamento}`;
    document.getElementById("perfil-dias").textContent =
    emp.dias.length > 0 ? emp.dias.map(d => d.charAt(0).toUpperCase() + d.slice(1)).join(", ") : "Nenhum";
    document.getElementById("codigo-acesso").textContent = codigoAcesso;

    sincronizarPainel();
}

function sincronizarPainel() {
    // Serviços no painel
    const containerS = document.getElementById("lista-servicos-painel");
    if (servicos.length === 0) {
        containerS.innerHTML = `<p class="lista-vazia">Nenhum serviço cadastrado.</p>`;
    } else {
        containerS.innerHTML = servicos.map(s => `
            <div class="item-card" data-id="${s.id}">
                <div class="ordem-btns">
                    <button class="ordem-btn" onclick="moverItemPainel('servico', '${s.id}', -1)">▲</button>
                    <button class="ordem-btn" onclick="moverItemPainel('servico', '${s.id}', 1)">▼</button>
                </div>
                ${s.foto
                    ? `<img class="item-card__foto" src="${s.foto}" alt="${s.nome}">`
                    : `<div class="item-card__foto-placeholder">✂️</div>`
                }
                <div class="item-card__nome">${s.nome}</div>
                <div class="item-card__meta">
                    <span>${s.tempo} min</span>
                    <span>R$ ${s.preco.toFixed(2).replace(".", ",")}</span>
                </div>
                <div class="item-card__acoes">
                    <button onclick="editarServico('${s.id}')">Editar</button>
                    <button class="btn-remover" onclick="removerServico('${s.id}')">Remover</button>
                </div>
            </div>
        `).join("");
    }

    // Profissionais no painel
    const containerP = document.getElementById("lista-profissionais-painel");
    if (profissionais.length === 0) {
        containerP.innerHTML = `<p class="lista-vazia">Nenhum profissional cadastrado.</p>`;
    } else {
        containerP.innerHTML = profissionais.map(p => `
            <div class="item-card" data-id="${p.id}">
                <div class="ordem-btns">
                    <button class="ordem-btn" onclick="moverItemPainel('profissional', '${p.id}', -1)">▲</button>
                    <button class="ordem-btn" onclick="moverItemPainel('profissional', '${p.id}', 1)">▼</button>
                </div>
                ${p.foto
                    ? `<img class="item-card__foto" src="${p.foto}" alt="${p.nome}">`
                    : `<div class="item-card__foto-placeholder">👤</div>`
                }
                <div class="item-card__nome">${p.nome}</div>
                <div class="item-card__meta" style="justify-content:center">
                    <span>${p.cargo}</span>
                </div>
                <div class="item-card__acoes">
                    <button onclick="editarProfissional('${p.id}')">Editar</button>
                    <button class="btn-remover" onclick="removerProfissional('${p.id}')">Remover</button>
                </div>
            </div>
        `).join("");
    }
}

function moverItemPainel(tipo, id, direcao) {
    moverItem(tipo, id, direcao);
}

/* ============================================================
   SIDEBAR: TROCA DE ABA
   ============================================================ */

function mudarAba(event, qual) {
    document.querySelectorAll(".aba").forEach(a => a.classList.remove("ativa"));
    document.querySelectorAll(".sidebar__item").forEach(i => i.classList.remove("ativo"));
    document.getElementById(`aba-${qual}`).classList.add("ativa");
    event.currentTarget.classList.add("ativo");
}

/* ============================================================
   EDIÇÃO DA EMPRESA (modal)
   ============================================================ */

function editarEmpresa() {
    let emp = JSON.parse(localStorage.getItem("empresa"))
    document.getElementById("edit-emp-nome").value = emp.nome;
    document.getElementById("edit-emp-categoria").value = emp.categoria;
    document.getElementById("edit-emp-cnpj").value = emp.cnpj;
    document.getElementById("edit-emp-abertura").value = emp.abertura;
    document.getElementById("edit-emp-fechamento").value = emp.fechamento;
    document.getElementById("edit-emp-fechamento").value = emp.dias;

    document.getElementById("modal-empresa").hidden = false;
    document.getElementById("modal-overlay").hidden = false;
}

function fecharModalEmpresa() {
    document.getElementById("modal-empresa").hidden = true;
    document.getElementById("modal-overlay").hidden = true;
}

function salvarEdicaoEmpresa() {
    const nome = document.getElementById("edit-emp-nome").value.trim();
    const categoria = document.getElementById("edit-emp-categoria").value;
    const cnpj = document.getElementById("edit-emp-cnpj").value.trim();
    const abertura = document.getElementById("edit-emp-abertura").value;
    const fechamento = document.getElementById("edit-emp-fechamento").value;

    if (!nome) { mostrarAviso("Informe o nome da empresa"); return; }

    const empresa = {
        nome,
        categoria,
        cnpj,
        abertura,
        fechamento
    }

    localStorage.setItem("empresa", JSON.stringify(empresa));
    preencherPainel();
    fecharModalEmpresa();
    mostrarAviso("Dados da empresa atualizados!");
}

/* ============================================================
   SERVIÇOS NO PAINEL (formulário)
   ============================================================ */

function abrirFormServico() {
    document.getElementById("form-servico-painel").hidden = false;
}

function fecharFormServico() {
    document.getElementById("form-servico-painel").hidden = true;
    document.getElementById("psrv-nome").value = "";
    document.getElementById("psrv-preco").value = "";
    document.getElementById("psrv-tempo").value = "";
    document.getElementById("psrv-foto").value = "";
}

async function adicionarServicoPainel() {
    const nome = document.getElementById("psrv-nome").value.trim();
    const preco = parseFloat(document.getElementById("psrv-preco").value);
    const tempo = parseInt(document.getElementById("psrv-tempo").value);
    const fotoInput = document.getElementById("psrv-foto");

    if (!nome) { mostrarAviso("Informe o nome do serviço"); return; }
    if (isNaN(preco)) { mostrarAviso("Informe o preço"); return; }
    if (isNaN(tempo)) { mostrarAviso("Informe a duração"); return; }

    const foto = await lerArquivoBase64(fotoInput);
    
    const servico = {
        id: gerarIdUnico(),
        nome: nome,
        preco: preco,
        tempo: tempo,
        foto: foto
    }

    servicos.push(servico);

    localStorage.setItem("servicos", JSON.stringify(servicos));

    fecharFormServico();
    sincronizarPainel();
    mostrarAviso("Serviço adicionado!");
}

/* ============================================================
   PROFISSIONAIS NO PAINEL (formulário)
   ============================================================ */

function abrirFormProfissional() {
    document.getElementById("form-profissional-painel").hidden = false;
}

function fecharFormProfissional() {
    document.getElementById("form-profissional-painel").hidden = true;
    document.getElementById("ppro-nome").value = "";
    document.getElementById("ppro-cargo").value = "";
    document.getElementById("ppro-foto").value = "";
}

async function adicionarProfissionalPainel() {
    const nome = document.getElementById("ppro-nome").value.trim();
    const cargo = document.getElementById("ppro-cargo").value.trim();
    const fotoInput = document.getElementById("ppro-foto");

    if (!nome) { mostrarAviso("Informe o nome do profissional"); return; }
    if (!cargo) { mostrarAviso("Informe o cargo"); return; }

    const foto = await lerArquivoBase64(fotoInput);
    
    const profissional = {
        id: gerarIdUnico(),
        nome: nome,
        cargo: cargo,
        foto: foto
    }

    profissionais.push(profissional);

    localStorage.setItem("profissionais", JSON.stringify(profissionais));

    fecharFormProfissional();
    sincronizarPainel();
    mostrarAviso("Profissional adicionado!");
}

function moverItem(tipo, id, direcao) {
    const lista = tipo === "servico" ? servicos : profissionais;
    const idx = lista.findIndex(i => i.id === id);
    const novoIdx = idx + direcao;
    if (novoIdx < 0 || novoIdx >= lista.length) return;
    [lista[idx], lista[novoIdx]] = [lista[novoIdx], lista[idx]];
    if (tipo === "servico") {
        sincronizarPainel();
    } else {
        sincronizarPainel();
    }
}


function removerServico(id) {
    servicos = servicos.filter(s => s.id !== id);
    localStorage.setItem("servicos", JSON.stringify(servicos));
    sincronizarPainel();
}

function editarServico(id) {
    const s = servicos.find(s => s.id === id);
    if (!s) return;
    const novoNome = prompt("Nome do serviço:", s.nome);
    if (novoNome !== null && novoNome.trim()) s.nome = novoNome.trim();
    const novoPreco = prompt("Preço (R$):", s.preco);
    if (novoPreco !== null && !isNaN(parseFloat(novoPreco))) s.preco = parseFloat(novoPreco);
    const novoTempo = prompt("Duração (min):", s.tempo);
    if (novoTempo !== null && !isNaN(parseInt(novoTempo))) s.tempo = parseInt(novoTempo);
    localStorage.setItem("servicos", JSON.stringify(servicos));
    sincronizarPainel();
}

function removerProfissional(id) {
    profissionais = profissionais.filter(p => p.id !== id);
    localStorage.setItem("profissionais", JSON.stringify(profissionais));
    sincronizarPainel();
}

function editarProfissional(id) {
    const p = profissionais.find(p => p.id === id);
    if (!p) return;
    const novoNome = prompt("Nome do profissional:", p.nome);
    if (novoNome !== null && novoNome.trim()) p.nome = novoNome.trim();
    const novoCargo = prompt("Cargo:", p.cargo);
    if (novoCargo !== null && novoCargo.trim()) p.cargo = novoCargo.trim();
    localStorage.setItem("profissionais", JSON.stringify(profissionais));
    sincronizarPainel();
}

/* ============================================================
   SAIR
   ============================================================ */

function sair() {
    if (!confirm("Deseja sair do sistema?")) return;
    /*localStorage.removeItem("usuario");
    localStorage.removeItem("empresa");
    localStorage.removeItem("servicos");
    localStorage.removeItem("profissionais");
    localStorage.removeItem("codigoAcesso");*/
    window.location.href = "autenticacao.html"
}

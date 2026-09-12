/* ============================================================
   ESTADO SERVIÇOS
   ============================================================ */

let servicos = JSON.parse(localStorage.getItem("servicos")) || [];

renderizarCardsServicos("lista-cards-servicos", servicos, "vazia-servicos");
sincronizarPainel();

/* ============================================================
   UTILITÁRIOS
   ============================================================ */

function mostrarAviso(msg) {
    const el = document.getElementById("aviso");
    el.textContent = msg;
    el.classList.add("visivel");
    setTimeout(() => el.classList.remove("visivel"), 2500);
}

function irParaTela(id) {
    document.querySelectorAll(".tela").forEach(t => {
        t.classList.remove("ativa");
        t.hidden = true;
    });
    const tela = document.getElementById(id);
    tela.hidden = false;
    tela.classList.add("ativa");
    window.scrollTo({ top: 0, behavior: "smooth" });
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
   ABAS DE AUTH
   ============================================================ */

document.querySelectorAll(".auth-aba").forEach(aba => {
    aba.addEventListener("click", () => {
        document.querySelectorAll(".auth-aba").forEach(a => a.classList.remove("ativa"));
        aba.classList.add("ativa");

        const qual = aba.dataset.aba;
        document.getElementById("form-login").hidden = qual !== "login";
        document.getElementById("form-cadastro").hidden = qual !== "cadastro";
    });
});

/* ============================================================
   DIAS DE FUNCIONAMENTO
   ============================================================ */

document.querySelectorAll(".dia-btn").forEach(btn => {
    btn.addEventListener("click", () => btn.classList.toggle("ativo"));
});

/* ============================================================
   TELA 4: SERVIÇOS (cadastro)
   ============================================================ */

async function adicionarServico() {
    const nome = document.getElementById("srv-nome").value.trim();
    const preco = parseFloat(document.getElementById("srv-preco").value);
    const tempo = parseInt(document.getElementById("srv-tempo").value);
    const fotoInput = document.getElementById("srv-foto");

    if (!nome) { mostrarAviso("Informe o nome do serviço"); return; }
    if (isNaN(preco) || preco < 0) { mostrarAviso("Informe um preço válido"); return; }
    if (isNaN(tempo) || tempo < 5) { mostrarAviso("Informe uma duração válida"); return; }

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

    document.getElementById("srv-nome").value = "";
    document.getElementById("srv-preco").value = "";
    document.getElementById("srv-tempo").value = "";
    fotoInput.value = "";

    renderizarCardsServicos("lista-cards-servicos", servicos, "vazia-servicos");
}

function renderizarCardsServicos(containerId, lista, vaziaId) {
    const container = document.getElementById(containerId);
    const vaziaEl = vaziaId ? document.getElementById(vaziaId) : null;

    if (lista.length === 0) {
        container.innerHTML = "";
        if (vaziaEl) container.appendChild(vaziaEl);
        if (vaziaEl) vaziaEl.style.display = "block";
        return;
    }

    if (vaziaEl) vaziaEl.style.display = "none";

    container.innerHTML = lista.map((s, idx) => `
        <div class="item-card" data-id="${s.id}">
            <div class="ordem-btns">
                <button class="ordem-btn" onclick="moverItem('${s.id}', -1)" title="Subir">▲</button>
                <button class="ordem-btn" onclick="moverItem('${s.id}', 1)" title="Descer">▼</button>
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

function removerServico(id) {
    servicos = servicos.filter(s => s.id !== id);
    localStorage.setItem("servicos", JSON.stringify(servicos));
    renderizarCardsServicos("lista-cards-servicos", servicos, "vazia-servicos");
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
    renderizarCardsServicos("lista-cards-servicos", servicos, "vazia-servicos");
    sincronizarPainel();
}

function moverItem(id, direcao) {
    const lista = servicos;
    const idx = lista.findIndex(i => i.id === id);
    const novoIdx = idx + direcao;
    if (novoIdx < 0 || novoIdx >= lista.length) return;
    [lista[idx], lista[novoIdx]] = [lista[novoIdx], lista[idx]];
    localStorage.setItem("servicos", JSON.stringify(servicos));
    renderizarCardsServicos("lista-cards-servicos", servicos, "vazia-servicos");
    sincronizarPainel();
}

/*function moverItem(tipo, id, direcao) {
    const lista = tipo === "servico" ? servicos : profissionais;
    const idx = lista.findIndex(i => i.id === id);
    const novoIdx = idx + direcao;
    if (novoIdx < 0 || novoIdx >= lista.length) return;
    [lista[idx], lista[novoIdx]] = [lista[novoIdx], lista[idx]];
    if (tipo === "servico") {
        renderizarCardsServicos("lista-cards-servicos", app.servicos, "vazia-servicos");
        sincronizarPainel();
    } else {
        renderizarCardsProfissionais("lista-cards-profissionais", app.profissionais, "vazia-profissionais");
        sincronizarPainel();
    }
}*/

function sincronizarPainel() {
    const containerS = document.getElementById("lista-servicos-painel");
    
    if (!containerS) return;

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
}

function voltar() {
    window.location.href = "cadastroEmpresa.html"
}

function salvarServicos() {
    localStorage.setItem("servicos", JSON.stringify(servicos));
    window.location.href = "painelAdministrativo.html"
}
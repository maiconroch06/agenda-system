/* ============================================================
   ESTADO SERVIÇOS
   ============================================================ */

let barbers = JSON.parse(localStorage.getItem("barber")) || [];
console.log(barbers)

/* ============================================================
   ELEMENTOS
   ============================================================ */

const els = {

}

/* ============================================================
   UTILITÁRIOS
   ============================================================ */

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
   BARBEIROS (adicionar, renderizar, remover, editar, cadastrar)
   ============================================================ */

async function addBarber() {
    const nome = document.getElementById("pro-nome").value.trim();
    const cargo = document.getElementById("pro-cargo").value.trim();
    const fotoInput = document.getElementById("pro-foto");

    if (!nome) { mostrarAviso("Informe o nome do barbeiro"); return; }
    if (!cargo) { mostrarAviso("Informe o cargo do barbeiro"); return; }

    const foto = await lerArquivoBase64(fotoInput);
    const barber = { id: gerarIdUnico(), nome, cargo, foto };
    barbers.push(barber);

    document.getElementById("pro-nome").value = "";
    document.getElementById("pro-cargo").value = "";
    fotoInput.value = "";

    renderizarCardsProfissionais("lista-cards-profissionais", barbers, "vazia-profissionais");
}

function renderizarCardsProfissionais(containerId, lista, vaziaId) {
    const container = document.getElementById(containerId);
    const vaziaEl = vaziaId ? document.getElementById(vaziaId) : null;

    if (lista.length === 0) {
        container.innerHTML = "";
        if (vaziaEl) container.appendChild(vaziaEl);
        if (vaziaEl) vaziaEl.style.display = "block";
        return;
    }

    if (vaziaEl) vaziaEl.style.display = "none";

    container.innerHTML = lista.map((p, idx) => `
        <div class="item-card" data-id="${p.id}">
            <div class="ordem-btns">
                <button class="ordem-btn" onclick="moverItem('barber', '${p.id}', -1)" title="Subir">▲</button>
                <button class="ordem-btn" onclick="moverItem('barber', '${p.id}', 1)" title="Descer">▼</button>
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

function removeBarber(id) {
    barbers = barbers.filter(p => p.id !== id);
    renderizarCardsProfissionais("lista-cards-profissionais", barbers, "vazia-profissionais");
    sincronizarPainel();
}

function editBarber(id) {
    const p = barbers.find(p => p.id === id);
    if (!p) return;
    const novoNome = prompt("Nome do barbeiro:", p.nome);
    if (novoNome !== null && novoNome.trim()) p.nome = novoNome.trim();
    const novoCargo = prompt("Cargo:", p.cargo);
    if (novoCargo !== null && novoCargo.trim()) p.cargo = novoCargo.trim();
    renderizarCardsProfissionais("lista-cards-profissionais", barbers, "vazia-profissionais");
    sincronizarPainel();
}

async function registerBarber() {
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

    barber = {
        foto: foto,
        telefone: tel,
        cargo: cargo,
        experiencia: exp
    }

    localStorage.setItem("barber", JSON.stringify(barber));
}
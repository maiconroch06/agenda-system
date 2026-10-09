/* ============================================================
   GESTOR PAINEL — BARBEIROS
   Requer gestor-painel-utilitarios.js carregado antes deste arquivo.
   ============================================================ */

/* ============================================================
   DADOS DA ABA DE BARBEIROS
   ============================================================ */

let barbeiroEmEdicaoId = null;

estado.abaAtual = "profissionais";

/* ============================================================
   MAPPING DOM
   ============================================================ */

Object.assign(els, {
    // Barbeiros
    formBarbeiroPainel: document.getElementById("form-barbeiro-painel"),
    // procura o ID do JS original e também o ID usado no barbeiros.html
    listaBarbeirosPainel: document.getElementById("lista-barbeiros-painel") || document.getElementById("lista-profissionais-painel"),
    pproNome: document.getElementById("ppro-nome"),
    pproCargo: document.getElementById("ppro-cargo"),
});

/* ============================================================
   ABA 4: PROFISSIONAIS (LÓGICA COMPLETA DE CADASTRO E RENDERIZAÇÃO)
   ============================================================ */

function renderizarBarbeiros() {
    if (!els.listaBarbeirosPainel) return;

    if (barbeiros.length === 0) {
        els.listaBarbeirosPainel.innerHTML = `<div class="col-span-full p-6 text-center text-xs text-[#888780] bg-[#232220] border border-[#38362f] rounded-2xl">Nenhum barbeiro cadastrado.</div>`;
        return;
    }

    els.listaBarbeirosPainel.innerHTML = barbeiros.map((p) => `
        <div class="relative flex flex-col items-center bg-white dark:bg-[#232220] rounded-2xl p-5 shadow-sm hover:shadow-md border border-zinc-100 dark:border-zinc-700/60 transition-all duration-200" data-id="${p.id}">
            <div class="absolute top-3 right-3 flex gap-1">
                <button class="w-7 h-7 flex items-center justify-center rounded-lg bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-700 dark:hover:bg-zinc-600 text-zinc-600 dark:text-zinc-300 text-xs transition-colors" onclick="moverItem('barber', '${p.id}', -1)" title="Subir">▲</button>
                <button class="w-7 h-7 flex items-center justify-center rounded-lg bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-700 dark:hover:bg-zinc-600 text-zinc-600 dark:text-zinc-300 text-xs transition-colors" onclick="moverItem('barber', '${p.id}', 1)" title="Descer">▼</button>
            </div>

            ${p.foto
                ? `<img class="w-20 h-20 rounded-full object-cover mb-3 border-2 border-amber-500 shadow-sm" src="${p.foto}" alt="${p.nome}">`
                : `<div class="w-20 h-20 rounded-full bg-zinc-100 dark:bg-zinc-700 border border-zinc-200 dark:border-zinc-600 flex items-center justify-center text-3xl mb-3 text-zinc-400">👤</div>`
            }

            <h3 class="font-bold text-zinc-800 dark:text-zinc-100 text-base mb-1 text-center">${p.nome}</h3>
            <p class="text-xs text-zinc-500 dark:text-zinc-400 text-center mb-3 line-clamp-2">${p.descricao || 'Sem descrição'}</p>

            <div class="flex flex-col gap-1 w-full text-xs text-zinc-500 dark:text-zinc-400 mb-4 bg-zinc-50 dark:bg-zinc-800/50 p-2.5 rounded-xl border border-zinc-100 dark:border-zinc-700/40">
                <span class="truncate"><strong>E-mail:</strong> ${p.email || '-'}</span>
                <span><strong>Tel:</strong> ${p.telefone || '-'}</span>
                ${p.endereco?.cidade ? `<span class="truncate mt-1 border-t border-zinc-200 dark:border-zinc-700 pt-1"><strong>End:</strong> ${p.endereco.cidade}-${p.endereco.uf}</span>` : ''}
            </div>

            <div class="flex gap-2 w-full mt-auto pt-3 border-t border-zinc-100 dark:border-zinc-700/50">
                <button onclick="editBarber('${p.id}')"   class="flex-1 py-1.5 px-3 rounded-lg border border-[#38362f] bg-transparent text-[#888780] hover:bg-[#2a2825] hover:text-[#f1efe8] text-xs font-medium transition-colors cursor-pointer text-center">Editar</button>
                <button onclick="removeBarber('${p.id}')" class="flex-1 py-1.5 px-3 rounded-lg border border-[#38362f] bg-transparent text-[#888780] hover:bg-[#2a2825] hover:text-[#f1efe8] text-xs font-medium transition-colors cursor-pointer text-center">Remover</button>
            </div>
        </div>
    `).join("");
}

function abrirFormBarbeiro() {
    if (els.formBarbeiroPainel) els.formBarbeiroPainel.classList.remove("hidden");
}

function fecharFormBarbeiro() {
    barbeiroEmEdicaoId = null;
    if (els.formBarbeiroPainel) els.formBarbeiroPainel.classList.add("hidden");
    if (els.pproNome) els.pproNome.value = "";
    if (els.pproCargo) els.pproCargo.value = "";
}

function editarBarbeiro(id) {
    const p = barbeiros.find(item => item.id === id);
    if (!p) return;
    barbeiroEmEdicaoId = id;
    if (els.pproNome) els.pproNome.value = p.nome;
    if (els.pproCargo) els.pproCargo.value = p.cargo;
    abrirFormBarbeiro();
}

function adicionarBarbeiroPainel() {
    const nome = els.pproNome ? els.pproNome.value.trim() : "";
    const cargo = els.pproCargo ? els.pproCargo.value.trim() : "";

    if (!nome) {
        mostrarAviso("Digite o nome do barbeiro.");
        return;
    }

    if (barbeiroEmEdicaoId) {
        const index = barbeiros.findIndex(p => p.id === barbeiroEmEdicaoId);
        if (index !== -1) {
            barbeiros[index] = { ...barbeiros[index], nome, cargo: cargo || "Barbeiro" };
        }
        mostrarAviso("Barbeiro atualizado com sucesso!");
    } else {
        const novoBarbeiro = {
            id: "p_" + Date.now(),
            nome,
            cargo: cargo || "Barbeiro"
        };
        barbeiros.push(novoBarbeiro);
        mostrarAviso("Barbeiro cadastrado com sucesso!");
    }

    salvarBarbeiros();
    popularFiltroBarbeiros();
    renderizarBarbeiros();
    fecharFormBarbeiro();
}

function excluirBarbeiro(id) {
    if (!confirm("Tem certeza que deseja remover este barbeiro?")) return;
    barbeiros = barbeiros.filter(p => p.id !== id);
    salvarBarbeiros();
    popularFiltroBarbeiros();
    renderizarBarbeiros();
    mostrarAviso("Barbeiro removido com sucesso.");
}

/* ============================================================
   INICIALIZAÇÃO
   ============================================================ */

function iniciar() {
    renderizarBarbeiros();

    if (els.bloqData) els.bloqData.value = hojeISO();
}

iniciar();

/* ============================================================
   GESTOR PAINEL — SERVIÇOS
   Requer gestor-painel-utilitarios.js carregado antes deste arquivo.
   ============================================================ */

/* ============================================================
   DADOS DA ABA DE SERVIÇOS
   ============================================================ */

const SERVICOS_PADRAO = [
    { id: "s1", nome: "Corte Social", duracao: 30, preco: 45, ativo: true },
    { id: "s2", nome: "Degradê", duracao: 40, preco: 50, ativo: true },
    { id: "s3", nome: "Degradê & Barba", duracao: 60, preco: 70, ativo: true }
];

let servicosManager = carregarDoStorage("servicos_manager", SERVICOS_PADRAO);

let servicoEmEdicaoId = null;

function salvarServicos() { salvarNoStorage("servicos_manager", servicosManager); }

estado.abaAtual = "servicos";

/* ============================================================
   MAPPING DOM
   ============================================================ */

Object.assign(els, {
    // Serviços
    formServicoPainel: document.getElementById("form-servico-painel"),
    listaServicosPainel: document.getElementById("lista-servicos-painel"),
    psrvNome: document.getElementById("psrv-nome"),
    psrvPreco: document.getElementById("psrv-preco"),
    psrvTempo: document.getElementById("psrv-tempo"),
});

/* ============================================================
   ABA 3: SERVIÇOS (LÓGICA COMPLETA DE CADASTRO E RENDERIZAÇÃO)
   ============================================================ */

function renderizarServicos() {
    if (!els.listaServicosPainel) return;

    if (servicosManager.length === 0) {
        els.listaServicosPainel.innerHTML = `<div class="col-span-full p-6 text-center text-xs text-[#888780] bg-[#232220] border border-[#38362f] rounded-2xl">Nenhum serviço cadastrado.</div>`;
        return;
    }

    els.listaServicosPainel.innerHTML = servicosManager.map((s) => `
        <div class="bg-white dark:bg-[#232220] rounded-2xl p-5 shadow-sm hover:shadow-md border border-zinc-100 dark:border-zinc-700/60 transition-all duration-200" data-id="${s.id}">
            <div class="relative flex flex-col items-center">
                <div class="absolute top-3 right-3 flex gap-1">
                    <button class="w-7 h-7 flex items-center justify-center rounded-lg bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-700 dark:hover:bg-zinc-600 text-zinc-600 dark:text-zinc-300 text-xs transition-colors" onclick="moverItem('barber', '${s.id}', -1)" title="Subir">▲</button>
                    <button class="w-7 h-7 flex items-center justify-center rounded-lg bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-700 dark:hover:bg-zinc-600 text-zinc-600 dark:text-zinc-300 text-xs transition-colors" onclick="moverItem('barber', '${s.id}', 1)" title="Descer">▼</button>
                </div>

                ${s.foto
                    ? `<img class="w-20 h-20 rounded-full object-cover mb-3 border-2 border-amber-500 shadow-sm" src="${s.foto}" alt="${s.nome}">`
                    : `<div class="w-20 h-20 rounded-full bg-zinc-100 dark:bg-zinc-700 border border-zinc-200 dark:border-zinc-600 flex items-center justify-center text-3xl mb-3 text-zinc-400">✂</div>`
                }

                <h3 class="font-bold text-zinc-800 dark:text-zinc-100 text-base mb-1 text-center">${s.nome}</h3>
                <p class="text-xs text-zinc-500 dark:text-zinc-400 text-center mb-3 line-clamp-2">${s.descricao || 'Sem descrição'}</p>
            </div>
            <div class="grid grid-cols-2 gap-2 mt-4 pt-3 border-t border-[#38362f]">
                <button onclick="editarServico('${s.id}')"  class="py-1.5 rounded-lg border border-[#38362f] bg-transparent text-[#888780] hover:bg-[#2a2825] hover:text-[#f1efe8] text-xs font-medium transition-colors cursor-pointer text-center">Editar</button>
                <button onclick="excluirServico('${s.id}')" class="py-1.5 rounded-lg border border-[#38362f] bg-transparent text-[#888780] hover:bg-[#2a2825] hover:text-[#f1efe8] text-xs font-medium transition-colors cursor-pointer text-center">Remover</button>
            </div>
        </div>
    `).join("");
}

function abrirFormServico() {
    if (els.formServicoPainel) els.formServicoPainel.classList.remove("hidden");
}

function fecharFormServico() {
    servicoEmEdicaoId = null;
    if (els.formServicoPainel) els.formServicoPainel.classList.add("hidden");
    if (els.psrvNome) els.psrvNome.value = "";
    if (els.psrvPreco) els.psrvPreco.value = "";
    if (els.psrvTempo) els.psrvTempo.value = "";
}

function editarServico(id) {
    const s = servicosManager.find(item => item.id === id);
    if (!s) return;
    servicoEmEdicaoId = id;
    if (els.psrvNome) els.psrvNome.value = s.nome;
    if (els.psrvPreco) els.psrvPreco.value = s.preco;
    if (els.psrvTempo) els.psrvTempo.value = s.duracao;
    abrirFormServico();
}

function adicionarServicoPainel() {
    const nome = els.psrvNome ? els.psrvNome.value.trim() : "";
    const preco = els.psrvPreco ? parseFloat(els.psrvPreco.value) : 0;
    const duracao = els.psrvTempo ? parseInt(els.psrvTempo.value) : 0;

    if (!nome || isNaN(preco) || isNaN(duracao) || preco <= 0 || duracao <= 0) {
        mostrarAviso("Preencha todos os campos do serviço corretamente.");
        return;
    }

    if (servicoEmEdicaoId) {
        const index = servicosManager.findIndex(s => s.id === servicoEmEdicaoId);
        if (index !== -1) {
            servicosManager[index] = { ...servicosManager[index], nome, preco, duracao };
        }
        mostrarAviso("Serviço atualizado com sucesso!");
    } else {
        const novoServico = {
            id: "s_" + Date.now(),
            nome,
            preco,
            duracao,
            ativo: true
        };
        servicosManager.push(novoServico);
        mostrarAviso("Serviço adicionado com sucesso!");
    }

    salvarServicos();
    renderizarServicos();
    fecharFormServico();
}

function excluirServico(id) {
    if (!confirm("Tem certeza que deseja excluir este serviço?")) return;
    servicosManager = servicosManager.filter(s => s.id !== id);
    salvarServicos();
    renderizarServicos();
    mostrarAviso("Serviço excluído com sucesso.");
}

/* ============================================================
   INICIALIZAÇÃO
   ============================================================ */

function iniciar() {
    renderizarServicos();

    if (els.bloqData) els.bloqData.value = hojeISO();
}

iniciar();

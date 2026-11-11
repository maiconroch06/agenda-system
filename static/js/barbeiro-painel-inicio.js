/* ============================================================
   ELEMENTOS CENTRALIZADOS (DOM)
   ============================================================ */

const els = {
    aviso: document.getElementById("aviso"),

    // KPI's & Aba Início
    progressoTexto: document.getElementById("progresso-texto"),
    progressoFill: document.getElementById("progresso-fill"),
    progressoCancelados: document.getElementById("progresso-cancelados"),
    progressoPendentes: document.getElementById("progresso-pendente"),
    listaInicioHoje: document.getElementById("lista-inicio-hoje"),

    // Modal: Detalhes do Atendimento
    detalheStatusBadge: document.getElementById("detalhe-status-badge"),
    detalheCliente: document.getElementById("detalhe-cliente"),
    detalheServico: document.getElementById("detalhe-servico"),
    detalheHorario: document.getElementById("detalhe-horario"),
    detalheValor: document.getElementById("detalhe-valor"),
    detalheTelefone: document.getElementById("detalhe-telefone"),
    detalheObs: document.getElementById("detalhe-obs"),
    detalheAcoes: document.getElementById("detalhe-acoes"),
    overlayDetalhe: document.getElementById("overlay-detalhe"),
    modalDetalhe: document.getElementById("modal-detalhe"),
};

/* ============================================================
   TOAST AVISOS
   ============================================================ */

function mostrarAviso(msg) {
    if (!els.aviso) return;
    els.aviso.textContent = msg;
    els.aviso.classList.remove("opacity-0", "translate-y-2.5", "pointer-events-none");
    els.aviso.classList.add("opacity-100", "translate-y-0");
    setTimeout(() => {
        els.aviso.classList.remove("opacity-100", "translate-y-0");
        els.aviso.classList.add("opacity-0", "translate-y-2.5", "pointer-events-none");
    }, 2500);
}

/* ============================================================
   CARD DE AGENDAMENTO
   ============================================================ */

function badgeStatusHTML(status) {
    const mapa = { agendado: "Agendado", concluido: "Concluído", cancelado: "Cancelado" };
    const classes = {
        agendado: "bg-[#3d2e05] text-[#f0c05a] border-[#7a5c0a]",
        concluido: "bg-[#085041] text-[#9fe1cb] border-[#0f6e56]",
        cancelado: "bg-[#3a1510] text-[#f0997b] border-[#993c1d]"
    };
    return `<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${classes[status] || ''}">${mapa[status]}</span>`;
}

function cardAgendamentoHTML(item) {
    const concluidoClasse = item.status === "concluido" ? " opacity-65" : "";
    
    return `
        <div class="bg-[#232220] border border-[#38362f] rounded-2xl p-3.5 flex gap-3 items-start cursor-pointer transition-colors hover:border-[#4a473f]${concluidoClasse}" onclick="abrirModalDetalhe('${item.id}')">
            <div class="min-w-[44px] text-center text-sm font-semibold leading-tight text-[#f1efe8]">${item.hora}</div>

            <div class="flex-1">
                <div class="text-sm font-medium">${item.cliente}</div>
                <div class="text-xs text-[#888780] mt-0.5">${item.servico}</div>
            </div>

            <div class="flex flex-col items-end gap-1 flex-shrink-0">
                ${badgeStatusHTML(item.status)}
                <div class="text-xs font-medium">Total: ${formatarMoeda(item.valor)}</div>
            </div>
        </div>
    `;
}

/* ============================================================
   ABA INÍCIO
   ============================================================ */

function renderizarInicio() {
    const hoje = hojeISO();

    // Filtra os agendamentos do dia e aplica a ordenação por Status e Hora
    const doDia = agendamentos
        .filter(a => a.data === hoje)
        .sort((a, b) => {
            // Define o peso (prioridade) de cada status
            const pesoStatus = { agendado: 1, concluido: 2, cancelado: 3 };
            
            // 1º Critério: Ordena pelo peso do status
            if (pesoStatus[a.status] !== pesoStatus[b.status]) {
                return pesoStatus[a.status] - pesoStatus[b.status];
            }
            
            // 2º Critério: Se o status for igual, ordena pela hora mais próxima (crescente)
            return a.hora.localeCompare(b.hora);
        });

    // Calcula os indicadores de progresso
    const concluidos = doDia.filter(a => a.status === "concluido").length;
    const cancelados = doDia.filter(a => a.status === "cancelado").length;
    const pendentes = doDia.filter(a => a.status === "agendado").length;
    
    const totalGeral = doDia.length;
    const totalValidos = totalGeral - cancelados;

    // Atualiza os textos e barras de progresso na tela
    if (els.progressoTexto) {
        els.progressoTexto.textContent = `${concluidos} de ${totalValidos} concluídos`;
    }

    const pctConcluidos = totalGeral ? (concluidos / totalGeral) * 100 : 0;
    const pctCancelados = totalGeral ? (cancelados / totalGeral) * 100 : 0;
    const pctPendentes = totalGeral ? (pendentes / totalGeral) * 100 : 0;

    if (els.progressoFill) els.progressoFill.style.width = `${pctConcluidos}%`;
    if (els.progressoCancelados) els.progressoCancelados.style.width = `${pctCancelados}%`;
    if (els.progressoPendentes) els.progressoPendentes.style.width = `${pctPendentes}%`;

    // Renderização dos cards da lista
    if (els.listaInicioHoje) {
        els.listaInicioHoje.innerHTML = totalGeral === 0
            ? `<p class="text-center text-[#888780] text-sm py-8 italic">Nenhum atendimento agendado para hoje.</p>`
            : doDia.map(cardAgendamentoHTML).join("");
    }
}

/* ============================================================
   MODAL: DETALHES DO ATENDIMENTO
   ============================================================ */

function abrirModalDetalhe(id) {
    const a = agendamentos.find(a => a.id === id);
    if (!a) return;

    els.detalheStatusBadge.innerHTML = badgeStatusHTML(a.status);
    els.detalheCliente.textContent = a.cliente;
    els.detalheServico.textContent = a.servico;
    els.detalheHorario.textContent = `${formatarDataExtenso(a.data)} às ${a.hora}`;
    els.detalheValor.textContent = formatarMoeda(a.valor);
    els.detalheTelefone.textContent = a.telefone;
    els.detalheObs.textContent = a.observacoes || "Nenhuma observação";

    let html = "";
    
    if (a.status === "agendado") {
        html += `<button class="w-full h-10 px-4 rounded-lg border border-[#0f6e56] bg-[#04342c] text-[#9fe1cb] font-semibold text-sm inline-flex items-center justify-center gap-2 cursor-pointer hover:opacity-85 transition-opacity" onclick="concluirAgendamento('${a.id}')">Concluir agendamento</button>`;
        html += `<button class="w-full h-10 px-4 rounded-lg border border-[#993c1d] bg-transparent text-[#f0997b] text-sm inline-flex items-center justify-center gap-2 cursor-pointer hover:bg-[#3a1510] transition-colors" onclick="cancelarAgendamento('${a.id}')">Cancelar</button>`;
    }
    if (a.status === "concluido") {
        html = `<p class="text-center text-[#888780] text-xs">Agendamento já concluído</p>`;
        html += `<button class="w-full h-11 px-5 rounded-lg bg-[#f1efe8] text-[#161513] font-semibold text-sm inline-flex items-center justify-center gap-2 cursor-pointer hover:opacity-90 active:scale-98 transition-all" onclick="resetarStatus('${a.id}')">Voltar status</button>`;
    }
    if (a.status === "cancelado") {
        html = `<p class="text-center text-[#888780] text-xs">Este agendamento foi cancelado</p>`;
        html += `<button class="w-full h-11 px-5 rounded-lg bg-[#f1efe8] text-[#161513] font-semibold text-sm inline-flex items-center justify-center gap-2 cursor-pointer hover:opacity-90 active:scale-98 transition-all" onclick="resetarStatus('${a.id}')">Voltar status</button>`;
    }
    
    els.detalheAcoes.innerHTML = html;

    els.overlayDetalhe.classList.remove("hidden");
    els.modalDetalhe.classList.remove("hidden");
}

function fecharModalDetalhe() {
    els.overlayDetalhe.classList.add("hidden");
    els.modalDetalhe.classList.add("hidden");
}

function concluirAtendimento(id) {
    atualizarStatus(id, "concluido");
    mostrarAviso("Atendimento concluído!");
}

function cancelarAtendimento(id) {
    if (!confirm("Deseja realmente cancelar este atendimento?")) return;
    atualizarStatus(id, "cancelado");
    mostrarAviso("Atendimento cancelado");
}

function atualizarStatus(id, novoStatus) {
    const a = agendamentos.find(a => a.id === id);
    if (a) a.status = novoStatus;
    
    fecharModalDetalhe();
    renderizarInicio();
}

/* ============================================================
   INICIALIZAÇÃO
   ============================================================ */

function iniciar() {
    localStorage.clear();

    renderizarInicio();
    
    if (typeof carregarData === "function") {
        carregarData();
    }
}

iniciar();
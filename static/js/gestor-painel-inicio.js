/* ============================================================
   GESTOR PAINEL — INÍCIO (dashboard de hoje)
   Requer gestor-painel-utilitarios.js carregado antes deste arquivo.
   Inclui também o Financeiro: o markup dele só existe no inicio.html.
   ============================================================ */

/* ============================================================
   MAPPING DOM
   ============================================================ */

Object.assign(els, {
    // KPIs & Cards Início
    kpiFaturamentoHoje: document.getElementById("kpi-faturamento-hoje"),
    kpiAtendimentosHoje: document.getElementById("kpi-atendimentos-hoje"),
    kpiOcupacaoHoje: document.getElementById("kpi-ocupacao-hoje"),
    kpiFaltasHoje: document.getElementById("kpi-faltas-hoje"),
    progressoTexto: document.getElementById("progresso-texto"),
    progressoFill: document.getElementById("progresso-fill"),
    progressoCancelados: document.getElementById("progresso-cancelados"),
    progressoPendentes: document.getElementById("progresso-pendente"),
    totalAgendamentosHoje: document.getElementById("total-agendamentos-hoje"),
    listaHojeCards: document.getElementById("lista-hoje-cards"),

    // Financeiro
    finReceitaMes: document.getElementById("fin-receita-mes"),
    finTotalCortes: document.getElementById("fin-total-cortes"),
    finTicketMedio: document.getElementById("fin-ticket-medio"),
    finMaisRealizado: document.getElementById("fin-mais-realizado"),
    finTabelaCorpo: document.getElementById("fin-tabela-corpo"),
});

/* ============================================================
   ABA INÍCIO — CARDS DE HOJE (CLICÁVEIS PARA DETALHES)
   ============================================================ */

function cardAtendimentoHojeHTML(item) {
    const concluidoClasse = item.status === "concluido" ? " opacity-65" : "";

    return `
        <div class="bg-[#232220] border border-[#38362f] rounded-2xl p-3.5 flex gap-3 items-start cursor-pointer transition-colors hover:border-[#4a473f]${concluidoClasse}" onclick="abrirModalDetalhe('${item.id}')">
            <div class="min-w-[44px] text-center text-sm font-semibold leading-tight text-[#f1efe8]">${item.hora}</div>

            <div class="flex-1">
                <div class="text-sm font-medium">${item.cliente}</div>
                <div class="text-xs text-[#888780] mt-0.5">${item.servico} • <span class="text-[#9fe1cb]">${item.barbeiro}</span></div>
            </div>

            <div class="flex flex-col items-end gap-1 flex-shrink-0">
                ${badgeStatusHTML(item.status)}
                <div class="text-xs font-medium">Total: ${formatarMoeda(item.valor)}</div>
            </div>

        </div>
    `;
}

function carregarDashboardInicio() {
    const hoje = hojeISO();

    const doDia = agendamentos.filter(a => a.data === hoje).sort((a, b) => (a.hora || "").localeCompare(b.hora || ""));

    // Cálculos de faturamento e contagens
    const faturamento = doDia
        .filter(a => a.status === "concluido" || a.status === "confirmado")
        .reduce((acc, a) => acc + Number(a.valor), 0);

    const concluidos = doDia.filter(a => a.status === "concluido").length;
    const cancelados = doDia.filter(a => a.status === "cancelado").length;
    const pendentes = doDia.filter(a => a.status === "agendado").length;
    const totalGeral = doDia.length;
    
    // Total válido decrementando os cancelados
    const totalValidos = totalGeral - cancelados;
    const ocupacao = totalValidos > 0 ? Math.round((concluidos / totalValidos) * 100) : 0;

    // Atualização dos KPIs principais
    if (els.kpiFaturamentoHoje) els.kpiFaturamentoHoje.textContent = formatarMoeda(faturamento);
    if (els.kpiAtendimentosHoje) els.kpiAtendimentosHoje.textContent = `${concluidos} / ${totalValidos}`;
    if (els.kpiOcupacaoHoje) els.kpiOcupacaoHoje.textContent = `${ocupacao}%`;
    if (els.kpiFaltasHoje) els.kpiFaltasHoje.textContent = cancelados;
    if (els.totalAgendamentosHoje) els.totalAgendamentosHoje.textContent = `${totalGeral} agendamentos`;

    // Atualização do texto e das barras de progresso (Verde e Vermelha)
    if (els.progressoTexto) {
        els.progressoTexto.textContent = `${concluidos} de ${totalValidos} concluídos`;
    }

    const pctConcluidos = totalGeral ? (concluidos / totalGeral) * 100 : 0;
    const pctCancelados = totalGeral ? (cancelados / totalGeral) * 100 : 0;
    const pctPendentes = totalGeral ? (pendentes / totalGeral) * 100 : 0;

    if (els.progressoFill) els.progressoFill.style.width = `${pctConcluidos}%`;
    if (els.progressoCancelados) els.progressoCancelados.style.width = `${pctCancelados}%`;
    if (els.progressoPendentes) els.progressoPendentes.style.width = `${pctPendentes}%`;

    // Renderização da lista de cards
    if (!els.listaHojeCards) return;

    if (totalGeral === 0) {
        els.listaHojeCards.innerHTML = `<div class="col-span-full p-8 text-center text-[#888780] bg-[#232220] border border-[#38362f] rounded-2xl">Nenhum agendamento para hoje.</div>`;
        return;
    }

    els.listaHojeCards.innerHTML = doDia.map(cardAtendimentoHojeHTML).join("");
}

/* ============================================================
   INICIALIZAÇÃO
   ============================================================ */

function iniciar() {
    localStorage.clear();
    
    carregarDashboardInicio();
    renderizarFinanceiro();

    // Utilitario
    carregarData();
    
    if (els.bloqData) els.bloqData.value = hojeISO();
}

iniciar();

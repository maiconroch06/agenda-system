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
    progressoFill: document.getElementById("progresso-fill"),
    progressoTexto: document.getElementById("progresso-texto"),
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
                <div class="text-xs text-[#888780] mt-0.5">${item.servico}</div>
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

    const doDia = agendamentos.filter(a => a.data === hoje).sort((a, b) => a.hora.localeCompare(b.hora));

    const faturamento = doDia
        .filter(a => a.status === "concluido" || a.status === "confirmado")
        .reduce((acc, a) => acc + Number(a.valor), 0);

    const concluidos = doDia.filter(a => a.status === "concluido").length;
    const total = doDia.length;
    const ocupacao = total > 0 ? Math.round((concluidos / total) * 100) : 0;
    const faltas = doDia.filter(a => a.status === "cancelado").length;

    if (els.kpiFaturamentoHoje) els.kpiFaturamentoHoje.textContent = formatarMoeda(faturamento);
    if (els.kpiAtendimentosHoje) els.kpiAtendimentosHoje.textContent = `${concluidos} / ${total}`;
    if (els.kpiOcupacaoHoje) els.kpiOcupacaoHoje.textContent = `${ocupacao}%`;
    if (els.kpiFaltasHoje) els.kpiFaltasHoje.textContent = faltas;
    if (els.totalAgendamentosHoje) els.totalAgendamentosHoje.textContent = `${total} agendamentos`;

    if (!els.listaHojeCards) return;

    if (doDia.length === 0) {
        els.listaHojeCards.innerHTML = `<div class="col-span-full p-8 text-center text-[#888780] bg-[#232220] border border-[#38362f] rounded-2xl">Nenhum agendamento para hoje.</div>`;
        return;
    }

    els.progressoFill.style.width = pct + "%";
    els.progressoTexto.textContent = `${concluidos.length} de ${total} concluídos`;

    els.listaHojeCards.innerHTML = doDia.map(cardAtendimentoHojeHTML).join("");

}

/* ============================================================
   ABA 6: FINANCEIRO (ESTATÍSTICAS E HISTÓRICO REAL)
   ============================================================ */

function renderizarFinanceiro() {
    const concluidos = agendamentos.filter(a => a.status === "concluido");

    const receitaTotal = concluidos.reduce((acc, a) => acc + Number(a.valor || 0), 0);
    const totalCortes = concluidos.length;
    const ticketMedio = totalCortes > 0 ? receitaTotal / totalCortes : 0;

    const contagemServicos = {};
    concluidos.forEach(a => {
        if (a.servico) {
            contagemServicos[a.servico] = (contagemServicos[a.servico] || 0) + 1;
        }
    });

    let maisRealizado = "—";
    let maxQtd = 0;
    for (const [srv, qtd] of Object.entries(contagemServicos)) {
        if (qtd > maxQtd) {
            maxQtd = qtd;
            maisRealizado = srv;
        }
    }

    if (els.finReceitaMes) els.finReceitaMes.textContent = formatarMoeda(receitaTotal);
    if (els.finTotalCortes) els.finTotalCortes.textContent = totalCortes;
    if (els.finTicketMedio) els.finTicketMedio.textContent = formatarMoeda(ticketMedio);
    if (els.finMaisRealizado) els.finMaisRealizado.textContent = maisRealizado;

    if (!els.finTabelaCorpo) return;

    if (agendamentos.length === 0) {
        els.finTabelaCorpo.innerHTML = `<tr><td colspan="6" class="p-6 text-center text-[#888780]">Nenhum atendimento registrado ainda.</td></tr>`;
        return;
    }

    const ordenados = [...agendamentos].sort((a, b) => (b.data + b.hora).localeCompare(a.data + a.hora));

    els.finTabelaCorpo.innerHTML = ordenados.map(a => `
        <tr class="border-b border-[#38362f] hover:bg-[#2a2825]/50 transition-colors">
            <td class="p-3 px-4 font-mono text-[#888780]">${a.data} ${a.hora}</td>
            <td class="p-3 px-4 font-medium">${a.cliente}</td>
            <td class="p-3 px-4 text-[#888780]">${a.servico}</td>
            <td class="p-3 px-4 text-[#888780]">${a.barbeiro || "Não atribuído"}</td>
            <td class="p-3 px-4 font-semibold text-[#f1efe8]">${formatarMoeda(a.valor)}</td>
            <td class="p-3 px-4">${badgeStatusHTML(a.status)}</td>
        </tr>
    `).join("");
}

/* ============================================================
   INICIALIZAÇÃO
   ============================================================ */

function iniciar() {
    carregarDashboardInicio();
    renderizarFinanceiro();

    // Utilitario
    carregarData();
    
    if (els.bloqData) els.bloqData.value = hojeISO();
}

iniciar();

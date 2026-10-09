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
        <div class="bg-[#232220] border border-[#38362f] rounded-2xl p-4 flex flex-col justify-between cursor-pointer hover:border-[#4a473f] transition-all hover:scale-[1.01] active:scale-[0.99]${concluidoClasse}" onclick="abrirModalDetalhe('${item.id}')">
            <div class="flex justify-between items-start mb-3">
                <div>
                    <span class="text-xs font-mono font-bold text-[#9fe1cb] bg-[#04342c] px-2 py-0.5 rounded-md border border-[#0f6e56]">${item.hora}</span>
                    <span class="text-xs text-[#888780] ml-2">Barbeiro: <strong class="text-[#f1efe8]">${item.barbeiro || "N/A"}</strong></span>
                </div>
                ${badgeStatusHTML(item.status)}
            </div>
            
            <div class="mb-3">
                <h3 class="text-sm font-semibold text-[#f1efe8]">${item.cliente}</h3>
                <p class="text-xs text-[#888780]">${item.servico}</p>
            </div>

            <div class="flex justify-between items-center border-t border-[#38362f] pt-2.5 mt-1">
                <span class="text-xs font-semibold text-[#f1efe8]">${formatarMoeda(item.valor)}</span>
                <span class="text-[11px] text-[#888780] flex items-center gap-1">Ver detalhes →</span>
            </div>
        </div>
    `;
}

function carregarDashboardInicio() {
    const hoje = hojeISO();
    const dataFormatted = new Date().toLocaleDateString("pt-BR", { weekday: "long", day: "2-digit", month: "long" });
    const elData = document.getElementById("data-atual-str");
    if (elData) elData.textContent = dataFormatted.charAt(0).toUpperCase() + dataFormatted.slice(1);

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

    if (els.bloqData) els.bloqData.value = hojeISO();
}

iniciar();

/* ============================================================
   ELEMENTOS CENTRALIZADOS (DOM)
   ============================================================ */

const els = {
    aviso: document.getElementById("aviso"),

    // Visões e Conteúdos da Agenda
    agendaVisaoDia: document.getElementById("agenda-visao-dia"),
    agendaVisaoSemana: document.getElementById("agenda-visao-semana"),
    agendaVisaoMes: document.getElementById("agenda-visao-mes"),
    listaAgendaDia: document.getElementById("lista-agenda-dia"),
    semanaScroll: document.getElementById("semana-scroll"),
    mesTitulo: document.getElementById("mes-titulo"),
    mesGrid: document.getElementById("mes-grid"),
    mesDiaSelecionadoTitulo: document.getElementById("mes-dia-selecionado-titulo"),
    listaMesDia: document.getElementById("lista-mes-dia"),

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

    // Modal: Bloqueio de Horários
    overlayBloquear: document.getElementById("overlay-bloquear"),
    modalBloquear: document.getElementById("modal-bloquear"),
    bloqData: document.getElementById("bloq-data"),
    bloqInicio: document.getElementById("bloq-inicio"),
    bloqFim: document.getElementById("bloq-fim"),
    bloqMotivo: document.getElementById("bloq-motivo"),

    // Modal Bloquear
    overlayFiltro: document.getElementById("overlay-filtro"),
    modalFiltro: document.getElementById("modal-filtro"),

    // Modal: Menu Mais
    overlayMais: document.getElementById("overlay-mais"),
    modalMais: document.getElementById("modal-mais"),

    abasFunc: () => document.querySelectorAll(".aba-func"),
    sidebarItems: () => document.querySelectorAll(".sidebar-func__item"),
    bottomNavItems: () => document.querySelectorAll(".bottom-nav__item"),
    filtroBtns: () => document.querySelectorAll(".filtro-btn"),

    getAba: (aba) => document.getElementById(`aba-${aba}`),
    getSidebarItem: (aba) => document.querySelector(`.sidebar-func__item[data-aba="${aba}"]`),
    getBottomNavItem: (aba) => document.querySelector(`.bottom-nav__item[data-aba="${aba}"]`),
    getFiltroBtn: (visao) => document.querySelector(`.filtro-btn[data-filtro="${visao}"]`)
};

/* ============================================================
   ESTADO DA TELA
   ============================================================ */

const estado = {
    abaAtual: "inicio",
    visaoAgenda: "dia",
    mesAtual: new Date(),
    diaSelecionadoMes: null,
    configTipo: null,
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
    const mapa = { aguardando: "Aguardando", confirmado: "Confirmado", concluido: "Concluído", cancelado: "Cancelado" };
    const classes = {
        aguardando: "bg-[#3d2e05] text-[#f0c05a] border-[#7a5c0a]",
        confirmado: "bg-[#0a2940] text-[#5ab4f0] border-[#1a5a8a]",
        concluido: "bg-[#085041] text-[#9fe1cb] border-[#0f6e56]",
        cancelado: "bg-[#3a1510] text-[#f0997b] border-[#993c1d]"
    };
    return `<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${classes[status] || ''}">${mapa[status]}</span>`;
}

function cardAgendamentoHTML(a) {
    const concluidoClasse = a.status === "concluido" ? " opacity-65" : "";
    return `
        <div class="bg-[#232220] border border-[#38362f] rounded-2xl p-3.5 flex gap-3 items-start cursor-pointer transition-colors hover:border-[#4a473f]${concluidoClasse}" onclick="abrirModalDetalhe('${a.id}')">
            <div class="min-w-[44px] text-center text-sm font-semibold leading-tight text-[#f1efe8]">${a.hora}</div>
            <div class="flex-1">
                <div class="text-sm font-medium">${a.cliente}</div>
                <div class="text-xs text-[#888780] mt-0.5">${a.servico}</div>
            </div>
            <div class="flex flex-col items-end gap-1 flex-shrink-0">
                ${badgeStatusHTML(a.status)}
                <div class="text-xs font-medium">${formatarMoeda(a.valor)}</div>
            </div>
        </div>
    `;
}

/* ============================================================
   ABA AGENDA
   ============================================================ */

function mudarVisaoAgenda(visao) {
    estado.visaoAgenda = visao;
    els.filtroBtns().forEach(b => {
        b.classList.remove("bg-[#f1efe8]", "text-[#161513]", "border-[#f1efe8]");
        b.classList.add("bg-transparent", "text-[#888780]", "border-[#4a473f]");
    });
    const activeBtn = els.getFiltroBtn(visao);
    if (activeBtn) {
        activeBtn.classList.add("bg-[#f1efe8]", "text-[#161513]", "border-[#f1efe8]");
        activeBtn.classList.remove("bg-transparent", "text-[#888780]", "border-[#4a473f]");
    }

    els.agendaVisaoDia.classList.toggle("hidden", visao !== "dia");
    els.agendaVisaoSemana.classList.toggle("hidden", visao !== "semana");
    els.agendaVisaoMes.classList.toggle("hidden", visao !== "mes");

    if (visao === "dia") renderizarAgendaDia();
    if (visao === "semana") renderizarAgendaSemana();
    if (visao === "mes") renderizarAgendaMes();
}

function renderizarAgendaDia() {
    const hoje = hojeISO();
    const doDia = agendamentos.filter(a => a.data === hoje).sort((a, b) => a.hora.localeCompare(b.hora));
    els.listaAgendaDia.innerHTML = doDia.length === 0
        ? `<p class="text-center text-[#888780] text-sm py-8 italic">Nenhum agendamento para hoje.</p>`
        : doDia.map(cardAgendamentoHTML).join("");
}

function renderizarAgendaSemana() {
    const nomesDias = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
    let html = "";

    for (let i = 0; i < 7; i++) {
        const d = new Date();
        d.setDate(d.getDate() + i);
        const iso = formatarISO(d);
        const ehHoje = iso === hojeISO();
        const doDia = agendamentos.filter(a => a.data === iso).sort((a, b) => a.hora.localeCompare(b.hora));

        const borderCol = ehHoje ? "border-[#0f6e56]" : "border-[#38362f]";
        const bgHead = ehHoje ? "bg-[#04342c]" : "bg-[#2a2825]";

        html += `
            <div class="flex-none w-[130px] bg-[#232220] border ${borderCol} rounded-lg overflow-hidden">
                <div class="p-2 text-center border-b border-[#38362f] ${bgHead}">
                    <div class="text-[11px] uppercase ${ehHoje ? 'text-[#9fe1cb]' : 'text-[#888780]'}">${nomesDias[d.getDay()]}</div>
                    <div class="text-lg font-semibold ${ehHoje ? 'text-[#9fe1cb]' : ''}">${d.getDate()}</div>
                </div>
                <div class="p-2 flex flex-col gap-1 min-h-[80px]">
                    ${doDia.length === 0
                        ? `<span class="text-[11px] text-[#6b6963] text-center pt-2">Livre</span>`
                        : doDia.map(a => `
                            <div class="bg-[#2a2825] rounded p-1.5 text-[11px] cursor-pointer border-l-2 border-l-[#0f6e56]" onclick="abrirModalDetalhe('${a.id}')">
                                <div class="text-[#888780] text-[10px]">${a.hora}</div>
                                <div class="font-medium truncate">${a.cliente}</div>
                            </div>
                        `).join("")
                    }
                </div>
            </div>
        `;
    }
    els.semanaScroll.innerHTML = html;
}

function renderizarAgendaMes() {
    const nomesMeses = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"];
    const ano = estado.mesAtual.getFullYear();
    const mes = estado.mesAtual.getMonth();

    els.mesTitulo.textContent = `${nomesMeses[mes]} ${ano}`;

    const primeiroDiaSemana = new Date(ano, mes, 1).getDay();
    const totalDiasMes = new Date(ano, mes + 1, 0).getDate();
    const totalDiasMesAnterior = new Date(ano, mes, 0).getDate();

    const labels = ["D", "S", "T", "Q", "Q", "S", "S"];
    let html = labels.map(l => `<div class="text-center text-[10px] text-[#888780] py-1 uppercase">${l}</div>`).join("");

    for (let i = primeiroDiaSemana - 1; i >= 0; i--) {
        html += `<button class="aspect-square flex flex-col items-center justify-center rounded-lg text-sm cursor-pointer border-none bg-transparent text-[#6b6963]" disabled>${totalDiasMesAnterior - i}</button>`;
    }

    for (let dia = 1; dia <= totalDiasMes; dia++) {
        const dataObj = new Date(ano, mes, dia);
        const iso = formatarISO(dataObj);
        const ehHoje = iso === hojeISO();
        const temAgendamento = agendamentos.some(a => a.data === iso);
        const classeHoje = ehHoje ? "bg-[#04342c] text-[#9fe1cb] font-semibold" : "text-[#f1efe8] hover:bg-[#232220]";

        html += `
            <button class="aspect-square flex flex-col items-center justify-center rounded-lg text-sm cursor-pointer relative border-none bg-transparent ${classeHoje}" onclick="selecionarDiaMes('${iso}')">
                ${dia}
                ${temAgendamento ? `<span class="absolute bottom-[3px] w-1.5 h-1.5 rounded-full bg-[#9fe1cb]"></span>` : ""}
            </button>
        `;
    }

    els.mesGrid.innerHTML = html;
    if (!estado.diaSelecionadoMes) estado.diaSelecionadoMes = hojeISO();
    selecionarDiaMes(estado.diaSelecionadoMes);
}

function mudarMes(delta) {
    estado.mesAtual.setMonth(estado.mesAtual.getMonth() + delta);
    renderizarAgendaMes();
}

function selecionarDiaMes(iso) {
    estado.diaSelecionadoMes = iso;
    const doDia = agendamentos.filter(a => a.data === iso).sort((a, b) => a.hora.localeCompare(b.hora));
    els.mesDiaSelecionadoTitulo.textContent = `Agendamentos — ${formatarDataExtenso(iso)}`;
    els.listaMesDia.innerHTML = doDia.length === 0
        ? `<p class="text-center text-[#888780] text-sm py-8 italic">Nenhum agendamento neste dia.</p>`
        : doDia.map(cardAgendamentoHTML).join("");
}

/* ============================================================
   INICIALIZAÇÃO
   ============================================================ */

function iniciar() {
    renderizarAgendaDia();
    if (els.bloqData) els.bloqData.value = hojeISO();

    // Na pasta utilitaria
    carregarData();

}

iniciar();
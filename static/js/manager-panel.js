/* ============================================================
   UTILITÁRIOS DE DATA E FORMATAÇÃO
   ============================================================ */

function formatarISO(data) {
    const y = data.getFullYear();
    const m = String(data.getMonth() + 1).padStart(2, "0");
    const d = String(data.getDate()).padStart(2, "0");
    return `${y}-${m}-${d}`;
}

function diasAPartirDeHoje(offset) {
    const d = new Date();
    d.setDate(d.getDate() + offset);
    return formatarISO(d);
}

function hojeISO() {
    return formatarISO(new Date());
}

function formatarDataExtenso(iso) {
    if (!iso) return "—";
    const d = new Date(iso + "T00:00:00");
    return d.toLocaleDateString("pt-BR", { weekday: "long", day: "2-digit", month: "long" });
}

function formatarMoeda(v) {
    return "R$ " + Number(v || 0).toFixed(2).replace(".", ",");
}

/* ============================================================
   PERSISTÊNCIA (localStorage)
   ============================================================ */

function carregarDoStorage(chave, valorPadrao) {
    try {
        const bruto = localStorage.getItem(chave);
        if (!bruto) return valorPadrao;
        return JSON.parse(bruto);
    } catch (erro) {
        return valorPadrao;
    }
}

function salvarNoStorage(chave, valor) {
    try {
        localStorage.setItem(chave, JSON.stringify(valor));
    } catch (erro) {
        console.warn(`Não foi possível salvar "${chave}".`, erro);
    }
}

/* ============================================================
   DADOS INICIAIS DA BARBEARIA
   ============================================================ */

const PROFISSIONAIS_PADRAO = [
    { id: "p1", nome: "Carlos Silva", cargo: "Barbeiro Master" },
    { id: "p2", nome: "Lucas Mendes", cargo: "Especialista em Barba" }
];

const AGENDAMENTOS_PADRAO = [
    { id: "a1", barbeiro: "Carlos Silva",  data: diasAPartirDeHoje(0), hora: "09:00", cliente: "Carlos Eduardo",  telefone: "(11) 98765-4321", servico: "Corte Social",       valor: 45, status: "concluido",  observacoes: "" },
    { id: "a2", barbeiro: "Lucas Mendes",  data: diasAPartirDeHoje(0), hora: "10:00", cliente: "Bruno Alves",      telefone: "(11) 91234-5678", servico: "Degradê & Barba",    valor: 70, status: "concluido",  observacoes: "Cliente prefere degradê baixo" },
    { id: "a3", barbeiro: "Carlos Silva",  data: diasAPartirDeHoje(0), hora: "11:30", cliente: "Rafael Souza",     telefone: "(11) 99887-6655", servico: "Barba",              valor: 35, status: "confirmado", observacoes: "" },
    { id: "a4", barbeiro: "Lucas Mendes",  data: diasAPartirDeHoje(0), hora: "14:00", cliente: "Diego Martins",    telefone: "(11) 98111-2233", servico: "Corte Infantil",      valor: 40, status: "aguardando", observacoes: "Primeira vez" },
    { id: "a5", barbeiro: "Carlos Silva",  data: diasAPartirDeHoje(0), hora: "15:30", cliente: "Felipe Costa",     telefone: "(11) 97222-3344", servico: "Corte Militar",       valor: 45, status: "aguardando", observacoes: "" },
    { id: "a6", barbeiro: "Lucas Mendes",  data: diasAPartirDeHoje(0), hora: "16:30", cliente: "Gustavo Lima",     telefone: "(11) 96333-4455", servico: "Social & Barba",      valor: 70, status: "cancelado",  observacoes: "Cliente cancelou" },
    { id: "a7", barbeiro: "Carlos Silva",  data: diasAPartirDeHoje(1), hora: "09:30", cliente: "Henrique Dias",    telefone: "(11) 95444-5566", servico: "Degradê",              valor: 50, status: "aguardando", observacoes: "" },
    { id: "a8", barbeiro: "Lucas Mendes",  data: diasAPartirDeHoje(1), hora: "13:00", cliente: "Igor Pereira",     telefone: "(11) 94555-6677", servico: "Corte Social",         valor: 45, status: "aguardando", observacoes: "" }
];

const SERVICOS_PADRAO = [
    { id: "s1", nome: "Corte Social", duracao: 30, preco: 45, ativo: true },
    { id: "s2", nome: "Degradê", duracao: 40, preco: 50, ativo: true },
    { id: "s3", nome: "Degradê & Barba", duracao: 60, preco: 70, ativo: true }
];

let profissionais = carregarDoStorage("profissionais_manager", PROFISSIONAIS_PADRAO);
let agendamentos = carregarDoStorage("agendamentos_manager", AGENDAMENTOS_PADRAO);
let servicosManager = carregarDoStorage("servicos_manager", SERVICOS_PADRAO);
let bloqueios = carregarDoStorage("bloqueios_manager", []);

let servicoEmEdicaoId = null;
let profissionalEmEdicaoId = null;

function salvarAgendamentos() { salvarNoStorage("agendamentos_manager", agendamentos); }
function salvarProfissionais() { salvarNoStorage("profissionais_manager", profissionais); }
function salvarServicos() { salvarNoStorage("servicos_manager", servicosManager); }
function salvarBloqueios() { salvarNoStorage("bloqueios_manager", bloqueios); }

/* ============================================================
   ESTADO GLOBAL DA TELA DO GESTOR
   ============================================================ */

const estado = {
    abaAtual: "inicio",
    visaoAgenda: "dia",
    barbeiroFiltro: "todos",
    mesAtual: new Date(),
    diaSelecionadoMes: null
};

/* ============================================================
   MAPPING DOM
   ============================================================ */

const els = {
    aviso: document.getElementById("aviso"),
    
    // KPIs & Cards Início
    kpiFaturamentoHoje: document.getElementById("kpi-faturamento-hoje"),
    kpiAtendimentosHoje: document.getElementById("kpi-atendimentos-hoje"),
    kpiOcupacaoHoje: document.getElementById("kpi-ocupacao-hoje"),
    kpiFaltasHoje: document.getElementById("kpi-faltas-hoje"),
    totalAgendamentosHoje: document.getElementById("total-agendamentos-hoje"),
    listaHojeCards: document.getElementById("lista-hoje-cards"),

    // Agenda
    filtroBarbeiroAgenda: document.getElementById("filtro-barbeiro-agenda"),
    agendaVisaoDia: document.getElementById("agenda-visao-dia"),
    agendaVisaoSemana: document.getElementById("agenda-visao-semana"),
    agendaVisaoMes: document.getElementById("agenda-visao-mes"),
    listaAgendaDia: document.getElementById("lista-agenda-dia"),
    semanaScroll: document.getElementById("semana-scroll"),
    mesTitulo: document.getElementById("mes-titulo"),
    mesGrid: document.getElementById("mes-grid"),
    mesDiaSelecionadoTitulo: document.getElementById("mes-dia-selecionado-titulo"),
    listaMesDia: document.getElementById("lista-mes-dia"),

    // Serviços
    formServicoPainel: document.getElementById("form-servico-painel"),
    listaServicosPainel: document.getElementById("lista-servicos-painel"),
    psrvNome: document.getElementById("psrv-nome"),
    psrvPreco: document.getElementById("psrv-preco"),
    psrvTempo: document.getElementById("psrv-tempo"),

    // Profissionais
    formProfissionalPainel: document.getElementById("form-profissional-painel"),
    listaProfissionaisPainel: document.getElementById("lista-profissionais-painel"),
    pproNome: document.getElementById("ppro-nome"),
    pproCargo: document.getElementById("ppro-cargo"),

    // Clientes
    buscaCliente: document.getElementById("busca-cliente"),
    tabelaClientesCorpo: document.getElementById("tabela-clientes-corpo"),

    // Financeiro
    finReceitaMes: document.getElementById("fin-receita-mes"),
    finTotalCortes: document.getElementById("fin-total-cortes"),
    finTicketMedio: document.getElementById("fin-ticket-medio"),
    finMaisRealizado: document.getElementById("fin-mais-realizado"),
    finTabelaCorpo: document.getElementById("fin-tabela-corpo"),

    // Modal Detalhes
    overlayDetalhe: document.getElementById("overlay-detalhe"),
    modalDetalhe: document.getElementById("modal-detalhe"),
    detalheStatusBadge: document.getElementById("detalhe-status-badge"),
    detalheBarbeiro: document.getElementById("detalhe-barbeiro"),
    detalheCliente: document.getElementById("detalhe-cliente"),
    detalheServico: document.getElementById("detalhe-servico"),
    detalheHorario: document.getElementById("detalhe-horario"),
    detalheValor: document.getElementById("detalhe-valor"),
    detalheTelefone: document.getElementById("detalhe-telefone"),
    detalheObs: document.getElementById("detalhe-obs"),
    detalheAcoes: document.getElementById("detalhe-acoes"),

    // Modal Bloquear
    overlayBloquear: document.getElementById("overlay-bloquear"),
    modalBloquear: document.getElementById("modal-bloquear"),
    bloqBarbeiro: document.getElementById("bloq-barbeiro"),
    bloqData: document.getElementById("bloq-data"),
    bloqInicio: document.getElementById("bloq-inicio"),
    bloqFim: document.getElementById("bloq-fim"),
    bloqMotivo: document.getElementById("bloq-motivo"),

    abasFunc: () => document.querySelectorAll(".aba-func"),
    sidebarItems: () => document.querySelectorAll(".sidebar-func__item"),
    bottomNavItems: () => document.querySelectorAll(".bottom-nav__item"),
    filtroBtns: () => document.querySelectorAll(".filtro-btn"),

    getAba: (aba) => document.getElementById(`aba-${aba}`),
    getFiltroBtn: (visao) => document.querySelector(`.filtro-btn[data-filtro="${visao}"]`)
};

/* ============================================================
   FEEDBACK & TOAST
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
   NAVEGAÇÃO ENTRE ABAS
   ============================================================ */

function irParaAba(aba) {
    els.abasFunc().forEach(el => el.classList.add("hidden"));
    const abaEl = els.getAba(aba);
    if (abaEl) abaEl.classList.remove("hidden");

    els.sidebarItems().forEach(btn => {
        if (btn.getAttribute("data-aba") === aba) {
            btn.className = "sidebar-func__item flex items-center gap-2.5 p-2.5 px-3 rounded-lg border-none bg-[#2a2825] text-[#f1efe8] font-medium text-sm cursor-pointer text-left w-full transition-colors";
        } else {
            btn.className = "sidebar-func__item flex items-center gap-2.5 p-2.5 px-3 rounded-lg border-none bg-transparent text-[#888780] font-medium text-sm cursor-pointer text-left w-full transition-colors hover:bg-[#2a2825] hover:text-[#f1efe8]";
        }
    });

    els.bottomNavItems().forEach(btn => {
        if (btn.getAttribute("data-aba") === aba) {
            btn.classList.remove("text-[#888780]");
            btn.classList.add("text-[#f1efe8]");
        } else {
            btn.classList.remove("text-[#f1efe8]");
            btn.classList.add("text-[#888780]");
        }
    });

    estado.abaAtual = aba;

    if (aba === "inicio") carregarDashboardInicio();
    else if (aba === "agenda") atualizarAgendaGeral();
    else if (aba === "servicos") renderizarServicos();
    else if (aba === "profissionais") renderizarProfissionais();
    else if (aba === "clientes") renderizarClientes();
    else if (aba === "financeiro") renderizarFinanceiro();

    window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ============================================================
   BADGES DE STATUS DEDICADOS
   ============================================================ */

function badgeStatusHTML(status) {
    const mapa = { aguardando: "Aguardando", confirmado: "Confirmado", concluido: "Concluido", cancelado: "Cancelado" };
    const classes = {
        aguardando: "bg-[#3d2e05] text-[#f0c05a] border-[#7a5c0a]",
        confirmado: "bg-[#0a2940] text-[#5ab4f0] border-[#1a5a8a]",
        concluido: "bg-[#085041] text-[#9fe1cb] border-[#0f6e56]",
        cancelado: "bg-[#3a1510] text-[#f0997b] border-[#993c1d]"
    };
    return `<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${classes[status] || ''}">${mapa[status] || status}</span>`;
}

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
   ABA AGENDA — VISÃO COMPLETA DE TODOS OS BARBEIROS
   ============================================================ */

function popularFiltroBarbeiros() {
    if (!els.filtroBarbeiroAgenda) return;
    let html = `<option value="todos">Todos os Barbeiros</option>`;
    let htmlModal = ``;
    
    profissionais.forEach(p => {
        html += `<option value="${p.nome}">${p.nome}</option>`;
        htmlModal += `<option value="${p.nome}">${p.nome}</option>`;
    });

    els.filtroBarbeiroAgenda.innerHTML = html;
    if (els.bloqBarbeiro) els.bloqBarbeiro.innerHTML = htmlModal;
}

function filtrarPorBarbeiro(nome) {
    estado.barbeiroFiltro = nome;
    atualizarAgendaGeral();
}

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

    atualizarAgendaGeral();
}

function atualizarAgendaGeral() {
    if (estado.visaoAgenda === "dia") renderizarAgendaDia();
    if (estado.visaoAgenda === "semana") renderizarAgendaSemana();
    if (estado.visaoAgenda === "mes") renderizarAgendaMes();
}

function obterAgendamentosFiltrados() {
    if (estado.barbeiroFiltro === "todos") return agendamentos;
    return agendamentos.filter(a => a.barbeiro === estado.barbeiroFiltro);
}

function cardAgendamentoHTML(a) {
    const concluidoClasse = a.status === "concluido" ? " opacity-65" : "";
    return `
        <div class="bg-[#232220] border border-[#38362f] rounded-2xl p-3.5 flex gap-3 items-start cursor-pointer transition-colors hover:border-[#4a473f]${concluidoClasse}" onclick="abrirModalDetalhe('${a.id}')">
            <div class="min-w-[44px] text-center text-sm font-semibold leading-tight text-[#f1efe8]">${a.hora}</div>
            <div class="flex-1">
                <div class="text-sm font-medium">${a.cliente}</div>
                <div class="text-xs text-[#888780] mt-0.5">${a.servico} • <span class="text-[#9fe1cb]">${a.barbeiro}</span></div>
            </div>
            <div class="flex flex-col items-end gap-1 flex-shrink-0">
                ${badgeStatusHTML(a.status)}
                <div class="text-xs font-medium">${formatarMoeda(a.valor)}</div>
            </div>
        </div>
    `;
}

function renderizarAgendaDia() {
    const hoje = hojeISO();
    const lista = obterAgendamentosFiltrados();
    const doDia = lista.filter(a => a.data === hoje).sort((a, b) => a.hora.localeCompare(b.hora));
    
    els.listaAgendaDia.innerHTML = doDia.length === 0
        ? `<p class="text-center text-[#888780] text-sm py-8 italic">Nenhum agendamento para hoje.</p>`
        : doDia.map(cardAgendamentoHTML).join("");
}

function renderizarAgendaSemana() {
    const nomesDias = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
    const lista = obterAgendamentosFiltrados();
    let html = "";

    for (let i = 0; i < 7; i++) {
        const d = new Date();
        d.setDate(d.getDate() + i);
        const iso = formatarISO(d);
        const ehHoje = iso === hojeISO();
        const doDia = lista.filter(a => a.data === iso).sort((a, b) => a.hora.localeCompare(b.hora));

        const borderCol = ehHoje ? "border-[#0f6e56]" : "border-[#38362f]";
        const bgHead = ehHoje ? "bg-[#04342c]" : "bg-[#2a2825]";

        html += `
            <div class="flex-none w-[140px] bg-[#232220] border ${borderCol} rounded-lg overflow-hidden">
                <div class="p-2 text-center border-b border-[#38362f] ${bgHead}">
                    <div class="text-[11px] uppercase ${ehHoje ? 'text-[#9fe1cb]' : 'text-[#888780]'}">${nomesDias[d.getDay()]}</div>
                    <div class="text-lg font-semibold ${ehHoje ? 'text-[#9fe1cb]' : ''}">${d.getDate()}</div>
                </div>
                <div class="p-2 flex flex-col gap-1 min-h-[80px]">
                    ${doDia.length === 0
                        ? `<span class="text-[11px] text-[#6b6963] text-center pt-2">Livre</span>`
                        : doDia.map(a => `
                            <div class="bg-[#2a2825] rounded p-1.5 text-[11px] cursor-pointer border-l-2 border-l-[#0f6e56]" onclick="abrirModalDetalhe('${a.id}')">
                                <div class="text-[#888780] text-[10px]">${a.hora} - ${a.barbeiro}</div>
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
    const lista = obterAgendamentosFiltrados();

    const labels = ["D", "S", "T", "Q", "Q", "S", "S"];
    let html = labels.map(l => `<div class="text-center text-[10px] text-[#888780] py-1 uppercase">${l}</div>`).join("");

    for (let i = primeiroDiaSemana - 1; i >= 0; i--) {
        html += `<button class="aspect-square flex flex-col items-center justify-center rounded-lg text-sm cursor-pointer border-none bg-transparent text-[#6b6963]" disabled>${totalDiasMesAnterior - i}</button>`;
    }

    for (let dia = 1; dia <= totalDiasMes; dia++) {
        const dataObj = new Date(ano, mes, dia);
        const iso = formatarISO(dataObj);
        const ehHoje = iso === hojeISO();
        const temAgendamento = lista.some(a => a.data === iso);
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
    const lista = obterAgendamentosFiltrados();
    const doDia = lista.filter(a => a.data === iso).sort((a, b) => a.hora.localeCompare(b.hora));
    els.mesDiaSelecionadoTitulo.textContent = `Agendamentos — ${formatarDataExtenso(iso)}`;
    els.listaMesDia.innerHTML = doDia.length === 0
        ? `<p class="text-center text-[#888780] text-sm py-8 italic">Nenhum agendamento neste dia.</p>`
        : doDia.map(cardAgendamentoHTML).join("");
}

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
                <button onclick="editarServico('${s.id}')" class="py-1.5 rounded-lg border border-[#38362f] bg-transparent text-[#888780] hover:bg-[#2a2825] hover:text-[#f1efe8] text-xs font-medium transition-colors cursor-pointer text-center">Editar</button>
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
   ABA 4: PROFISSIONAIS (LÓGICA COMPLETA DE CADASTRO E RENDERIZAÇÃO)
   ============================================================ */

function renderizarProfissionais() {
    if (!els.listaProfissionaisPainel) return;

    if (profissionais.length === 0) {
        els.listaProfissionaisPainel.innerHTML = `<div class="col-span-full p-6 text-center text-xs text-[#888780] bg-[#232220] border border-[#38362f] rounded-2xl">Nenhum profissional cadastrado.</div>`;
        return;
    }

    els.listaProfissionaisPainel.innerHTML = profissionais.map((p) => `
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
                <button class="flex-1 py-2 px-3 bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-700 dark:hover:bg-zinc-600 text-zinc-700 dark:text-zinc-200 text-xs font-semibold rounded-xl transition-colors" onclick="editBarber('${p.id}')">Editar</button>
                <button class="flex-1 py-2 px-3 bg-red-50 hover:bg-red-100 dark:bg-red-950/40 text-red-600 dark:text-red-400 text-xs font-semibold rounded-xl transition-colors" onclick="removeBarber('${p.id}')">Remover</button>
            </div>
        </div>
    `).join("");
}

function abrirFormProfissional() {
    if (els.formProfissionalPainel) els.formProfissionalPainel.classList.remove("hidden");
}

function fecharFormProfissional() {
    profissionalEmEdicaoId = null;
    if (els.formProfissionalPainel) els.formProfissionalPainel.classList.add("hidden");
    if (els.pproNome) els.pproNome.value = "";
    if (els.pproCargo) els.pproCargo.value = "";
}

function editarProfissional(id) {
    const p = profissionais.find(item => item.id === id);
    if (!p) return;
    profissionalEmEdicaoId = id;
    if (els.pproNome) els.pproNome.value = p.nome;
    if (els.pproCargo) els.pproCargo.value = p.cargo;
    abrirFormProfissional();
}

function adicionarProfissionalPainel() {
    const nome = els.pproNome ? els.pproNome.value.trim() : "";
    const cargo = els.pproCargo ? els.pproCargo.value.trim() : "";

    if (!nome) {
        mostrarAviso("Digite o nome do profissional.");
        return;
    }

    if (profissionalEmEdicaoId) {
        const index = profissionais.findIndex(p => p.id === profissionalEmEdicaoId);
        if (index !== -1) {
            profissionais[index] = { ...profissionais[index], nome, cargo: cargo || "Barbeiro" };
        }
        mostrarAviso("Profissional atualizado com sucesso!");
    } else {
        const novoProfissional = {
            id: "p_" + Date.now(),
            nome,
            cargo: cargo || "Barbeiro"
        };
        profissionais.push(novoProfissional);
        mostrarAviso("Profissional cadastrado com sucesso!");
    }

    salvarProfissionais();
    popularFiltroBarbeiros();
    renderizarProfissionais();
    fecharFormProfissional();
}

function excluirProfissional(id) {
    if (!confirm("Tem certeza que deseja remover este profissional?")) return;
    profissionais = profissionais.filter(p => p.id !== id);
    salvarProfissionais();
    popularFiltroBarbeiros();
    renderizarProfissionais();
    mostrarAviso("Profissional removido com sucesso.");
}

/* ============================================================
   ABA 5: CLIENTES (AGREGAÇÃO DE CLIENTES A PARTIR DE AGENDAMENTOS)
   ============================================================ */

function extrairClientes() {
    const mapaClientes = {};

    agendamentos.forEach(a => {
        if (!a.cliente) return;
        const chave = a.cliente.toLowerCase().trim();
        
        if (!mapaClientes[chave]) {
            mapaClientes[chave] = {
                nome: a.cliente,
                telefone: a.telefone || "Não informado",
                ultimaVisita: a.data,
                totalVisitas: 0,
                totalGasto: 0
            };
        }

        if (a.data > mapaClientes[chave].ultimaVisita) {
            mapaClientes[chave].ultimaVisita = a.data;
        }

        if (a.status === "concluido") {
            mapaClientes[chave].totalVisitas += 1;
            mapaClientes[chave].totalGasto += Number(a.valor || 0);
        }
    });

    return Object.values(mapaClientes);
}

function renderizarClientes(filtro = "") {
    if (!els.tabelaClientesCorpo) return;

    const clientes = extrairClientes();
    const termo = filtro.toLowerCase().trim();

    const filtrados = clientes.filter(c => 
        c.nome.toLowerCase().includes(termo) || 
        c.telefone.toLowerCase().includes(termo)
    );

    if (filtrados.length === 0) {
        els.tabelaClientesCorpo.innerHTML = `<tr><td colspan="5" class="p-6 text-center text-[#888780]">Nenhum cliente encontrado.</td></tr>`;
        return;
    }

    els.tabelaClientesCorpo.innerHTML = filtrados.map(c => `
        <tr class="border-b border-[#38362f] hover:bg-[#2a2825]/50 transition-colors">
            <td class="p-3.5 px-4 font-medium text-[#f1efe8]">${c.nome}</td>
            <td class="p-3.5 px-4 text-[#888780]">${c.telefone}</td>
            <td class="p-3.5 px-4 text-[#888780]">${formatarDataExtenso(c.ultimaVisita)}</td>
            <td class="p-3.5 px-4 font-medium">${c.totalVisitas} visita(s)</td>
            <td class="p-3.5 px-4 font-semibold text-[#9fe1cb]">${formatarMoeda(c.totalGasto)}</td>
        </tr>
    `).join("");
}

function filtrarClientes() {
    const valor = els.buscaCliente ? els.buscaCliente.value : "";
    renderizarClientes(valor);
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
   MODAL DETALHES DO ATENDIMENTO
   ============================================================ */

function abrirModalDetalhe(id) {
    const a = agendamentos.find(a => a.id === id);
    if (!a) return;

    els.detalheStatusBadge.innerHTML = badgeStatusHTML(a.status);
    if (els.detalheBarbeiro) els.detalheBarbeiro.textContent = a.barbeiro || "Não informado";
    els.detalheCliente.textContent = a.cliente;
    els.detalheServico.textContent = a.servico;
    els.detalheHorario.textContent = `${formatarDataExtenso(a.data)} às ${a.hora}`;
    els.detalheValor.textContent = formatarMoeda(a.valor);
    els.detalheTelefone.textContent = a.telefone;
    els.detalheObs.textContent = a.observacoes || "Nenhuma observação";

    let html = "";
    if (a.status === "aguardando") {
        html += `<button class="w-full h-10 px-4 rounded-lg border border-[#0f6e56] bg-[#04342c] text-[#9fe1cb] font-medium text-sm inline-flex items-center justify-center gap-2 cursor-pointer hover:opacity-85 transition-opacity" onclick="confirmarPresenca('${a.id}')">Confirmar presença</button>`;
    }
    if (a.status === "confirmado") {
        html += `<button class="w-full h-10 px-4 rounded-lg border border-[#0f6e56] bg-[#04342c] text-[#9fe1cb] font-medium text-sm inline-flex items-center justify-center gap-2 cursor-pointer hover:opacity-85 transition-opacity" onclick="iniciarAtendimento('${a.id}')">Iniciar atendimento</button>`;
    }
    if (a.status === "aguardando" || a.status === "confirmado") {
        html += `<button class="w-full h-11 px-5 rounded-lg bg-[#f1efe8] text-[#161513] font-semibold text-sm inline-flex items-center justify-center gap-2 cursor-pointer hover:opacity-90 active:scale-98 transition-all" onclick="concluirAtendimento('${a.id}')">Concluir atendimento</button>`;
        html += `<button class="w-full h-10 px-4 rounded-lg border border-[#993c1d] bg-transparent text-[#f0997b] text-sm inline-flex items-center justify-center gap-2 cursor-pointer hover:bg-[#3a1510] transition-colors" onclick="cancelarAtendimento('${a.id}')">Cancelar</button>`;
    }
    if (a.status === "concluido") {
        html = `<p class="text-center text-[#888780] text-xs">Atendimento já concluído</p>`;
    }
    if (a.status === "cancelado") {
        html = `<p class="text-center text-[#888780] text-xs">Este atendimento foi cancelado</p>`;
    }
    els.detalheAcoes.innerHTML = html;

    els.overlayDetalhe.classList.remove("hidden");
    els.modalDetalhe.classList.remove("hidden");
}

function fecharModalDetalhe() {
    els.overlayDetalhe.classList.add("hidden");
    els.modalDetalhe.classList.add("hidden");
}

function confirmarPresenca(id) { atualizarStatus(id, "confirmado"); mostrarAviso("Presença confirmada!"); }
function iniciarAtendimento(id) { mostrarAviso("Atendimento iniciado!"); fecharModalDetalhe(); }
function concluirAtendimento(id) { atualizarStatus(id, "concluido"); mostrarAviso("Atendimento concluído!"); }
function cancelarAtendimento(id) {
    if (!confirm("Deseja realmente cancelar este atendimento?")) return;
    atualizarStatus(id, "cancelado");
    mostrarAviso("Atendimento cancelado");
}

function atualizarStatus(id, novoStatus) {
    const a = agendamentos.find(a => a.id === id);
    if (a) a.status = novoStatus;
    salvarAgendamentos();
    fecharModalDetalhe();
    carregarDashboardInicio();
    atualizarAgendaGeral();
}

/* ============================================================
   MODAL BLOQUEAR HORÁRIO
   ============================================================ */

function abrirModalBloquear() {
    els.overlayBloquear.classList.remove("hidden");
    els.modalBloquear.classList.remove("hidden");
}

function fecharModalBloquear() {
    els.overlayBloquear.classList.add("hidden");
    els.modalBloquear.classList.add("hidden");
}

function confirmarBloqueio() {
    const barbeiro = els.bloqBarbeiro ? els.bloqBarbeiro.value : "";
    const data = els.bloqData.value;
    const inicio = els.bloqInicio.value;
    const fim = els.bloqFim.value;
    const motivo = els.bloqMotivo.value.trim();

    if (!data || !inicio || !fim || !barbeiro) { mostrarAviso("Preencha todos os campos do bloqueio"); return; }
    if (fim <= inicio) { mostrarAviso("O horário final deve ser maior que o inicial"); return; }

    bloqueios.push({ barbeiro, data, inicio, fim, motivo: motivo || "Horário bloqueado" });
    salvarBloqueios();
    mostrarAviso(`Horário bloqueado para ${barbeiro}!`);
    fecharModalBloquear();
}

function sairDaConta() {
    if (confirm("Deseja realmente sair do painel administrativo?")) {
        mostrarAviso("Saindo...");
    }
}

/* ============================================================
   INICIALIZAÇÃO
   ============================================================ */

function iniciar() {
    popularFiltroBarbeiros();
    carregarDashboardInicio();
    atualizarAgendaGeral();
    renderizarServicos();
    renderizarProfissionais();
    renderizarClientes();
    renderizarFinanceiro();

    if (els.bloqData) els.bloqData.value = hojeISO();
}

iniciar();
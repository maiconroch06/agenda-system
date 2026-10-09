/* ============================================================
   GESTOR PAINEL — UTILITÁRIOS COMPARTILHADOS
   Carregado em TODAS as telas do painel, antes do JS da própria tela.
   ============================================================ */

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

let barbeiros = carregarDoStorage("barbeiros_manager", PROFISSIONAIS_PADRAO);
let agendamentos = carregarDoStorage("agendamentos_manager", AGENDAMENTOS_PADRAO);
let bloqueios = carregarDoStorage("bloqueios_manager", []);

function salvarAgendamentos() { salvarNoStorage("agendamentos_manager", agendamentos); }
function salvarBarbeiros() { salvarNoStorage("barbeiros_manager", barbeiros); }
function salvarBloqueios() { salvarNoStorage("bloqueios_manager", bloqueios); }

/* ============================================================
   ESTADO GLOBAL DA TELA DO GESTOR
   ============================================================ */

const estado = {
    abaAtual: "inicio"
};

/* ============================================================
   MAPPING DOM
   ============================================================ */

const els = {
    aviso: document.getElementById("aviso"),
    
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

    getAba: (aba) => document.getElementById(`aba-${aba}`),
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

/* Cada aba agora é uma página própria (o sidebar foi componentizado).
   Ajuste as URLs abaixo para as rotas reais do seu backend. */
const ROTAS_ABAS = {
    inicio: "/gestor/painel/inicio",
    agenda: "/gestor/painel/agenda",
    servicos: "/gestor/painel/servicos",
    clientes: "/gestor/painel/clientes",
    profissionais: "/gestor/painel/barbeiros"
};

function irParaAba(aba) {
    // Se a aba pedida não é a desta página, vai para a página dela
    if (aba !== estado.abaAtual && ROTAS_ABAS[aba]) {
        window.location.href = ROTAS_ABAS[aba];
        return;
    }

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
    else if (aba === "barbeiros") renderizarBarbeiros();
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
   FILTRO DE BARBEIROS (Agenda e modal "Bloquear horário")
   Fica aqui porque a tela de Barbeiros também chama esta função.
   ============================================================ */

function popularFiltroBarbeiros() {
    if (!els.filtroBarbeiroAgenda) return;
    let html = `<option value="todos">Todos os Barbeiros</option>`;
    let htmlModal = ``;
    
    barbeiros.forEach(p => {
        html += `<option value="${p.nome}">${p.nome}</option>`;
        htmlModal += `<option value="${p.nome}">${p.nome}</option>`;
    });

    els.filtroBarbeiroAgenda.innerHTML = html;
    if (els.bloqBarbeiro) els.bloqBarbeiro.innerHTML = htmlModal;
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
    // Cada tela carrega só o seu JS: atualiza apenas o que existir nesta página
    if (typeof carregarDashboardInicio === "function") carregarDashboardInicio();
    if (typeof atualizarAgendaGeral === "function") atualizarAgendaGeral();
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

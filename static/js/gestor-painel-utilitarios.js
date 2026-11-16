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
   DADOS DA BARBEARIA (Injetados pelo Flask/Jinja via JSON)
   ============================================================ */

function lerDadosInjetados(idElemento) {
    try {
        const elemento = document.getElementById(idElemento);
        if (elemento) {
            return JSON.parse(elemento.textContent);
        }
    } catch (e) {
        console.error("Erro ao ler dados injetados:", e);
    }
    return null;
}

const DADOS_BARBEIROS_INJETADOS = lerDadosInjetados("dados-barbeiros-json");
const DADOS_AGENDAMENTOS_INJETADOS = lerDadosInjetados("dados-agendamentos-json");

let barbeiros = carregarDoStorage("barbeiros_manager", DADOS_BARBEIROS_INJETADOS || []);
let agendamentos = carregarDoStorage("agendamentos_manager", DADOS_AGENDAMENTOS_INJETADOS || []);
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

    // Modal Bloquear
    overlayBloquear: document.getElementById("overlay-bloquear"),
    modalBloquear: document.getElementById("modal-bloquear"),
    bloqBarbeiro: document.getElementById("bloq-barbeiro"),
    bloqData: document.getElementById("bloq-data"),
    bloqInicio: document.getElementById("bloq-inicio"),
    bloqFim: document.getElementById("bloq-fim"),
    bloqMotivo: document.getElementById("bloq-motivo"),

    // Modal Filtro
    overlayFiltro: document.getElementById("overlay-filtro"),
    modalFiltro: document.getElementById("modal-filtro"),

    // Modal: Menu Mais
    overlayMais: document.getElementById("overlay-mais"),
    modalMais: document.getElementById("modal-mais"),

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

const ROTAS_ABAS = {
    inicio: "/gestor/painel/",
    agenda: "/gestor/painel/agenda",
    servicos: "/gestor/painel/servicos",
    clientes: "/gestor/painel/clientes",
    profissionais: "/gestor/painel/barbeiros"
};

function irParaAba(aba) {
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

    if (aba === "inicio") if (typeof carregarDashboardInicio === "function") carregarDashboardInicio();
    else if (aba === "agenda") if (typeof atualizarAgendaGeral === "function") atualizarAgendaGeral();
    
    window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ============================================================
   BADGES DE STATUS DEDICADOS
   ============================================================ */

function badgeStatusHTML(status) {
    const mapa = { agendado: "Agendado", concluido: "Concluído", cancelado: "Cancelado" };
    const classes = {
        agendado: "bg-[#3d2e05] text-[#f0c05a] border-[#7a5c0a]",
        concluido: "bg-[#085041] text-[#9fe1cb] border-[#0f6e56]",
        cancelado: "bg-[#3a1510] text-[#f0997b] border-[#993c1d]"
    };
    return `<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${classes[status] || ''}">${mapa[status] || status}</span>`;
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

/* ============================================================
   MODAL FILTRAR AGENDA
   ============================================================ */

function abrirModalFiltro() {
    if (els.overlayFiltro && els.modalFiltro) {
        els.overlayFiltro.classList.remove("hidden");
        els.modalFiltro.classList.remove("hidden");
    }
}

function fecharModalFiltro() {
    if (els.overlayFiltro && els.modalFiltro) {
        els.overlayFiltro.classList.add("hidden");
        els.modalFiltro.classList.add("hidden");
    }
}

function confirmarFiltro() {
    fecharModalFiltro();
}

/* ============================================================
   MENU "MAIS" (mobile)
   ============================================================ */

function abrirMenuMais() {
    els.overlayMais.classList.remove("hidden");
    els.modalMais.classList.remove("hidden");
}

function fecharMenuMais() {
    els.overlayMais.classList.add("hidden");
    els.modalMais.classList.add("hidden");
}

function carregarData() {
    const dataFormatted = new Date().toLocaleDateString("pt-BR", { weekday: "long", day: "2-digit", month: "long" });
    const elData = document.getElementById("data-atual-str");
    if (elData) elData.textContent = dataFormatted.charAt(0).toUpperCase() + dataFormatted.slice(1);
}

carregarData();
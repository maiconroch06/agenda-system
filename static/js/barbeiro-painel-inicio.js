/* ============================================================
   UTILITÁRIOS DE DATA
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

function horaAtual() {
    const d = new Date();
    return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}

function formatarDataExtenso(iso) {
    const d = new Date(iso + "T00:00:00");
    return d.toLocaleDateString("pt-BR", { weekday: "long", day: "2-digit", month: "long" });
}

function formatarMoeda(v) {
    return "R$ " + v.toFixed(2).replace(".", ",");
}

/* ============================================================
   DADOS MOCK — AGENDAMENTOS
   ============================================================ */

const AGENDAMENTOS_PADRAO = [
    { id: "a1",  data: diasAPartirDeHoje(0), hora: "09:00", cliente: "Carlos Eduardo",  telefone: "(11) 98765-4321", servico: "Corte Social",       valor: 18, status: "concluido",  observacoes: "" },
    { id: "a2",  data: diasAPartirDeHoje(0), hora: "10:00", cliente: "Bruno Alves",      telefone: "(11) 91234-5678", servico: "Degradê & Barba",    valor: 30, status: "concluido",  observacoes: "Cliente prefere degradê baixo" },
    { id: "a3",  data: diasAPartirDeHoje(0), hora: "11:30", cliente: "Rafael Souza",     telefone: "(11) 99887-6655", servico: "Barba",              valor: 15, status: "confirmado", observacoes: "" },
    { id: "a4",  data: diasAPartirDeHoje(0), hora: "14:00", cliente: "Diego Martins",    telefone: "(11) 98111-2233", servico: "Corte Infantil",      valor: 20, status: "aguardando", observacoes: "Primeira vez, criança de 6 anos" },
    { id: "a5",  data: diasAPartirDeHoje(0), hora: "15:30", cliente: "Felipe Costa",     telefone: "(11) 97222-3344", servico: "Corte Militar",       valor: 15, status: "aguardando", observacoes: "" },
    { id: "a6",  data: diasAPartirDeHoje(0), hora: "16:30", cliente: "Gustavo Lima",     telefone: "(11) 96333-4455", servico: "Social & Barba",      valor: 30, status: "cancelado",  observacoes: "Cliente cancelou por telefone" },
    { id: "a7",  data: diasAPartirDeHoje(1), hora: "09:30", cliente: "Henrique Dias",    telefone: "(11) 95444-5566", servico: "Degradê",              valor: 22, status: "aguardando", observacoes: "" },
    { id: "a8",  data: diasAPartirDeHoje(1), hora: "13:00", cliente: "Igor Pereira",     telefone: "(11) 94555-6677", servico: "Corte Social",         valor: 18, status: "aguardando", observacoes: "" }
];

const agendamentos = carregarDoStorage("agendamentos", AGENDAMENTOS_PADRAO);

/* ============================================================
   DADOS DO FUNCIONÁRIO LOGADO
   ============================================================ */

const FUNCIONARIO_PADRAO = {
    nome: "Maicon",
    foto: null,
    empresa: "Barbearia do Zé",
    telefone: "(11) 98888-7777",
    descricao: "Barbeiro especializado em degradê e barboterapia.",
    comissaoPercentual: 50,
};

let funcionario = carregarDoStorage("profissional", FUNCIONARIO_PADRAO);

/* ============================================================
   SERVIÇOS
   ============================================================ */

const SERVICOS_PADRAO = [
    { id: "s1", nome: "Corte Social",       duracao: 30, preco: 18, ativo: true },
    { id: "s2", nome: "Degradê",            duracao: 40, preco: 22, ativo: true },
    { id: "s3", nome: "Degradê & Barba",    duracao: 60, preco: 30, ativo: true },
    { id: "s4", nome: "Social & Barba",     duracao: 50, preco: 30, ativo: true }
];

const servicosFunc = carregarDoStorage("servicosFunc", SERVICOS_PADRAO);
const bloqueios = carregarDoStorage("bloqueios", []);

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

function salvarFuncionario()   { salvarNoStorage("profissional", funcionario); }
function salvarAgendamentos()  { salvarNoStorage("agendamentos", agendamentos); }
function salvarServicos()      { salvarNoStorage("servicosFunc", servicosFunc); }
function salvarBloqueios()     { salvarNoStorage("bloqueios", bloqueios); }

/* ============================================================
   ELEMENTOS CENTRALIZADOS (DOM)
   ============================================================ */

const els = {
    aviso: document.getElementById("aviso"),

    // KPI's & Aba Início
    inicioNome: document.getElementById("inicio-primeiro-nome"),
    kpiTotalHoje: document.getElementById("kpi-total-hoje"),
    kpiTotalHojeSub: document.getElementById("kpi-total-hoje-sub"),
    kpiProximo: document.getElementById("kpi-proximo"),
    kpiProximoSub: document.getElementById("kpi-proximo-sub"),
    progressoFill: document.getElementById("progresso-fill"),
    progressoTexto: document.getElementById("progresso-texto"),
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

    // Modal: Bloqueio de Horários
    overlayBloquear: document.getElementById("overlay-bloquear"),
    modalBloquear: document.getElementById("modal-bloquear"),
    bloqData: document.getElementById("bloq-data"),
    bloqInicio: document.getElementById("bloq-inicio"),
    bloqFim: document.getElementById("bloq-fim"),
    bloqMotivo: document.getElementById("bloq-motivo"),

    // Serviços
    listaServicosFunc: document.getElementById("lista-servicos-func"),

    // Modal: Configurações
    overlayConfig: document.getElementById("overlay-config"),
    modalConfig: document.getElementById("modal-config"),
    configModalTitulo: document.getElementById("config-modal-titulo"),
    configCampoLabel: document.getElementById("config-campo-label"),
    configCampoTexto: document.getElementById("config-campo-texto"),
    configCampoTextarea: document.getElementById("config-campo-textarea"),
    configCampoSenha: document.getElementById("config-campo-senha"),
    configInput: document.getElementById("config-input"),
    configTextarea: document.getElementById("config-textarea"),
    configSenhaAtual: document.getElementById("config-senha-atual"),
    configSenhaNova: document.getElementById("config-senha-nova"),
    configTelefoneAtual: document.getElementById("config-telefone-atual"),
    toggleNotif: document.getElementById("toggle-notif"),
    toggleTema: document.getElementById("toggle-tema"),

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
   ABA INÍCIO
   ============================================================ */

function renderizarInicio() {
    if (els.inicioNome) els.inicioNome.textContent = funcionario.nome;
    const hoje = hojeISO();
    const doDia = agendamentos.filter(a => a.data === hoje).sort((a, b) => a.hora.localeCompare(b.hora));

    const concluidos = doDia.filter(a => a.status === "concluido");
    const pendentes = doDia.filter(a => a.status === "aguardando" || a.status === "confirmado");

    els.kpiTotalHoje.textContent = doDia.length;
    els.kpiTotalHojeSub.textContent = doDia.length === 0 ? "Nenhum agendamento" : `${concluidos.length} concluídos, ${pendentes.length} restantes`;

    const proximo = pendentes.find(a => a.hora >= horaAtual()) || pendentes[0];
    els.kpiProximo.textContent = proximo ? proximo.hora : "—";
    els.kpiProximoSub.textContent = proximo ? proximo.cliente : "Nenhum pendente";

    const total = doDia.length;
    const pct = total ? Math.round((concluidos.length / total) * 100) : 0;
    els.progressoFill.style.width = pct + "%";
    els.progressoTexto.textContent = `${concluidos.length} de ${total} concluídos`;

    els.listaInicioHoje.innerHTML = doDia.length === 0
        ? `<p class="text-center text-[#888780] text-sm py-8 italic">Nenhum atendimento agendado para hoje.</p>`
        : doDia.map(cardAgendamentoHTML).join("");
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

function confirmarPresenca(id) {
    atualizarStatus(id, "confirmado");
    mostrarAviso("Presença confirmada!");
}

function iniciarAtendimento(id) {
    mostrarAviso("Atendimento iniciado!");
    fecharModalDetalhe();
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
    salvarAgendamentos();
    fecharModalDetalhe();
    atualizarTudo();
}

function atualizarTudo() {
    renderizarInicio();
    if (estado.visaoAgenda === "dia") renderizarAgendaDia();
    if (estado.visaoAgenda === "semana") renderizarAgendaSemana();
    if (estado.visaoAgenda === "mes") renderizarAgendaMes();
}

/* ============================================================
   ABA CONFIGURAÇÕES
   ============================================================ */

function abrirModalConfig(tipo) {
    estado.configTipo = tipo;
    els.configCampoTexto.classList.add("hidden");
    els.configCampoTextarea.classList.add("hidden");
    els.configCampoSenha.classList.add("hidden");

    if (tipo === "telefone") {
        els.configModalTitulo.textContent = "Alterar telefone";
        els.configCampoLabel.textContent = "Telefone / WhatsApp";
        els.configInput.type = "tel";
        els.configInput.value = funcionario.telefone;
        els.configCampoTexto.classList.remove("hidden");
    } else if (tipo === "descricao") {
        els.configModalTitulo.textContent = "Editar descrição profissional";
        els.configTextarea.value = funcionario.descricao;
        els.configCampoTextarea.classList.remove("hidden");
    } else if (tipo === "senha") {
        els.configModalTitulo.textContent = "Alterar senha";
        els.configSenhaAtual.value = "";
        els.configSenhaNova.value = "";
        els.configCampoSenha.classList.remove("hidden");
    }

    els.overlayConfig.classList.remove("hidden");
    els.modalConfig.classList.remove("hidden");
}

function fecharModalConfig() {
    els.overlayConfig.classList.add("hidden");
    els.modalConfig.classList.add("hidden");
}

function salvarConfig() {
    const tipo = estado.configTipo;

    if (tipo === "telefone") {
        const valor = els.configInput.value.trim();
        if (!valor) { mostrarAviso("Informe um telefone válido"); return; }
        funcionario.telefone = valor;
        if (els.configTelefoneAtual) els.configTelefoneAtual.textContent = valor;
    } else if (tipo === "descricao") {
        funcionario.descricao = els.configTextarea.value.trim();
    } else if (tipo === "senha") {
        const atual = els.configSenhaAtual.value;
        const nova = els.configSenhaNova.value;
        if (!atual || !nova) { mostrarAviso("Preencha os dois campos de senha"); return; }
        if (nova.length < 6) { mostrarAviso("A nova senha deve ter ao menos 6 caracteres"); return; }
    }

    salvarFuncionario();
    mostrarAviso("Alterações salvas com sucesso!");
    fecharModalConfig();
}

function alternarNotificacoes() {
    mostrarAviso(els.toggleNotif.checked ? "Notificações ativadas" : "Notificações desativadas");
}

function alternarTema() {
    mostrarAviso("Em breve: tema claro disponível");
    els.toggleTema.checked = true;
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

function sairDaConta() {
    if (confirm("Deseja realmente sair da sua conta?")) {
        mostrarAviso("Saindo...");
    }
}

/* ============================================================
   INICIALIZAÇÃO
   ============================================================ */

function iniciar() {
    renderizarInicio();
    if (els.configTelefoneAtual) els.configTelefoneAtual.textContent = funcionario.telefone;
}

iniciar();
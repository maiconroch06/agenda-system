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
    if (els.configTelefoneAtual) els.configTelefoneAtual.textContent = funcionario.telefone;
}

iniciar();
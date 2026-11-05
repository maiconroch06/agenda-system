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
    // Na pasta utilitaria
    carregarData();
}

iniciar();
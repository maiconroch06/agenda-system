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
   NAVEGAÇÃO ENTRE ABAS
   ============================================================ */

function irParaAba(aba) {
    els.abasFunc().forEach(el => el.classList.add("hidden"));
    const abaEl = els.getAba(aba);
    if (abaEl) abaEl.classList.remove("hidden");

    els.sidebarItems().forEach(el => {
        el.classList.remove("bg-[#2a2825]", "text-[#f1efe8]");
        el.classList.add("text-[#888780]", "bg-transparent");
    });
    const sidebarEl = els.getSidebarItem(aba);
    if (sidebarEl) {
        sidebarEl.classList.add("bg-[#2a2825]", "text-[#f1efe8]");
        sidebarEl.classList.remove("text-[#888780]", "bg-transparent");
    }

    els.bottomNavItems().forEach(el => {
        el.classList.remove("text-[#9fe1cb]");
        el.classList.add("text-[#888780]");
    });
    const targetNav = ["avaliacoes", "notificacoes", "configuracoes"].includes(aba) ? "mais" : aba;
    const bottomNavEl = els.getBottomNavItem(targetNav);
    if (bottomNavEl) {
        bottomNavEl.classList.add("text-[#9fe1cb]");
        bottomNavEl.classList.remove("text-[#888780]");
    }

    estado.abaAtual = aba;
    window.scrollTo({ top: 0, behavior: "smooth" });
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
   MODAL: BLOQUEAR HORÁRIO
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
    const data = els.bloqData.value;
    const inicio = els.bloqInicio.value;
    const fim = els.bloqFim.value;
    const motivo = els.bloqMotivo.value.trim();

    if (!data || !inicio || !fim) { mostrarAviso("Preencha data, início e fim"); return; }
    if (fim <= inicio) { mostrarAviso("O horário final deve ser depois do inicial"); return; }

    bloqueios.push({ data, inicio, fim, motivo: motivo || "Horário bloqueado" });
    salvarBloqueios();
    mostrarAviso("Horário bloqueado com sucesso!");
    fecharModalBloquear();
}

/* ============================================================
   ABA SERVIÇOS
   ============================================================ */

function renderizarServicos() {
    els.listaServicosFunc.innerHTML = servicosFunc.map(s => `
        <div class="bg-[#232220] border border-[#38362f] rounded-2xl p-3.5 px-4 flex items-center gap-3.5 ${s.ativo ? "" : "opacity-50"}">
            <div class="flex-1">
                <div class="text-sm font-medium">${s.nome}</div>
                <div class="text-xs text-[#888780] mt-0.5">${s.duracao} min</div>
            </div>
            <div class="text-sm font-medium flex-shrink-0">${formatarMoeda(s.preco)}</div>
            <label class="relative inline-block w-11 h-6 flex-shrink-0 cursor-pointer">
                <input type="checkbox" class="sr-only peer" ${s.ativo ? "checked" : ""} onchange="alternarServico('${s.id}')">
                <span class="absolute inset-0 bg-[#4a473f] rounded-full transition-colors peer-checked:bg-[#0f6e56] peer-checked:after:translate-x-[20px] peer-checked:after:bg-white after:content-[''] after:absolute after:w-[18px] after:h-[18px] after:rounded-full after:left-[3px] after:bottom-[3px] after:bg-[#888780] after:transition-all"></span>
            </label>
        </div>
    `).join("");
}

function alternarServico(id) {
    const s = servicosFunc.find(s => s.id === id);
    if (!s) return;
    s.ativo = !s.ativo;
    salvarServicos();
    renderizarServicos();
    mostrarAviso(s.ativo ? `${s.nome} ativado` : `${s.nome} desativado temporariamente`);
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
    renderizarAgendaDia();
    renderizarServicos();
    if (els.configTelefoneAtual) els.configTelefoneAtual.textContent = funcionario.telefone;
    if (els.bloqData) els.bloqData.value = hojeISO();
}

iniciar();
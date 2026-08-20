/* ============================================================
   PERSISTÊNCIA (localStorage)
   ============================================================ */

function carregarDoStorage(chave, valorPadrao) {
    try {
        const bruto = localStorage.getItem(chave);
        if (!bruto) return valorPadrao;

        const valor = JSON.parse(bruto);

        // Padrão é array (agendamentos, serviços...): se o salvo não for array, descarta e usa o padrão
        if (Array.isArray(valorPadrao)) {
            return Array.isArray(valor) ? valor : valorPadrao;
        }

        // Padrão é objeto (funcionario...): mescla por cima do padrão,
        // assim campos que faltarem no valor salvo (ex: "nome") vêm do padrão em vez de quebrar
        if (valorPadrao && typeof valorPadrao === "object") {
            return (valor && typeof valor === "object") ? { ...valorPadrao, ...valor } : valorPadrao;
        }

        return valor;
    } catch (erro) {
        console.warn(`Não foi possível ler "${chave}" do localStorage, usando dados padrão.`, erro);
        return valorPadrao;
    }
}

function salvarNoStorage(chave, valor) {
    try {
        localStorage.setItem(chave, JSON.stringify(valor));
    } catch (erro) {
        console.warn(`Não foi possível salvar "${chave}" no localStorage.`, erro);
    }
}

function salvarFuncionario()   { salvarNoStorage("profissional", funcionario); }
function salvarAgendamentos()  { salvarNoStorage("agendamentos", agendamentos); }
function salvarServicos()      { salvarNoStorage("servicosFunc", servicosFunc); }
function salvarAvaliacoes()    { salvarNoStorage("avaliacoes", avaliacoes); }
function salvarNotificacoes()  { salvarNoStorage("notificacoes", notificacoes); }
function salvarBloqueios()     { salvarNoStorage("bloqueios", bloqueios); }

/* ============================================================
   DADOS DO FUNCIONÁRIO LOGADO (padrão / seed)
   ============================================================ */

const FUNCIONARIO_PADRAO = {
    nome: "Maicon",
    foto: null,
    empresa: "Barbearia do Zé",
    telefone: "(11) 98888-7777",
    descricao: "Barbeiro especializado em degradê e barboterapia, com foco em atendimento personalizado.",
    comissaoPercentual: 50,
};

let funcionario = carregarDoStorage("profissional", FUNCIONARIO_PADRAO);

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

function formatarDataCurta(iso) {
    const d = new Date(iso + "T00:00:00");
    return d.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" });
}

function formatarMoeda(v) {
    return "R$ " + v.toFixed(2).replace(".", ",");
}

function gerarEstrelas(nota) {
    return "★".repeat(nota) + "☆".repeat(5 - nota);
}

/* ============================================================
   DADOS MOCK — AGENDAMENTOS (padrão / seed)
   ============================================================ */

const AGENDAMENTOS_PADRAO = [
    { id: "a1",  data: diasAPartirDeHoje(0), hora: "09:00", cliente: "Carlos Eduardo",  telefone: "(11) 98765-4321", servico: "Corte Social",       valor: 18, status: "concluido",  observacoes: "" },
    { id: "a2",  data: diasAPartirDeHoje(0), hora: "10:00", cliente: "Bruno Alves",      telefone: "(11) 91234-5678", servico: "Degradê & Barba",    valor: 30, status: "concluido",  observacoes: "Cliente prefere degradê baixo" },
    { id: "a3",  data: diasAPartirDeHoje(0), hora: "11:30", cliente: "Rafael Souza",     telefone: "(11) 99887-6655", servico: "Barba",               valor: 15, status: "confirmado", observacoes: "" },
    { id: "a4",  data: diasAPartirDeHoje(0), hora: "14:00", cliente: "Diego Martins",    telefone: "(11) 98111-2233", servico: "Corte Infantil",      valor: 20, status: "aguardando", observacoes: "Primeira vez, criança de 6 anos" },
    { id: "a5",  data: diasAPartirDeHoje(0), hora: "15:30", cliente: "Felipe Costa",     telefone: "(11) 97222-3344", servico: "Corte Militar",       valor: 15, status: "aguardando", observacoes: "" },
    { id: "a6",  data: diasAPartirDeHoje(0), hora: "16:30", cliente: "Gustavo Lima",     telefone: "(11) 96333-4455", servico: "Social & Barba",      valor: 30, status: "cancelado",  observacoes: "Cliente cancelou por telefone" },

    { id: "a7",  data: diasAPartirDeHoje(1), hora: "09:30", cliente: "Henrique Dias",    telefone: "(11) 95444-5566", servico: "Degradê",              valor: 22, status: "aguardando", observacoes: "" },
    { id: "a8",  data: diasAPartirDeHoje(1), hora: "13:00", cliente: "Igor Pereira",     telefone: "(11) 94555-6677", servico: "Corte Social",         valor: 18, status: "aguardando", observacoes: "" },
    { id: "a9",  data: diasAPartirDeHoje(2), hora: "10:00", cliente: "João Vitor",       telefone: "(11) 93666-7788", servico: "Barba",                valor: 15, status: "aguardando", observacoes: "" },
    { id: "a10", data: diasAPartirDeHoje(3), hora: "11:00", cliente: "Lucas Fernandes",  telefone: "(11) 92777-8899", servico: "Degradê & Barba",      valor: 30, status: "aguardando", observacoes: "" },
    { id: "a11", data: diasAPartirDeHoje(3), hora: "15:00", cliente: "Marcelo Rocha",    telefone: "(11) 91888-9900", servico: "Sobrancelha",          valor: 15, status: "aguardando", observacoes: "" },

    { id: "a12", data: diasAPartirDeHoje(-1), hora: "09:00", cliente: "Nathan Oliveira", telefone: "(11) 90999-0011", servico: "Corte Social",        valor: 18, status: "concluido", observacoes: "" },
    { id: "a13", data: diasAPartirDeHoje(-1), hora: "14:00", cliente: "Otávio Santos",   telefone: "(11) 90111-2233", servico: "Degradê",              valor: 22, status: "concluido", observacoes: "" },
    { id: "a14", data: diasAPartirDeHoje(-2), hora: "10:00", cliente: "Paulo Ricardo",   telefone: "(11) 90222-3344", servico: "Barba",                valor: 15, status: "concluido", observacoes: "" },
    { id: "a15", data: diasAPartirDeHoje(-2), hora: "16:00", cliente: "Renato Alves",    telefone: "(11) 90333-4455", servico: "Corte Militar",        valor: 15, status: "concluido", observacoes: "" },
    { id: "a16", data: diasAPartirDeHoje(-3), hora: "11:00", cliente: "Sérgio Nunes",    telefone: "(11) 90444-5566", servico: "Social & Barba",       valor: 30, status: "concluido", observacoes: "" },
    { id: "a17", data: diasAPartirDeHoje(-4), hora: "09:30", cliente: "Thiago Melo",     telefone: "(11) 90555-6677", servico: "Corte Social",         valor: 18, status: "concluido", observacoes: "" },
    { id: "a18", data: diasAPartirDeHoje(-5), hora: "15:00", cliente: "Vinícius Barros", telefone: "(11) 90666-7788", servico: "Degradê & Barba",      valor: 30, status: "concluido", observacoes: "" },
    { id: "a19", data: diasAPartirDeHoje(-6), hora: "10:30", cliente: "William Cardoso", telefone: "(11) 90777-8899", servico: "Barba",                valor: 15, status: "concluido", observacoes: "" },
];

const agendamentos = carregarDoStorage("agendamentos", AGENDAMENTOS_PADRAO);

/* ============================================================
   DADOS MOCK — SERVIÇOS AUTORIZADOS (padrão / seed)
   ============================================================ */

const SERVICOS_PADRAO = [
    { id: "s1", nome: "Corte Social",      duracao: 30, preco: 18, ativo: true },
    { id: "s2", nome: "Degradê",           duracao: 40, preco: 22, ativo: true },
    { id: "s3", nome: "Degradê & Barba",   duracao: 60, preco: 30, ativo: true },
    { id: "s4", nome: "Social & Barba",    duracao: 50, preco: 30, ativo: true },
    { id: "s5", nome: "Barba",             duracao: 25, preco: 15, ativo: true },
    { id: "s6", nome: "Corte Militar",     duracao: 20, preco: 15, ativo: true },
    { id: "s7", nome: "Corte Infantil",    duracao: 30, preco: 20, ativo: false },
    { id: "s8", nome: "Sobrancelha",       duracao: 5,  preco: 15, ativo: true },
];

const servicosFunc = carregarDoStorage("servicosFunc", SERVICOS_PADRAO);

/* ============================================================
   DADOS MOCK — AVALIAÇÕES (padrão / seed)
   ============================================================ */

const AVALIACOES_PADRAO = [
    { cliente: "Carlos Eduardo", nota: 5, comentario: "Excelente profissional, corte impecável!",           data: "15/07/2026" },
    { cliente: "Bruno Alves",    nota: 5, comentario: "Sempre pontual e caprichoso.",                        data: "12/07/2026" },
    { cliente: "Nathan Oliveira",nota: 4, comentario: "Muito bom, mas demorou um pouco além do horário.",    data: "10/07/2026" },
    { cliente: "Otávio Santos",  nota: 5, comentario: "Melhor barbeiro da região!",                           data: "08/07/2026" },
    { cliente: "Paulo Ricardo",  nota: 4, comentario: "Gostei do resultado, recomendo.",                      data: "05/07/2026" },
];

const avaliacoes = carregarDoStorage("avaliacoes", AVALIACOES_PADRAO);

/* ============================================================
   DADOS MOCK — NOTIFICAÇÕES (padrão / seed)
   ============================================================ */

const NOTIFICACOES_PADRAO = [
    { id: "n1", icone: "📅", mensagem: "Novo agendamento de Diego Martins às 14:00 de hoje.",              data: "Há 2 horas", lida: false },
    { id: "n2", icone: "❌", mensagem: "Gustavo Lima cancelou o horário das 16:30.",                        data: "Há 3 horas", lida: false },
    //{ id: "n3", icone: "⭐", mensagem: "Você recebeu uma nova avaliação de 5 estrelas de Bruno Alves.",     data: "Ontem",       lida: false },
    { id: "n4", icone: "📢", mensagem: "A administração alterou o horário de funcionamento de sábado.",    data: "Há 2 dias",   lida: true },
    { id: "n5", icone: "📅", mensagem: "Lembrete: você tem 6 atendimentos agendados para amanhã.",         data: "Há 2 dias",   lida: true },
];

const notificacoes = carregarDoStorage("notificacoes", NOTIFICACOES_PADRAO);

/* Bloqueios de horário criados pelo funcionário */
const bloqueios = carregarDoStorage("bloqueios", []);

/* ============================================================
   ESTADO DA TELA (não persiste — reinicia a cada acesso)
   ============================================================ */

const estado = {
    abaAtual: "inicio",
    visaoAgenda: "dia",
    mesAtual: new Date(),
    diaSelecionadoMes: null,
    configTipo: null,
};

/* ============================================================
   TOAST
   ============================================================ */

function mostrarAviso(msg) {
    const el = document.getElementById("aviso");
    el.textContent = msg;
    el.classList.add("visivel");
    setTimeout(() => el.classList.remove("visivel"), 2500);
}

/* ============================================================
   CABEÇALHO (topbar + sidebar)
   ============================================================ */

function preencherCabecalho() {
    document.getElementById("topbar-nome").textContent = funcionario.nome;
    document.getElementById("topbar-empresa").textContent = funcionario.empresa;
    document.getElementById("sidebar-nome").textContent = funcionario.nome;
    document.getElementById("sidebar-empresa").textContent = funcionario.empresa;
    document.getElementById("inicio-primeiro-nome").textContent = funcionario.nome.split(" ")[0];
    document.getElementById("config-telefone-atual").textContent = funcionario.telefone;
    atualizarAvatar();
}

function atualizarAvatar() {
    const inicial = funcionario.nome.charAt(0).toUpperCase();
    const topbarAv = document.getElementById("topbar-avatar");
    const sidebarAv = document.getElementById("sidebar-avatar");
    if (funcionario.foto) {
        const imgHtml = `<img src="${funcionario.foto}" alt="${funcionario.nome}" style="width:100%;height:100%;object-fit:cover;border-radius:50%">`;
        topbarAv.innerHTML = imgHtml;
        sidebarAv.innerHTML = imgHtml;
    } else {
        topbarAv.textContent = inicial;
        sidebarAv.textContent = inicial;
    }
}

document.getElementById("inp-nova-foto").addEventListener("change", async function () {
    const arquivo = this.files[0];
    if (!arquivo) return;
    const reader = new FileReader();
    reader.onload = () => {
        funcionario.foto = reader.result;
        atualizarAvatar();
        salvarFuncionario();
        mostrarAviso("Foto atualizada com sucesso!");
    };
    reader.readAsDataURL(arquivo);
});

/* ============================================================
   NAVEGAÇÃO ENTRE ABAS
   ============================================================ */

function irParaAba(aba) {
    document.querySelectorAll(".aba-func").forEach(el => el.classList.remove("ativa"));
    document.getElementById(`aba-${aba}`).classList.add("ativa");

    document.querySelectorAll(".sidebar-func__item").forEach(el => el.classList.remove("ativo"));
    document.querySelector(`.sidebar-func__item[data-aba="${aba}"]`)?.classList.add("ativo");

    const abasSecundarias = ["avaliacoes", "notificacoes", "configuracoes"];
    document.querySelectorAll(".bottom-nav__item").forEach(el => el.classList.remove("ativo"));
    if (abasSecundarias.includes(aba)) {
        document.querySelector('.bottom-nav__item[data-aba="mais"]')?.classList.add("ativo");
    } else {
        document.querySelector(`.bottom-nav__item[data-aba="${aba}"]`)?.classList.add("ativo");
    }

    estado.abaAtual = aba;
    window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ============================================================
   CARD DE AGENDAMENTO (reutilizado em várias abas)
   ============================================================ */

function badgeStatusHTML(status) {
    const mapa = { aguardando: "Aguardando", confirmado: "Confirmado", concluido: "Concluído", cancelado: "Cancelado" };
    return `<span class="badge badge--${status}">${mapa[status]}</span>`;
}

function cardAgendamentoHTML(a) {
    const concluidoClasse = a.status === "concluido" ? " agend-card--concluido" : "";
    return `
        <div class="agend-card${concluidoClasse}" onclick="abrirModalDetalhe('${a.id}')">
            <div class="agend-card__hora">${a.hora}</div>
            <div class="agend-card__info">
                <div class="agend-card__cliente">${a.cliente}</div>
                <div class="agend-card__servico">${a.servico}</div>
            </div>
            <div class="agend-card__direita">
                ${badgeStatusHTML(a.status)}
                <div class="agend-card__valor">${formatarMoeda(a.valor)}</div>
            </div>
        </div>
    `;
}

/* ============================================================
   ABA INÍCIO
   ============================================================ */

function renderizarInicio() {
    const hoje = hojeISO();
    const doDia = agendamentos.filter(a => a.data === hoje).sort((a, b) => a.hora.localeCompare(b.hora));

    const concluidos = doDia.filter(a => a.status === "concluido");
    const pendentes = doDia.filter(a => a.status === "aguardando" || a.status === "confirmado");

    document.getElementById("kpi-total-hoje").textContent = doDia.length;
    document.getElementById("kpi-total-hoje-sub").textContent =
        doDia.length === 0 ? "Nenhum agendamento" : `${concluidos.length} concluídos, ${pendentes.length} restantes`;

    const proximo = pendentes.find(a => a.hora >= horaAtual()) || pendentes[0];
    document.getElementById("kpi-proximo").textContent = proximo ? proximo.hora : "—";
    document.getElementById("kpi-proximo-sub").textContent = proximo ? proximo.cliente : "Nenhum pendente";

    const ganhoHoje = concluidos.reduce((soma, a) => soma + a.valor, 0);
    document.getElementById("kpi-ganhos-hoje").textContent = formatarMoeda(ganhoHoje);

    const mediaAval = avaliacoes.length
        ? (avaliacoes.reduce((s, a) => s + a.nota, 0) / avaliacoes.length).toFixed(1)
        : "—";
    document.getElementById("kpi-avaliacao").textContent = mediaAval;
    document.getElementById("kpi-avaliacao-sub").textContent = `${avaliacoes.length} avaliações`;

    const total = doDia.length;
    const pct = total ? Math.round((concluidos.length / total) * 100) : 0;
    document.getElementById("progresso-fill").style.width = pct + "%";
    document.getElementById("progresso-texto").textContent = `${concluidos.length} de ${total} concluídos`;

    const lista = document.getElementById("lista-inicio-hoje");
    lista.innerHTML = doDia.length === 0
        ? `<p class="lista-vazia">Nenhum atendimento agendado para hoje.</p>`
        : doDia.map(cardAgendamentoHTML).join("");
}

/* ============================================================
   ABA AGENDA
   ============================================================ */

function mudarVisaoAgenda(visao) {
    estado.visaoAgenda = visao;
    document.querySelectorAll(".filtro-btn").forEach(b => b.classList.remove("ativo"));
    document.querySelector(`.filtro-btn[data-filtro="${visao}"]`).classList.add("ativo");

    document.getElementById("agenda-visao-dia").hidden = visao !== "dia";
    document.getElementById("agenda-visao-semana").hidden = visao !== "semana";
    document.getElementById("agenda-visao-mes").hidden = visao !== "mes";

    if (visao === "dia") renderizarAgendaDia();
    if (visao === "semana") renderizarAgendaSemana();
    if (visao === "mes") renderizarAgendaMes();
}

function renderizarAgendaDia() {
    const hoje = hojeISO();
    const doDia = agendamentos.filter(a => a.data === hoje).sort((a, b) => a.hora.localeCompare(b.hora));
    const lista = document.getElementById("lista-agenda-dia");
    lista.innerHTML = doDia.length === 0
        ? `<p class="lista-vazia">Nenhum agendamento para hoje.</p>`
        : doDia.map(cardAgendamentoHTML).join("");
}

function renderizarAgendaSemana() {
    const nomesDias = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
    const container = document.getElementById("semana-scroll");
    let html = "";

    for (let i = 0; i < 7; i++) {
        const d = new Date();
        d.setDate(d.getDate() + i);
        const iso = formatarISO(d);
        const ehHoje = iso === hojeISO();
        const doDia = agendamentos.filter(a => a.data === iso).sort((a, b) => a.hora.localeCompare(b.hora));

        html += `
            <div class="semana-col${ehHoje ? " semana-col--hoje" : ""}">
                <div class="semana-col__head">
                    <div class="semana-col__dia">${nomesDias[d.getDay()]}</div>
                    <div class="semana-col__num">${d.getDate()}</div>
                </div>
                <div class="semana-col__corpo">
                    ${doDia.length === 0
                        ? `<span style="font-size:11px;color:var(--cor-texto-muted);text-align:center;padding-top:8px">Livre</span>`
                        : doDia.map(a => `
                            <div class="semana-mini semana-mini--${a.status}" onclick="abrirModalDetalhe('${a.id}')">
                                <div class="semana-mini__hora">${a.hora}</div>
                                <div class="semana-mini__cliente">${a.cliente}</div>
                            </div>
                        `).join("")
                    }
                </div>
            </div>
        `;
    }
    container.innerHTML = html;
}

function renderizarAgendaMes() {
    const nomesMeses = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"];
    const ano = estado.mesAtual.getFullYear();
    const mes = estado.mesAtual.getMonth();

    document.getElementById("mes-titulo").textContent = `${nomesMeses[mes]} ${ano}`;

    const primeiroDiaSemana = new Date(ano, mes, 1).getDay();
    const totalDiasMes = new Date(ano, mes + 1, 0).getDate();
    const totalDiasMesAnterior = new Date(ano, mes, 0).getDate();

    const labels = ["D", "S", "T", "Q", "Q", "S", "S"];
    let html = labels.map(l => `<div class="mes-label">${l}</div>`).join("");

    for (let i = primeiroDiaSemana - 1; i >= 0; i--) {
        html += `<button class="mes-dia mes-dia--outro" disabled>${totalDiasMesAnterior - i}</button>`;
    }

    for (let dia = 1; dia <= totalDiasMes; dia++) {
        const dataObj = new Date(ano, mes, dia);
        const iso = formatarISO(dataObj);
        const ehHoje = iso === hojeISO();
        const temAgendamento = agendamentos.some(a => a.data === iso);
        html += `
            <button class="mes-dia${ehHoje ? " mes-dia--hoje" : ""}" onclick="selecionarDiaMes('${iso}')">
                ${dia}
                ${temAgendamento ? `<span class="mes-dia__dot"></span>` : ""}
            </button>
        `;
    }

    const totalCelulas = primeiroDiaSemana + totalDiasMes;
    const restante = (7 - (totalCelulas % 7)) % 7;
    for (let i = 1; i <= restante; i++) {
        html += `<button class="mes-dia mes-dia--outro" disabled>${i}</button>`;
    }

    document.getElementById("mes-grid").innerHTML = html;

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

    document.getElementById("mes-dia-selecionado-titulo").textContent =
        `Agendamentos — ${formatarDataExtenso(iso)}`;

    const lista = document.getElementById("lista-mes-dia");
    lista.innerHTML = doDia.length === 0
        ? `<p class="lista-vazia">Nenhum agendamento neste dia.</p>`
        : doDia.map(cardAgendamentoHTML).join("");
}

/* ============================================================
   MODAL: DETALHES DO ATENDIMENTO
   ============================================================ */

function abrirModalDetalhe(id) {
    const a = agendamentos.find(a => a.id === id);
    if (!a) return;

    document.getElementById("detalhe-status-badge").innerHTML = badgeStatusHTML(a.status);
    document.getElementById("detalhe-cliente").textContent = a.cliente;
    document.getElementById("detalhe-servico").textContent = a.servico;
    document.getElementById("detalhe-horario").textContent = `${formatarDataExtenso(a.data)} às ${a.hora}`;
    document.getElementById("detalhe-valor").textContent = formatarMoeda(a.valor);
    document.getElementById("detalhe-telefone").textContent = a.telefone;
    document.getElementById("detalhe-obs").textContent = a.observacoes || "Nenhuma observação";

    const acoes = document.getElementById("detalhe-acoes");
    let html = "";
    if (a.status === "aguardando") {
        html += `<button class="btn-acento" onclick="confirmarPresenca('${a.id}')">Confirmar presença</button>`;
    }
    if (a.status === "confirmado") {
        html += `<button class="btn-acento" onclick="iniciarAtendimento('${a.id}')">Iniciar atendimento</button>`;
    }
    if (a.status === "aguardando" || a.status === "confirmado") {
        html += `<button class="btn-prim" onclick="concluirAtendimento('${a.id}')">Concluir atendimento</button>`;
        html += `<button class="btn-perigo" onclick="cancelarAtendimento('${a.id}')">Cancelar</button>`;
    }
    if (a.status === "concluido") {
        html = `<p style="text-align:center;color:var(--cor-texto-suave);font-size:13px">Atendimento já concluído</p>`;
    }
    if (a.status === "cancelado") {
        html = `<p style="text-align:center;color:var(--cor-texto-suave);font-size:13px">Este atendimento foi cancelado</p>`;
    }
    acoes.innerHTML = html;

    document.getElementById("overlay-detalhe").hidden = false;
    document.getElementById("modal-detalhe").hidden = false;
}

function fecharModalDetalhe() {
    document.getElementById("overlay-detalhe").hidden = true;
    document.getElementById("modal-detalhe").hidden = true;
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
    renderizarGanhos();
}

/* ============================================================
   MODAL: BLOQUEAR HORÁRIO
   ============================================================ */

function abrirModalBloquear() {
    document.getElementById("overlay-bloquear").hidden = false;
    document.getElementById("modal-bloquear").hidden = false;
}

function fecharModalBloquear() {
    document.getElementById("overlay-bloquear").hidden = true;
    document.getElementById("modal-bloquear").hidden = true;
}

function confirmarBloqueio() {
    const data = document.getElementById("bloq-data").value;
    const inicio = document.getElementById("bloq-inicio").value;
    const fim = document.getElementById("bloq-fim").value;
    const motivo = document.getElementById("bloq-motivo").value.trim();

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
    const lista = document.getElementById("lista-servicos-func");
    lista.innerHTML = servicosFunc.map(s => `
        <div class="servico-item${s.ativo ? "" : " servico-item--inativo"}">
            <div class="servico-item__info">
                <div class="servico-item__nome">${s.nome}</div>
                <div class="servico-item__meta">${s.duracao} min</div>
            </div>
            <div class="servico-item__preco">${formatarMoeda(s.preco)}</div>
            <label class="toggle">
                <input type="checkbox" ${s.ativo ? "checked" : ""} onchange="alternarServico('${s.id}')">
                <span class="toggle__slider"></span>
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
   ABA GANHOS
   ============================================================ */

function renderizarGanhos() {
    const hoje = hojeISO();
    const concluidos = agendamentos.filter(a => a.status === "concluido");

    const ganhoHoje = concluidos.filter(a => a.data === hoje).reduce((s, a) => s + a.valor, 0);

    const inicioSemana = new Date();
    inicioSemana.setDate(inicioSemana.getDate() - inicioSemana.getDay());
    const isoInicioSemana = formatarISO(inicioSemana);
    const ganhoSemana = concluidos.filter(a => a.data >= isoInicioSemana).reduce((s, a) => s + a.valor, 0);

    const hojeObj = new Date();
    const isoInicioMes = formatarISO(new Date(hojeObj.getFullYear(), hojeObj.getMonth(), 1));
    const ganhoMes = concluidos.filter(a => a.data >= isoInicioMes).reduce((s, a) => s + a.valor, 0);

    document.getElementById("ganhos-hoje").textContent = formatarMoeda(ganhoHoje);
    document.getElementById("ganhos-semana").textContent = formatarMoeda(ganhoSemana);
    document.getElementById("ganhos-mes").textContent = formatarMoeda(ganhoMes);

    document.getElementById("comissao-aviso").innerHTML =
        `Sua comissão atual é de <strong>${funcionario.comissaoPercentual}%</strong> sobre cada atendimento.`;

    const grafico = document.getElementById("grafico-ganhos");
    const dadosGrafico = [];
    for (let i = 6; i >= 0; i--) {
        const d = new Date();
        d.setDate(d.getDate() - i);
        const iso = formatarISO(d);
        const total = concluidos.filter(a => a.data === iso).reduce((s, a) => s + a.valor, 0);
        dadosGrafico.push({ dia: d.toLocaleDateString("pt-BR", { weekday: "short" }).replace(".", ""), total });
    }
    const maxValor = Math.max(...dadosGrafico.map(d => d.total), 1);

    grafico.innerHTML = dadosGrafico.map(d => `
        <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%;justify-content:flex-end">
            <span style="font-size:10px;color:var(--cor-texto-suave)">${d.total > 0 ? formatarMoeda(d.total) : ""}</span>
            <div style="width:100%;max-width:28px;background:var(--cor-acento);border-radius:4px 4px 0 0;height:${(d.total / maxValor * 80) || 2}px;min-height:2px"></div>
            <span style="font-size:10px;color:var(--cor-texto-suave);text-transform:capitalize">${d.dia}</span>
        </div>
    `).join("");

    const corpo = document.getElementById("tabela-ganhos-corpo");
    const historico = [...concluidos].sort((a, b) => (b.data + b.hora).localeCompare(a.data + a.hora)).slice(0, 15);
    corpo.innerHTML = historico.length === 0
        ? `<tr><td colspan="5" class="lista-vazia">Nenhum atendimento concluído ainda.</td></tr>`
        : historico.map(a => `
            <tr>
                <td>${formatarDataCurta(a.data)}</td>
                <td>${a.cliente}</td>
                <td>${a.servico}</td>
                <td>${formatarMoeda(a.valor)}</td>
                <td>${formatarMoeda(a.valor * funcionario.comissaoPercentual / 100)}</td>
            </tr>
        `).join("");
}

/* ============================================================
   ABA AVALIAÇÕES
   ============================================================ */

function renderizarAvaliacoes() {
    const media = avaliacoes.length
        ? avaliacoes.reduce((s, a) => s + a.nota, 0) / avaliacoes.length
        : 0;

    document.getElementById("media-avaliacao").textContent = media.toFixed(1);
    document.querySelector(".media-card .estrelas").textContent = gerarEstrelas(Math.round(media));
    document.getElementById("total-avaliacoes").textContent = `Baseado em ${avaliacoes.length} avaliações`;

    const lista = document.getElementById("lista-avaliacoes");
    lista.innerHTML = avaliacoes.map(a => `
        <div class="aval-item">
            <div class="aval-item__head">
                <span class="aval-item__cliente">${a.cliente}</span>
                <span class="aval-item__data">${a.data}</span>
            </div>
            <div class="estrelas" style="margin-bottom:6px">${gerarEstrelas(a.nota)}</div>
            <div class="aval-item__comentario">${a.comentario}</div>
        </div>
    `).join("");
}

/* ============================================================
   ABA NOTIFICAÇÕES
   ============================================================ */

function renderizarNotificacoes() {
    const naoLidas = notificacoes.filter(n => !n.lida).length;

    document.getElementById("sino-badge").hidden = naoLidas === 0;
    document.getElementById("sino-badge").textContent = naoLidas;
    document.getElementById("sidebar-notif-dot").hidden = naoLidas === 0;
    document.getElementById("bottomnav-notif-dot").hidden = naoLidas === 0;

    const lista = document.getElementById("lista-notificacoes");
    lista.innerHTML = notificacoes.map(n => `
        <div class="notif-item${n.lida ? "" : " notif-item--nova"}" onclick="marcarNotificacaoLida('${n.id}')">
            <div class="notif-item__icone">${n.icone}</div>
            <div>
                <div class="notif-item__msg">${n.mensagem}</div>
                <div class="notif-item__data">${n.data}</div>
            </div>
        </div>
    `).join("");
}

function marcarNotificacaoLida(id) {
    const n = notificacoes.find(n => n.id === id);
    if (n) n.lida = true;
    salvarNotificacoes();
    renderizarNotificacoes();
}

function marcarTodasLidas() {
    notificacoes.forEach(n => n.lida = true);
    salvarNotificacoes();
    renderizarNotificacoes();
    mostrarAviso("Todas as notificações foram marcadas como lidas");
}

/* ============================================================
   ABA CONFIGURAÇÕES
   ============================================================ */

function abrirModalConfig(tipo) {
    estado.configTipo = tipo;
    document.getElementById("config-campo-texto").hidden = true;
    document.getElementById("config-campo-textarea").hidden = true;
    document.getElementById("config-campo-senha").hidden = true;

    if (tipo === "telefone") {
        document.getElementById("config-modal-titulo").textContent = "Alterar telefone";
        document.getElementById("config-campo-label").textContent = "Telefone / WhatsApp";
        document.getElementById("config-input").type = "tel";
        document.getElementById("config-input").value = funcionario.telefone;
        document.getElementById("config-campo-texto").hidden = false;
    } else if (tipo === "descricao") {
        document.getElementById("config-modal-titulo").textContent = "Editar descrição profissional";
        document.getElementById("config-textarea").value = funcionario.descricao;
        document.getElementById("config-campo-textarea").hidden = false;
    } else if (tipo === "senha") {
        document.getElementById("config-modal-titulo").textContent = "Alterar senha";
        document.getElementById("config-senha-atual").value = "";
        document.getElementById("config-senha-nova").value = "";
        document.getElementById("config-campo-senha").hidden = false;
    }

    document.getElementById("overlay-config").hidden = false;
    document.getElementById("modal-config").hidden = false;
}

function fecharModalConfig() {
    document.getElementById("overlay-config").hidden = true;
    document.getElementById("modal-config").hidden = true;
}

function salvarConfig() {
    const tipo = estado.configTipo;

    if (tipo === "telefone") {
        const valor = document.getElementById("config-input").value.trim();
        if (!valor) { mostrarAviso("Informe um telefone válido"); return; }
        funcionario.telefone = valor;
        document.getElementById("config-telefone-atual").textContent = valor;
    } else if (tipo === "descricao") {
        funcionario.descricao = document.getElementById("config-textarea").value.trim();
    } else if (tipo === "senha") {
        const atual = document.getElementById("config-senha-atual").value;
        const nova = document.getElementById("config-senha-nova").value;
        if (!atual || !nova) { mostrarAviso("Preencha os dois campos de senha"); return; }
        if (nova.length < 6) { mostrarAviso("A nova senha deve ter ao menos 6 caracteres"); return; }
    }

    salvarFuncionario();
    mostrarAviso("Alterações salvas com sucesso!");
    fecharModalConfig();
}

function alternarNotificacoes() {
    const ativado = document.getElementById("toggle-notif").checked;
    mostrarAviso(ativado ? "Notificações ativadas" : "Notificações desativadas");
}

function alternarTema() {
    mostrarAviso("Em breve: tema claro disponível");
    document.getElementById("toggle-tema").checked = true;
}

/* ============================================================
   MENU "MAIS" (mobile)
   ============================================================ */

function abrirMenuMais() {
    document.getElementById("overlay-mais").hidden = false;
    document.getElementById("modal-mais").hidden = false;
}

function fecharMenuMais() {
    document.getElementById("overlay-mais").hidden = true;
    document.getElementById("modal-mais").hidden = true;
}

/* ============================================================
   SAIR
   ============================================================ */

function sairDaConta() {
    if (confirm("Deseja realmente sair da sua conta?")) {
        mostrarAviso("Saindo...");
        window.location.href = "autenticacao.html";
    }
}

/* ============================================================
   INICIALIZAÇÃO
   ============================================================ */

function iniciar() {
    preencherCabecalho();
    renderizarInicio();
    renderizarAgendaDia();
    renderizarServicos();
    renderizarGanhos();
    renderizarAvaliacoes();
    renderizarNotificacoes();
    document.getElementById("bloq-data").value = hojeISO();
}

iniciar();
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

function carregarData() {
    // Data debaixo do titulo
    const dataFormatted = new Date().toLocaleDateString("pt-BR", { weekday: "long", day: "2-digit", month: "long" });
    const elData = document.getElementById("data-atual-str");
    if (elData) elData.textContent = dataFormatted.charAt(0).toUpperCase() + dataFormatted.slice(1);
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
   DADOS MOCK — AGENDAMENTOS
   ============================================================ */

const AGENDAMENTOS_PADRAO = [
    { id: "a1",  data: diasAPartirDeHoje(0), hora: "09:00", cliente: "Carlos Eduardo",  telefone: "(11) 98765-4321", servico: "Corte Social",       valor: 18, status: "concluido",  observacoes: "" },
    { id: "a2",  data: diasAPartirDeHoje(0), hora: "10:00", cliente: "Bruno Alves",      telefone: "(11) 91234-5678", servico: "Degradê & Barba",    valor: 30, status: "concluido",  observacoes: "Cliente prefere degradê baixo" },
    { id: "a3",  data: diasAPartirDeHoje(0), hora: "11:30", cliente: "Rafael Souza",     telefone: "(11) 99887-6655", servico: "Barba",              valor: 15, status: "aguardando", observacoes: "" },
    { id: "a4",  data: diasAPartirDeHoje(0), hora: "14:00", cliente: "Diego Martins",    telefone: "(11) 98111-2233", servico: "Corte Infantil",      valor: 20, status: "aguardando", observacoes: "Primeira vez, criança de 6 anos" },
    { id: "a5",  data: diasAPartirDeHoje(0), hora: "15:30", cliente: "Felipe Costa",     telefone: "(11) 97222-3344", servico: "Corte Militar",       valor: 15, status: "aguardando", observacoes: "" },
    { id: "a6",  data: diasAPartirDeHoje(0), hora: "16:30", cliente: "Gustavo Lima",     telefone: "(11) 96333-4455", servico: "Social & Barba",      valor: 30, status: "cancelado",  observacoes: "Cliente cancelou por telefone" },
    { id: "a7",  data: diasAPartirDeHoje(1), hora: "09:30", cliente: "Henrique Dias",    telefone: "(11) 95444-5566", servico: "Degradê",              valor: 22, status: "aguardando", observacoes: "" },
    { id: "a9",  data: diasAPartirDeHoje(1), hora: "14:00", cliente: "Igor Pereira",     telefone: "(11) 94555-6677", servico: "Corte Social",         valor: 18, status: "aguardando", observacoes: "" },
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

carregarData();
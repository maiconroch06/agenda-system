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
   CARREGAMENTO DE DADOS (JINJA/FLASK)
   ============================================================ */
let agendamentos = [];
let barbeiros = [];
let funcionario = { nome: "Barbeiro", telefone: "", descricao: "" };

try {
    const jsonAgend = document.getElementById("dados-agendamentos-json");
    if (jsonAgend) agendamentos = JSON.parse(jsonAgend.textContent);

    const jsonBarb = document.getElementById("dados-barbeiros-json");
    if (jsonBarb) {
        barbeiros = JSON.parse(jsonBarb.textContent);
        if (barbeiros.length > 0) funcionario = barbeiros[0]; // Puxa o 1º barbeiro do Mock/Flask
    }
} catch (e) {
    console.warn("Não foi possível carregar os dados JSON do Jinja.", e);
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

function salvarFuncionario()   { salvarNoStorage("profissional", funcionario); }
function salvarAgendamentos()  { salvarNoStorage("agendamentos", agendamentos); }
function salvarServicos()      { salvarNoStorage("servicosFunc", servicosFunc); }
function salvarBloqueios()     { salvarNoStorage("bloqueios", bloqueios); }

carregarData();
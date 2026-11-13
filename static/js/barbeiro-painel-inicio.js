/* ============================================================
   ELEMENTOS CENTRALIZADOS (DOM)
   ============================================================ */

const els = {
    aviso: document.getElementById("aviso"),

    // KPI's & Aba Início
    progressoTexto: document.getElementById("progresso-texto"),
    progressoFill: document.getElementById("progresso-fill"),
    progressoCancelados: document.getElementById("progresso-cancelados"),
    progressoPendentes: document.getElementById("progresso-pendente"),
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
   ESTADO GLOBAL DE NAVEGAÇÃO
   ============================================================ */
// Define o dia atual em exibição. Inicialmente é hoje.
let dataExibicaoAtual = new Date();

/* ============================================================
   MUDAR DE DIA E ATUALIZAR INTERFACE
   ============================================================ */

function formatarDataNavegacao(data) {
    const hoje = new Date();
    const amanha = new Date();
    amanha.setDate(hoje.getDate() + 1);
    const ontem = new Date();
    ontem.setDate(hoje.getDate() - 1);

    if (formatarISO(data) === formatarISO(hoje)) return "Hoje";
    if (formatarISO(data) === formatarISO(amanha)) return "Amanhã";
    if (formatarISO(data) === formatarISO(ontem)) return "Ontem";

    // Para outros dias, exibe o formato curto, ex: "Qua, 11/11"
    const opcoes = { weekday: 'short', day: '2-digit', month: '2-digit' };
    let formatada = data.toLocaleDateString('pt-BR', opcoes);
    // Capitaliza a primeira letra do dia da semana
    return formatada.charAt(0).toUpperCase() + formatada.slice(1);
}

function atualizarInterfaceNavegacao() {
    const navDisplay = document.getElementById("nav-data-display");
    const btnHoje = document.getElementById("btn-hoje");
    const tituloLista = document.querySelector(".text-xs.font-medium.text-\\[\\#888780\\].uppercase.tracking-wider.mb-3");
    
    const stringDataFormatada = formatarDataNavegacao(dataExibicaoAtual);
    const isHoje = formatarISO(dataExibicaoAtual) === hojeISO();

    // Atualiza o texto central entre os botões
    if (navDisplay) {
        navDisplay.textContent = stringDataFormatada;
    }

    // Exibe ou oculta o botão "Voltar para Hoje"
    if (btnHoje) {
        if (isHoje) {
            btnHoje.classList.add("hidden");
        } else {
            btnHoje.classList.remove("hidden");
        }
    }

    // Atualiza o título acima da lista de cards
    if (tituloLista) {
        tituloLista.textContent = isHoje ? "Agendamentos de hoje" : `Agendamentos de ${stringDataFormatada}`;
    }

    // Re-renderiza a lista de cards baseada na nova data
    //renderizarInicio(); 
}

function mudarDia(delta) {
    // Adiciona ou subtrai dias da data atual em exibição
    dataExibicaoAtual.setDate(dataExibicaoAtual.getDate() + delta);
    atualizarInterfaceNavegacao();
}

function irParaHoje() {
    dataExibicaoAtual = new Date(); // Reseta para a data real de hoje
    atualizarInterfaceNavegacao();
}

/* ============================================================
   ABA INÍCIO
   ============================================================ */

function renderizarInicio() {
    const hoje = hojeISO();

    // Filtra os agendamentos do dia e aplica a ordenação por Status e Hora
    const dataAlvoStr = formatarISO(dataExibicaoAtual); 
    const doDia = agendamentos
        .filter(a => a.data === dataAlvoStr)
        .sort((a, b) => {
            // Define o peso (prioridade) de cada status
            const pesoStatus = { agendado: 1, concluido: 2, cancelado: 3 };
            
            // 1º Critério: Ordena pelo peso do status
            if (pesoStatus[a.status] !== pesoStatus[b.status]) {
                return pesoStatus[a.status] - pesoStatus[b.status];
            }

            // 2º Critério: Se o status for igual, ordena pela hora mais próxima (crescente)
            return a.hora.localeCompare(b.hora);
        });
        
    // Calcula os indicadores de progresso
    const concluidos = doDia.filter(a => a.status === 2).length;
    const cancelados = doDia.filter(a => a.status === 0).length;
    const pendentes = doDia.filter(a => a.status === 1).length;
    
    const totalGeral = doDia.length;
    const totalValidos = totalGeral - cancelados;

    // Atualiza os textos e barras de progresso na tela
    if (els.progressoTexto) {
        els.progressoTexto.textContent = `${concluidos} de ${totalValidos} concluídos`;
    }

    const pctConcluidos = totalGeral ? (concluidos / totalGeral) * 100 : 0;
    const pctCancelados = totalGeral ? (cancelados / totalGeral) * 100 : 0;
    const pctPendentes = totalGeral ? (pendentes / totalGeral) * 100 : 0;

    if (els.progressoFill) els.progressoFill.style.width = `${pctConcluidos}%`;
    if (els.progressoCancelados) els.progressoCancelados.style.width = `${pctCancelados}%`;
    if (els.progressoPendentes) els.progressoPendentes.style.width = `${pctPendentes}%`;

}

/* ============================================================
   INICIALIZAÇÃO
   ============================================================ */

function iniciar() {
    localStorage.clear();

    renderizarInicio();
    
    if (typeof carregarData === "function") {
        carregarData();
    }
}

iniciar();
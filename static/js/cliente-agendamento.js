
/* ============================================================
   DADOS
   ============================================================ */

const SERVICOS = [
    { id: "infantil", name: "Corte Infantil", duration: 30, price: 20, icon: "../../static/assets/img/cortes/corte-infantil.jpeg", alt: "corte-infantil" },
    { id: "social", name: "Corte Social", duration: 30, price: 18, icon: "../../static/assets/img/cortes/corte-social.jpeg", alt: "corte-social" },
    { id: "social-barba", name: "Social & Barba", duration: 50, price: 30, icon: "../../static/assets/img/cortes/corte-social&barba.jpeg", alt: "corte-social-barba" },
    { id: "degrade", name: "Degradê", duration: 40, price: 22, icon: "../../static/assets/img/cortes/corte-degrade.jpeg", alt: "corte-degrade" },
    { id: "degrade-barba", name: "Degradê & Barba", duration: 60, price: 30, icon: "../../static/assets/img/cortes/corte-degrade-barba.jpeg", alt: "corte-degrade-barba" },
    { id: "militar", name: "Corte Militar", duration: 20, price: 15, icon: "../../static/assets/img/cortes/corte-militar.jpeg", alt: "corte-militar" },
    { id: "barba", name: "Barba", duration: 25, price: 15, icon: "../../static/assets/img/cortes/corte-barba.jpeg", alt: "corte-barba" },
];

const PROFISSIONAIS = [
    { id: "thiago", name: "Thiago Tomaz", description: "Barbeiro sênior", icon: "../../static/assets/img/barbeiros/barbeiro-master-thiago-silva.png", alt: "thiago" },
    { id: "samuel", name: "Samuel", description: "Barbeiro sênior", icon: "../../static/assets/img/barbeiros/barbeiro-tres-samuca.png", alt: "samuel" },
    { id: "maik", name: "Maik", description: "Barbeiro novato", icon: "../../static/assets/img/barbeiros/barbeiro_dois_maik.png", alt: "maik" },
    { id: "any", name: "Sem preferência", description: "Qualquer profissional disponível", icon: "", alt: "⇄" },
];

const NOMES_DIAS = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

const TODOS_HORARIOS = [
    "09:00", "09:30", "10:00", "10:30", "11:00",
    "13:00", "13:30", "14:00", "14:30",
    "15:00", "15:30", "16:00", "16:30", "17:00"
];

const HORARIOS_OCUPADOS = {};

const historicoCortes = [];

/* ============================================================
   ESTADO
   ============================================================ */

const estado = {
    etapaAtual: 1,
    servicosSelecionados: [],
    profissionalSelecionado: null,
    diaSelecionado: null,
    horarioSelecionado: null,
    agendamentoConcluido: false,
    nome: "Maicon Rocha"
};

const limparAoCarregar =
    sessionStorage.getItem("limparAgendamento") === "true";

/* ============================================================
   ELEMENTOS
   ============================================================ */

const els = {
    etapa: document.getElementById("etapa"),
    listaServico: document.getElementById("lista-servico"),
    listaProfissionais: document.getElementById("lista-profissionais"),
    abasDias: document.getElementById("abas-dias"),
    gradeHorarios: document.getElementById("grade-horarios"),
    resumo: document.getElementById("resumo"),
    btnVoltar: document.getElementById("btn-voltar"),
    btnContinuar: document.getElementById("btn-continuar"),
    navEtapa: document.getElementById("nav-etapa"),
    aviso: document.getElementById("aviso"),
    sucesso: document.getElementById("painel-5"),
    sucessoTexto: document.getElementById("sucesso-texto"),
    btnVoltarInicio: document.getElementById("btn-voltar-inicio"),
    btnHistorico: document.getElementById("btn-toggle-historico"),
    painelHistorico: document.getElementById("painel-historico"),
    listaHistorico: document.getElementById("lista-historico"),
    modalHistorico: document.getElementById("modal-historico"),
    resumoModal: document.getElementById("resumo-modal-conteudo")
};

const form = {};

/* ============================================================
   LOCALSTORAGE & HISTÓRICO
   ============================================================ */

function salvarNoHistorico(novoItem) {
    const historico = historicoCortes;

    historico.unshift(novoItem);

    localStorage.setItem(
        "historicoAgendamentos",
        JSON.stringify(historico)
    );
}

/* ============================================================
   AVISO (TOAST)
   ============================================================ */

function mostrarAviso(mensagem) {
    els.aviso.textContent = mensagem;
    els.aviso.classList.add("visivel");

    setTimeout(() => {
        els.aviso.classList.remove("visivel");
    }, 2500);
}

/* ============================================================
   CONTROLE DE PAINÉIS
   ============================================================ */

function mostrarPainel(numero) {

    for (let i = 1; i <= 4; i++) {
        const painel = document.getElementById(`painel-${i}`);

        if (painel) {
            painel.hidden = i !== numero;
        }
    }

    els.sucesso.hidden = true;

    if (els.painelHistorico) {
        els.painelHistorico.hidden = true;
    }

    atualizarStepper();
    atualizarBotoes();

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

/* ============================================================
   HISTÓRICO DE AGENDAMENTOS
   ============================================================ */

function abrirHistorico() {

    for (let i = 1; i <= 4; i++) {
        const painel = document.getElementById(`painel-${i}`);

        if (painel) painel.hidden = true;
    }

    els.sucesso.hidden = true;
    els.etapa.hidden = true;
    els.navEtapa.hidden = true;
    els.painelHistorico.hidden = false;

    carregarHistorico();

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

function voltarParaAgendamento() {

    els.painelHistorico.hidden = true;

    if (estado.agendamentoConcluido) {
        reiniciar();
    } else {
        els.etapa.hidden = false;
        els.navEtapa.hidden = false;

        mostrarPainel(estado.etapaAtual);
    }

    const textoBtn = document.getElementById("texto-btn-historico");

    if (textoBtn) {
        textoBtn.textContent = "Meus Agendamentos";
    }

    if (els.btnHistorico) {
        els.btnHistorico.classList.remove(
            "border-brand-gold",
            "text-brand-gold"
        );
    }
}

function alternarHistorico() {
    window.location.href = URL_MEUS_AGENDAMENTOS;
}


function carregarHistorico() {

    const historico = historicoCortes;

    if (!historico || historico.length === 0) {

        els.listaHistorico.innerHTML = `
            <p class="text-[#888780] text-sm text-center col-span-full py-8">
                Nenhum agendamento encontrado.
            </p>
        `;

        return;
    }

    els.listaHistorico.innerHTML = historico.map(item => `
        <div class="bg-[#1c1c1c] border border-[#38362f] rounded-xl p-4 flex flex-col gap-3 hover:border-brand-gold/50 cursor-pointer transition-all"
             onclick="exibirDetalhesHistorico('${item.id}')">

            <div class="flex justify-between items-center border-b border-[#2e2d29] pb-2">

                <span class="font-medium text-[#f1efe8] text-[15px]">
                    ${item.servico}
                </span>

                <span class="text-[12px] px-2 py-0.5 rounded-full font-medium
                    ${item.status === 'Concluído'
                        ? 'bg-green-900/40 text-green-400 border border-green-800'
                        : 'bg-amber-900/40 text-amber-400 border border-amber-800'}">
                    ${item.status}
                </span>

            </div>

            <div class="flex flex-col gap-1 text-[13px] text-[#888780]">

                <span>
                    <strong class="text-[#f1efe8]">Profissional:</strong>
                    ${item.profissional}
                </span>

                <span>
                    <strong class="text-[#f1efe8]">Data:</strong>
                    ${item.data}
                </span>

                <span>
                    <strong class="text-[#f1efe8]">Horário:</strong>
                    ${item.horario}
                </span>

            </div>

            <div class="flex justify-between items-center pt-2 border-t border-[#2e2d29]">

                <span class="font-bold text-[#f1efe8] text-[14px]">
                    ${item.valor}
                </span>

                <span class="text-[12px] text-brand-gold hover:underline">
                    Ver resumo →
                </span>

            </div>

        </div>
    `).join("");
}

function exibirDetalhesHistorico(id) {

    const historico = historicoCortes;
    const item = historico.find(h => h.id === id);

    if (!item) return;

    els.resumoModal.innerHTML = `
        <div class="divide-y divide-[#38362f] text-[14px]">

            <div class="flex justify-between py-2.5">
                <span class="text-[#888780]">Serviço</span>
                <span class="font-medium text-[#f1efe8]">${item.servico}</span>
            </div>

            <div class="flex justify-between py-2.5">
                <span class="text-[#888780]">Profissional</span>
                <span class="font-medium text-[#f1efe8]">${item.profissional}</span>
            </div>

            <div class="flex justify-between py-2.5">
                <span class="text-[#888780]">Data</span>
                <span class="font-medium text-[#f1efe8]">${item.data}</span>
            </div>

            <div class="flex justify-between py-2.5">
                <span class="text-[#888780]">Horário</span>
                <span class="font-medium text-[#f1efe8]">${item.horario}</span>
            </div>

            <div class="flex justify-between py-2.5">
                <span class="text-[#888780]">Valor</span>
                <span class="font-medium text-[#f1efe8]">${item.valor}</span>
            </div>

            <div class="flex justify-between py-2.5">
                <span class="text-[#888780]">Status</span>
                <span class="font-medium text-[#f1efe8]">${item.status}</span>
            </div>

        </div>
    `;

    els.modalHistorico.hidden = false;
}

function fecharModalHistorico() {
    els.modalHistorico.hidden = true;
}

/* ============================================================
   STEPPER
   ============================================================ */

function atualizarStepper() {

    const itens = els.etapa.querySelectorAll(".etapa__item");

    itens.forEach((item, index) => {

        const numero = index + 1;
        const ciclo = item.querySelector(".etapa__ciclo");
        const label = item.querySelector(".etapa__label");

        if (numero < estado.etapaAtual) {

            item.classList.remove("before:bg-brand-border");
            item.classList.add("before:bg-brand-gold");

            ciclo.className = "relative z-10 w-[28px] h-[28px] rounded-full bg-brand-gold border border-brand-gold flex items-center justify-center text-[13px] font-bold text-black etapa__ciclo";

            ciclo.textContent = "✓";

            label.className = "text-brand-gold font-medium etapa__label";

        } else if (numero === estado.etapaAtual) {

            item.classList.remove("before:bg-brand-border");
            item.classList.add("before:bg-brand-gold");

            ciclo.className = "relative z-10 w-[28px] h-[28px] rounded-full bg-brand-gold border border-brand-gold flex items-center justify-center text-[13px] font-bold text-black etapa__ciclo shadow-md shadow-brand-gold/30";

            ciclo.textContent = numero;

            label.className = "text-white font-bold etapa__label";

        } else {

            item.classList.remove("before:bg-brand-gold");
            item.classList.add("before:bg-brand-border");

            ciclo.className = "relative z-10 w-[28px] h-[28px] rounded-full bg-[#111215] border border-brand-border flex items-center justify-center text-[13px] font-medium text-brand-muted etapa__ciclo";

            ciclo.textContent = numero;

            label.className = "text-brand-muted etapa__label";
        }
    });
}

/* ============================================================
   BOTÕES DE NAVEGAÇÃO
   ============================================================ */

function atualizarBotoes() {

    // O botão nunca fica desabilitado.
    // Na primeira etapa, ele permite sair do agendamento.
    els.btnVoltar.disabled = false;

    const podeContinuar = verificarEtapaAtual();

    els.btnContinuar.disabled = !podeContinuar;

    els.btnContinuar.textContent =
        estado.etapaAtual === 4 ? "Finalizar" : "Continuar";

    els.btnVoltar.textContent =
        estado.etapaAtual === 1 ? "Voltar ao Início" : "Voltar";
}

function verificarEtapaAtual() {

    switch (estado.etapaAtual) {

        case 1:
            return estado.servicosSelecionados.length > 0;

        case 2:
            return estado.profissionalSelecionado !== null;

        case 3:
            return estado.diaSelecionado !== null &&
                   estado.horarioSelecionado !== null;

        case 4:
            return true;

        default:
            return false;
    }
}

/* ============================================================
   AVANÇAR / VOLTAR
   ============================================================ */

function avancarEtapa() {

    ocultarMensagemFlash();

    if (estado.etapaAtual === 4) {
        if (!validarFormulario()) {
            mostrarAviso("Verifique os campos destacados");
            return;
        }

        confirmarAgendamento();
        return;
    }

    if (!verificarEtapaAtual()) {
        const mensagens = {
            1: "Selecione um serviço para continuar",
            2: "Selecione um profissional para continuar",
            3: "Selecione um dia e horário para continuar"
        };

        mostrarAviso(mensagens[estado.etapaAtual]);
        return;
    }

    // Impede entrar na etapa de horários sem agenda mensal.
    if (estado.etapaAtual === 2 && !AGENDA_DISPONIVEL) {
        mostrarAviso("Não existe uma agenda disponível para agendamentos.");
        return;
    }

    estado.etapaAtual++;

    if (estado.etapaAtual === 3) {
        renderizarDias();
        renderizarHorarios();
    }

    if (estado.etapaAtual === 4) {
        renderizarResumo();
    }

    mostrarPainel(estado.etapaAtual);
}

function voltarEtapa() {

    // PRIMEIRA ETAPA: RETORNA À PÁGINA INICIAL
    if (estado.etapaAtual === 1) {

        window.location.href = "/";
        return;
    }

    // DEMAIS ETAPAS: RETORNA UMA ETAPA
    estado.etapaAtual--;

    mostrarPainel(estado.etapaAtual);
}

/* ============================================================
   ETAPA 1 — SERVIÇOS
   ============================================================ */

function carregarServicos() {

    if (!els.listaServico) return;

    const inputs = els.listaServico.querySelectorAll(
        "input[name='inputCorte']"
    );

    inputs.forEach(input => {

        input.checked = estado.servicosSelecionados.includes(
            Number(input.value)
        );

        input.addEventListener("change", () => {
            estado.servicosSelecionados = obterServicoSelecionados()
                .map(servico => servico.id);

            ocultarMensagemFlash();

            atualizarBotoes();
        });
    });
}

/* ============================================================
   ETAPA 2 — PROFISSIONAIS
   ============================================================ */

    function carregarProfissionais() {

        if (!els.listaProfissionais) return;

        const inputs = els.listaProfissionais.querySelectorAll(
            "input[name='inputBarbeiro']"
        );

        inputs.forEach(input => {

            input.checked =
                estado.profissionalSelecionado === input.value;

            input.addEventListener("change", () => {

                estado.profissionalSelecionado = input.value;

                atualizarBotoes();
            });
        });
    }

/* ============================================================
   ETAPA 3 — DIAS E HORÁRIOS
   ============================================================ */

function obterDiasDaAgenda() {

    if (!AGENDA_MENSAL) {
        return [];
    }

    const [anoInicial, mesInicial, diaInicial] =
        AGENDA_MENSAL.dataInicial.split("-").map(Number);

    const [anoFinal, mesFinal, diaFinal] =
        AGENDA_MENSAL.dataFinal.split("-").map(Number);

    const inicio = new Date(
        anoInicial, mesInicial - 1, diaInicial
    );

    const fim = new Date(
        anoFinal, mesFinal - 1, diaFinal
    );

    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);

    const dataInicial = inicio < hoje ? hoje : inicio;

    const dias = [];

    for (
        let data = new Date(dataInicial);
        data <= fim;
        data.setDate(data.getDate() + 1)
    ) {
        dias.push(new Date(data));
    }

    return dias;
}


function renderizarDias() {

    if (!els.abasDias) {
        console.error("Elemento abas-dias não encontrado no HTML.");
        return;
    }

    const dias = obterDiasDaAgenda();

    if (dias.length === 0) {
        els.abasDias.innerHTML = `
            <p class="text-brand-muted text-sm">
                Não existem datas disponíveis na agenda.
            </p>
        `;
        return;
    }

    els.abasDias.innerHTML = dias.map(data => {

        const dataISO = [
            data.getFullYear(),
            String(data.getMonth() + 1).padStart(2, "0"),
            String(data.getDate()).padStart(2, "0")
        ].join("-");

        const diaSemana = data.getDay();

        const diaDisponivel =
            DIAS_FUNCIONAMENTO.includes(diaSemana);

        const diaEmRecesso =
            dataEstaEmRecesso(dataISO);

        const diaIndisponivel =
            !diaDisponivel || diaEmRecesso;

        const ativo = estado.diaSelecionado === dataISO;

        return `
            <button
                type="button"
                data-dia="${dataISO}"
                ${diaIndisponivel ? "disabled" : ""}
                class="
                    flex flex-col items-center justify-center
                    min-w-[60px] py-2 px-3 rounded-xl transition-all

                    ${diaIndisponivel
                        ? "bg-[#111215] border border-[#252525] text-[#555] cursor-not-allowed opacity-50"
                        : ativo
                            ? "bg-[#f1efe8] text-[#161513]"
                            : "bg-[#1c1c1c] border-2 border-[#38362f] text-white hover:border-brand-gold"
                    }
                "
                title="${diaEmRecesso ? "Barbearia em recesso" : ""}"
            >
                <span class="text-xs">
                    ${NOMES_DIAS[diaSemana]}
                </span>

                <strong class="text-base">
                    ${data.getDate()}
                </strong>
            </button>
        `;

    }).join("");

    els.abasDias.querySelectorAll("[data-dia]:not(:disabled)")
        .forEach(botao => {

            botao.addEventListener("click", () => {

                estado.diaSelecionado = botao.dataset.dia;
                estado.horarioSelecionado = null;

                renderizarDias();
                renderizarHorarios();
                atualizarBotoes();
            });
        });
}


function renderizarHorarios() {

    if (!els.gradeHorarios) return;

    const horario = obterHorarioBarbeiroSelecionado();

    renderizarInformacoesHorario(horario);

    if (!estado.diaSelecionado) {
        els.gradeHorarios.innerHTML = `
            <p class="col-span-full text-center text-brand-muted text-sm">
                Selecione um dia para visualizar os horários disponíveis.
            </p>
        `;
        return;
    }

    if (dataEstaEmRecesso(estado.diaSelecionado)) {

        els.gradeHorarios.innerHTML = `
            <p class="col-span-full text-center text-brand-muted text-sm">
                A barbearia estará em recesso nesta data.
            </p>
        `;

        estado.horarioSelecionado = null;

        atualizarBotoes();

        return;
    }

    if (!horario) {
        els.gradeHorarios.innerHTML = `
            <p class="col-span-full text-center text-brand-muted text-sm">
                Não foi possível consultar o expediente do profissional.
            </p>
        `;
        return;
    }

    const diaSemana = new Date(
        estado.diaSelecionado + "T12:00:00"
    ).getDay();

    if (!DIAS_FUNCIONAMENTO.includes(diaSemana)) {
        els.gradeHorarios.innerHTML = `
            <p class="col-span-full text-center text-brand-muted text-sm">
                A barbearia não funciona neste dia.
            </p>
        `;
        return;
    }

    const abertura = horarioParaMinutos(horario.horario_abertura);
    const fechamento = horarioParaMinutos(horario.horario_fechamento);

    const inicioIntervalo = horarioParaMinutos(
        horario.horario_inicio_intrajornada
    );

    const fimIntervalo = horarioParaMinutos(
        horario.horario_fim_intrajornada
    );

    const servicos = obterServicoSelecionados();
    const barbeiro = obterBarbeiroSelecionado();

    const duracaoTotal = servicos.reduce(
        (total, servico) => total + servico.duracao,
        0
    );

    const intervalo = 30;

    const horarios = [];

    for (
        let inicio = abertura;
        inicio + duracaoTotal <= fechamento;
        inicio += intervalo
    ) {

        const fim = inicio + duracaoTotal;

        const horarioInicio = minutosParaHorario(inicio);

        // Verifica se o horário já passou.
        if (horarioJaPassou(estado.diaSelecionado, horarioInicio)) {
            continue;
        }

        // Verifica se o atendimento invade o intervalo.
        const invadeIntervalo =
            inicio < fimIntervalo &&
            fim > inicioIntervalo;

        if (invadeIntervalo) continue;

        if (
            barbeiro &&
            horarioEmFaltaJustificada(
                barbeiro.id,
                estado.diaSelecionado,
                inicio,
                fim
            )
        ) {
            continue;
        }

        horarios.push({
            horario: horarioInicio,
            ocupado: horarioEstaOcupado(
                barbeiro.id,
                estado.diaSelecionado,
                inicio,
                fim
            )
        });
    }

    // Horários ocupados devem vir da consulta de agendamentos.
    const ocupados = HORARIOS_OCUPADOS[estado.diaSelecionado] || [];

    els.gradeHorarios.innerHTML = horarios.map(item => {

    const indisponivel = item.ocupado;

    const selecionado =
        estado.horarioSelecionado === item.horario;

        return `
            <button
                type="button"
                data-horario="${item.horario}"
                ${indisponivel ? "disabled" : ""}
                class="
                    rounded-lg p-3 text-sm font-semibold transition-all
                    ${indisponivel
                        ? "bg-[#111215] text-[#777] border border-[#38362f] cursor-not-allowed opacity-60"
                        : selecionado
                            ? "bg-brand-gold text-black border border-brand-gold"
                            : "bg-[#1c1c1c] border border-[#38362f] text-white hover:border-brand-gold"
                    }
                "
                title="${indisponivel ? "Horário já reservado" : "Selecionar horário"}"
            >
                ${item.horario}
                
            </button>
        `;
    }).join("");

els.gradeHorarios
    .querySelectorAll("[data-horario]:not(:disabled)")
    .forEach(botao => {

        botao.addEventListener("click", () => {

            estado.horarioSelecionado = botao.dataset.horario;

            renderizarHorarios();

            atualizarBotoes();
        });
    });

    els.gradeHorarios
        .querySelectorAll("[data-horario]:not(:disabled)")
        .forEach(botao => {

            botao.addEventListener("click", () => {

                estado.horarioSelecionado =
                    botao.dataset.horario;

                renderizarHorarios();

                atualizarBotoes();
            });
        });
}

function obterServicoSelecionados() {
    const inputs = document.querySelectorAll(
        "input[name='inputCorte']:checked"
    );

    return Array.from(inputs).map(input => ({
        id: Number(input.value),
        nome: input.dataset.nome,
        valor: Number(input.dataset.valor),
        duracao: Number(input.dataset.duracao),
        foto: input.dataset.foto
    }));
}

function obterBarbeiroSelecionado() {

    const input = document.querySelector(
        "input[name='inputBarbeiro']:checked"
    );

    if (!input) return null;

    const semPreferencia = input.value === "any";

    return {
        id: semPreferencia ? null : Number(input.value),
        semPreferencia: semPreferencia,
        nome: input.dataset.nome,
        foto: input.dataset.foto
    };
}

function obterHorarioBarbeiroSelecionado() {
    const barbeiro = obterBarbeiroSelecionado();

    if (!barbeiro) return null;

    return HORARIOS_BARBEARIA;
}

function renderizarInformacoesHorario(horario) {

    const elemento = document.getElementById(
        "informacoes-horario"
    );

    if (!elemento) return;

    if (!horario) {
        elemento.innerHTML = `
            <p>Selecione um profissional para consultar os horários.</p>
        `;
        return;
    }

    elemento.innerHTML = `
        <div class="flex flex-wrap gap-x-5 gap-y-2
                    bg-[#1c1c1c] border border-[#38362f]
                    rounded-xl p-3">

            <span>
                <strong class="text-white">Abertura:</strong>
                ${horario.horario_abertura}
            </span>

            <span>
                <strong class="text-white">Fechamento:</strong>
                ${horario.horario_fechamento}
            </span>

            <span>
                <strong class="text-white">Intervalo:</strong>
                ${horario.horario_inicio_intrajornada}
                às
                ${horario.horario_fim_intrajornada}
            </span>

        </div>
    `;
}

function horarioParaMinutos(horario) {
    const [hora, minuto] = horario.split(":").map(Number);

    return hora * 60 + minuto;
}

function minutosParaHorario(minutos) {

    const hora = Math.floor(minutos / 60);
    const minuto = minutos % 60;

    return (
        String(hora).padStart(2, "0") +
        ":" +
        String(minuto).padStart(2, "0")
    );
}

function horarioJaPassou(data, horario) {

    const agora = new Date();

    const [ano, mes, dia] = data.split("-").map(Number);
    const [hora, minuto] = horario.split(":").map(Number);

    const dataHorario = new Date(
        ano,
        mes - 1,
        dia,
        hora,
        minuto
    );

    return dataHorario <= agora;
}

function dataEstaEmRecesso(dataISO) {

    return RECESSOS.some(recesso => {

        return (
            dataISO >= recesso.data_inicio_recesso &&
            dataISO <= recesso.data_fim_recesso
        );

    });

}

function horarioEmFaltaJustificada(idBarbeiro, data, inicio, fim) {

    return FALTAS_BARBEIROS.some(falta => {

        // Verifica se a falta pertence ao barbeiro selecionado.
        if (Number(falta.id_barbeiro) !== Number(idBarbeiro)) {
            return false;
        }

        // Verifica se a falta pertence à data selecionada.
        if (falta.data !== data) {
            return false;
        }

        const inicioFalta = horarioParaMinutos(
            falta.horario_inicio
        );

        const fimFalta = horarioParaMinutos(
            falta.horario_fim
        );

        // Verifica se existe sobreposição entre os horários.
        return inicio < fimFalta && fim > inicioFalta;
    });
}

function horarioEstaOcupado(idBarbeiro, data, inicio, fim) {

    return AGENDAMENTOS.some(agendamento => {

        // Verifica se pertence ao barbeiro selecionado.
        if (
            Number(agendamento.id_barbeiro) !== Number(idBarbeiro)
        ) {
            return false;
        }

        // Verifica se pertence à data selecionada.
        if (agendamento.data !== data) {
            return false;
        }

        const inicioAgendamento = horarioParaMinutos(
            agendamento.horario_inicio
        );

        const fimAgendamento = horarioParaMinutos(
            agendamento.horario_fim
        );

        // Verifica a sobreposição dos horários.
        return inicio < fimAgendamento && fim > inicioAgendamento;
    });
}

function calcularHorarioFinal(horarioInicial, duracaoTotal) {

    const inicio = horarioParaMinutos(horarioInicial);

    const fim = inicio + duracaoTotal;

    return minutosParaHorario(fim);
}

function renderizarResumo() {

    if (!els.resumo) return;

    const servicos = obterServicoSelecionados();
    const profissional = obterBarbeiroSelecionado();

    const formatarMoeda = valor =>
        Number(valor).toLocaleString("pt-BR", {
            style: "currency",
            currency: "BRL"
        });

    const formatarDataCompleta = () => {

        if (!estado.diaSelecionado) return "-";

        const [ano, mes, dia] = estado.diaSelecionado
            .split("-")
            .map(Number);

        return new Date(ano, mes - 1, dia).toLocaleDateString(
            "pt-BR",
            {
                day: "2-digit",
                month: "long",
                year: "numeric"
            }
        );
    };

    // Calcula o valor e a duração de todos os serviços.
    const valorTotal = servicos.reduce(
        (total, servico) => total + servico.valor,
        0
    );

    const duracaoTotal = servicos.reduce(
        (total, servico) => total + servico.duracao,
        0
    );

    // Gera o HTML de cada serviço selecionado.
    const htmlServicos = servicos.map(servico => `
        <div class="bg-[#25241f] rounded-xl p-4
                    border border-[#38362f]">

            <div class="flex justify-between items-center gap-3">

                <div class="flex items-center gap-3 min-w-0">

                    <div class="w-14 h-14 shrink-0 rounded-lg
                                overflow-hidden bg-[#1c1c1c]
                                border border-[#38362f]">

                        <img
                            src="${servico.foto}"
                            alt="${servico.nome}"
                            class="w-full h-full object-cover"
                            onerror="this.style.display='none'"
                        >

                    </div>

                    <div class="min-w-0">

                        <span class="block text-[10px] uppercase
                                     tracking-wider text-[#C9A34A]
                                     font-semibold">
                            Serviço
                        </span>

                        <h3 class="font-semibold text-white">
                            ${servico.nome}
                        </h3>

                        <span class="text-xs text-[#888780]">
                            ${servico.duracao} minutos
                        </span>

                    </div>

                </div>

                <strong class="text-[#C9A34A] whitespace-nowrap">
                    ${formatarMoeda(servico.valor)}
                </strong>

            </div>

        </div>
    `).join("");

    const dados = {
        profissional: profissional?.nome || "-",
        fotoProfissional: profissional?.foto || "",
        data: formatarDataCompleta(),
        horario: estado.horarioSelecionado || "-"
    };

    els.resumo.innerHTML = `

        <div class="bg-[#1c1c1c] border border-[#38362f]
                    rounded-2xl p-4 sm:p-5 space-y-5">

            <!-- CABEÇALHO -->
            <div class="flex items-center justify-between gap-3">

                <div>
                    <h2 class="text-base font-semibold text-white">
                        Resumo do agendamento
                    </h2>

                    <p class="text-xs text-[#888780] mt-1">
                        Confira os dados do atendimento
                    </p>
                </div>

                <div class="w-10 h-10 rounded-xl bg-[#C9A34A]/10
                            flex items-center justify-center">
                    <i class="fa-solid fa-calendar-check
                              text-[#C9A34A] text-lg"></i>
                </div>

            </div>

            <!-- SERVIÇOS SELECIONADOS -->
            <div class="space-y-3">

                <div class="flex justify-between items-center">

                    <h3 class="text-sm font-semibold text-white">
                        Serviços selecionados
                    </h3>

                    <span class="text-xs text-[#888780]">
                        ${servicos.length} serviço(s)
                    </span>

                </div>

                ${htmlServicos || `
                    <p class="text-sm text-[#888780]">
                        Nenhum serviço selecionado.
                    </p>
                `}

            </div>

            <!-- PROFISSIONAL -->
            <div class="flex items-center gap-3">

                <div class="w-12 h-12 shrink-0 rounded-full
                            overflow-hidden bg-[#25241f]
                            border border-[#38362f]">

                    <img
                        src="${dados.fotoProfissional}"
                        alt="${dados.profissional}"
                        class="w-full h-full object-cover"
                        onerror="this.style.display='none'"
                    >

                </div>

                <div class="min-w-0">

                    <span class="block text-[10px] uppercase
                                 tracking-wider text-[#888780]">
                        Profissional
                    </span>

                    <strong class="text-sm text-white">
                        ${dados.profissional}
                    </strong>

                </div>

            </div>

            <!-- DATA E HORÁRIO -->
            <div class="grid grid-cols-2 gap-3">

                <div class="bg-[#25241f] rounded-xl p-3
                            border border-[#38362f]">

                    <div class="flex items-center gap-2 mb-2">
                        <i class="fa-regular fa-calendar
                                  text-[#C9A34A]"></i>

                        <span class="text-[10px] uppercase
                                     tracking-wider text-[#888780]">
                            Data
                        </span>
                    </div>

                    <strong class="text-sm text-white capitalize">
                        ${dados.data}
                    </strong>

                </div>

                <div class="bg-[#25241f] rounded-xl p-3
                            border border-[#38362f]">

                    <div class="flex items-center gap-2 mb-2">
                        <i class="fa-regular fa-clock
                                  text-[#C9A34A]"></i>

                        <span class="text-[10px] uppercase
                                     tracking-wider text-[#888780]">
                            Horário
                        </span>
                    </div>

                    <strong class="text-sm text-white">
                        ${dados.horario}
                    </strong>

                </div>

            </div>

            <!-- DURAÇÃO TOTAL -->
            <div class="flex justify-between items-center
                        border-t border-[#38362f] pt-4">

                <span class="text-sm text-[#888780]">
                    Duração total
                </span>

                <strong class="text-white">
                    ${duracaoTotal} minutos
                </strong>

            </div>

            <!-- VALOR TOTAL -->
            <div class="flex items-center justify-between gap-3">

                <div>
                    <span class="block text-sm font-semibold text-white">
                        Total do atendimento
                    </span>

                    <span class="text-xs text-[#888780]">
                        Soma de todos os serviços
                    </span>
                </div>

                <strong class="text-xl sm:text-2xl
                               text-[#C9A34A] whitespace-nowrap">
                    ${formatarMoeda(valorTotal)}
                </strong>

            </div>

            <!-- AVISO -->
            <div class="flex items-start gap-2 bg-[#C9A34A]/5
                        border border-[#C9A34A]/20 rounded-lg p-3">

                <i class="fa-solid fa-circle-info
                          text-[#C9A34A] mt-0.5"></i>

                <p class="text-xs text-[#aaa69a] leading-relaxed">
                    Verifique todas as informações antes de confirmar.
                    O agendamento estará sujeito à validação final
                    de disponibilidade.
                </p>

            </div>

        </div>
    `;
}



/* ============================================================
   ETAPA 4 — RESUMO
   ============================================================ */

function formatarData() {
    if (!estado.diaSelecionado) return "-";

    const [ano, mes, dia] = estado.diaSelecionado
        .split("-")
        .map(Number);

    return new Date(ano, mes - 1, dia).toLocaleDateString("pt-BR", {
        weekday: "long",
        day: "2-digit",
        month: "long"
    });
}

/* ============================================================
   VALIDAÇÃO DO FORMULÁRIO
   ============================================================ */

function limparErro(input, erroEl) {

    input.classList.remove("invalido");

    erroEl.textContent = "";
}

function definirErro(input, erroEl, mensagem) {

    input.classList.add("invalido");

    erroEl.textContent = mensagem;
}

function validarFormulario() {

    let valido = true;

    return valido;
}

/* ============================================================
   CONFIRMAÇÃO FINAL
   ============================================================ */

async function confirmarAgendamento() {

    const servicos = obterServicoSelecionados();
    const barbeiro = obterBarbeiroSelecionado();

    if (
        servicos.length === 0 ||
        !barbeiro ||
        !estado.diaSelecionado ||
        !estado.horarioSelecionado
    ) {
        mostrarAviso("Preencha todos os dados do agendamento.");
        return;
    }

    const duracaoTotal = servicos.reduce(
        (total, servico) => total + servico.duracao,
        0
    );

    const horarioFinal = calcularHorarioFinal(
        estado.horarioSelecionado,
        duracaoTotal
    );

    els.btnContinuar.disabled = true;
    els.btnContinuar.textContent = "Agendando...";

    try {

        const resposta = await fetch(URL_CADASTRAR_AGENDAMENTO, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id_servicos: servicos.map(servico => servico.id),
                id_barbeiro: barbeiro.id,
                data: estado.diaSelecionado,
                horario_inicio: estado.horarioSelecionado,
                horario_fim: horarioFinal
            })
        });

        const dados = await resposta.json();

        if (!resposta.ok && resposta.status !== 409) {
            throw new Error(
                dados.erro || "Não foi possível realizar o agendamento."
            );
        }

        // Marca que as seleções devem ser limpas ao carregar a página.
        if (dados.limpar_selecao) {
            sessionStorage.setItem("limparAgendamento", "true");
        }

        // Navega somente agora para a página desejada.
        window.location.href = dados.redirect_url;

    } catch (erro) {

        mostrarAviso(erro.message);

        els.btnContinuar.disabled = false;
        els.btnContinuar.textContent = "Finalizar";
    }
}

function ocultarMensagemFlash() {
    const mensagens = document.getElementById("mensagens-flash");

    if (mensagens) {
        mensagens.style.transition = "opacity 0.3s ease";
        mensagens.style.opacity = "0";

        setTimeout(() => {
            mensagens.remove();
        }, 300);
    }
}

function limparSelecaoAgendamento() {

    // Limpa o estado do wizard.
    estado.etapaAtual = 1;
    estado.servicosSelecionados = [];
    estado.profissionalSelecionado = null;
    estado.diaSelecionado = null;
    estado.horarioSelecionado = null;
    estado.agendamentoConcluido = false;

    // Desmarca os serviços.
    document.querySelectorAll(
        "input[name='inputCorte']"
    ).forEach(input => {
        input.checked = false;
    });

    // Desmarca os barbeiros.
    document.querySelectorAll(
        "input[name='inputBarbeiro']"
    ).forEach(input => {
        input.checked = false;
    });

    // Volta para a primeira etapa.
    mostrarPainel(1);
    atualizarBotoes();
}

/* ============================================================
   REINICIAR E INICIALIZAÇÃO
   ============================================================ */

function reiniciar() {

    estado.etapaAtual = 1;
    estado.servicosSelecionados = [];
    estado.profissionalSelecionado = null;
    estado.diaSelecionado = null;
    estado.horarioSelecionado = null;
    estado.agendamentoConcluido = false;

    limparSelecaoAgendamento();

    if (els.navEtapa) els.navEtapa.hidden = false;
    if (els.etapa) els.etapa.hidden = false;
    if (els.sucesso) els.sucesso.hidden = true;

    mostrarPainel(1);
}

function iniciar() {

    if (limparAoCarregar) {
        sessionStorage.removeItem("limparAgendamento");
        limparSelecaoAgendamento();
    }
    carregarServicos();

    carregarProfissionais();

    if (els.btnVoltar) {
        els.btnVoltar.addEventListener("click", voltarEtapa);
    }

    if (els.btnContinuar) {
        els.btnContinuar.addEventListener("click", avancarEtapa);
    }

    if (els.btnHistorico) {
        els.btnHistorico.addEventListener("click", alternarHistorico);
    }

    if (els.btnVoltarInicio) {
        els.btnVoltarInicio.addEventListener("click", reiniciar);
    }

    mostrarPainel(estado.etapaAtual);
}

document.addEventListener("DOMContentLoaded", iniciar);

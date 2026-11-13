
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
    servicoSelecionado: null,
    profissionalSelecionado: null,
    diaSelecionado: null,
    horarioSelecionado: null,
    agendamentoConcluido: false,
    nome: "Maicon Rocha"
};

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
            return estado.servicoSelecionado !== null;

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

    if (!AGENDA_DISPONIVEL) {
        return;
    }

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

        input.checked = estado.servicoSelecionado === input.value;

        input.addEventListener("change", () => {

            estado.servicoSelecionado = input.value;

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

        const ativo = estado.diaSelecionado === dataISO;

        return `
            <button
                type="button"
                data-dia="${dataISO}"
                class="flex flex-col items-center justify-center
                       min-w-[60px] py-2 px-3 rounded-xl
                       ${ativo
                           ? "bg-[#f1efe8] text-[#161513]"
                           : "bg-[#1c1c1c] border-2 border-[#38362f] text-white"}"
            >
                <span class="text-xs">
                    ${NOMES_DIAS[data.getDay()]}
                </span>

                <strong class="text-base">
                    ${data.getDate()}
                </strong>
            </button>
        `;

    }).join("");

    els.abasDias.querySelectorAll("[data-dia]").forEach(botao => {

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

    if (!estado.diaSelecionado) {
        els.gradeHorarios.innerHTML = `
            <p class="col-span-full text-center text-brand-muted text-sm">
                Selecione um dia para visualizar os horários disponíveis.
            </p>
        `;
        return;
    }

    // Temporário: utiliza os horários fictícios existentes no arquivo.
    const dia = new Date(
        estado.diaSelecionado + "T12:00:00"
    ).getDay();

    const ocupados = HORARIOS_OCUPADOS[dia] || [];

    els.gradeHorarios.innerHTML = TODOS_HORARIOS.map(horario => {

        const indisponivel = ocupados.includes(horario);
        const selecionado = estado.horarioSelecionado === horario;

        return `
            <button
                type="button"
                data-horario="${horario}"
                ${indisponivel ? "disabled" : ""}
                class="
                    rounded-lg p-3 text-sm font-semibold transition-all
                    ${indisponivel
                        ? "bg-[#111215] text-[#555] cursor-not-allowed line-through"
                        : selecionado
                            ? "bg-brand-gold text-black border border-brand-gold"
                            : "bg-[#1c1c1c] border border-[#38362f] text-white hover:border-brand-gold"
                    }
                "
            >
                ${horario}
            </button>
        `;

    }).join("");

    els.gradeHorarios.querySelectorAll("[data-horario]").forEach(botao => {

        botao.addEventListener("click", () => {

            estado.horarioSelecionado = botao.dataset.horario;

            renderizarHorarios();

            atualizarBotoes();
        });

    });
}

function obterServicoSelecionado() {
    const input = document.querySelector(
        "input[name='inputCorte']:checked"
    );

    if (!input) return null;

    return {
        id: Number(input.value),
        nome: input.dataset.nome,
        valor: Number(input.dataset.valor),
        duracao: Number(input.dataset.duracao),
        foto: input.dataset.foto
    };
}

function obterBarbeiroSelecionado() {
    const input = document.querySelector(
        "input[name='inputBarbeiro']:checked"
    );

    if (!input) return null;

    return {
        id: Number(input.value),
        nome: input.dataset.nome,
        foto: input.dataset.foto
    };
}

function renderizarResumo() {
    if (!els.resumo) return;

    const servico = obterServicoSelecionado();
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

    const dados = {
        servico: servico?.nome || "-",
        duracao: servico?.duracao || 0,
        valor: servico?.valor || 0,
        fotoServico: servico?.foto || "",
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

            <!-- SERVIÇO -->
            <div class="bg-[#25241f] rounded-xl p-4
                        border border-[#38362f]">

                <div class="flex justify-between items-center gap-3">

                    <div class="flex items-center gap-3 min-w-0">

                        <div class="w-14 h-14 shrink-0 rounded-lg
                                    overflow-hidden bg-[#1c1c1c]
                                    border border-[#38362f]">

                            <img
                                src="${dados.fotoServico}"
                                alt="${dados.servico}"
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

                            <h3 class="font-semibold text-white truncate">
                                ${dados.servico}
                            </h3>

                            <span class="text-xs text-[#888780]">
                                ${dados.duracao} minutos
                            </span>
                        </div>

                    </div>

                    <strong class="text-[#C9A34A] whitespace-nowrap">
                        ${formatarMoeda(dados.valor)}
                    </strong>

                </div>
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

            <!-- TOTAL -->
            <div class="border-t border-[#38362f] pt-4
                        flex items-center justify-between gap-3">

                <div>
                    <span class="block text-sm font-semibold text-white">
                        Total do atendimento
                    </span>

                    <span class="text-xs text-[#888780]">
                        Valor do serviço selecionado
                    </span>
                </div>

                <strong class="text-xl sm:text-2xl
                               text-[#C9A34A] whitespace-nowrap">
                    ${formatarMoeda(dados.valor)}
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

    const servico = obterServicoSelecionado();
    const barbeiro = obterBarbeiroSelecionado();

    if (
        !servico ||
        !barbeiro ||
        !estado.diaSelecionado ||
        !estado.horarioSelecionado
    ) {
        mostrarAviso("Preencha todos os dados do agendamento.");
        return;
    }

    els.btnContinuar.disabled = true;
    els.btnContinuar.textContent = "Agendando...";

    try {

        const resposta = await fetch(URL_CADASTRAR_AGENDAMENTO, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id_servico: servico.id,
                id_barbeiro: barbeiro.id,
                data: estado.diaSelecionado,
                horario: estado.horarioSelecionado
            })
        });

        if (!resposta.ok) {
            throw new Error("Não foi possível realizar o agendamento.");
        }

        // Navega para a página para a qual o Flask redirecionou.
        window.location.href = resposta.url;

    } catch (erro) {

        mostrarAviso(erro.message);

        els.btnContinuar.disabled = false;
        els.btnContinuar.textContent = "Finalizar";
    }
}

/* ============================================================
   REINICIAR E INICIALIZAÇÃO
   ============================================================ */

function reiniciar() {

    estado.etapaAtual = 1;

    estado.servicoSelecionado = null;

    estado.profissionalSelecionado = null;

    estado.diaSelecionado = null;

    estado.horarioSelecionado = null;

    estado.agendamentoConcluido = false;

    if (els.navEtapa) els.navEtapa.hidden = false;

    if (els.etapa) els.etapa.hidden = false;

    if (els.sucesso) els.sucesso.hidden = true;

    carregarServicos();

    carregarProfissionais();

    mostrarPainel(1);
}

function iniciar() {

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

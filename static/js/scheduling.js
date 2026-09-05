/* ============================================================
   DADOS
   ============================================================ */

   const SERVICOS = [
    { id: "infantil",       name: "Corte Infantil",      duration: 30, price: 20, icon: "../static/assets/img/cortes/corte-infantil.jpeg",        alt: "corte-infantil" },
    { id: "social",         name: "Corte Social",        duration: 30, price: 18, icon: "../static/assets/img/cortes/corte-social.jpeg",           alt: "corte-social" },
    { id: "social-barba",   name: "Social & Barba",    duration: 50, price: 30, icon: "../static/assets/img/cortes/corte-social&barba.jpeg",     alt: "corte-social-barba" },
    { id: "degrade",        name: "Degradê",           duration: 40, price: 22, icon: "../static/assets/img/cortes/corte-degrade.jpeg",          alt: "corte-degrade" },
    { id: "degrade-barba",  name: "Degradê & Barba",   duration: 60, price: 30, icon: "../static/assets/img/cortes/corte-degradê&barba.jpeg",   alt: "corte-degrade-barba" },
    { id: "militar",        name: "Corte Militar",     duration: 20, price: 15, icon: "../static/assets/img/cortes/corte-militar.jpeg",          alt: "corte-militar" },
    { id: "barba",          name: "Barba",             duration: 25, price: 15, icon: "../static/assets/img/cortes/corte-barba.jpeg",            alt: "corte-barba" },
];

const PROFISSIONAIS = [
    { id: "any",    name: "Sem preferência", description: "Qualquer profissional disponível", icon: "", alt: "" },
    { id: "thiago", name: "Thiago Tomaz",          description: "Barbeiro sênior",                  icon: "../static/assets/img/funcionarios/thiago.jpg", alt: "thiago" },
    { id: "samuel", name: "Samuel",                description: "Barbeiro sênior",                  icon: "../static/assets/img/funcionarios/samuel.jpg", alt: "samuel" },
    { id: "maik",   name: "Maik",                  description: "Barbeiro novato",                  icon: "../static/assets/img/funcionarios/maik.png",   alt: "maik" },
];

const NOMES_DIAS = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

const TODOS_HORARIOS = [
    "09:00", "09:30", "10:00", "10:30", "11:00",
    "13:00", "13:30", "14:00", "14:30",
    "15:00", "15:30", "16:00", "16:30", "17:00"
];

const HORARIOS_OCUPADOS = {
    0: ["09:00", "09:30", "14:00"],
    1: ["10:00", "10:30"],
    2: [],
    3: ["13:00", "13:30"],
    4: ["15:00", "15:30"],
    5: ["14:00"],
    6: TODOS_HORARIOS
};

const historicoCortes = [ // dadosIniciais <- Nome antigo
    {
        id: "101",
        servico: "Social & Barba",
        profissional: "Thiago Tomaz",
        data: "Sábado, 15 de Agosto",
        horario: "14:00",
        valor: "R$ 30,00",
        status: "Concluído"
    },
    {
        id: "102",
        servico: "Degradê",
        profissional: "Samuel",
        data: "Quinta-feira, 20 de Agosto",
        horario: "10:30",
        valor: "R$ 22,00",
        status: "Concluído"
    },
    {
        id: "103",
        servico: "Corte Militar",
        profissional: "Maik",
        data: "Sexta-feira, 28 de Agosto",
        horario: "16:00",
        valor: "R$ 15,00",
        status: "Confirmado"
    }
];

// 

/* ============================================================
   ESTADO
   ============================================================ */

const estado = {
    etapaAtual:              1,
    servicoSelecionado:      null,
    profissionalSelecionado: null,
    diaSelecionado:          null,
    horarioSelecionado:      null,
    nome:                   "Maicon Rocha"
};

/* ============================================================
   ELEMENTOS
   ============================================================ */

const els = {
    etapa:              document.getElementById("etapa"),
    listaServico:       document.getElementById("lista-servico"),
    listaProfissionais: document.getElementById("lista-profissionais"),
    abasDias:           document.getElementById("abas-dias"),
    gradeHorarios:      document.getElementById("grade-horarios"),
    resumo:             document.getElementById("resumo"),
    btnVoltar:          document.getElementById("btn-voltar"),
    btnContinuar:       document.getElementById("btn-continuar"),
    navEtapa:           document.getElementById("nav-etapa"),
    aviso:              document.getElementById("aviso"),
    sucesso:            document.getElementById("painel-sucesso"),
    sucessoTexto:       document.getElementById("sucesso-texto"),
    btnHistorico:       document.getElementById("btn-historico"),
    painelHistorico:    document.getElementById("painel-historico"),
    listaHistorico:     document.getElementById("lista-historico"),
    modalHistorico:     document.getElementById("modal-historico"),
    resumoModal:        document.getElementById("resumo-modal-conteudo")
};

const form = {
    // nome:           document.getElementById("inp-nome"),
    // tel:            document.getElementById("inp-tel"),
    //email:           document.getElementById("inp-email"),
    //consentimento:     document.getElementById("inp-consentimento"),
    // erroNome:       document.getElementById("erro-nome"),
    // erroTel:        document.getElementById("erro-tel"),
    //erroEmail:       document.getElementById("erro-email"),
    //erroConsentimento: document.getElementById("erro-consentimento"),
};

/* ============================================================
   LOCALSTORAGE & HISTÓRICO INITIALIZATION
   ============================================================ */

// function inicializarLocalStorage() { ANTIGO NOME DA FUNÇÃO
//     if (!localStorage.getItem("historicoAgendamentos")) {
//         const dadosIniciais = [
//             {
//                 id: "101",
//                 servico: "Social & Barba",
//                 profissional: "Thiago Tomaz",
//                 data: "Sábado, 15 de Agosto",
//                 horario: "14:00",
//                 valor: "R$ 30,00",
//                 status: "Concluído"
//             },
//             {
//                 id: "102",
//                 servico: "Degradê",
//                 profissional: "Samuel",
//                 data: "Quinta-feira, 20 de Agosto",
//                 horario: "10:30",
//                 valor: "R$ 22,00",
//                 status: "Concluído"
//             },
//             {
//                 id: "103",
//                 servico: "Corte Militar",
//                 profissional: "Maik",
//                 data: "Sexta-feira, 28 de Agosto",
//                 horario: "16:00",
//                 valor: "R$ 15,00",
//                 status: "Confirmado"
//             }
//         ];
//         localStorage.setItem("historicoAgendamentos", JSON.stringify(dadosIniciais));
//     }
// }

// function obterHistorico() {
//     return JSON.parse(localStorage.getItem("historicoAgendamentos")) || [];
// }

function salvarNoHistorico(novoItem) {
    // const historico = obterHistorico();
    const historico = historicoCortes;
    historico.unshift(novoItem);
    localStorage.setItem("historicoAgendamentos", JSON.stringify(historico));
}

/* ============================================================
   AVISO (toast)
   ============================================================ */

function mostrarAviso(mensagem) {
    els.aviso.textContent = mensagem;
    els.aviso.classList.add("visivel");
    setTimeout(() => els.aviso.classList.remove("visivel"), 2500);
}

/* ============================================================
   CONTROLE DE PAINÉIS
   ============================================================ */

function mostrarPainel(numero) {
    for (let i = 1; i <= 4; i++) {
        const painel = document.getElementById(`painel-${i}`);
        if (painel) painel.hidden = i !== numero;
    }
    els.sucesso.hidden = true;
    if (els.painelHistorico) els.painelHistorico.hidden = true;
    atualizarStepper();
    atualizarBotoes();
    window.scrollTo({ top: 0, behavior: "smooth" });
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
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function voltarParaAgendamento() {
    els.painelHistorico.hidden = true;
    els.etapa.hidden = false;
    els.navEtapa.hidden = false;
    mostrarPainel(estado.etapaAtual);
}

function carregarHistorico() {
    const historico = historicoCortes;

    if (historico.length === 0) {
        els.listaHistorico.innerHTML = `<p class="text-[#888780] text-sm text-center">Nenhum agendamento encontrado.</p>`;
        return;
    }

    els.listaHistorico.innerHTML = historico.map(item => `
        <div class="bg-[#1c1c1c] border border-[#38362f] rounded-xl p-4 flex flex-col gap-3 hover:border-[#4a473f] cursor-pointer transition-all" onclick="exibirDetalhesHistorico('${item.id}')">
            <div class="flex justify-between items-center border-b border-[#2e2d29] pb-2">
                <span class="font-medium text-[#f1efe8] text-[15px]">${item.servico}</span>
                <span class="text-[12px] px-2 py-0.5 rounded-full font-medium ${item.status === 'Concluído' ? 'bg-green-900/40 text-green-400 border border-green-800' : 'bg-amber-900/40 text-amber-400 border border-amber-800'}">${item.status}</span>
            </div>
            <div class="flex flex-col gap-1 text-[13px] text-[#888780]">
                <span><strong class="text-[#f1efe8]">Profissional:</strong> ${item.profissional}</span>
                <span><strong class="text-[#f1efe8]">Data:</strong> ${item.data}</span>
                <span><strong class="text-[#f1efe8]">Horário:</strong> ${item.horario}</span>
            </div>
            <div class="flex justify-between items-center pt-2 border-t border-[#2e2d29]">
                <span class="font-bold text-[#f1efe8] text-[14px]">${item.valor}</span>
                <span class="text-[12px] text-[#9fe1cb] hover:underline">Ver resumo &rarr;</span>
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
            // ETAPA CONCLUÍDA: Verde preenchido com ícone de check
            item.classList.remove("before:bg-[#4a473f]");
            item.classList.add("before:bg-[#0f6e56]");

            ciclo.className = "relative z-10 w-[28px] h-[28px] rounded-full bg-[#0f6e56] border border-[#0f6e56] flex items-center justify-center text-[13px] font-bold text-white etapa__ciclo";
            ciclo.textContent = "✓";

            label.className = "text-[#9fe1cb] font-medium etapa__label";

        } else if (numero === estado.etapaAtual) {
            // ETAPA ATIVA: Verde destacado com borda
            item.classList.remove("before:bg-[#4a473f]");
            item.classList.add("before:bg-[#0f6e56]");

            ciclo.className = "relative z-10 w-[28px] h-[28px] rounded-full bg-[#085041] border border-[#0f6e56] flex items-center justify-center text-[13px] font-medium text-[#9fe1cb] etapa__ciclo";
            ciclo.textContent = numero;

            label.className = "text-[#f1efe8] font-medium etapa__label";

        } else {
            // ETAPA PENDENTE: Cinza escuro desativado
            item.classList.remove("before:bg-[#0f6e56]");
            item.classList.add("before:bg-[#4a473f]");

            ciclo.className = "relative z-10 w-[28px] h-[28px] rounded-full bg-[#232220] border border-[#4a473f] flex items-center justify-center text-[13px] font-medium text-[#888780] etapa__ciclo";
            ciclo.textContent = numero;

            label.className = "text-[#888780] etapa__label";
        }
    });
}

/* ============================================================
   BOTÕES DE NAVEGAÇÃO
   ============================================================ */

function atualizarBotoes() {
    els.btnVoltar.disabled = estado.etapaAtual === 1;

    const podeContinuar = verificarEtapaAtual();
    els.btnContinuar.disabled = !podeContinuar;

    els.btnContinuar.textContent =
        estado.etapaAtual === 4 ? "Confirmar agendamento" : "Continuar";
}

function verificarEtapaAtual() {
    switch (estado.etapaAtual) {
        case 1: return estado.servicoSelecionado !== null;
        case 2: return estado.profissionalSelecionado !== null;
        case 3: return estado.diaSelecionado !== null && estado.horarioSelecionado !== null;
        case 4: return true;
        default: return false;
    }
}

/* ============================================================
   AVANÇAR / VOLTAR
   ============================================================ */

function avancarEtapa() {
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
            3: "Selecione um dia e horário para continuar",
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
    if (estado.etapaAtual > 1) {
        estado.etapaAtual--;
        mostrarPainel(estado.etapaAtual);
    }
}

/* ============================================================
   ETAPA 1 — SERVIÇOS
   ============================================================ */

function carregarServicos() {
    els.listaServico.innerHTML = SERVICOS.map(servico => `
        <label class="cursor-pointer shrink-0">
            <input type="radio" name="inputCorte" id="${servico.id}" class="peer hidden" value="${servico.id}">
            <div class="w-[150px] bg-[#1c1c1c] border-2 border-[#2a2825] rounded-xl p-3 flex flex-col items-center gap-2 transition-all peer-checked:border-[#0f6e56] peer-checked:bg-[#0d2b24] hover:border-[#4a473f]">
                <img src="${servico.icon}" alt="${servico.alt}" class="w-full h-full object-cover rounded-lg">
                <span class="font-medium text-[13px] text-[#f1efe8] text-center peer-checked:text-[#9fe1cb]">${servico.name}</span>
                <div class="flex justify-between w-full text-[12px] text-[#888780] pt-1 border-t border-[#2e2d29]">
                    <span>${servico.duration} min</span>
                    <span class="font-medium text-[#f1efe8]">R$ ${servico.price.toFixed(2).replace(".", ",")}</span>
                </div>
            </div>
        </label>
    `).join("");

    els.listaServico.querySelectorAll("input[type='radio']").forEach(input => {
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
    els.listaProfissionais.innerHTML = PROFISSIONAIS.map(profissional => `
        <label class="cursor-pointer shrink-0">
            <input type="radio" name="inputFuncionario" id="${profissional.id}" class="peer hidden" value="${profissional.id}">
            <div class="w-[150px] h-[210px] bg-[#1c1c1c] border-2 border-[#2a2825] rounded-xl p-3 flex flex-col items-center justify-between text-center transition-all peer-checked:border-[#0f6e56] peer-checked:bg-[#0d2b24] hover:border-[#4a473f]">
                <div class="w-full h-full rounded-lg bg-[#232220] flex items-center justify-center overflow-hidden">
                    ${profissional.icon
                        ? `<img src="${profissional.icon}" alt="${profissional.alt}" class="w-full h-full object-cover">`
                        : `<div class="w-full h-full flex items-center justify-center text-[#f1efe8] font-bold text-xl">${profissional.name.charAt(0)}</div>`
                    }
                </div>
                <div>
                    <h3 class="font-medium text-[13px] text-[#f1efe8] peer-checked:text-[#9fe1cb] pt-1">${profissional.name}</h3>
                    <p class="text-[11px] text-[#888780] mt-0.5">${profissional.description}</p>
                </div>
            </div>
        </label>
    `).join("");

    els.listaProfissionais.querySelectorAll("input[type='radio']").forEach(input => {
        input.addEventListener("change", () => {
            estado.profissionalSelecionado = input.value;
            atualizarBotoes();
        });
    });
}

/* ============================================================
   ETAPA 3 — DIAS E HORÁRIOS
   ============================================================ */

function obterProximosDias() {
    const dias = [];
    const hoje = new Date();
    for (let i = 0; i < 7; i++) {
        const data = new Date();
        data.setDate(hoje.getDate() + i);
        dias.push(data);
    }
    return dias;
}

function renderizarDias() {
    const dias = obterProximosDias();
    els.abasDias.innerHTML = dias.map((data, indice) => {
        const fechado = HORARIOS_OCUPADOS[indice]?.length === TODOS_HORARIOS.length;
        const ativo = estado.diaSelecionado === indice;

        const classeEstado = ativo
            ? "bg-[#f1efe8] text-[#161513] border-[#f1efe8]"
            : "bg-[#1c1c1c] border-[#38362f] text-[#f1efe8] hover:border-[#888780]";

        return `
            <button
                class="flex flex-col items-center justify-center min-w-[60px] py-2 px-3 rounded-xl border transition-all ${classeEstado} ${fechado ? "opacity-35 cursor-not-allowed" : ""}"
                data-dia="${indice}"
                ${fechado ? "disabled" : ""}
            >
                <span class="text-[12px] uppercase font-medium">${NOMES_DIAS[data.getDay()]}</span>
                <strong class="text-[16px] font-bold">${data.getDate()}</strong>
            </button>
        `;
    }).join("");

    els.abasDias.querySelectorAll("[data-dia]").forEach(botao => {
        botao.addEventListener("click", () => {
            estado.diaSelecionado = Number(botao.dataset.dia);
            estado.horarioSelecionado = null;
            renderizarDias();
            renderizarHorarios();
            atualizarBotoes();
        });
    });
}

function renderizarHorarios() {
    if (estado.diaSelecionado === null) {
        els.gradeHorarios.innerHTML = `<p class="text-[#888780] text-sm text-center col-span-full">Escolha um dia para visualizar os horários.</p>`;
        return;
    }

    const ocupados = HORARIOS_OCUPADOS[estado.diaSelecionado] || [];

    els.gradeHorarios.innerHTML = TODOS_HORARIOS.map(horario => {
        const ocupado = ocupados.includes(horario);
        const ativo = estado.horarioSelecionado === horario;

        let classeEstado = "bg-[#1c1c1c] border-[#38362f] text-[#f1efe8] hover:border-[#888780]";
        if (ativo) {
            classeEstado = "bg-[#085041] border-[#0f6e56] text-[#9fe1cb] font-medium";
        } else if (ocupado) {
            classeEstado = "bg-[#1c1c1c] border-[#38362f] text-[#f1efe8] opacity-35 line-through cursor-not-allowed";
        }

        return `
            <button
                class="py-2.5 px-3 border rounded-xl text-[14px] text-center transition-all ${classeEstado}"
                data-horario="${horario}"
                ${ocupado ? "disabled" : ""}
            >
                ${horario}
            </button>
        `;
    }).join("");

    els.gradeHorarios.querySelectorAll("[data-horario]:not(:disabled)").forEach(botao => {
        botao.addEventListener("click", () => {
            estado.horarioSelecionado = botao.dataset.horario;
            renderizarHorarios();
            atualizarBotoes();
        });
    });
}

/* ============================================================
   ETAPA 4 — RESUMO
   ============================================================ */

function formatarData() {
    const dias = obterProximosDias();
    const data = dias[estado.diaSelecionado];
    return data.toLocaleDateString("pt-BR", { weekday: "long", day: "2-digit", month: "long" });
}

function renderizarResumo() {
    const servico = SERVICOS.find(s => s.id === estado.servicoSelecionado);
    const profissional = PROFISSIONAIS.find(p => p.id === estado.profissionalSelecionado);

    els.resumo.innerHTML = `
        <div class="divide-y divide-[#38362f] text-[14px]">
            <div class="flex justify-between py-2.5">
                <span class="text-[#888780]">Serviço</span>
                <span class="font-medium text-[#f1efe8]">${servico.name}</span>
            </div>
            <div class="flex justify-between py-2.5">
                <span class="text-[#888780]">Profissional</span>
                <span class="font-medium text-[#f1efe8]">${profissional.name}</span>
            </div>
            <div class="flex justify-between py-2.5">
                <span class="text-[#888780]">Data</span>
                <span class="font-medium text-[#f1efe8]">${formatarData()}</span>
            </div>
            <div class="flex justify-between py-2.5">
                <span class="text-[#888780]">Horário</span>
                <span class="font-medium text-[#f1efe8]">${estado.horarioSelecionado}</span>
            </div>
            <div class="flex justify-between py-2.5">
                <span class="text-[#888780]">Valor</span>
                <span class="font-medium text-[#f1efe8]">R$ ${servico.price.toFixed(2).replace(".", ",")}</span>
            </div>
        </div>
    `;
}

/* ============================================================
   MÁSCARA DE TELEFONE
   ============================================================ */

// form.tel.addEventListener("input", () => {
//     let digitos = form.tel.value.replace(/\D/g, "").slice(0, 11);
//     if (digitos.length > 6) {
//         digitos = digitos.replace(/^(\d{2})(\d{5})(\d{0,4})/, "($1) $2-$3");
//     } else if (digitos.length > 2) {
//         digitos = digitos.replace(/^(\d{2})(\d{0,5})/, "($1) $2");
//     } else {
//         digitos = digitos.replace(/^(\d{0,2})/, "($1");
//     }
//     form.tel.value = digitos;
// });

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

    // limparErro(form.nome, form.erroNome);
    // limparErro(form.tel, form.erroTel);
    //limparErro(form.email, form.erroEmail);
    //form.erroConsentimento.textContent = "";

    // if (form.nome.value.trim().length < 3) {
    //     definirErro(form.nome, form.erroNome, "Informe seu nome completo");
    //     valido = false;
    // }

    // const digitos = form.tel.value.replace(/\D/g, "");
    // if (digitos.length < 10) {
    //     definirErro(form.tel, form.erroTel, "Informe um telefone válido com DDD");
    //     valido = false;
    // }

    /*const emailValor = form.email.value.trim();
    if (emailValor && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailValor)) {
        definirErro(form.email, form.erroEmail, "Informe um e-mail válido");
        valido = false;
    }*/

    /*if (!form.consentimento.checked) {
        form.erroConsentimento.textContent = "É necessário concordar para continuar";
        valido = false;
    }*/

    return valido;
}

/* ============================================================
   CONFIRMAÇÃO FINAL
   ============================================================ */

function confirmarAgendamento() {
    const servico = SERVICOS.find(s => s.id === estado.servicoSelecionado);
    const profissional = PROFISSIONAIS.find(p => p.id === estado.profissionalSelecionado);

    // Salva o agendamento
    const novoAgendamento = {
        id: Date.now().toString(),
        servico: servico.name,
        profissional: profissional.name,
        data: formatarData(),
        horario: estado.horarioSelecionado,
        valor: `R$ ${servico.price.toFixed(2).replace(".", ",")}`,
        status: "Confirmado"
    };
    salvarNoHistorico(novoAgendamento);

    for (let i = 1; i <= 4; i++) {
        const painel = document.getElementById(`painel-${i}`);
        if (painel) painel.hidden = true;
    }

    els.navEtapa.hidden = true;
    els.etapa.hidden = true;

    els.sucessoTexto.textContent =
        `${estado.nome.trim()}, seu agendamento de ${servico.name.toLowerCase()} foi confirmado ` +
        `para ${formatarData()} às ${estado.horarioSelecionado}. ` +
        `Você receberá uma confirmação em breve.`;

    els.sucesso.hidden = false;
    window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ============================================================
   REINICIAR
   ============================================================ */

function reiniciar() {
    // 1. Reseta o estado na memória JS
    estado.etapaAtual = 1;
    estado.servicoSelecionado = null;
    estado.profissionalSelecionado = null;
    estado.diaSelecionado = null;
    estado.horarioSelecionado = null;

    // 2. Restaura a visibilidade dos elementos da tela
    els.navEtapa.hidden = false;
    els.etapa.hidden = false;
    els.sucesso.hidden = true;

    // 3. Recarrega as listas para gerar inputs sem a propriedade 'checked'
    carregarServicos();
    carregarProfissionais();

    // 4. Desmarca o checkbox de consentimento e limpa mensagens de erro
    /*if (form.consentimento) {
        form.consentimento.checked = false;
    }
    if (form.erroConsentimento) {
        form.erroConsentimento.textContent = "";
    }*/

    // 5. Exibe o painel inicial
    mostrarPainel(1);
}

/* ============================================================
   INICIALIZAÇÃO & LISTENERS
   ============================================================ */

els.btnHistorico.addEventListener("click", abrirHistorico);
//inicializarLocalStorage();
carregarServicos();
carregarProfissionais();
mostrarPainel(1);
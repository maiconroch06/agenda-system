/* ============================================================
   DADOS
   ============================================================ */

   const SERVICOS = [
    { id: "infantil",       name: "Corte Infantil",      duration: 30, price: 20, icon: "../assets/images/cortes/corte-infantil.jpeg",        alt: "corte-infantil" },
    { id: "social",         name: "Corte Social",        duration: 30, price: 18, icon: "../assets/images/cortes/corte-social.jpeg",           alt: "corte-social" },
    { id: "social-barba",   name: "Social & Barba",    duration: 50, price: 30, icon: "../assets/images/cortes/corte-social&barba.jpeg",     alt: "corte-social-barba" },
    { id: "degrade",        name: "Degradê",           duration: 40, price: 22, icon: "../assets/images/cortes/corte-degrade.jpeg",          alt: "corte-degrade" },
    { id: "degrade-barba",  name: "Degradê & Barba",   duration: 60, price: 30, icon: "../assets/images/cortes/corte-degradê&barba.jpeg",   alt: "corte-degrade-barba" },
    { id: "militar",        name: "Corte Militar",     duration: 20, price: 15, icon: "../assets/images/cortes/corte-militar.jpeg",          alt: "corte-militar" },
    { id: "barba",          name: "Barba",             duration: 25, price: 15, icon: "../assets/images/cortes/corte-barba.jpeg",            alt: "corte-barba" },
    { id: "sobrancelha",    name: "Sobrancelha",       duration: 5,  price: 15, icon: "../assets/images/cortes/sombrancelha.png",            alt: "sombrancelha" },
];

const PROFISSIONAIS = [
    { id: "any",    name: "Sem preferência", description: "Qualquer profissional disponível", icon: "", alt: "" },
    { id: "thiago", name: "Thiago Tomaz",          description: "Barbeiro sênior",                  icon: "../assets/images/funcionarios/thiago.jpg", alt: "thiago" },
    { id: "samuel", name: "Samuel",                description: "Barbeiro sênior",                  icon: "../assets/images/funcionarios/samuel.jpg", alt: "samuel" },
    { id: "maik",   name: "Maik",                  description: "Barbeiro novato",                  icon: "../assets/images/funcionarios/maik.png",   alt: "maik" },
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

const dadosIniciais = [
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
    etapaAtual: 1,
    servicoSelecionado: null,
    profissionalSelecionado: null,
    diaSelecionado: null,
    horarioSelecionado: null,
    nome: "Maicon Rocha"
};

/* ============================================================
   ELEMENTOS
   ============================================================ */

const els = {
    etapa:             document.getElementById("etapa"),
    listaServico:      document.getElementById("lista-servico"),
    listaProfissionais: document.getElementById("lista-profissionais"),
    abasDias:          document.getElementById("abas-dias"),
    gradeHorarios:     document.getElementById("grade-horarios"),
    resumo:            document.getElementById("resumo"),
    btnVoltar:         document.getElementById("btn-voltar"),
    btnContinuar:      document.getElementById("btn-continuar"),
    navEtapa:          document.getElementById("nav-etapa"),
    aviso:             document.getElementById("aviso"),
    sucesso:           document.getElementById("painel-sucesso"),
    sucessoTexto:      document.getElementById("sucesso-texto"),
    btnHistorico:      document.getElementById("btn-historico"),
    painelHistorico:   document.getElementById("painel-historico"),
    listaHistorico:    document.getElementById("lista-historico"),
    modalHistorico:    document.getElementById("modal-historico"),
    resumoModal:       document.getElementById("resumo-modal-conteudo")
};

const form = {
    // nome:           document.getElementById("inp-nome"),
    // tel:            document.getElementById("inp-tel"),
    //email:          document.getElementById("inp-email"),
    consentimento:  document.getElementById("inp-consentimento"),
    // erroNome:       document.getElementById("erro-nome"),
    // erroTel:        document.getElementById("erro-tel"),
    //erroEmail:      document.getElementById("erro-email"),
    erroConsentimento: document.getElementById("erro-consentimento"),
};

/* ============================================================
   LOCALSTORAGE & HISTÓRICO INITIALIZATION
   ============================================================ */

// function inicializarLocalStorage() {
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

function obterHistorico() {
    return JSON.parse(localStorage.getItem("historicoAgendamentos")) || [];
}

function salvarNoHistorico(novoItem) {
    const historico = obterHistorico();
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
    const historico = obterHistorico();

    if (historico.length === 0) {
        els.listaHistorico.innerHTML = `<p class="mensagem">Nenhum agendamento encontrado.</p>`;
        return;
    }

    els.listaHistorico.innerHTML = historico.map(item => `
        <div class="card-historico" onclick="exibirDetalhesHistorico('${item.id}')">
            <div class="card-historico__topo">
                <span class="card-historico__servico">${item.servico}</span>
                <span class="card-historico__status status--${item.status.toLowerCase()}">${item.status}</span>
            </div>
            <div class="card-historico__info">
                <span><strong>Profissional:</strong> ${item.profissional}</span>
                <span><strong>Data:</strong> ${item.data}</span>
                <span><strong>Horário:</strong> ${item.horario}</span>
            </div>
            <div class="card-historico__rodape">
                <span class="card-historico__valor">${item.valor}</span>
                <span class="card-historico__link">Ver resumo &rarr;</span>
            </div>
        </div>
    `).join("");
}

function exibirDetalhesHistorico(id) {
    const historico = obterHistorico();
    const item = historico.find(h => h.id === id);
    if (!item) return;

    els.resumoModal.innerHTML = `
        <div class="resumo__linha">
            <span class="resumo__rotulo">Serviço</span>
            <span class="resumo__valor">${item.servico}</span>
        </div>
        <div class="resumo__linha">
            <span class="resumo__rotulo">Profissional</span>
            <span class="resumo__valor">${item.profissional}</span>
        </div>
        <div class="resumo__linha">
            <span class="resumo__rotulo">Data</span>
            <span class="resumo__valor">${item.data}</span>
        </div>
        <div class="resumo__linha">
            <span class="resumo__rotulo">Horário</span>
            <span class="resumo__valor">${item.horario}</span>
        </div>
        <div class="resumo__linha">
            <span class="resumo__rotulo">Valor</span>
            <span class="resumo__valor">${item.valor}</span>
        </div>
        <div class="resumo__linha">
            <span class="resumo__rotulo">Status</span>
            <span class="resumo__valor">${item.status}</span>
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
        item.classList.remove("ativo", "concluido");
        if (numero === estado.etapaAtual) item.classList.add("ativo");
        if (numero < estado.etapaAtual) item.classList.add("concluido");
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
        <input type="radio" name="inputCorte" id="${servico.id}" value="${servico.id}">
        <label class="card" for="${servico.id}">
            <span class="icon">
                <img src="${servico.icon}" alt="${servico.alt}">
            </span>
            <span class="titulo">${servico.name}</span>
            <span class="dados">
                <span>${servico.duration} min</span>
                <span>R$ ${servico.price.toFixed(2).replace(".", ",")}</span>
            </span>
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
        <input type="radio" name="inputFuncionario" id="${profissional.id}" value="${profissional.id}">
        <label class="card" for="${profissional.id}">
            ${profissional.icon
                ? `<img src="${profissional.icon}" alt="${profissional.alt}">`
                : `<div class="card__sem-foto">${profissional.name.charAt(0)}</div>`
            }
            <span class="titulo">${profissional.name}</span>
            <span class="dados" style="justify-content:center">
                <span>${profissional.description}</span>
            </span>
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
        return `
            <button
                class="dia ${estado.diaSelecionado === indice ? "ativo" : ""}"
                data-dia="${indice}"
                ${fechado ? "disabled" : ""}
            >
                <span>${NOMES_DIAS[data.getDay()]}</span>
                <strong>${data.getDate()}</strong>
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
        els.gradeHorarios.innerHTML = `<p class="mensagem">Escolha um dia para visualizar os horários.</p>`;
        return;
    }

    const ocupados = HORARIOS_OCUPADOS[estado.diaSelecionado] || [];

    els.gradeHorarios.innerHTML = TODOS_HORARIOS.map(horario => {
        const ocupado = ocupados.includes(horario);
        return `
            <button
                class="horario ${estado.horarioSelecionado === horario ? "ativo" : ""}"
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
        <div class="resumo__linha">
            <span class="resumo__rotulo">Serviço</span>
            <span class="resumo__valor">${servico.name}</span>
        </div>
        <div class="resumo__linha">
            <span class="resumo__rotulo">Profissional</span>
            <span class="resumo__valor">${profissional.name}</span>
        </div>
        <div class="resumo__linha">
            <span class="resumo__rotulo">Data</span>
            <span class="resumo__valor">${formatarData()}</span>
        </div>
        <div class="resumo__linha">
            <span class="resumo__rotulo">Horário</span>
            <span class="resumo__valor">${estado.horarioSelecionado}</span>
        </div>
        <div class="resumo__linha">
            <span class="resumo__rotulo">Valor</span>
            <span class="resumo__valor">R$ ${servico.price.toFixed(2).replace(".", ",")}</span>
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
    form.erroConsentimento.textContent = "";

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

    if (!form.consentimento.checked) {
        form.erroConsentimento.textContent = "É necessário concordar para continuar";
        valido = false;
    }

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
    estado.etapaAtual = 1;
    estado.servicoSelecionado = null;
    estado.profissionalSelecionado = null;
    estado.diaSelecionado = null;
    estado.horarioSelecionado = null;

    //Limpa o formulario que esta comentado 
    // document.getElementById("formulario").reset();
    // [form.nome, form.tel/*, form.email*/].forEach(i => i.classList.remove("invalido"));
    // document.querySelectorAll(".campo__erro").forEach(e => e.textContent = "");

    els.navEtapa.hidden = false;
    els.etapa.hidden = false;
    els.sucesso.hidden = true;

    carregarServicos();
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
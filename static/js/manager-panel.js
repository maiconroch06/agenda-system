/* ============================================================
   ESTADO GLOBAL DA APLICAÇÃO
   ============================================================ */
const estadoApp = {
    empresa: {
        nome: "TMS Barbearia",
        categoria: "barbearia",
        cnpj: "12.345.678/0001-90",
        abertura: "08:00",
        fechamento: "20:00",
        dias: "Segunda a Sábado",
        codigoAcesso: "TMS-8942"
    },
    servicos: [
        { id: 1, nome: "Corte", preco: 45.00, tempo: 40, imagem: null },
        { id: 2, nome: "Barba Completa", preco: 35.00, tempo: 30, imagem: null },
        { id: 3, nome: "Combo (Corte + Barba)", preco: 70.00, tempo: 60, imagem: null }
    ],
    profissionais: [
        { id: 1, nome: "Carlos Silva", cargo: "Barbeiro Master", imagem: null },
        { id: 2, nome: "Lucas Mendes", cargo: "Especialista em Barba", imagem: null }
    ],
    agendamentosHoje: [
        { id: "1", horario: "09:00", cliente: "Lucas Andrade", servico: "Corte Degradê", profissional: "Carlos Silva", valor: 45.00, status: "Concluído" },
        { id: "2", horario: "10:00", cliente: "Gabriel Santos", servico: "Barba Completa", profissional: "Lucas Mendes", valor: 35.00, status: "Em Atendimento" },
        { id: "3", horario: "11:30", cliente: "Rafael Lima", servico: "Combo (Corte + Barba)", profissional: "Carlos Silva", valor: 70.00, status: "Aguardando" },
        { id: "4", horario: "14:00", cliente: "Felipe Silva", servico: "Corte Degradê", profissional: "Lucas Mendes", valor: 45.00, status: "Aguardando" }
    ],
    clientes: [
        { id: 1, nome: "Lucas Andrade", telefone: "(11) 98888-1111", ultimaVisita: "Hoje", visitas: 5, totalGasto: "R$ 225,00" },
        { id: 2, nome: "Gabriel Santos", telefone: "(11) 97777-2222", ultimaVisita: "Hoje", visitas: 3, totalGasto: "R$ 105,00" },
        { id: 3, nome: "Rafael Lima", telefone: "(11) 96666-3333", ultimaVisita: "15/02/2026", visitas: 8, totalGasto: "R$ 560,00" }
    ],
    historicoFinanceiro: [
        { data: "10/09/2026 14:30", cliente: "João Pedro", servico: "Corte", profissional: "Carlos Silva", valor: 45.00 },
        { data: "10/09/2026 15:15", cliente: "Mateus Souza", servico: "Barba Completa", profissional: "Lucas Mendes", valor: 35.00 },
        { data: "10/09/2026 16:00", cliente: "Rafael Lima", servico: "Combo (Corte + Barba)", profissional: "Carlos Silva", valor: 70.00 }
    ]
};

// Mapeamento dinâmico de elementos do DOM
const els = {};

function mapearElementos() {
    // Perfil / Configurações
    els.perfilNome = document.getElementById("perfil-nome");
    els.perfilCategoria = document.getElementById("perfil-categoria");
    els.perfilCnpj = document.getElementById("perfil-cnpj");
    els.perfilExpediente = document.getElementById("perfil-expediente");
    els.perfilDias = document.getElementById("perfil-dias");
    els.codigoAcesso = document.getElementById("codigo-acesso");

    // Modal Empresa
    els.editEmpNome = document.getElementById("edit-emp-nome");
    els.editEmpCategoria = document.getElementById("edit-emp-categoria");
    els.editEmpCnpj = document.getElementById("edit-emp-cnpj");
    els.editEmpAbertura = document.getElementById("edit-emp-abertura");
    els.editEmpFechamento = document.getElementById("edit-emp-fechamento");
    els.modalOverlay = document.getElementById("modal-overlay");
    els.modalEmpresa = document.getElementById("modal-empresa");

    // Serviços
    els.formServicoPainel = document.getElementById("form-servico-painel");
    els.psrvNome = document.getElementById("psrv-nome");
    els.psrvPreco = document.getElementById("psrv-preco");
    els.psrvTempo = document.getElementById("psrv-tempo");
    els.psrvFoto = document.getElementById("psrv-foto");
    els.listaServicosPainel = document.getElementById("lista-servicos-painel");

    // Profissionais
    els.formProfissionalPainel = document.getElementById("form-profissional-painel");
    els.pproNome = document.getElementById("ppro-nome");
    els.pproCargo = document.getElementById("ppro-cargo");
    els.pproFoto = document.getElementById("ppro-foto");
    els.listaProfissionaisPainel = document.getElementById("lista-profissionais-painel");

    // Clientes
    els.tabelaClientesCorpo = document.getElementById("tabela-clientes-corpo");
    els.buscaCliente = document.getElementById("busca-cliente");

    // Financeiro
    els.finReceitaMes = document.getElementById("fin-receita-mes");
    els.finTotalCortes = document.getElementById("fin-total-cortes");
    els.finTicketMedio = document.getElementById("fin-ticket-medio");
    els.finMaisRealizado = document.getElementById("fin-mais-realizado");
    els.finTabelaCorpo = document.getElementById("fin-tabela-corpo");

    // Feedbacks & NAVEGAÇÃO
    els.aviso = document.getElementById("aviso");
    els.abasFunc = document.querySelectorAll(".aba-func");
    els.sidebarItems = document.querySelectorAll(".sidebar-func__item");
    els.bottomNavItems = document.querySelectorAll(".bottom-nav__item");
}

/* ============================================================
   NAVEGAÇÃO ENTRE ABAS
   ============================================================ */
function irParaAba(nomeAba) {
    // Esconde todas as seções
    document.querySelectorAll(".aba-func").forEach(sec => {
        sec.classList.add("hidden");
        sec.classList.remove("block");
    });

    // Exibe a aba ativa
    const abaAtiva = document.getElementById(`aba-${nomeAba}`);
    if (abaAtiva) {
        abaAtiva.classList.remove("hidden");
        abaAtiva.classList.add("block");
    }

    // Estilização Sidebar Desktop
    document.querySelectorAll(".sidebar-func__item").forEach(btn => {
        if (btn.getAttribute("data-aba") === nomeAba) {
            btn.className = "sidebar-func__item flex items-center gap-2.5 p-2.5 px-3 rounded-lg border-none bg-[#2a2825] text-[#f1efe8] font-medium text-sm cursor-pointer text-left w-full transition-colors";
        } else {
            btn.className = "sidebar-func__item flex items-center gap-2.5 p-2.5 px-3 rounded-lg border-none bg-transparent text-[#888780] font-medium text-sm cursor-pointer text-left w-full transition-colors hover:bg-[#2a2825] hover:text-[#f1efe8]";
        }
    });

    // Estilização Navegação Mobile
    document.querySelectorAll(".bottom-nav__item").forEach(btn => {
        if (btn.getAttribute("data-aba") === nomeAba) {
            btn.classList.remove("text-[#888780]");
            btn.classList.add("text-[#f1efe8]");
        } else {
            btn.classList.remove("text-[#f1efe8]");
            btn.classList.add("text-[#888780]");
        }
    });

    // Roteamento de dados da aba
    switch (nomeAba) {
        case "inicio": carregarDashboardInicio(); break;
        case "servicos": renderizarServicos(); break;
        case "profissionais": renderizarProfissionais(); break;
        case "clientes": carregarClientes(); break;
        case "financeiro": renderizarFinanceiro(); break;
        case "config": carregarPerfil(); break;
    }
}

/* ============================================================
   ABA 1: INÍCIO (DASHBOARD OPERACIONAL DO DIA)
   ============================================================ */
function carregarDashboardInicio() {
    const hoje = new Date();
    const dataFormatted = hoje.toLocaleDateString("pt-BR", { weekday: "long", day: "2-digit", month: "long" });
    const elData = document.getElementById("data-atual-str");
    if (elData) elData.textContent = dataFormatted.charAt(0).toUpperCase() + dataFormatted.slice(1);

    const agendamentos = estadoApp.agendamentosHoje;

    // Métricas operacionais em tempo real
    const faturamento = agendamentos
        .filter(a => a.status === "Concluído" || a.status === "Em Atendimento")
        .reduce((acc, a) => acc + a.valor, 0);

    const concluidos = agendamentos.filter(a => a.status === "Concluído" || a.status === "Em Atendimento").length;
    const total = agendamentos.length;
    const ocupacao = total > 0 ? Math.round((concluidos / total) * 100) : 0;
    const faltas = agendamentos.filter(a => a.status === "Cancelado").length;

    const elFat = document.getElementById("kpi-faturamento-hoje");
    if (elFat) elFat.textContent = `R$ ${faturamento.toFixed(2).replace(".", ",")}`;

    const elAtend = document.getElementById("kpi-atendimentos-hoje");
    if (elAtend) elAtend.textContent = `${concluidos} / ${total}`;

    const elOcup = document.getElementById("kpi-ocupacao-hoje");
    if (elOcup) elOcup.textContent = `${ocupacao}%`;

    const elFaltas = document.getElementById("kpi-faltas-hoje");
    if (elFaltas) elFaltas.textContent = faltas;

    const elTotal = document.getElementById("total-agendamentos-hoje");
    if (elTotal) elTotal.textContent = `${total} agendamentos`;

    // Renderização da tabela diária
    const tbody = document.getElementById("tabela-hoje-corpo");
    if (!tbody) return;

    if (agendamentos.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="p-6 text-center text-[#888780]">Nenhum agendamento para hoje.</td></tr>`;
        return;
    }

    tbody.innerHTML = agendamentos.map(item => `
        <tr class="border-b border-[#38362f]/50 hover:bg-[#2a2825]/50 transition-colors">
            <td class="p-3.5 px-4 font-mono font-medium">${item.horario}</td>
            <td class="p-3.5 px-4 font-medium">${item.cliente}</td>
            <td class="p-3.5 px-4 text-[#888780]">${item.servico}</td>
            <td class="p-3.5 px-4 text-[#888780]">${item.profissional}</td>
            <td class="p-3.5 px-4">${obterBadgeStatus(item.status)}</td>
        </tr>
    `).join("");
            // <td class="p-3.5 px-4 text-right">
            //     ${item.status === "Aguardando" ? `<button onclick="alterarStatus('${item.id}', 'Em Atendimento')" class="text-xs text-amber-400 hover:underline mr-2">Iniciar</button>` : ""}
            //     ${item.status === "Em Atendimento" ? `<button onclick="alterarStatus('${item.id}', 'Concluído')" class="text-xs text-emerald-400 hover:underline">Concluir</button>` : ""}
            // </td>
}

function obterBadgeStatus(status) {
    const estilos = {
        "Concluído": "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
        "Em Atendimento": "bg-amber-500/10 text-amber-400 border-amber-500/20",
        "Aguardando": "bg-blue-500/10 text-blue-400 border-blue-500/20",
        "Cancelado": "bg-red-500/10 text-red-400 border-red-500/20"
    };
    return `<span class="px-2 py-1 rounded-full text-[10px] font-medium border ${estilos[status] || ""}">${status}</span>`;
}

function alterarStatus(id, novoStatus) {
    const item = estadoApp.agendamentosHoje.find(a => a.id === id);
    if (item) {
        item.status = novoStatus;
        carregarDashboardInicio();
        mostrarAviso(`Status alterado para: ${novoStatus}`);
    }
}

function abrirModalEncaixe() { mostrarAviso("Módulo de Novo Encaixe"); }
function abrirModalBloqueio() { mostrarAviso("Módulo de Bloqueio de Horário"); }

/* ============================================================
   ABA 3: GESTÃO DE SERVIÇOS
   ============================================================ */
function abrirFormServico() {
    if (els.formServicoPainel) els.formServicoPainel.classList.remove("hidden");
}

function fecharFormServico() {
    if (els.formServicoPainel) els.formServicoPainel.classList.add("hidden");
    limparInputsServico();
}

async function adicionarServicoPainel() {
    const nome = els.psrvNome ? els.psrvNome.value : "";
    const preco = parseFloat(els.psrvPreco ? els.psrvPreco.value : 0);
    const tempo = parseInt(els.psrvTempo ? els.psrvTempo.value : 0);

    if (!nome || isNaN(preco) || isNaN(tempo) || preco <= 0) {
        mostrarAviso("Preencha corretamente os campos do serviço.");
        return;
    }

    const imagem = await lerImagem(els.psrvFoto);

    estadoApp.servicos.push({ id: Date.now(), nome, preco, tempo, imagem });
    renderizarServicos();
    fecharFormServico();
    mostrarAviso("Serviço adicionado com sucesso!");
}

function removerServico(id) {
    estadoApp.servicos = estadoApp.servicos.filter(s => s.id !== id);
    renderizarServicos();
    mostrarAviso("Serviço removido.");
}

function moverServico(index, direcao) {
    const novoIndex = index + direcao;
    if (novoIndex < 0 || novoIndex >= estadoApp.servicos.length) return;
    
    const item = estadoApp.servicos.splice(index, 1)[0];
    estadoApp.servicos.splice(novoIndex, 0, item);
    renderizarServicos();
}

function editarServico(id) {
    const s = estadoApp.servicos.find(item => item.id === id);
    if (!s) return;
    abrirFormServico();
    if (els.psrvNome) els.psrvNome.value = s.nome;
    if (els.psrvPreco) els.psrvPreco.value = s.preco;
    if (els.psrvTempo) els.psrvTempo.value = s.tempo;
}

function renderizarServicos() {
    if (!els.listaServicosPainel) return;

    if (estadoApp.servicos.length === 0) {
        els.listaServicosPainel.innerHTML = `<div class="col-span-full p-6 text-center text-xs text-[#888780] bg-[#232220] border border-[#38362f] rounded-2xl">Nenhum serviço cadastrado.</div>`;
        return;
    }

    els.listaServicosPainel.innerHTML = estadoApp.servicos.map((s, index) => `
        <div class="bg-[#232220] border border-[#38362f] rounded-2xl p-2.5 flex flex-col justify-between">
            <div class="relative w-full aspect-square bg-[#181715] rounded-xl border border-[#38362f] flex items-center justify-center mb-2.5 overflow-hidden group">
                ${s.imagem 
                    ? `<img src="${s.imagem}" alt="${s.nome}" class="w-full h-full object-cover">` 
                    : `<span class="text-3xl select-none">✂</span>`
                }
                <div class="absolute top-1.5 right-1.5 flex flex-col gap-1 z-10">
                    <button onclick="moverServico(${index}, -1)" class="w-5 h-5 rounded border border-[#4a473f] bg-[#232220]/90 text-[#888780] hover:text-[#f1efe8] hover:bg-[#38362f] flex items-center justify-center text-[9px] cursor-pointer">▲</button>
                    <button onclick="moverServico(${index}, 1)" class="w-5 h-5 rounded border border-[#4a473f] bg-[#232220]/90 text-[#888780] hover:text-[#f1efe8] hover:bg-[#38362f] flex items-center justify-center text-[9px] cursor-pointer">▼</button>
                </div>
            </div>
            <h4 class="text-xs sm:text-sm font-medium text-[#f1efe8] truncate mb-1" title="${s.nome}">${s.nome}</h4>
            <div class="flex items-center justify-between text-[11px] sm:text-xs text-[#888780] mb-2.5">
                <span>${s.tempo} min</span>
                <span class="font-medium text-[#c4a977]">R$ ${s.preco.toFixed(2).replace('.', ',')}</span>
            </div>
            <div class="grid grid-cols-2 gap-1.5 mt-auto">
                <button onclick="editarServico(${s.id})" class="py-1 rounded-lg border border-[#38362f] bg-transparent text-[#888780] hover:bg-[#2a2825] hover:text-[#f1efe8] text-[11px] font-medium transition-colors cursor-pointer text-center">Editar</button>
                <button onclick="removerServico(${s.id})" class="py-1 rounded-lg border border-[#38362f] bg-transparent text-[#888780] hover:bg-[#2a2825] hover:text-[#f1efe8] text-[11px] font-medium transition-colors cursor-pointer text-center">Remover</button>
            </div>
        </div>
    `).join("");
}

/* ============================================================
   ABA 4: GESTÃO DE PROFISSIONAIS
   ============================================================ */
function abrirFormProfissional() {
    if (els.formProfissionalPainel) els.formProfissionalPainel.classList.remove("hidden");
}

function fecharFormProfissional() {
    if (els.formProfissionalPainel) els.formProfissionalPainel.classList.add("hidden");
    limparInputsProfissional();
}

async function adicionarProfissionalPainel() {
    const nome = els.pproNome ? els.pproNome.value : "";
    const cargo = els.pproCargo ? els.pproCargo.value : "";

    if (!nome || !cargo) {
        mostrarAviso("Preencha o nome e o cargo do profissional.");
        return;
    }

    const imagem = await lerImagem(els.pproFoto);

    estadoApp.profissionais.push({ id: Date.now(), nome, cargo, imagem });
    renderizarProfissionais();
    fecharFormProfissional();
    mostrarAviso("Profissional adicionado com sucesso!");
}

function removerProfissional(id) {
    estadoApp.profissionais = estadoApp.profissionais.filter(p => p.id !== id);
    renderizarProfissionais();
    mostrarAviso("Profissional removido.");
}

function moverProfissional(index, direcao) {
    const novoIndex = index + direcao;
    if (novoIndex < 0 || novoIndex >= estadoApp.profissionais.length) return;
    
    const item = estadoApp.profissionais.splice(index, 1)[0];
    estadoApp.profissionais.splice(novoIndex, 0, item);
    renderizarProfissionais();
}

function editarProfissional(id) {
    const p = estadoApp.profissionais.find(item => item.id === id);
    if (!p) return;
    abrirFormProfissional();
    if (els.pproNome) els.pproNome.value = p.nome;
    if (els.pproCargo) els.pproCargo.value = p.cargo;
}

function renderizarProfissionais() {
    if (!els.listaProfissionaisPainel) return;

    if (estadoApp.profissionais.length === 0) {
        els.listaProfissionaisPainel.innerHTML = `<div class="col-span-full p-6 text-center text-xs text-[#888780] bg-[#232220] border border-[#38362f] rounded-2xl">Nenhum profissional cadastrado.</div>`;
        return;
    }

    els.listaProfissionaisPainel.innerHTML = estadoApp.profissionais.map((p, index) => `
        <div class="bg-[#232220] border border-[#38362f] rounded-2xl p-2.5 flex flex-col justify-between">
            <div class="relative w-full aspect-square bg-[#181715] rounded-xl border border-[#38362f] flex items-center justify-center mb-2.5 overflow-hidden group">
                ${p.imagem 
                    ? `<img src="${p.imagem}" alt="${p.nome}" class="w-full h-full object-cover">` 
                    : `<span class="text-3xl select-none">👤</span>`
                }
                <div class="absolute top-1.5 right-1.5 flex flex-col gap-1 z-10">
                    <button onclick="moverProfissional(${index}, -1)" class="w-5 h-5 rounded border border-[#4a473f] bg-[#232220]/90 text-[#888780] hover:text-[#f1efe8] hover:bg-[#38362f] flex items-center justify-center text-[9px] cursor-pointer">▲</button>
                    <button onclick="moverProfissional(${index}, 1)" class="w-5 h-5 rounded border border-[#4a473f] bg-[#232220]/90 text-[#888780] hover:text-[#f1efe8] hover:bg-[#38362f] flex items-center justify-center text-[9px] cursor-pointer">▼</button>
                </div>
            </div>
            <h4 class="text-xs sm:text-sm font-medium text-[#f1efe8] truncate mb-1" title="${p.nome}">${p.nome}</h4>
            <div class="text-[11px] sm:text-xs text-[#888780] mb-2.5 truncate" title="${p.cargo}">${p.cargo}</div>
            <div class="grid grid-cols-2 gap-1.5 mt-auto">
                <button onclick="editarProfissional(${p.id})" class="py-1 rounded-lg border border-[#38362f] bg-transparent text-[#888780] hover:bg-[#2a2825] hover:text-[#f1efe8] text-[11px] font-medium transition-colors cursor-pointer text-center">Editar</button>
                <button onclick="removerProfissional(${p.id})" class="py-1 rounded-lg border border-[#38362f] bg-transparent text-[#888780] hover:bg-[#2a2825] hover:text-[#f1efe8] text-[11px] font-medium transition-colors cursor-pointer text-center">Remover</button>
            </div>
        </div>
    `).join("");
}

/* ============================================================
   ABA 5: CLIENTES (CRM)
   ============================================================ */
function carregarClientes() {
    if (!els.tabelaClientesCorpo) return;
    renderizarListaClientes(estadoApp.clientes);
}

function renderizarListaClientes(lista) {
    if (!els.tabelaClientesCorpo) return;

    if (lista.length === 0) {
        els.tabelaClientesCorpo.innerHTML = `<tr><td colspan="5" class="p-6 text-center text-[#888780]">Nenhum cliente encontrado.</td></tr>`;
        return;
    }

    els.tabelaClientesCorpo.innerHTML = lista.map(c => `
        <tr class="border-b border-[#38362f]/50 hover:bg-[#2a2825]/50 transition-colors">
            <td class="p-3.5 px-4 font-medium">${c.nome}</td>
            <td class="p-3.5 px-4 text-[#888780]">${c.telefone}</td>
            <td class="p-3.5 px-4 text-[#888780]">${c.ultimaVisita}</td>
            <td class="p-3.5 px-4">${c.visitas}</td>
            <td class="p-3.5 px-4 font-medium text-emerald-400">${c.totalGasto}</td>
        </tr>
    `).join("");
}

function filtrarClientes() {
    const termo = els.buscaCliente ? els.buscaCliente.value.toLowerCase() : "";
    const filtrados = estadoApp.clientes.filter(c => 
        c.nome.toLowerCase().includes(termo) || c.telefone.includes(termo)
    );
    renderizarListaClientes(filtrados);
}

/* ============================================================
   ABA 6: FINANCEIRO
   ============================================================ */
function renderizarFinanceiro() {
    const totalReceita = estadoApp.historicoFinanceiro.reduce((acc, item) => acc + item.valor, 0);
    const totalCortes = estadoApp.historicoFinanceiro.length;
    const ticketMedio = totalCortes > 0 ? (totalReceita / totalCortes) : 0;

    if (els.finReceitaMes) els.finReceitaMes.textContent = `R$ ${totalReceita.toFixed(2).replace('.', ',')}`;
    if (els.finTotalCortes) els.finTotalCortes.textContent = totalCortes.toString();
    if (els.finTicketMedio) els.finTicketMedio.textContent = `R$ ${ticketMedio.toFixed(2).replace('.', ',')}`;
    if (els.finMaisRealizado) els.finMaisRealizado.textContent = totalCortes > 0 ? estadoApp.historicoFinanceiro[0].servico : "—";

    if (!els.finTabelaCorpo) return;

    if (estadoApp.historicoFinanceiro.length === 0) {
        els.finTabelaCorpo.innerHTML = `<tr><td colspan="5" class="p-6 text-center text-[#888780]">Nenhum atendimento registrado ainda.</td></tr>`;
        return;
    }

    els.finTabelaCorpo.innerHTML = estadoApp.historicoFinanceiro.map(item => `
        <tr class="border-b border-[#38362f]/50 hover:bg-[#2a2825] transition-colors">
            <td class="p-3 px-4">${item.data}</td>
            <td class="p-3 px-4 font-medium text-[#f1efe8]">${item.cliente}</td>
            <td class="p-3 px-4 text-[#888780]">${item.servico}</td>
            <td class="p-3 px-4 text-[#888780]">${item.profissional}</td>
            <td class="p-3 px-4 font-semibold text-[#f1efe8]">R$ ${item.valor.toFixed(2).replace('.', ',')}</td>
        </tr>
    `).join("");
}

/* ============================================================
   ABA 7: CONFIGURAÇÕES DA EMPRESA E CÓDIGO DE ACESSO
   ============================================================ */
function carregarPerfil() {
    const emp = estadoApp.empresa;
    if (els.perfilNome) els.perfilNome.textContent = emp.nome;
    if (els.perfilCategoria) els.perfilCategoria.textContent = formatarCategoria(emp.categoria);
    if (els.perfilCnpj) els.perfilCnpj.textContent = emp.cnpj;
    if (els.perfilExpediente) els.perfilExpediente.textContent = emp.expediente || `${emp.abertura} às ${emp.fechamento}`;
    if (els.perfilDias && emp.dias) els.perfilDias.textContent = emp.dias;
    if (els.codigoAcesso) els.codigoAcesso.textContent = emp.codigoAcesso;
}

function abrirModalEmpresa() {
    const emp = estadoApp.empresa;
    if (els.editEmpNome) els.editEmpNome.value = emp.nome;
    if (els.editEmpCategoria) els.editEmpCategoria.value = emp.categoria;
    if (els.editEmpCnpj) els.editEmpCnpj.value = emp.cnpj;
    if (els.editEmpAbertura) els.editEmpAbertura.value = emp.abertura;
    if (els.editEmpFechamento) els.editEmpFechamento.value = emp.fechamento;

    if (els.modalOverlay) els.modalOverlay.classList.remove("hidden");
    if (els.modalEmpresa) els.modalEmpresa.classList.remove("hidden");
}

function fecharModalEmpresa() {
    if (els.modalOverlay) els.modalOverlay.classList.add("hidden");
    if (els.modalEmpresa) els.modalEmpresa.classList.add("hidden");
}

function salvarEdicaoEmpresa() {
    const emp = estadoApp.empresa;
    emp.nome = els.editEmpNome?.value || emp.nome;
    emp.categoria = els.editEmpCategoria?.value || emp.categoria;
    emp.cnpj = els.editEmpCnpj?.value || emp.cnpj;
    emp.abertura = els.editEmpAbertura?.value || emp.abertura;
    emp.fechamento = els.editEmpFechamento?.value || emp.fechamento;
    emp.expediente = `${emp.abertura} às ${emp.fechamento}`;

    carregarPerfil();
    fecharModalEmpresa();
    mostrarAviso("Dados da empresa atualizados com sucesso!");
}

function gerarCodigo() {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let novoCodigo = "TMS-";
    for (let i = 0; i < 4; i++) {
        novoCodigo += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    estadoApp.empresa.codigoAcesso = novoCodigo;
    if (els.codigoAcesso) els.codigoAcesso.textContent = novoCodigo;
    mostrarAviso("Novo código de acesso gerado!");
}

function copiarCodigo() {
    navigator.clipboard.writeText(estadoApp.empresa.codigoAcesso);
    mostrarAviso("Código copiado para a área de transferência!");
}

/* ============================================================
   UTILITÁRIOS E TOAST DE FEEDBACK
   ============================================================ */
function lerImagem(input) {
    return new Promise((resolve) => {
        const file = input && input.files ? input.files[0] : null;
        if (!file) {
            resolve(null);
            return;
        }
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = () => resolve(null);
        reader.readAsDataURL(file);
    });
}

function mostrarAviso(mensagem) {
    if (!els.aviso) return;
    els.aviso.textContent = mensagem;
    els.aviso.classList.remove("opacity-0", "pointer-events-none");
    els.aviso.classList.add("opacity-100");

    setTimeout(() => {
        els.aviso.classList.remove("opacity-100");
        els.aviso.classList.add("opacity-0", "pointer-events-none");
    }, 2500);
}

function formatarCategoria(cat) {
    const categorias = {
        barbearia: "Barbearia",
        salao: "Salão de Beleza",
        estetica: "Estética",
        clinica: "Clínica",
        outro: "Outro"
    };
    return categorias[cat] || cat;
}

function limparInputsServico() {
    if (els.psrvNome) els.psrvNome.value = "";
    if (els.psrvPreco) els.psrvPreco.value = "";
    if (els.psrvTempo) els.psrvTempo.value = "";
    if (els.psrvFoto) els.psrvFoto.value = "";
}

function limparInputsProfissional() {
    if (els.pproNome) els.pproNome.value = "";
    if (els.pproCargo) els.pproCargo.value = "";
    if (els.pproFoto) els.pproFoto.value = "";
}

function sairDaConta() {
    mostrarAviso("Saindo do painel...");
}

/* ============================================================
   INICIALIZAÇÃO
   ============================================================ */
function iniciar() {
    mapearElementos();
    irParaAba("inicio");
}

document.addEventListener("DOMContentLoaded", iniciar);
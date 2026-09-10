// Estado global da aplicação (dados iniciais)
const estadoEmpresa = {
    nome: "TMS Barbearia",
    categoria: "barbearia",
    cnpj: "12.345.678/0001-90",
    abertura: "08:00",
    fechamento: "20:00",
    dias: "Segunda a Sábado",
    codigoAcesso: "TMS-8942"
};

let servicos = [
    { id: 1, nome: "Corte Degradê", preco: 45.00, tempo: 40 },
    { id: 2, nome: "Barba Completa", preco: 35.00, tempo: 30 },
    { id: 3, nome: "Combo (Corte + Barba)", preco: 70.00, tempo: 60 }
];

let profissionais = [
    { id: 1, nome: "Carlos Silva", cargo: "Barbeiro Master" },
    { id: 2, nome: "Lucas Mendes", cargo: "Especialista em Barba" }
];

let historicoFinanceiro = [
    { data: "10/09/2026 14:30", cliente: "João Pedro", servico: "Corte Degradê", profissional: "Carlos Silva", valor: 45.00 },
    { data: "10/09/2026 15:15", cliente: "Mateus Souza", servico: "Barba Completa", profissional: "Lucas Mendes", valor: 35.00 },
    { data: "10/09/2026 16:00", cliente: "Rafael Lima", servico: "Combo (Corte + Barba)", profissional: "Carlos Silva", valor: 70.00 }
];

// Inicialização
document.addEventListener("DOMContentLoaded", () => {
    carregarPerfil();
    renderizarServicos();
    renderizarProfissionais();
    renderizarFinanceiro();
});

// Navegação entre Abas
function irParaAba(nomeAba) {
    // Ocultar todas as seções
    document.querySelectorAll(".aba-func").forEach(sec => {
        sec.classList.add("hidden");
        sec.classList.remove("block");
    });

    // Exibir seção selecionada
    const abaAtiva = document.getElementById(`aba-${nomeAba}`);
    if (abaAtiva) {
        abaAtiva.classList.remove("hidden");
        abaAtiva.classList.add("block");
    }

    // Atualizar estado visual da Sidebar (Desktop)
    document.querySelectorAll(".sidebar-func__item").forEach(btn => {
        if (btn.getAttribute("data-aba") === nomeAba) {
            btn.className = "sidebar-func__item flex items-center gap-2.5 p-2.5 px-3 rounded-lg border-none bg-[#2a2825] text-[#f1efe8] font-medium text-sm cursor-pointer text-left w-full transition-colors";
        } else {
            btn.className = "sidebar-func__item flex items-center gap-2.5 p-2.5 px-3 rounded-lg border-none bg-transparent text-[#888780] font-medium text-sm cursor-pointer text-left w-full transition-colors hover:bg-[#2a2825] hover:text-[#f1efe8]";
        }
    });

    // Atualizar estado visual do Bottom Nav (Mobile)
    document.querySelectorAll(".bottom-nav__item").forEach(btn => {
        if (btn.getAttribute("data-aba") === nomeAba) {
            btn.classList.remove("text-[#888780]");
            btn.classList.add("text-[#9fe1cb]");
        } else {
            btn.classList.remove("text-[#9fe1cb]");
            btn.classList.add("text-[#888780]");
        }
    });
}

// Gestão de Perfil & Modal
function carregarPerfil() {
    document.getElementById("perfil-nome").textContent = estadoEmpresa.nome;
    document.getElementById("perfil-categoria").textContent = formatarCategoria(estadoEmpresa.categoria);
    document.getElementById("perfil-cnpj").textContent = estadoEmpresa.cnpj;
    document.getElementById("perfil-expediente").textContent = `${estadoEmpresa.abertura} às ${estadoEmpresa.fechamento}`;
    document.getElementById("perfil-dias").textContent = estadoEmpresa.dias;
    //document.getElementById("codigo-acesso").textContent = estadoEmpresa.codigoAcesso;
}

function abrirModalEmpresa() {
    document.getElementById("edit-emp-nome").value = estadoEmpresa.nome;
    document.getElementById("edit-emp-categoria").value = estadoEmpresa.categoria;
    document.getElementById("edit-emp-cnpj").value = estadoEmpresa.cnpj;
    document.getElementById("edit-emp-abertura").value = estadoEmpresa.abertura;
    document.getElementById("edit-emp-fechamento").value = estadoEmpresa.fechamento;

    document.getElementById("modal-overlay").classList.remove("hidden");
    document.getElementById("modal-empresa").classList.remove("hidden");
}

function fecharModalEmpresa() {
    document.getElementById("modal-overlay").classList.add("hidden");
    document.getElementById("modal-empresa").classList.add("hidden");
}

function salvarEdicaoEmpresa() {
    estadoEmpresa.nome = document.getElementById("edit-emp-nome").value || estadoEmpresa.nome;
    estadoEmpresa.categoria = document.getElementById("edit-emp-categoria").value;
    estadoEmpresa.cnpj = document.getElementById("edit-emp-cnpj").value || estadoEmpresa.cnpj;
    estadoEmpresa.abertura = document.getElementById("edit-emp-abertura").value || estadoEmpresa.abertura;
    estadoEmpresa.fechamento = document.getElementById("edit-emp-fechamento").value || estadoEmpresa.fechamento;

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
    estadoEmpresa.codigoAcesso = novoCodigo;
    document.getElementById("codigo-acesso").textContent = novoCodigo;
    mostrarAviso("Novo código gerado!");
}

function copiarCodigo() {
    navigator.clipboard.writeText(estadoEmpresa.codigoAcesso);
    mostrarAviso("Código copiado para a área de transferência!");
}

// CRUD Serviços
function abrirFormServico() {
    document.getElementById("form-servico-painel").classList.remove("hidden");
}

function fecharFormServico() {
    document.getElementById("form-servico-painel").classList.add("hidden");
    limparInputsServico();
}

function adicionarServicoPainel() {
    const nome = document.getElementById("psrv-nome").value;
    const preco = parseFloat(document.getElementById("psrv-preco").value);
    const tempo = parseInt(document.getElementById("psrv-tempo").value);

    if (!nome || isNaN(preco) || isNaN(tempo)) {
        mostrarAviso("Preencha todos os campos do serviço.");
        return;
    }

    servicos.push({ id: Date.now(), nome, preco, tempo });
    renderizarServicos();
    fecharFormServico();
    mostrarAviso("Serviço adicionado com sucesso!");
}

function removerServico(id) {
    servicos = servicos.filter(s => s.id !== id);
    renderizarServicos();
    mostrarAviso("Serviço removido.");
}

function renderizarServicos() {
    const container = document.getElementById("lista-servicos-painel");
    if (servicos.length === 0) {
        container.innerHTML = `<div class="p-4 text-center text-xs text-[#888780] bg-[#232220] border border-[#38362f] rounded-2xl">Nenhum serviço cadastrado.</div>`;
        return;
    }

    container.innerHTML = servicos.map(s => `
        <div class="bg-[#232220] border border-[#38362f] rounded-2xl p-4 flex items-center justify-between">
            <div>
                <h4 class="text-sm font-semibold text-[#f1efe8]">${s.nome}</h4>
                <p class="text-xs text-[#888780] mt-0.5">R$ ${s.preco.toFixed(2)} • ${s.tempo} min</p>
            </div>
            <button onclick="removerServico(${s.id})" class="px-3 py-1.5 rounded-lg border border-[#38362f] bg-transparent text-[#888780] text-xs font-medium hover:bg-[#38362f] hover:text-[#f1efe8] transition-colors">
                Excluir
            </button>
        </div>
    `).join("");
}

// CRUD Profissionais
function abrirFormProfissional() {
    document.getElementById("form-profissional-painel").classList.remove("hidden");
}

function fecharFormProfissional() {
    document.getElementById("form-profissional-painel").classList.add("hidden");
    limparInputsProfissional();
}

function adicionarProfissionalPainel() {
    const nome = document.getElementById("ppro-nome").value;
    const cargo = document.getElementById("ppro-cargo").value;

    if (!nome || !cargo) {
        mostrarAviso("Preencha o nome e cargo do profissional.");
        return;
    }

    profissionais.push({ id: Date.now(), nome, cargo });
    renderizarProfissionais();
    fecharFormProfissional();
    mostrarAviso("Profissional adicionado com sucesso!");
}

function removerProfissional(id) {
    profissionais = profissionais.filter(p => p.id !== id);
    renderizarProfissionais();
    mostrarAviso("Profissional removido.");
}

function renderizarProfissionais() {
    const container = document.getElementById("lista-profissionais-painel");
    if (profissionais.length === 0) {
        container.innerHTML = `<div class="p-4 text-center text-xs text-[#888780] bg-[#232220] border border-[#38362f] rounded-2xl">Nenhum profissional cadastrado.</div>`;
        return;
    }

    container.innerHTML = profissionais.map(p => `
        <div class="bg-[#232220] border border-[#38362f] rounded-2xl p-4 flex items-center justify-between">
            <div>
                <h4 class="text-sm font-semibold text-[#f1efe8]">${p.nome}</h4>
                <p class="text-xs text-[#888780] mt-0.5">${p.cargo}</p>
            </div>
            <button onclick="removerProfissional(${p.id})" class="px-3 py-1.5 rounded-lg border border-[#38362f] bg-transparent text-[#888780] text-xs font-medium hover:bg-[#38362f] hover:text-[#f1efe8] transition-colors">
                Excluir
            </button>
        </div>
    `).join("");
}

// Módulo Financeiro
function renderizarFinanceiro() {
    const totalReceita = historicoFinanceiro.reduce((acc, item) => acc + item.valor, 0);
    const totalCortes = historicoFinanceiro.length;
    const ticketMedio = totalCortes > 0 ? (totalReceita / totalCortes) : 0;

    document.getElementById("fin-receita-mes").textContent = `R$ ${totalReceita.toFixed(2)}`;
    document.getElementById("fin-total-cortes").textContent = totalCortes.toString();
    document.getElementById("fin-ticket-medio").textContent = `R$ ${ticketMedio.toFixed(2)}`;
    document.getElementById("fin-mais-realizado").textContent = totalCortes > 0 ? historicoFinanceiro[0].servico : "—";

    const tabelaCorpo = document.getElementById("fin-tabela-corpo");
    if (historicoFinanceiro.length === 0) {
        tabelaCorpo.innerHTML = `<tr><td colspan="5" class="p-6 text-center text-[#888780]">Nenhum atendimento registrado ainda.</td></tr>`;
        return;
    }

    tabelaCorpo.innerHTML = historicoFinanceiro.map(item => `
        <tr class="border-b border-[#38362f]/50 hover:bg-[#2a2825] transition-colors">
            <td class="p-3 px-4">${item.data}</td>
            <td class="p-3 px-4 font-medium text-[#f1efe8]">${item.cliente}</td>
            <td class="p-3 px-4">${item.servico}</td>
            <td class="p-3 px-4">${item.profissional}</td>
            <td class="p-3 px-4 font-semibold text-[#f1efe8]">R$ ${item.valor.toFixed(2)}</td>
        </tr>
    `).join("");
}

// Auxiliares & Feedbacks
function mostrarAviso(mensagem) {
    const elAviso = document.getElementById("aviso");
    elAviso.textContent = mensagem;
    elAviso.classList.remove("opacity-0", "pointer-events-none", "translate-y-2.5");
    elAviso.classList.add("opacity-100", "translate-y-0");

    setTimeout(() => {
        elAviso.classList.remove("opacity-100", "translate-y-0");
        elAviso.classList.add("opacity-0", "pointer-events-none", "translate-y-2.5");
    }, 3000);
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
    document.getElementById("psrv-nome").value = "";
    document.getElementById("psrv-preco").value = "";
    document.getElementById("psrv-tempo").value = "";
    document.getElementById("psrv-foto").value = "";
}

function limparInputsProfissional() {
    document.getElementById("ppro-nome").value = "";
    document.getElementById("ppro-cargo").value = "";
    document.getElementById("ppro-foto").value = "";
}

function sairDaConta() {
    mostrarAviso("Saindo do painel...");
}
/* ============================================================
   GESTOR PAINEL — CLIENTES
   Requer gestor-painel-utilitarios.js carregado antes deste arquivo.
   ============================================================ */

estado.abaAtual = "clientes";

/* ============================================================
   MAPPING DOM
   ============================================================ */

Object.assign(els, {
    // Clientes
    buscaCliente: document.getElementById("busca-cliente"),
    tabelaClientesCorpo: document.getElementById("tabela-clientes-corpo"),
});

/* ============================================================
   ABA 5: CLIENTES (AGREGAÇÃO DE CLIENTES A PARTIR DE AGENDAMENTOS)
   ============================================================ */

function extrairClientes() {
    const mapaClientes = {};

    agendamentos.forEach(a => {
        if (!a.cliente) return;
        const chave = a.cliente.toLowerCase().trim();
        
        if (!mapaClientes[chave]) {
            mapaClientes[chave] = {
                nome: a.cliente,
                telefone: a.telefone || "Não informado",
                ultimaVisita: a.data,
                totalVisitas: 0,
                totalGasto: 0
            };
        }

        if (a.data > mapaClientes[chave].ultimaVisita) {
            mapaClientes[chave].ultimaVisita = a.data;
        }

        if (a.status === "concluido") {
            mapaClientes[chave].totalVisitas += 1;
            mapaClientes[chave].totalGasto += Number(a.valor || 0);
        }
    });

    return Object.values(mapaClientes);
}

function renderizarClientes(filtro = "") {
    if (!els.tabelaClientesCorpo) return;

    const clientes = extrairClientes();
    const termo = filtro.toLowerCase().trim();

    const filtrados = clientes.filter(c => 
        c.nome.toLowerCase().includes(termo) || 
        c.telefone.toLowerCase().includes(termo)
    );

    if (filtrados.length === 0) {
        els.tabelaClientesCorpo.innerHTML = `<tr><td colspan="5" class="p-6 text-center text-[#888780]">Nenhum cliente encontrado.</td></tr>`;
        return;
    }

    els.tabelaClientesCorpo.innerHTML = filtrados.map(c => `
        <tr class="border-b border-[#38362f] hover:bg-[#2a2825]/50 transition-colors">
            <td class="p-3.5 px-4 font-medium text-[#f1efe8]">${c.nome}</td>
            <td class="p-3.5 px-4 text-[#888780]">${c.telefone}</td>
            <td class="p-3.5 px-4 text-[#888780]">${formatarDataExtenso(c.ultimaVisita)}</td>
            <td class="p-3.5 px-4 font-medium">${c.totalVisitas} visita(s)</td>
            <td class="p-3.5 px-4 font-semibold text-[#9fe1cb]">${formatarMoeda(c.totalGasto)}</td>
        </tr>
    `).join("");
}

function filtrarClientes() {
    const valor = els.buscaCliente ? els.buscaCliente.value : "";
    renderizarClientes(valor);
}

/* ============================================================
   INICIALIZAÇÃO
   ============================================================ */

function iniciar() {
    renderizarClientes();
}

iniciar();

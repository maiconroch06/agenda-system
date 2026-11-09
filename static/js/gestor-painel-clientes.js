/* ============================================================
   GESTOR PAINEL — CLIENTES
   Requer gestor-painel-utilitarios.js carregado antes deste arquivo.
   ============================================================ */

estado.abaAtual = "clientes";

/* ============================================================
   INICIALIZAÇÃO & FILTRO DE BUSCA LOCAL
   ============================================================ */

function iniciar() {
    // Carrega a data no cabeçalho, provida pelo utilitários
    if (typeof carregarData === "function") {
        carregarData();
    }

    // Configura o filtro de clientes em tempo real no Front-end
    const inputBusca = document.getElementById("busca-cliente");
    
    if (inputBusca) {
        inputBusca.addEventListener("input", function (e) {
            const termo = e.target.value.toLowerCase();
            const linhas = document.querySelectorAll(".cliente-row");
            let visiveis = 0;

            linhas.forEach(linha => {
                const nome = linha.querySelector(".cliente-nome")?.textContent.toLowerCase() || "";
                const tel = linha.querySelector(".cliente-tel")?.textContent.toLowerCase() || "";
                
                // Oculta a linha se não bater com a pesquisa
                if (nome.includes(termo) || tel.includes(termo)) {
                    linha.style.display = "";
                    visiveis++;
                } else {
                    linha.style.display = "none";
                }
            });

            // Gerencia a exibição da mensagem de "Nenhum cliente encontrado"
            let linhaVazia = document.getElementById("linha-vazia-busca");
            
            if (visiveis === 0 && linhas.length > 0) {
                if (!linhaVazia) {
                    const tbody = document.getElementById("tabela-clientes-corpo");
                    linhaVazia = document.createElement("tr");
                    linhaVazia.id = "linha-vazia-busca";
                    linhaVazia.innerHTML = `<td colspan="5" class="p-6 text-center text-[#888780]">Nenhum cliente encontrado para "${e.target.value}".</td>`;
                    tbody.appendChild(linhaVazia);
                }
            } else if (linhaVazia) {
                linhaVazia.remove();
            }
        });
    }
}

iniciar();
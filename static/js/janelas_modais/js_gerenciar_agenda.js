document.addEventListener("DOMContentLoaded", function () {
    // Seleciona o elemento modal
    const modalAgenda = document.getElementById("janela_modal_cadastrar_editar_agenda");
    
    // Seleciona os botões
    const btnAbrirModal = document.getElementById("btn-abrir-modal-agenda"); // Crie um botão com esse ID para testar
    const btnCancelar = document.getElementById("btn-cancelar-agenda");
    const formAgenda = document.getElementById("form-agenda");

    // Função para ABRIR o modal
    function abrirModalAgenda(dados = null) {
        if (modalAgenda) {
            if (dados) {
                // Modo Edição: preenche os campos
                document.getElementById("form-title-agenda").textContent = "Editar Agenda";
                document.getElementById("form-subtitle-agenda").textContent = "Atualize as informações da agenda";
                document.getElementById("agenda-id").value = dados.id || "";
                document.getElementById("agenda-nome").value = dados.nome || "";
                document.getElementById("agenda-data-inicio").value = dados.data_inicio || "";
                document.getElementById("agenda-data-fim").value = dados.data_fim || "";
            } else {
                // Modo Cadastro: limpa os campos
                formAgenda.reset();
                document.getElementById("form-title-agenda").textContent = "Cadastrar Agenda";
                document.getElementById("form-subtitle-agenda").textContent = "Defina o nome e o período de funcionamento";
                document.getElementById("agenda-id").value = "";
            }
            
            // Abre o modal com a camada escurecida ao fundo (backdrop)
            modalAgenda.showModal();
        }
    }

    // Função para FECHAR o modal
    function fecharModalAgenda() {
        if (modalAgenda) {
            modalAgenda.close();
        }
    }

    // Evento de clique para abrir (Exemplo)
    if (btnAbrirModal) {
        btnAbrirModal.addEventListener("click", function () {
            abrirModalAgenda();
        });
    }

    // Evento de clique no botão Cancelar
    if (btnCancelar) {
        btnCancelar.addEventListener("click", fecharModalAgenda);
    }

    // Fecha o modal ao clicar fora dele (no fundo escuro / backdrop)
    if (modalAgenda) {
        modalAgenda.addEventListener("click", function (event) {
            const rect = modalAgenda.getBoundingClientRect();
            const clicouFora = (
                event.clientX < rect.left ||
                event.clientX > rect.right ||
                event.clientY < rect.top ||
                event.clientY > rect.bottom
            );
            if (clicouFora) {
                fecharModalAgenda();
            }
        });
    }
});
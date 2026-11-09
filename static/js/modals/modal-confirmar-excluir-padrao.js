//const modal = document.querySelector("#modal");
const form_remover_servico = document.querySelectorAll('#form-confirmar-exclusao');// seleciona todos os forms criados pelo for da tela de servicos
const botao_fechar = document.querySelector("#botao-fechar");
const botao_cancelar = document.querySelector("#botao-cancelar");
const botao_aceitar= document.querySelector("#botao-aceitar");

const conteiner_div_mensagem_modal = document.getElementById("mensagem_modal_servico_excluir");
const descricao_classe = document.getElementById("titulo-modal");
const titulo_janela_modal = document.getElementById("titulo-janela-modal");


// trabalahdno com multiplos formularios
// preciso selecionar qual formulario disparou o evento
// por que não var? Porque let possui um escopo mais previsível e é a escolha recomendada para variáveis que precisam mudar de valor.
let formSelecionado = null;

form_remover_servico.forEach(

    (formulario) => {

    formulario.addEventListener('submit', (event) => {

        formSelecionado = formulario;
        event.preventDefault();
        
        // O método closest() sobe pela hierarquia do HTML procurando o primeiro elemento que corresponda ao seletor informado.
        const card = formSelecionado.closest("#card_servicos");
        
        const descricao_servico = card.querySelector("#campo-padrao");

        titulo_janela_modal.textContent = " Confirmar exclusão de "+ descricao_classe.textContent;

        conteiner_div_mensagem_modal.innerHTML= "<p> Excluir o "+descricao_classe.textContent +": <strong> "+  descricao_servico.textContent  + " </strong>? </p> Todos os agendamentos com este serviço serão excluidos." ;
                
        modal.showModal();
    });
});


botao_fechar.addEventListener('click', ()=>{
    modal.close();
});

botao_cancelar.addEventListener('click', ()=>{
    modal.close();
});

botao_aceitar.addEventListener('click', ()=>{
    modal.close();
    if (formSelecionado){
        formSelecionado.submit();
    }
    
});
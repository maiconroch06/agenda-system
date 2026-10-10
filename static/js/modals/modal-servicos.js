const modal = document.querySelector("#modal");
const form_remover_servico = document.querySelectorAll('#form-confirmar-exclusao');// seleciona todos os forms criados pelo for da tela de servicos
const botao_fechar = document.querySelector("#botao-fechar");
const botao_cancelar = document.querySelector("#botao-cancelar");
const botao_aceitar= document.querySelector("#botao-aceitar");

// trabalahdno com multiplos formularios
// preciso selecionar qual formulario disparou o evento
// por que não var? Porque let possui um escopo mais previsível e é a escolha recomendada para variáveis que precisam mudar de valor.
let formSelecionado = null;

form_remover_servico.forEach(
    (formulario) => {
    formulario.addEventListener('submit', (event) => {

        formSelecionado = formulario;

        event.preventDefault();
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
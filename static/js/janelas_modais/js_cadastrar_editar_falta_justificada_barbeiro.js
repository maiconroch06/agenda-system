const modal_editar_faltas_justificadas_barbeiro = document.getElementById("janela_modal_cadastrar_editar_faltas_justificadas_barbeiro");
const botao_editar = document.querySelectorAll("#editar-servico");
const botao_fechar_modal_faltas_justificadas = document.querySelector("#fechar-modal-falta-justificada");
const botao_fechar_modal_faltas_justificadas_local = document.querySelector("#fechar_modal_falta_justificada");
const botao_cadastrar_faltas_justificadas_global = document.querySelectorAll("#botao_cadastrar_falta_barbeiro");
const botao_editar_faltas_justificadas_global = document.querySelectorAll("#editar-agenda-mensal");
const titulo_modal_faltas_justificadas = document.querySelector("#titulo_modal_faltas_justificadas");


// campos do formulario
const formulario_faltas_justificadas = document.querySelector("#form_faltas_justificadas");

// campos do html do MODAL
const form_campo_id_barbeiro = document.getElementById("id_barbeiro_falta");
const form_campo_id_falta_justificativa = document.getElementById("id_falta_justificativa");
const form_campo_nome_barbeiro = document.getElementById("nome_barbeiro_falta");
const form_campo_data_falta_justificada = document.getElementById("data_falta");
const form_campo_hora_inicio_falta = document.getElementById("hora_inicio_falta");
const form_campo_hora_fim_falta = document.getElementById("hora_fim_falta");
const form_campo_motivo_falta = document.getElementById("motivo_falta_justificada");
const botao_cadastrar_editar_faltas_justificadas_modal = document.getElementById("cadastrar-editar-falta");

botao_editar_faltas_justificadas_global.forEach((editar)=>{
    editar.addEventListener("click", ()=>{
       const dados_barbeiro =editar.value.split("#");

        form_campo_id_barbeiro.value = dados_barbeiro[0];
        form_campo_id_falta_justificativa.value = dados_barbeiro[2];
        form_campo_nome_barbeiro.value = dados_barbeiro[1];
        form_campo_data_falta_justificada.value=dados_barbeiro[3];
        form_campo_hora_inicio_falta.value=dados_barbeiro[4];
        form_campo_hora_fim_falta.value=dados_barbeiro[5];
        form_campo_motivo_falta.value = dados_barbeiro[6];
        
        botao_cadastrar_editar_faltas_justificadas_modal.textContent = "Editar falta justificada";
        titulo_modal_faltas_justificadas.textContent = botao_cadastrar_editar_faltas_justificadas_modal.textContent;
        formulario_faltas_justificadas.action = "/gestor/painel/barbeiros/faltas-justificadas/atualizar";

        modal_editar_faltas_justificadas_barbeiro.showModal();
    });

});


botao_cadastrar_faltas_justificadas_global.forEach((cadastrar)=>{
    cadastrar.addEventListener("click", ()=>{
       const dados_barbeiro =cadastrar.value.split("#");

        form_campo_id_barbeiro.value = dados_barbeiro[0];
        form_campo_nome_barbeiro.value = dados_barbeiro[1];
        form_campo_data_falta_justificada.value=new Date().toLocaleDateString("en-CA");
        
        botao_cadastrar_editar_faltas_justificadas_modal.textContent = "Cadastrar falta justificada";
        titulo_modal_faltas_justificadas.textContent = botao_cadastrar_editar_faltas_justificadas_modal.textContent;
        formulario_faltas_justificadas.action = "/gestor/painel/barbeiros/faltas-justificadas/cadastrar";

        modal_editar_faltas_justificadas_barbeiro.showModal();
    });

});


botao_fechar_modal_faltas_justificadas.addEventListener("click", ()=>{
    modal_editar_faltas_justificadas_barbeiro.close();
});

botao_fechar_modal_faltas_justificadas_local.addEventListener("click", ()=>{
    modal_editar_faltas_justificadas_barbeiro.close();
});

modal_editar_faltas_justificadas_barbeiro.addEventListener("close", () => {
    document.getElementById("div-validation-message").classList.add("hidden");
});

formulario_faltas_justificadas.addEventListener("submit", (event)=>{
   event.preventDefault();
    const message = document.querySelector("#validation_menssage_falta_justificada");
    const div_messagem = document.querySelector("#div_validation_message_falta_justificada");

    message.textContent = ''; 

    console.log(formulario_faltas_justificadas.action);
    
    const erros = validarValoresFaltaJustificada();

    if (erros.length > 0){
        
            erros.forEach(
                    function(erro){
                        message.innerHTML += erro + '</br>';
                    }
                );

                
        div_messagem.classList.remove('hidden'); // Remove a ocultação do elemento
    
    }else{
        modal_editar_faltas_justificadas_barbeiro.close();
        formulario_faltas_justificadas.submit();
    }
    
});

function limpar_campos_modal_faltas_justificadas(){
    form_campo_data_falta_justificada.classList.remove("border-red-400");
    form_campo_motivo_falta.classList.remove("border-red-400");
    form_campo_hora_inicio_falta.classList.remove("border-red-400");
    form_campo_hora_fim_falta.classList.remove("border-red-400");
}


function validarValoresFaltaJustificada(){

    const errors = []; 
    const data_atual = new Date();
    

    if (form_campo_data_falta_justificada.value===''){
         form_campo_data_falta_justificada.classList.add("border-red-400");
        errors.push('O campo data não pode ser vazio!');
    }else if (form_campo_data_falta_justificada.value < data_atual.toLocaleDateString('en-CA') ){
         form_campo_data_falta_justificada.classList.add("border-red-400");
        errors.push('O campo data não poder ser menor que a data atual. Data atual [ ', data_atual.toLocaleDateString("pt-br")+' ]');

    }

    if (form_campo_motivo_falta.value===''){
        form_campo_motivo_falta.classList.add("border-red-400");
        errors.push('O campo motivo da falta é obrigatório e deve ser preenchido!');
    }

    if(form_campo_hora_inicio_falta.value==='' ){
        form_campo_hora_inicio_falta.classList.add("border-red-400");
        errors.push('Os campos hora inicio é obrigatório e deve ser preenchido!');
    }else if( form_campo_hora_fim_falta.value===''){
            form_campo_hora_fim_falta.classList.add("border-red-400");
            errors.push('O campos hora fim é obrigatório e deve ser preenchido!');
    }else if (form_campo_hora_inicio_falta.value > form_campo_hora_fim_falta.value){
        form_campo_hora_inicio_falta.classList.add("border-red-400");
        form_campo_hora_fim_falta.classList.add("border-red-400");
        errors.push('O campo hora inicio não pode ser menor que o campo hora fim');
    }
    
    return errors;     
        
}
    
modal_editar_faltas_justificadas_barbeiro.addEventListener("close", () => {
    limpar_campos_modal_faltas_justificadas();
    document.getElementById("div_validation_message_falta_justificada").classList.add("hidden");
});
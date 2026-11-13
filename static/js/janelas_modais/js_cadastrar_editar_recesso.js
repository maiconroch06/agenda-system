const dlg_editar_cadastrar_recesso = document.querySelector("#janela_modal_cadastrar_editar_recesso");
const botao_cadastrar_recesso_global = document.querySelector("#btn-abrir-modal-recesso");
const botao_editar_recesso_global = document.querySelectorAll("#editar-recesso-mensal");

const form_campo_id_recesso = document.getElementById("id_recesso");
const form_campo_descricao_recesso = document.getElementById("motivo_recesso");
const form_campo_data_inicio_recesso = document.getElementById("data_inicio_recesso");
const form_campo_data_fim_recesso = document.getElementById("data_fim_recesso");

const txt_cadastrar_recesso = document.getElementById("btn-cadastrar-recesso");
const btn_cancelar_recesso = document.getElementById("btn-cancelar-recesso");
const txt_titulo_modal_recesso = document.getElementById("form-title-recesso");

const formulario = document.getElementById("form-agenda-recesso");

botao_editar_recesso_global.forEach(

    (editar)=>{

    editar.addEventListener("click", (event)=>{
        const dados_agenda = editar.value.split("#");

        form_campo_id_recesso.value = dados_agenda[0];
        form_campo_descricao_recesso.value = dados_agenda[1];
        form_campo_data_inicio_recesso.value = dados_agenda[2];
        form_campo_data_fim_recesso.value = dados_agenda[3];

        txt_titulo_modal_recesso.textContent = "Atualizar agenda: "+ form_campo_descricao_recesso.value

        document.getElementById("btn-cadastrar-recesso").textContent="Atualizar agenda";

        formulario.action = "/gestor/painel/recessos/atualizar";

        dlg_editar_cadastrar_recesso.showModal();

        
    });
});


botao_cadastrar_recesso_global.addEventListener("click", ()=>{
    const data_atual = new Date();
    txt_titulo_modal_recesso.textContent= "Cadastrar Recesso";
    
    form_campo_data_inicio_recesso.value = data_atual.toLocaleDateString('en-CA');
    form_campo_data_fim_recesso.value = data_atual.toLocaleDateString('en-CA');
    form_campo_descricao_recesso.value= '';

    formulario.action = "/gestor/painel/recessos/cadastrar";

    dlg_editar_cadastrar_recesso.showModal();
});

formulario.addEventListener("submit", (event)=>{

    const message = document.querySelector("#validation-menssage");
    const div_messagem = document.querySelector("#div-validation-message");
    message.textContent = '';
   
    const erros = validacoes();
   
    if (erros.length > 0){
        event.preventDefault();
        erros.forEach(
                function(erro){
                    message.innerHTML += erro + '</br>';
                }
            );
            
            div_messagem.classList.remove('hidden'); // Remove a ocultação do elemento
    }else{
        dlg_editar_cadastrar_recesso.close();
        formulario.submit();
    }

});


btn_cancelar_recesso.addEventListener("click", ()=>{
    dlg_editar_cadastrar_recesso.close();
});


dlg_editar_cadastrar_recesso.addEventListener("close", ()=>{
    document.getElementById("div-validation-message").classList.add("hidden");
});

function validacoes(){
    const erros = [];
    const data_atual = new Date();

    if (form_campo_descricao_recesso.value===''){
         erros.push('ATENÇÃO, campo titulo da recesso é obrigatorio!');
    }
    if (form_campo_data_inicio_recesso.value==='' || form_campo_data_fim_recesso.value===''){
         erros.push('ATENÇÃO, campos data inicio e data fim da recesso são obrigatorio!');
    }else if(form_campo_data_inicio_recesso.value < data_atual.toLocaleDateString('en-CA') || form_campo_data_fim_recesso.value < data_atual.toLocaleDateString('en-CA')){
        erros.push('ATENÇÃO, campos data inicio e data fim da recesso não pode ser menos que a data atual [ '+data_atual.toLocaleDateString('pt-br')+' ]');
    }
    else if(form_campo_data_inicio_recesso.value > form_campo_data_fim_recesso.value){
        erros.push('ATENÇÃO, A data inicio do recesso não pode ser maior que sua data fim.');
    }

    return erros;
}


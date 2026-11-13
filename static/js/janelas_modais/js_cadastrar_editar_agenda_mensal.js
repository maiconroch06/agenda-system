const dlg_modal_cadastrar_editar_agenda_mensal = document.getElementById("janela_modal_cadastrar_editar_agenda");

const btn_cadastrar_agenda_mensal = document.getElementById("btn-abrir-modal-agenda");
const btn_fechar_modal = document.getElementById("btn-cancelar-agenda");
const btn_editar_agenda_mensal = document.querySelectorAll("#editar-agenda-mensal");
const dlg_form_agenda_mensal = document.getElementById("form-agenda-mensal");
const ipt_titulo_agenda = document.getElementById("titulo_agenda");
const ipt_data_inicio = document.getElementById("agenda-data-inicio");
const ipt_data_fim = document.getElementById("agenda-data-fim");
const id_agenda = document.getElementById("id_agenda");


btn_cadastrar_agenda_mensal.addEventListener("click", (event)=>{
    const dataAtual = new Date();
    ipt_data_inicio.value =  dataAtual.toLocaleDateString('en-CA');
    ipt_data_fim.value = dataAtual.toLocaleDateString('en-CA');

    ipt_titulo_agenda.value =  '';
    dlg_modal_cadastrar_editar_agenda_mensal.showModal();

    document.getElementById("btn-salvar-agenda").textContent="Cadastrar agenda";

    dlg_form_agenda_mensal.action = "/gestor/painel/agenda_mensal/cadastrar";
});

btn_editar_agenda_mensal.forEach((editar)=>{
    editar.addEventListener("click", (event)=>{
        const dados_agenda = editar.value.split("#");

        id_agenda.value = dados_agenda[0];
        ipt_data_inicio.value = dados_agenda[2];
        ipt_data_fim.value = dados_agenda[3];

        ipt_titulo_agenda.value = dados_agenda[1];

        document.getElementById("btn-salvar-agenda").textContent="Atualizar agenda";

        dlg_form_agenda_mensal.action = "/gestor/painel/agenda_mensal/atualizar";

        dlg_modal_cadastrar_editar_agenda_mensal.showModal();

        
    });
});




btn_fechar_modal.addEventListener("click", ()=>{
    dlg_modal_cadastrar_editar_agenda_mensal.close();
});

dlg_form_agenda_mensal.addEventListener("submit", (event)=>{
   
    const message = document.querySelector("#validation-menssage");
    const div_messagem = document.querySelector("#div-validation-message");
    message.textContent = '';
   
    const erros = validacoes();
    console.log("erros passou ");

    if (erros.length > 0){
        event.preventDefault();
        erros.forEach(
                function(erro){
                    message.innerHTML += erro + '</br>';
                }
            );
            
            div_messagem.classList.remove('hidden'); // Remove a ocultação do elemento
    }else{
        dlg_form_agenda_mensal.close();
        dlg_form_agenda_mensal.submit();
    }
});


function validacoes(){
    const erros = [];
    const data_atual = new Date();

    if (ipt_titulo_agenda.value===''){
         erros.push('ATENÇÃO, campo titulo da agenda é obrigatorio!');
    }
    if (ipt_data_inicio.value==='' || ipt_data_fim.value===''){
         erros.push('ATENÇÃO, campos data inicio e data fim da agenda são obrigatorio!');
    }else if(ipt_data_inicio.value < data_atual.toLocaleDateString('en-CA') || ipt_data_fim.value < data_atual.toLocaleDateString('en-CA')){
        erros.push('ATENÇÃO, campos data inicio e data fim da agenda não pode ser menos que a data atual [ '+data_atual.toLocaleDateString('pt-br')+' ]');
    }
    else if(ipt_data_inicio.value > ipt_data_fim.value){
        erros.push('ATENÇÃO, A data inicio da agenda não pode ser maior que a data fim.');
    }

    

    return erros;
}

dlg_modal_cadastrar_editar_agenda_mensal.addEventListener("close", () => {
    document.getElementById("div-validation-message").classList.add("hidden");
});
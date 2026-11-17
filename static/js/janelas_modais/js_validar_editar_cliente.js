const modal_editar_cliente = document.querySelector("#janela_modal_editar_cliente");

const botao_editar_cliente_global = document.querySelectorAll("#atualizar-cliente-barbearia");
const botao_limpar_consulta_cliente_global = document.getElementById("limpar-consulta-cliente");
const titulo = document.getElementById("nome_cliente");

const nome_cliente_editar = document.getElementById("cliente_nome");
const id_cliente_editar = document.getElementById("cliente_id");
const telefone = document.getElementById("cliente_telefone");
const email = document.getElementById("cliente_email");
const senha = document.getElementById("cliente_senha");
const confirmar_senha = document.getElementById("cliente_confirmar_senha");
const cliente_motivo_bloqueio = document.getElementById("cliente_motivo_bloqueio");
const cliente_status_cliente = document.getElementById("status_cliente");
const cliente_cpf = document.getElementById("cliente_cpf");

const botao_fechar_modal = document.getElementById("btn_cancelar_modal_cliente");

const formulario = document.getElementById("form_cliente_atualizar");
const formulario_consultar_cliente_nome = document.getElementById("form-consultar-cliente-nome");

/*
const nome_cliente_titulo = document.getElementById("campo-padrao");

*/

formulario_consultar_cliente_nome.addEventListener("submit",(event)=>{
    event.preventDefault();

    const message = document.querySelector("#validation-menssage");
    const div_messagem = document.querySelector("#div-validation-message");
   
    message.textContent = '';

    const input_consultar_cliente = document.getElementById("input-nome-cliente-consulta");

    if (input_consultar_cliente.value.trim() === ''){
        input_consultar_cliente.classList.remove(("border-[#38362f]"));
        input_consultar_cliente.classList.add(("border-red-400"));
        message.innerHTML = 'Campo de pesquisa nome não pode ser vazio.';
        div_messagem.classList.remove('hidden');
        return;
    }
    formulario_consultar_cliente_nome.submit();
    

});

let descricao_anterior = '';

botao_limpar_consulta_cliente_global.addEventListener("click", ()=>{
    botao_limpar_consulta_cliente_global.classList.add("hidden");
    window.location.href ="/gestor/painel/clientes";
});

botao_editar_cliente_global.forEach(
    (editar)=>{
        editar.addEventListener("click", (event)=>{
           // titulo.textContent = "Editar barbeiro: "+ nome_barbeiro_titulo.textContent;
            const detalhes_cliente = editar.value.split("#");
            limparCampos();
          

            id_cliente_editar.value = detalhes_cliente[0];
            nome_cliente_editar.value = detalhes_cliente[1];
            telefone.value = (detalhes_cliente[2])? "("+detalhes_cliente[2].slice(0,2)+") "+detalhes_cliente[2].slice(2,7)+"-"+detalhes_cliente[2].slice(7,11) :'';
            email.value = detalhes_cliente[3];

            cliente_status_cliente.value=detalhes_cliente[4];
            cliente_motivo_bloqueio.value=detalhes_cliente[5];
            cliente_cpf.value=detalhes_cliente[6];

            

            if(cliente_status_cliente.value ==0){
                document.getElementById("ativado_cliente").selected = false;
                document.getElementById("desativado_cliente").selected = true;
            }else{
                document.getElementById("ativado_cliente").selected = true;
                document.getElementById("desativado_cliente").selected = false; 
            }

           
            modal_editar_cliente.showModal();
          
    });
    
});

cliente_status_cliente.addEventListener("change",()=>{
    
    if (cliente_motivo_bloqueio.value !=='') { descricao_anterior = cliente_motivo_bloqueio.value }

    cliente_motivo_bloqueio.value= (cliente_status_cliente.value==1)?'':descricao_anterior;
});

modal_editar_cliente.addEventListener("close", ()=>{
    document.getElementById("div-validation-message").classList.add("hidden");
});

botao_fechar_modal.addEventListener("click", (event)=>{
    modal_editar_cliente.close();
});


formulario.addEventListener("submit", (event)=>{  
    
   limparCampos();
event.preventDefault();

    const message = document.querySelector("#validation-menssage");
    const div_messagem = document.querySelector("#div-validation-message");
    message.textContent = '';

    const erros = validacoesBarbeiros();
   
    if (erros.length > 0){
       
        erros.forEach(
                function(erro){
                    message.innerHTML += erro + '</br>';
                }
            );
            
            div_messagem.classList.remove('hidden'); // Remove a ocultação do elemento
    }else{
        modal_editar_cliente.close();
       formulario.submit();
    }

});




function validacoesBarbeiros(){

    const errors = [];
    

    
    if (nome_cliente_editar.value === ""){
        nome_cliente_editar.classList.add("border-red-400");
        errors.push("O nome precisa não pode ser vazio!");
    }
    if (email.value === "" ){
        email.classList.add("border-red-400");
        errors.push("O email não pode ser vazio precisa ser preenchido!");
    }else if(!email.value.includes("@")){
        email.classList.add("border-red-400");
        errors.push("O email  precisa conter @!");
    }else  if (!email.value.includes('.')) {
        email.classList.add("border-red-400");
        errors.push('ATENÇÃO, o e-mail deve possuir .');
    }else if (email.value.endsWith('.')) {//verifica se o texto termina com .
        email.classList.add("border-red-400");
        errors.push('ATENÇÃO, o e-mail não pode terminar com .');
    }
    if (senha.value !== confirmar_senha.value){
        senha.classList.add("border-red-400");
        confirmar_senha.classList.add("border-red-400");
        errors.push("confirmar senha diferente de senha, as senhas precisa ser iguais!");
    }
    if (telefone.value === ""){
        telefone.classList.add("border-red-400");
        errors.push("O telefone precisa ser preenchido!");
    }else if(telefone.value.length<15){
        telefone.classList.add("border-red-400");
        errors.push("telefone incompleto, por favor verifique o número digitado.");
    }
   
    if (cliente_status_cliente.value == 0 && cliente_motivo_bloqueio.value===''){
        cliente_motivo_bloqueio.classList.add("border-red-400");
        errors.push("Você desativou o cliente, por isso O campo motivo deve ser preenchido!");
    }else if (cliente_status_cliente.value == 1 && cliente_motivo_bloqueio.value!==''){
        cliente_motivo_bloqueio.classList.add("border-red-400");
        errors.push("Você ativou o cliente, por isso O campo motivo deve ser vazio!");
    }

    return errors;     
        
}

function limparCampos(){
   
    nome_cliente_editar.classList.remove("border-red-400");
    email.classList.remove("border-red-400");
    senha.classList.remove("border-red-400");
    confirmar_senha.classList.remove("border-red-400");
    telefone.classList.remove("border-red-400");
    cliente_status_cliente.classList.remove("border-red-400");
    cliente_motivo_bloqueio.classList.remove("border-red-400");
    
    document.getElementById("div-validation-message").classList.add("hidden");
    
}




/*============================================================
  MÁSCARAS
  ============================================================ */
function aplicarMascaras() {
   telefone?.addEventListener("input", (e) => {
       let value = e.target.value.replace(/\D/g, "").slice(0, 11);
       value = value.replace(/^(\d{2})(\d)/, "($1) $2").replace(/(\d{4,5})(\d{4})$/, "$1-$2");
       e.target.value = value;
   });

}

    



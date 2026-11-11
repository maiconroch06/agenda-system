const modal_editar_barbeiro_endereco = document.getElementById("janela_modal_cadastrar_editar_endereco");
const titulo = document.getElementById("form-title-endereco");
const nome_barbeiro_titulo = document.getElementById("campo-padrao");

const botao_editar_barbeiro_endereco = document.querySelectorAll("#editar-endereco");

const botao_fechar_janela_endereco = document.getElementById("btn-cancelar-endereco");

const formulario = document.getElementById("form-endereco-barbeiro");

// campos
const cep_end = document.getElementById("bar-end-cep");
const id_end = document.getElementById("bab-end-id");
const uf_end = document.getElementById("bar-end-uf");
const cidade = document.getElementById("bar-end-cidade");
const bairro_end = document.getElementById("bar-end-bairro");
const logradouro_end = document.getElementById("bar-end-logradouro");
const numero_end = document.getElementById("bar-end-numero");
const complemento = document.getElementById("bar-end-complemento");
const sequencia = document.getElementById("bar-end-sequencia");


botao_editar_barbeiro_endereco.forEach(
    (editar_endereco)=>{
        editar_endereco.addEventListener("click", (event)=>{
            titulo.textContent =  nome_barbeiro_titulo.textContent;
            const detalhes_endereco_barbeiro = editar_endereco.value.split("&");

           inicializarMensagensErros();
          
            cep_end.value = detalhes_endereco_barbeiro[1] ?? "";
            id_end.value = detalhes_endereco_barbeiro[0] ?? "";
            uf_end.value = detalhes_endereco_barbeiro[3] ?? "";
            cidade.value = detalhes_endereco_barbeiro[2] ?? "";
            bairro_end.value = detalhes_endereco_barbeiro[6] ?? "";
            logradouro_end.value = detalhes_endereco_barbeiro[4] ?? "";
            numero_end.value = detalhes_endereco_barbeiro[5] ?? "";
            sequencia.value = detalhes_endereco_barbeiro[7] ?? "";
            complemento.value = detalhes_endereco_barbeiro[8] ?? "";

            modal_editar_barbeiro_endereco.showModal();
    });
    
});

formulario.addEventListener("submit", (event)=>{  
     event.preventDefault();

    inicializarMensagensErros();

    const erros = validarValores();

    console.log(erros);

    if (erros.length > 0){
       
        erros.forEach(
                function(erro){
                    document.querySelector("#menssagem-erros-endereco").innerHTML += erro + '</br>';
                }
            );
            document.getElementById("exibir-menssagem-erros-endereco").classList.remove('hidden'); // Remove a ocultação do elemento
    }else{
        modal_editar_barbeiro_endereco.close();
        formulario.submit();
    }
});


botao_fechar_janela_endereco.addEventListener("click", (event)=>{
    modal_editar_barbeiro_endereco.close();
});


function inicializarMensagensErros(){
    const mensagem = document.querySelector("#menssagem-erros-endereco").textContent = "";
    document.getElementById("exibir-menssagem-erros-endereco").classList.add("hidden"); 
    
}

function validarValores(){

    const errors = [];
    
    if (cep_end.value === null || cep_end.value.trim() === "" ){
        errors.push("campo cep vazio ou nulo, por favor preencha!");
    }
     if (cidade.value === null || cidade.value.trim() === "" ){
        errors.push("campo cidade vazio ou nulo, por favor preencha!");
    }
     if (bairro_end.value === null || bairro_end.value.trim() === "" ){
        errors.push("campo bairro vazio ou nulo, por favor preencha!");
    }
     if (uf_end.value === null || uf_end.value.trim() === "" ){
        errors.push("campo estado vazio ou nulo, por favor preencha!");
    }
     if (logradouro_end.value === null || logradouro_end.value.trim() === "" ){
        errors.push("campo logradouro vazio ou nulo, por favor preencha!");
    }
     
    if (isNaN(numero_end.value)) {
       errors.push("O campo número aceita apenas valores numéricos!"); 
    }else if (Number(numero_end.value)<=0){
         errors.push("O campo número aceita apenas valores maior que zero!"); 
    }

    return errors;             
}

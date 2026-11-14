const modal_cadastrar_editar_barbeiro = document.querySelector("#janela_modal_cadastrar_editar_barbeiro");

const botao_editar_barbeiro = document.querySelectorAll("#editar-barbeiro");
const titulo = document.getElementById("form-title");
const formulario = document.getElementById("form-barbeiro");
const botao_voltar = document.getElementById("btn-cancelar");

//campos
const cpf = document.getElementById("bar-cpf");
const nome_barbeiro_titulo = document.getElementById("campo-padrao");
const nome_barbeiro_editar = document.getElementById("bar-nome");
const email = document.getElementById("bar-email");
const senha = document.getElementById("bar-senha");
const confirmar_senha = document.getElementById("bar-confirmar-senha");
const telefone = document.getElementById("bar-telefone");
const bio = document.getElementById("bar-bio");
const id = document.getElementById("bar-id");
const especialidade = document.getElementById("bar-especialidade");
const anos_experiencia = document.getElementById("bar-anos_experiencia");

const campo_imagem_anterior = document.querySelector("#bar-foto_nome_anterior");
const imagem_preview = document.querySelector('#img_srv-preview');

botao_editar_barbeiro.forEach(
    (editar)=>{
        editar.addEventListener("click", (event)=>{
            titulo.textContent = "Editar barbeiro: "+ nome_barbeiro_titulo.textContent;
            const detalhes_barbeiro = editar.value.split("#");

            id.value = detalhes_barbeiro[0];
            nome_barbeiro_editar.value = detalhes_barbeiro[1];
            cpf.value = detalhes_barbeiro[2].slice(0,3)+"."+detalhes_barbeiro[2].slice(3,6)+"."+detalhes_barbeiro[2].slice(6,9)+"-"+detalhes_barbeiro[2].slice(9,11);
            email.value= detalhes_barbeiro[3];
            telefone.value = detalhes_barbeiro[4];
            bio.value = detalhes_barbeiro[8];
            especialidade.value = detalhes_barbeiro[9];
            anos_experiencia.value = detalhes_barbeiro[10];
            
            imagem_preview.classList.remove("hidden");
            imagem_preview.src = detalhes_barbeiro[5];

            campo_imagem_anterior.value=detalhes_barbeiro[6];
  
            if (detalhes_barbeiro[7]==0){
                document.getElementById("ativado").selected = false;
                document.getElementById("desativado").selected = true;
            }
            else{
                document.getElementById("ativado").selected = true;
                document.getElementById("desativado").selected = false;
            }

            verificarOcultarBotao();
            limparCampos();

            modal_cadastrar_editar_barbeiro.showModal();
          
    });
    
});

modal_cadastrar_editar_barbeiro.addEventListener("close", ()=>{
    document.getElementById("div-validation-message").classList.add("hidden");
});

formulario.addEventListener("submit", (event)=>{  
    
   limparCampos();

    const message = document.querySelector("#validation-menssage");
    const div_messagem = document.querySelector("#div-validation-message");
    message.textContent = '';

    const erros = validacoesBarbeiros();
   
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

import { ocultarExibirBotaoRemoverImagem } from '../validacoes/exibir-imagem-servico.js';

function verificarOcultarBotao(){
    if (!imagem_preview.classList.contains('hidden') && !imagem_preview.src.includes("default.png")) {
        ocultarExibirBotaoRemoverImagem(true);
    } else {
        ocultarExibirBotaoRemoverImagem(false);
    }
    //chamar o campo para verificar se existe imagem
    // mostrar ou ocultar o botão
}


botao_voltar.addEventListener("click", (event)=>{
    modal_cadastrar_editar_barbeiro.close();
});


function validacoesBarbeiros(){

    const errors = [];
    
    if (cpf.value === ""){
        cpf.classList.add("border-red-400");
        errors.push("O cpf precisa ser preenchido!");
    }
    if (nome_barbeiro_editar.value === ""){
        nome_barbeiro_editar.classList.add("border-red-400");
        errors.push("O nome precisa ser preenchido!");
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
    }
    if (bio.value === ""){
        bio.classList.add("border-red-400");
        errors.push("A bio precisa ser preenchido!");
    }
   
    if (especialidade.value === ""){
        especialidade.classList.add("border-red-400");
        errors.push("A especialidade precisa ser preenchido!");
    }
    if (anos_experiencia.value === ""){
        anos_experiencia.classList.add("border-red-400");
        errors.push("O campo anos de experiencia deve ser preenchido!");
    }

    return errors;     
        
}

function limparCampos(){
    cpf.classList.remove("border-red-400");
    nome_barbeiro_editar.classList.remove("border-red-400");
    email.classList.remove("border-red-400");
    senha.classList.remove("border-red-400");
    confirmar_senha.classList.remove("border-red-400");
    telefone.classList.remove("border-red-400");
    bio.classList.remove("border-red-400");
    especialidade.classList.remove("border-red-400");
    anos_experiencia.classList.remove("border-red-400");

    document.getElementById("div-validation-message").classList.add("hidden");
    
}



    



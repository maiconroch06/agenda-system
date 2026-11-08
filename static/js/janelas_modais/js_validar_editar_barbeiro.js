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
const descricao = document.getElementById("bar-descricao");
const id = document.getElementById("bab-id");

const campo_imagem_anterior = document.querySelector("#bab-foto_nome_anterior");
const imagem_preview = document.querySelector('#img_srv-preview');

botao_editar_barbeiro.forEach(
    (editar)=>{
        editar.addEventListener("click", (event)=>{
            titulo.textContent = "Editar barbeiro: "+nome_barbeiro_titulo.textContent ;
            const detalhes_barbeiro = editar.value.split("&");

            id.value = detalhes_barbeiro[0];
            nome_barbeiro_editar.value = detalhes_barbeiro[1];
            cpf.value = detalhes_barbeiro[2];
            email.value= detalhes_barbeiro[3];
            telefone.value = detalhes_barbeiro[4];
            descricao.value = detalhes_barbeiro[8];
            
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

            modal_cadastrar_editar_barbeiro.showModal();
          
    });
    
});

formulario.addEventListener("submit", (event)=>{  
    event.preventDefault();
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


function validarValores(){

    const errors = [];
    

    return errors;     
        
}





    



const modal_editar_servico = document.querySelector("#janela_modal_editar_servico");
const botao_editar = document.querySelectorAll("#editar-servico");
const botao_cancelar_modal_servico = document.querySelector("#fechar-modal-editar");
const botao_cadastrar_editar = document.querySelector("#botao-cadastrar-editar");
const botao_cadastrar_servico = document.getElementById("cadastrar-servico");


// campos do formulario
const campo_descrico_servico = document.querySelector("#srv-nome");
const formulario = document.querySelector("#form-servico");

// campos do html
const descricao_servico = document.querySelector("#srv-descricao-servico");
const valor_servico = document.querySelector("#srv-valor");
const duracao_servico = document.querySelector("#srv-duracao");

const campo_imagem_anterior = document.querySelector("#srv-foto_nome_anterior");

const imagem_preview = document.querySelector('#img_srv-preview');


let tipo_dados = -1;

botao_cadastrar_servico.addEventListener("click", ()=>{
    document.getElementById("div-seletor-status").classList.add("hidden");

    formulario.action ="/gestor/painel/servicos/cadastrar";
    document.getElementById("form-title").textContent = "Cadastrar Serviço";
    botao_cadastrar_editar.textContent="Cadastrar Serviço";

    descricao_servico.value="";
    duracao_servico.value="";
    valor_servico.value="";
    imagem_preview.src="";

    campo_imagem_anterior.value="";
    imagem_preview.classList.add("hidden");

    verificarOcultarBotao();

    modal_editar_servico.showModal();
});


// trabalahdno com multiplos formularios
// preciso selecionar qual formulario disparou o evento
// por que não var? Porque let possui um escopo mais previsível e é a escolha recomendada para variáveis que precisam mudar de valor.
botao_editar.forEach(
    (botao) => {
        botao.addEventListener("click", (event) => {
        event.preventDefault();
        //preencher as informações
        document.getElementById("div-seletor-status").classList.remove("hidden");

        const dados_servicos = botao.value.split('&');

        if (dados_servicos.length === 0){
            return;
        }

        tipo_dados = dados_servicos[6];

        
        
        document.getElementById("form-title").textContent = "Editar Serviço";
        botao_cadastrar_editar.textContent = "Editar Serviço";
        imagem_preview.classList.remove("hidden");
        formulario.action ="/gestor/painel/servicos/editar";
        
        
        document.getElementById("srv-id").value = dados_servicos[0];
        descricao_servico.value  = dados_servicos[1];
        valor_servico.value  = dados_servicos[2];
        duracao_servico.value  = dados_servicos[3];

     
        if (dados_servicos[5] == 1){
            document.getElementById("ativado").selected = true;
             document.getElementById("desativado").selected = false;
        }else{
            document.getElementById("desativado").selected = true;
        }

        imagem_preview.src = dados_servicos[7];

        campo_imagem_anterior.value=dados_servicos[4];

        verificarOcultarBotao();
    
        modal_editar_servico.showModal();

});

});

botao_cancelar_modal_servico.addEventListener("click", ()=>{
    modal_editar_servico.close();
});

modal_editar_servico.addEventListener("close", () => {
    document.getElementById("div-validation-message").classList.add("hidden");
});

formulario.addEventListener("submit", (event)=>{
    event.preventDefault();
    const message = document.querySelector("#validation-menssage");
    const div_messagem = document.querySelector("#div-validation-message");
    const erros = validarValores();
    message.textContent = '';

    

    if (erros.length > 0){
       
        erros.forEach(
                function(erro){
                    message.innerHTML += erro + '</br>';
                }
            );
            div_messagem.classList.remove('hidden'); // Remove a ocultação do elemento
    }else{
        modal_editar_servico.close();
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

function validarValores(){

    const errors = [];
    const valorTratado = valor_servico.value.replace(',', '.').trim();

    if (descricao_servico.value===''){
         errors.push('ATENÇÃO, campo descricao não pode ser vazio!');
    }
    
    // 2. Validação do Valor do Serviço
    if (valorTratado === '') {
        errors.push('ATENÇÃO, o valor do serviço não pode ser vazio!');
    } else if (isNaN(valorTratado)) { // Se NÃO for um número válido
        errors.push('ATENÇÃO, o valor do serviço aceita apenas números!');
    } else if (parseFloat(valorTratado) < 0) { // Se for menor que zero
        errors.push('ATENÇÃO, o valor do serviço deve ser no mínimo 0!');
    }
    
    // 3. Validação da Duração
    const duracaoTratada = duracao_servico.value.trim();
    if (duracaoTratada === '') {
        errors.push('ATENÇÃO, a duração do serviço não pode ser vazia!');
    } else if (isNaN(duracaoTratada) || parseInt(duracaoTratada) < 1) {
        errors.push('ATENÇÃO, a duração do serviço deve ser no mínimo 1 minuto!');
    }

    return errors;     
        
}
    


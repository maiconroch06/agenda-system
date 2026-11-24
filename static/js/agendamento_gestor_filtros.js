const agendamento_data_inicio = document.getElementById("agendamento-data-inicio");
const agendamento_data_fim = document.getElementById("agendamento-data-fim");
const formulario_filtro_agendamento = document.getElementById("agendamento_form_filtros");
const agendamento_div_filtro = document.getElementById("exibir-menssagem-erros-agendamento");
const agendamento_mensagem_filtro = document.getElementById("menssagem-erros-agendamento");

const agendamento_servico_filtro = document.getElementById("agendamento-filtro-servico");
const agendamento_status_filtro = document.getElementById("agendamento-filtro-status");
const agendamento_barbeiro_filtro = document.getElementById("agendamento-filtro-barbeiro");





document.addEventListener("DOMContentLoaded", () => {
    const data_hoje = new Date();
    agendamento_data_inicio.value = data_hoje.toLocaleDateString('en-CA');
    agendamento_data_fim.value = data_hoje.toLocaleDateString('en-CA');
    agendamento_mensagem_filtro.textContent='';

    if (localStorage.getItem('servico')!=null){
        agendamento_servico_filtro.value = localStorage.getItem('servico');
        localStorage.removeItem('servico');
    }
    if (localStorage.getItem('barbeiro')!=null){
        agendamento_barbeiro_filtro.value = localStorage.getItem('barbeiro');
        localStorage.removeItem('barbeiro');
    }
    if (localStorage.getItem('status')!=null){
        agendamento_status_filtro.value = localStorage.getItem('status');
        localStorage.removeItem('status');
    }
    if (localStorage.getItem('data_inicio')!=null){
        agendamento_data_inicio.value = localStorage.getItem('data_inicio');
        localStorage.removeItem('data_inicio');
    }
    if (localStorage.getItem('data_fim')!=null){
        agendamento_data_fim.value = localStorage.getItem('data_fim');
        localStorage.removeItem('data_fim');
    }

    
});

formulario_filtro_agendamento.addEventListener("submit",(event)=>{  
    event.preventDefault();
    
    limparCampos();
    if (agendamento_data_fim.value < agendamento_data_inicio.value) {
        agendamento_mensagem_filtro.textContent = 'A data final deve ser maior ou igual que a data inicial';
        agendamento_div_filtro.classList.remove('hidden');
        return;
    }

    localStorage.setItem('servico', agendamento_servico_filtro.value);
    localStorage.setItem('barbeiro', agendamento_barbeiro_filtro.value);
    localStorage.setItem('status', agendamento_status_filtro.value);
    localStorage.setItem('data_inicio', agendamento_data_inicio.value);
    localStorage.setItem('data_fim', agendamento_data_fim.value);

    formulario_filtro_agendamento.submit();
});

function limparCampos(){
    agendamento_div_filtro.classList.add('hidden');
    agendamento_mensagem_filtro.textContent='';
}


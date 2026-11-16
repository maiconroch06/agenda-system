/* ============================================================
   ESTADO DA APLICAÇÃO E VARIÁVEIS DO WIZARD
   ============================================================ */
const state = {
    etapaAtual: 1
};

    const message = document.querySelector("#validation-menssage");
    const div_messagem = document.querySelector("#div-validation-message");

const els = {
    // Formulário
    form: document.getElementById("form-profissional"),
    
    // Upload de Imagens
    fotoInput: document.getElementById("pro-foto"),
    imgPreview: document.getElementById("img_pro-preview"),
    divButoes: document.getElementById("butao-remover-imagem-pro"),

    // Inputs com Máscaras
    cpf: document.getElementById("bar-cpf"),
    telefone: document.getElementById("bar-telefone"),
    


     nome_barbeiro_titulo: document.getElementById("campo-padrao"),
     nome_barbeiro_editar: document.getElementById("bar-nome"),
     email: document.getElementById("bar-email"),
     senha: document.getElementById("bar-senha"),
     confirmar_senha: document.getElementById("bar-confirmar-senha"),
     bio: document.getElementById("bar-bio"),
     especialidade: document.getElementById("bar-especialidade"),
     anos_experiencia: document.getElementById("bar-anos_experiencia"),



    cep: document.getElementById("bar-end-cep"),
    uf_end: document.getElementById("bar-end-uf"),
    cidade: document.getElementById("bar-end-cidade"),
    bairro_end: document.getElementById("bar-end-bairro"),
    logradouro_end: document.getElementById("bar-end-logradouro"),
    numero_end: document.getElementById("bar-end-numero"),
    complemento: document.getElementById("bar-end-complemento"),
    sequencia: document.getElementById("bar-end-sequencia"),

    // Controles de Etapa (Wizard)
    step1: document.getElementById("step-1"),
    step2: document.getElementById("step-2"),
    ind1: document.getElementById("step-indicator-1"),
    ind2: document.getElementById("step-indicator-2"),
    
    // Botões
    btnVoltar: document.getElementById("btn-voltar"),
    btnProximo: document.getElementById("btn-proximo"),
    btnSubmit: document.getElementById("btn-submit")
};

/* ============================================================
   ERROS
============================================================ */

function validacoesBarbeiros(){

    const errors = [];
    
    if (els.cpf.value === ""){
        els.cpf.classList.add("border-red-400");
        errors.push("O cpf precisa ser preenchido!");
    }
    if (els.nome_barbeiro_editar.value === ""){
        els.nome_barbeiro_editar.classList.add("border-red-400");
        errors.push("O nome precisa ser preenchido!");
    }
    if (els.email.value === "" ){
        els.email.classList.add("border-red-400");
        errors.push("O email não pode ser vazio precisa ser preenchido!");
    }else if(!els.email.value.includes("@")){
        els.email.classList.add("border-red-400");
        errors.push("O email  precisa conter @!");
    }else  if (!els.email.value.includes('.')) {
        els.email.classList.add("border-red-400");
        errors.push('ATENÇÃO, o e-mail deve possuir .');
    }else if (els.email.value.endsWith('.')) {//verifica se o texto termina com .
        els.email.classList.add("border-red-400");
        errors.push('ATENÇÃO, o e-mail não pode terminar com .');
    }
    if (els.senha.value !== els.confirmar_senha.value){
        els.senha.classList.add("border-red-400");
        els.confirmar_senha.classList.add("border-red-400");
        errors.push("confirmar senha diferente de senha, as senhas precisa ser iguais!");
    }
    if (els.telefone.value === ""){
        els.telefone.classList.add("border-red-400");
        errors.push("O telefone precisa ser preenchido!");
    }
    if (els.bio.value === ""){
        els.bio.classList.add("border-red-400");
        errors.push("A bio precisa ser preenchido!");
    }
   
    if (els.especialidade.value === ""){
        els.especialidade.classList.add("border-red-400");
        errors.push("A especialidade precisa ser preenchido!");
    }
    if (els.anos_experiencia.value === ""){
        els.anos_experiencia.classList.add("border-red-400");
        errors.push("O campo anos de experiencia deve ser preenchido!");
    }else if(els.anos_experiencia.value < 0){
         els.anos_experiencia.classList.add("border-red-400");
        errors.push("O campo anos de experiencia deve maior que zero!");
    }

    
    return errors;     
        
}


function validacoesEnderecos(){

    const errors = [];
    
    if (els.cep.value === ""){
        els.cep.classList.add("border-red-400");
        errors.push("O campo CEP deve ser preenchido!");
    }
     if (els.uf_end.value === ""){
        els.uf_end.classList.add("border-red-400");
        errors.push("O campo UF deve ser preenchido!");
    }
     if (els.cidade.value === ""){
        els.cidade.classList.add("border-red-400");
        errors.push("O campo cidade deve ser preenchido!");
    }
     if (els.bairro_end.value === ""){
        els.bairro_end.classList.add("border-red-400");
        errors.push("O campo bairro deve ser preenchido!");
    }
     if (els.logradouro_end.value === ""){
        els.logradouro_end.classList.add("border-red-400");
        errors.push("O campo logradouro deve ser preenchido!");
    }
    
    return errors;     
        
}

function limparCampos(){
    
    message.textContent = '';

    els.cpf.classList.remove("border-red-400");
    els.nome_barbeiro_editar.classList.remove("border-red-400");
    els.email.classList.remove("border-red-400");
    els.senha.classList.remove("border-red-400");
    els.confirmar_senha.classList.remove("border-red-400");
    els.telefone.classList.remove("border-red-400");
    els.bio.classList.remove("border-red-400");
    els.especialidade.classList.remove("border-red-400");
    els.cep.classList.remove("border-red-400");
    els.cidade.classList.remove("border-red-400");
    els.uf_end.classList.remove("border-red-400");
    els.bairro_end.classList.remove("border-red-400");
    els.logradouro_end.classList.remove("border-red-400");
    els.numero_end.classList.remove("border-red-400");
    els.complemento.classList.remove("border-red-400");
    els.sequencia.classList.remove("border-red-400");

    document.getElementById("div-validation-message").classList.add("hidden");
    
}
/* ============================================================
   INICIALIZAÇÃO
   ============================================================ */
function init() {
    limparCampos();

    document.getElementById("div-validation-message").classList.add("hidden");

    message.textContent = '';

    aplicarMascaras();
    configurarEventosWizard();
}

/* ============================================================
   NAVEGAÇÃO DO WIZARD (STEPPER)
   ============================================================ */
function alterarEtapa(direcao) {

    limparCampos();

    const erros =validacoesBarbeiros();

    
   
        if (direcao === 'next' && state.etapaAtual === 1) { 
            //campos barbeiros
            if(erros.length === 0){
            state.etapaAtual = 2;
            renderizarEtapa();
             }else{
        erros.forEach(
                function(erro){
                    message.innerHTML += erro + '</br>';
                }
            );
            
            div_messagem.classList.remove('hidden'); // Remove a ocultação do elemento
    }
        } else if (direcao === 'prev') {
            if (state.etapaAtual === 2) {
                // Se está no step 2, volta pro step 1
                state.etapaAtual = 1;
                renderizarEtapa();
            } else if (state.etapaAtual === 1) {
                // Se está no step 1, volta para o painel
                window.location.href = "/gestor/painel/barbeiros"; // Altere para a URL exata do seu painel se for diferente
                // ou use window.history.back(); para voltar à página anterior do histórico
            }
        }
   
    
}

function renderizarEtapa() {
    // Alterna a exibição das etapas
    if (state.etapaAtual === 1) {
        els.step1.classList.remove("hidden-step");
        els.step2.classList.add("hidden-step");
        
        els.btnVoltar.textContent = "Cancelar"; // Muda o texto para dar sentido de voltar ao painel
        els.btnProximo.classList.remove("hidden-step");
        els.btnSubmit.classList.add("hidden-step");
    } else {
        els.step1.classList.add("hidden-step");
        els.step2.classList.remove("hidden-step");
        
        els.btnVoltar.textContent = "Voltar"; // Muda o texto de volta para o padrão da etapa
        els.btnProximo.classList.add("hidden-step");
        els.btnSubmit.classList.remove("hidden-step");
    }

    atualizarEstiloIndicador();
}

function atualizarEstiloIndicador() {
    const itens = [els.ind1, els.ind2];

    itens.forEach((item, index) => {
        const numero = index + 1;
        const ciclo = item.querySelector("span:first-of-type");
        const label = item.querySelector("span:last-of-type");

        if (numero < state.etapaAtual) {
            item.classList.remove("before:bg-brand-border", "before:bg-[#4a473f]");
            item.classList.add("before:bg-brand-gold");

            ciclo.className = "relative z-10 w-[28px] h-[28px] rounded-full bg-brand-gold border border-brand-gold flex items-center justify-center text-[13px] font-bold text-black transition-all";
            ciclo.textContent = "✓";
            label.className = "text-brand-gold font-medium transition-all";

        } else if (numero === state.etapaAtual) {
            item.classList.remove("before:bg-brand-border", "before:bg-[#4a473f]");
            item.classList.add("before:bg-brand-gold");

            ciclo.className = "relative z-10 w-[28px] h-[28px] rounded-full bg-brand-gold border border-brand-gold flex items-center justify-center text-[13px] font-bold text-black shadow-md shadow-brand-gold/30 transition-all";
            ciclo.textContent = numero;
            label.className = "text-white font-bold transition-all";

        } else {
            item.classList.remove("before:bg-brand-gold");
            item.classList.add("before:bg-brand-border");

            ciclo.className = "relative z-10 w-[28px] h-[28px] rounded-full bg-[#111215] border border-brand-border flex items-center justify-center text-[13px] font-medium text-brand-muted transition-all";
            ciclo.textContent = numero;
            label.className = "text-brand-muted transition-all";
        }
    });
}

function configurarEventosWizard() {
    els.btnProximo.addEventListener("click", () => alterarEtapa('next'));
    els.btnVoltar.addEventListener("click", () => alterarEtapa('prev'));
    
    // Submete o formulário direto
    els.btnSubmit.addEventListener("click", () => {
         // Previne múltiplos envios
        
        limparCampos();

        const erros =validacoesEnderecos();

        if(erros.length === 0){
            els.btnSubmit.disabled = true;
            els.btnSubmit.textContent = "Aguarde...";
            els.form.submit();
        }else{
        erros.forEach(
                function(erro){
                    message.innerHTML += erro + '</br>';
                }
            );
            
            div_messagem.classList.remove('hidden'); // Remove a ocultação do elemento
    }
    });
}

/* ============================================================
   MÁSCARAS
   ============================================================ */
function aplicarMascaras() {
    els.telefone?.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "").slice(0, 11);
        value = value.replace(/^(\d{2})(\d)/, "($1) $2").replace(/(\d{4,5})(\d{4})$/, "$1-$2");
        e.target.value = value;
    });

    els.cpf?.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "").slice(0, 11);
        value = value.replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d{1,2})$/, "$1-$2");
        e.target.value = value;
    });

    els.cep?.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "").slice(0, 8);
        value = value.replace(/^(\d{5})(\d)/, "$1-$2");
        e.target.value = value;
    });
}

// Inicializa a aplicação
init();
/* ============================================================
   ESTADO DA APLICAÇÃO E VARIÁVEIS DO WIZARD
   ============================================================ */
const state = {
    etapaAtual: 1
};

const els = {
    // Formulário
    form: document.getElementById("form-profissional"),
    
    // Upload de Imagens
    fotoInput: document.getElementById("pro-foto"),
    imgPreview: document.getElementById("img_pro-preview"),
    divButoes: document.getElementById("butao-remover-imagem-pro"),

    // Inputs com Máscaras
    cpf: document.getElementById("pro-cpf"),
    telefone: document.getElementById("pro-telefone"),
    cep: document.getElementById("pro-cep"),
    
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
   INICIALIZAÇÃO
   ============================================================ */
function init() {
    aplicarMascaras();
    configurarEventosWizard();
    configurarUploadImagem();
}

/* ============================================================
   NAVEGAÇÃO DO WIZARD (STEPPER)
   ============================================================ */
function alterarEtapa(direcao) {
    if (direcao === 'next' && state.etapaAtual === 1) {
        state.etapaAtual = 2;
        renderizarEtapa();
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
        els.btnSubmit.disabled = true; // Previne múltiplos envios
        els.btnSubmit.textContent = "Aguarde...";
        els.form.submit();
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
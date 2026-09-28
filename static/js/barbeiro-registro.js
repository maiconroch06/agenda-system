/* ============================================================
   ESTADO DA APLICAÇÃO
   ============================================================ */
const state = {
    etapaAtual: 1,
    isEditing: false,
    fotoBase64: null
};

/* ============================================================
   MAPEAMENTO DE ELEMENTOS
   ============================================================ */
const els = {
    // Inputs Step 1
    fotoInput: document.getElementById("pro-foto"),
    cpf: document.getElementById("pro-cpf"),
    nome: document.getElementById("pro-nome"),
    email: document.getElementById("pro-email"),
    telefone: document.getElementById("pro-telefone"),
    descricao: document.getElementById("pro-descricao"),
    
    // Inputs Step 2
    cep: document.getElementById("pro-cep"),
    cidade: document.getElementById("pro-cidade"),
    uf: document.getElementById("pro-uf"),
    bairro: document.getElementById("pro-bairro"),
    logradouro: document.getElementById("pro-logradouro"),
    numero: document.getElementById("pro-numero"),
    complemento: document.getElementById("pro-complemento"),
    sequencia: document.getElementById("pro-sequencia"),
    
    // Controles de Etapa
    step1: document.getElementById("step-1"),
    step2: document.getElementById("step-2"),
    ind1: document.getElementById("step-indicator-1"),
    ind2: document.getElementById("step-indicator-2"),
    
    // Botões
    btnVoltar: document.getElementById("btn-voltar"),
    btnProximo: document.getElementById("btn-proximo"),
    btnSubmit: document.getElementById("btn-submit"),
    
    // Títulos
    formTitle: document.getElementById("form-title"),
    formSubtitle: document.getElementById("form-subtitle"),
};

/* ============================================================
   INICIALIZAÇÃO & MODO DE EDIÇÃO
   ============================================================ */
function init() {
    aplicarMascaras();
    configurarEventos();
    
    const urlParams = new URLSearchParams(window.location.search);
    const cpfEdicao = urlParams.get('cpf');

    if (cpfEdicao) {
        state.isEditing = true;
        prepararModoEdicao(cpfEdicao);
    }
}

function prepararModoEdicao(cpf) {
    els.formTitle.textContent = "Atualizar Barbeiro";
    els.formSubtitle.textContent = "Altere os dados do profissional";
    els.btnSubmit.textContent = "Atualizar";
    
    els.cpf.value = cpf;
    els.cpf.disabled = true;

    // Exemplo de mock para edição
    const mockBarbeiro = {
        nome: "Maicon Pablo Marcelino da Rocha",
        email: "maiconpablo588@gmail.com",
        telefone: "(84) 99169-9246",
        descricao: "Especialista em cortes modernos.",
        cep: "59200-000",
        cidade: "Nova Cruz",
        uf: "RN",
        bairro: "Centro",
        logradouro: "Rua Exemplo",
        numero: "123",
        complemento: "",
        sequencia: "1"
    };
    
    preencherFormulario(mockBarbeiro);
}

function preencherFormulario(dados) {
    els.nome.value = dados.nome || "";
    els.email.value = dados.email || "";
    els.telefone.value = dados.telefone || "";
    els.descricao.value = dados.descricao || "";
    els.cep.value = dados.cep || "";
    els.cidade.value = dados.cidade || "";
    els.uf.value = dados.uf || "";
    els.bairro.value = dados.bairro || "";
    els.logradouro.value = dados.logradouro || "";
    els.numero.value = dados.numero || "";
    els.complemento.value = dados.complemento || "";
    els.sequencia.value = dados.sequencia || "";
}

/* ============================================================
   NAVEGAÇÃO DO WIZARD E ESTILO DO STEPPER
   ============================================================ */
function alterarEtapa(direcao) {
    if (direcao === 'next' && state.etapaAtual === 1) {
        state.etapaAtual = 2;
    } else if (direcao === 'prev' && state.etapaAtual === 2) {
        state.etapaAtual = 1;
    }
    renderizarEtapa();
}

function renderizarEtapa() {
    if (state.etapaAtual === 1) {
        els.step1.classList.remove("hidden-step");
        els.step2.classList.add("hidden-step");
        
        els.btnVoltar.classList.add("hidden-step");
        els.btnProximo.classList.remove("hidden-step");
        els.btnSubmit.classList.add("hidden-step");
    } else {
        els.step1.classList.add("hidden-step");
        els.step2.classList.remove("hidden-step");
        
        els.btnVoltar.classList.remove("hidden-step");
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

/* ============================================================
   EVENTOS & MÁSCARAS
   ============================================================ */
function configurarEventos() {
    els.btnProximo.addEventListener("click", () => alterarEtapa('next'));
    els.btnVoltar.addEventListener("click", () => alterarEtapa('prev'));
    
    els.btnSubmit.addEventListener("click", (e) => {
        e.preventDefault();
        salvarDados();
    });

    els.fotoInput.addEventListener('change', async (e) => {
        const foto = await lerArquivoBase64(e.target);
        const label = e.target.closest('label');
        
        if (foto) {
            state.fotoBase64 = foto;
            label.style.backgroundImage = `url(${foto})`;
            label.style.backgroundSize = 'cover';
            label.style.backgroundPosition = 'center';
            label.querySelectorAll('span').forEach(span => span.style.opacity = '0');
        }
    });
}

function aplicarMascaras() {
    els.telefone.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "").slice(0, 11);
        value = value.replace(/^(\d{2})(\d)/, "($1) $2").replace(/(\d{4,5})(\d{4})$/, "$1-$2");
        e.target.value = value;
    });

    els.cpf.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "").slice(0, 11);
        value = value.replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d{1,2})$/, "$1-$2");
        e.target.value = value;
    });

    els.cep.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "").slice(0, 8);
        value = value.replace(/^(\d{5})(\d)/, "$1-$2");
        e.target.value = value;
    });
}

function lerArquivoBase64(input) {
    return new Promise((resolve) => {
        if (!input || !input.files || !input.files[0]) return resolve(null);
        const reader = new FileReader();
        reader.onload = (e) => {
            resolve(e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    });
}

function salvarDados() {
    const payload = {
        cpf: els.cpf.value,
        nome: els.nome.value,
        email: els.email.value,
        telefone: els.telefone.value,
        descricao: els.descricao.value,
        foto: state.fotoBase64,
        endereco: {
            cep: els.cep.value,
            cidade: els.cidade.value,
            uf: els.uf.value,
            bairro: els.bairro.value,
            logradouro: els.logradouro.value,
            numero: els.numero.value,
            complemento: els.complemento.value,
            sequencia: els.sequencia.value
        }
    };

    console.log(state.isEditing ? "Atualizar:" : "Cadastrar:", payload);
    alert(state.isEditing ? "Barbeiro Atualizado!" : "Barbeiro Cadastrado!");
}

init();
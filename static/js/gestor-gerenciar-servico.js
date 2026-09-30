/* ============================================================
   ESTADO DA APLICAÇÃO
   ============================================================ */
const state = {
    isEditing: false,
    fotoBase64: null
};

/* ============================================================
   MAPEAMENTO DE ELEMENTOS
   ============================================================ */
const els = {
    // Inputs
    fotoInput: document.getElementById("srv-foto"),
    nome: document.getElementById("srv-nome"),
    preco: document.getElementById("srv-preco"),
    duracao: document.getElementById("srv-duracao"),
    
    // Botão Submit
    btnSubmit: document.getElementById("btn-submit"),
    
    // Títulos
    formTitle: document.getElementById("form-title"),
    formSubtitle: document.getElementById("form-subtitle"),

    // Modal Resumo
    modalOverlay: document.getElementById("overlay-resumo"),
    modalResumo: document.getElementById("modal-resumo"),
    rNome: document.getElementById("resumo-nome"),
    rPreco: document.getElementById("resumo-preco"),
    rDuracao: document.getElementById("resumo-duracao")
};

/* ============================================================
   INICIALIZAÇÃO & MODO DE EDIÇÃO
   ============================================================ */
function init() {
    aplicarMascaras();
    configurarEventos();
    
    const urlParams = new URLSearchParams(window.location.search);
    const serviceId = urlParams.get('id');

    if (serviceId) {
        state.isEditing = true;
        prepararModoEdicao(serviceId);
    }
}

function prepararModoEdicao(id) {
    els.formTitle.textContent = "Atualizar Serviço";
    els.formSubtitle.textContent = "Altere as opções do serviço registrado";
    els.btnSubmit.textContent = "Atualizar Serviço";

    // Mock de dados para edição
    const mockServico = {
        nome: "Corte e Barba Premium",
        preco: "R$ 65,00",
        duracao: "50 min"
    };
    
    preencherFormulario(mockServico);
}

function preencherFormulario(dados) {
    els.nome.value = dados.nome || "";
    els.preco.value = dados.preco || "";
    els.duracao.value = dados.duracao || "";
}

/* ============================================================
   EVENTOS & MÁSCARAS
   ============================================================ */
function configurarEventos() {
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
    // Máscara para Preço (R$)
    els.preco.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "");
        if (!value) {
            e.target.value = "";
            return;
        }
        value = (parseInt(value, 10) / 100).toFixed(2);
        value = value.replace(".", ",").replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1.");
        e.target.value = `R$ ${value}`;
    });

    // Máscara para Duração (minutos)
    els.duracao.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "");
        e.target.value = value ? `${value} min` : "";
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

/* ============================================================
   FUNÇÕES DO MODAL DE RESUMO
   ============================================================ */
function salvarDados() {
    els.rNome.textContent = els.nome.value || "—";
    els.rPreco.textContent = els.preco.value || "—";
    els.rDuracao.textContent = els.duracao.value || "—";

    abrirModalResumo();
}

window.abrirModalResumo = function() {
    els.modalOverlay.classList.remove("hidden");
    els.modalResumo.classList.remove("hidden");
};

window.fecharModalResumo = function() {
    els.modalOverlay.classList.add("hidden");
    els.modalResumo.classList.add("hidden");
};

window.finalizarCadastro = function() {
    window.location.href = "/gestor/painel";
};

window.novoCadastro = function() {
    fecharModalResumo();
    document.getElementById("form-servico").reset();
    
    // Reseta imagem visualmente
    const labelFoto = els.fotoInput.closest('label');
    labelFoto.style.backgroundImage = 'none';
    labelFoto.querySelectorAll('span').forEach(span => span.style.opacity = '1');
    state.fotoBase64 = null;
};

init();
/* ============================================================
   MAPEAMENTO DE ELEMENTOS
   ============================================================ */
const els = {
    // Inputs
    preco: document.getElementById("srv-preco"),
    duracao: document.getElementById("srv-duracao"),
};

/* ============================================================
   INICIALIZAÇÃO & MODO DE EDIÇÃO
   ============================================================ */
function init() {
    aplicarMascaras();
}

/* ============================================================
   MÁSCARAS
   ============================================================ */
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

init();
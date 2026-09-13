document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-empresa");
    if (!form) return; 

    const cepInput = document.getElementById("end-cep");
    const numeroInput = document.getElementById("end-numero");
    const cidadeInput = document.getElementById("end-cidade");
    const logradouroInput = document.getElementById("end-logradouro");
    const bairroInput = document.getElementById("end-bairro");

    // ==========================================
    // FORMATADORES EM TEMPO REAL (MÁSCARAS)
    // ==========================================

    if (cepInput) {
        // Máscara de CEP: 00.000-000
        cepInput.addEventListener("input", (e) => {
            let value = e.target.value.replace(/\D/g, ""); // Remove letras
            if (value.length > 8) value = value.slice(0, 8); // Limita a 8 números

            // Aplica os pontos e traços conforme digita
            if (value.length > 5) {
                value = value.replace(/^(\d{2})(\d{3})(\d{0,3})$/, "$1.$2-$3");
            } else if (value.length > 2) {
                value = value.replace(/^(\d{2})(\d{0,3})$/, "$1.$2");
            }
            e.target.value = value;
        });
    }

    if (numeroInput) {
        // Impede digitação de caracteres inválidos no campo número (e, +, -, .)
        numeroInput.addEventListener("keydown", (e) => {
            if (["e", "E", "+", "-", ",", "."].includes(e.key)) {
                e.preventDefault();
            }
        });
    }

    // ==========================================
    // VALIDAÇÃO ANTES DE ENVIAR
    // ==========================================
    form.addEventListener("submit", (e) => {
        limparErros();
        let valido = true;

        // Valida comprimento do CEP formatado (00.000-000 tem 10 caracteres)
        if (cepInput && cepInput.value.length < 10) {
            mostrarErro("erro-cep", "Informe um CEP válido.");
            valido = false;
        }

        if (cidadeInput && cidadeInput.value.trim() === "") {
            mostrarErro("erro-cidade", "A cidade é obrigatória.");
            valido = false;
        }

        if (logradouroInput && logradouroInput.value.trim() === "") {
            mostrarErro("erro-logradouro", "O logradouro é obrigatório.");
            valido = false;
        }

        if (numeroInput && (numeroInput.value.trim() === "" || parseInt(numeroInput.value) <= 0)) {
            mostrarErro("erro-numero", "Informe um número válido maior que 0.");
            valido = false;
        }

        if (bairroInput && bairroInput.value.trim() === "") {
            mostrarErro("erro-bairro", "O bairro é obrigatório.");
            valido = false;
        }

        if (!valido) {
            e.preventDefault(); // Para o envio se houver erros
        }
    });

    // ==========================================
    // FUNÇÕES AUXILIARES
    // ==========================================
    function mostrarErro(idErro, mensagem) {
        const spanErro = document.getElementById(idErro);
        if (spanErro) {
            spanErro.textContent = mensaje || mensagem;
            spanErro.style.display = "block";
        }
    }

    function limparErros() {
        const erros = document.querySelectorAll(".campo__erro");
        erros.forEach(span => {
            span.textContent = "";
            span.style.display = "none";
        });
    }
});

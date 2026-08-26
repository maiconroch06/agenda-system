document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-empresa");
    
    const cpfInput = document.getElementById("prop-cpf");
    const telefoneInput = document.getElementById("prop-telefone");
    const emailInput = document.getElementById("prop-email");
    const nomeInput = document.getElementById("prop-nome");
    const sobrenomeInput = document.getElementById("prop-sobrenome");
    const senhaInput = document.getElementById("prop-senha");

    // ==========================================
    // MÁSCARAS EM TEMPO REAL (Formatação)
    // ==========================================

    // Máscara de CPF: 000.000.000-00
    cpfInput.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, ""); // Remove tudo que não for número
        if (value.length > 11) value = value.slice(0, 11);
        
        value = value.replace(/(\d{3})(\d)/, "$1.$2");
        value = value.replace(/(\d{3})(\d)/, "$1.$2");
        value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
        
        e.target.value = value;
    });

    // Máscara de Telefone: (00) 00000-0000
    telefoneInput.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, ""); // Remove tudo que não for número
        if (value.length > 11) value = value.slice(0, 11);

        if (value.length > 10) {
            // Formato com 9 dígitos: (XX) XXXXX-XXXX
            value = value.replace(/^(\d{2})(\d{5})(\d{4})$/, "($1) $2-$3");
        } else if (value.length > 5) {
            // Formato temporário durante digitação
            value = value.replace(/^(\d{2})(\d{4})(\d{0,4})$/, "($1) $2-$3");
        } else if (value.length > 2) {
            value = value.replace(/^(\d{2})(\d{0,5})$/, "($1) $2");
        } else if (value.length > 0) {
            value = `(${value}`;
        }
        
        e.target.value = value;
    });

    // ==========================================
    // FUNÇÕES DE AUXÍLIO PARA VALIDAÇÃO
    // ==========================================

    const mostrarErro = (idErro, mensagem) => {
        const spanErro = document.getElementById(idErro);
        if (spanErro) {
            spanErro.textContent = mensagem;
            spanErro.style.display = "block";
        }
    };

    const limparErros = () => {
        const erros = document.querySelectorAll(".campo__erro");
        erros.forEach(span => {
            span.textContent = "";
            span.style.display = "none";
        });
    };

    const validarEmail = (email) => {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    };

    // ==========================================
    // EVENTO DE SUBMIT DO FORMULÁRIO
    // ==========================================
    form.addEventListener("submit", (e) => {
        limparErros();
        let valido = true;

        // Validar Nome
        if (nomeInput.value.trim() === "") {
            mostrarErro("erro-prop-nome", "O nome é obrigatório.");
            valido = false;
        }

        // Validar Sobrenome
        if (sobrenomeInput.value.trim() === "") {
            mostrarErro("erro-prop-sobrenome", "O sobrenome é obrigatório.");
            valido = false;
        }

        // Validar CPF (Tamanho completo com máscara)
        if (cpfInput.value.length < 14) {
            mostrarErro("erro-prop-cpf", "Informe um CPF válido no formato 000.000.000-00.");
            valido = false;
        }

        // Validar Telefone (Tamanho mínimo aceitável)
        if (telefoneInput.value.length < 14) {
            mostrarErro("erro-prop-telefone", "Informe um telefone válido com DDD.");
            valido = false;
        }

        // Validar E-mail
        if (!validarEmail(emailInput.value.trim())) {
            mostrarErro("erro-prop-email", "Insira um endereço de e-mail válido.");
            valido = false;
        }

        // Validar Senha
        if (senhaInput.value.length < 6) {
            mostrarErro("erro-prop-senha", "A senha deve conter no mínimo 6 caracteres.");
            valido = false;
        }

        // Impede o envio do formulário para o Flask se houver erros
        if (!valido) {
            e.preventDefault();
        }
    });
});

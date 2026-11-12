
document.addEventListener("DOMContentLoaded", () => {

    const botoesFiltro = document.querySelectorAll(".filtro-btn");
    const cards = document.querySelectorAll(".agendamento-card");
    const mensagemVazia = document.getElementById("filtro-vazio");

    botoesFiltro.forEach(botao => {

        botao.addEventListener("click", () => {

            const filtro = botao.dataset.filtro;
            let quantidadeVisivel = 0;

            // Atualiza aparência dos botões
            botoesFiltro.forEach(item => {
                item.classList.remove(
                    "active",
                    "border-[#C9A34A]",
                    "bg-[#C9A34A]/10",
                    "text-[#C9A34A]"
                );

                item.classList.add(
                    "border-[#38362f]",
                    "text-[#AAA69A]"
                );
            });

            botao.classList.add(
                "active",
                "border-[#C9A34A]",
                "bg-[#C9A34A]/10",
                "text-[#C9A34A]"
            );

            botao.classList.remove(
                "border-[#38362f]",
                "text-[#AAA69A]"
            );

            // Filtra os agendamentos
            cards.forEach(card => {

                const status = card.dataset.status;

                const mostrar =
                    filtro === "todos" || status === filtro;

                card.hidden = !mostrar;

                if (mostrar) {
                    quantidadeVisivel++;
                }

            });

            // Exibe mensagem quando não existem resultados
            if (mensagemVazia) {
                mensagemVazia.hidden = quantidadeVisivel > 0;
            }

        });

    });

});

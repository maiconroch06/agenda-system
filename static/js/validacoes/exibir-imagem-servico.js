const input = document.querySelector('#srv-foto');
const img_preview = document.querySelector('#img_srv-preview');
const div_butoes = document.querySelector('#butao-remover-imagem');


const elementos = input.parentElement.querySelectorAll('span');

document.addEventListener('DOMContentLoaded', () => {

    if (!img_preview.classList.contains('hidden') && !img_preview.src.includes("default.png")) {
        ocultarExibirBotaoRemoverImagem(true);
    } else {
        ocultarExibirBotaoRemoverImagem(false);
    }
    //chamar o campo para verificar se existe imagem
    // mostrar ou ocultar o botão

});

function ocultarExibirBotaoRemoverImagem(visivel) {

    if (visivel) {
        const botaoRemoverImagem = document.createElement('button');

        botaoRemoverImagem.setAttribute('type', 'button')
        botaoRemoverImagem.innerText = "Remover Imagem";
        botaoRemoverImagem.classList.add("h-10", "px-5", "text-white", "rounded-[8px]", "bg-red-800", "hover:bg-red-600", "text-[#161513]", "text-[14px]", "hover:opacity-90", "active:scale-[0.98]", "transition-all");

        botaoRemoverImagem.addEventListener('click', function (event) {
            img_preview.classList.add('hidden');
            img_preview.removeAttribute('src');
            // criar um novo campo para simbolizar que não existe mais imagem
             elementos.forEach(elemento => {
            elemento.classList.remove('hidden');
            });
            
            criarInputDefault(true);     
            
            input.value="";
               
            botaoRemoverImagem.remove();
        });

        div_butoes.appendChild(botaoRemoverImagem);

    } else {
        div_butoes.querySelector('button')?.remove();        
    }
}

function criarInputDefault(visivel){

    if (visivel) {

        const input_imagem_padrao = document.createElement('input');
            
        input_imagem_padrao.classList.add('hidden', "w-full","h-10", "px-3", "rounded-[8px]", "border", "border-[#4a473f]", "bg-[#161513]", "text-[#f1efe8]", "text-[14px]", "focus:outline-none", "focus:border-brand-gold-hover", "focus:ring-2", "focus:ring-brand-gold");

        input_imagem_padrao.type="text";
        input_imagem_padrao.id="imagem-padrao";
        input_imagem_padrao.name="imagem-padrao";
        input_imagem_padrao.value="default.png";

        div_butoes.appendChild(input_imagem_padrao); 
    }else{
        div_butoes.querySelector("#imagem-padrao")?.remove();
    }
}

input.addEventListener('change', () => {
    const arquivo = input.files[0];


    if (arquivo && arquivo.type.startsWith('image/')) {
        img_preview.src = URL.createObjectURL(arquivo);
        img_preview.classList.remove('hidden');

        elementos.forEach(elemento => {
            elemento.classList.add('hidden');
        });

        if (!div_butoes.querySelector('button')) {
            ocultarExibirBotaoRemoverImagem(true);
        }

        criarInputDefault(false);

    } else {
        img_preview.classList.add('hidden');
        img_preview.removeAttribute('src');

        elementos.forEach(elemento => {
            elemento.classList.remove('hidden');
        });


    }
});








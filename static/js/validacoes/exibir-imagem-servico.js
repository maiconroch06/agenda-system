const input = document.querySelector('#srv-foto');
const preview = document.querySelector('#srv-preview');

const elementos = input.parentElement.querySelectorAll('span');

input.addEventListener('change', () => {
    const arquivo = input.files[0];

    if (arquivo && arquivo.type.startsWith('image/')) {
        preview.src = URL.createObjectURL(arquivo);
        preview.classList.remove('hidden');

        elementos.forEach(elemento => {
            elemento.classList.add('hidden');
        });
    } else {
        preview.classList.add('hidden');
        preview.removeAttribute('src');

        elementos.forEach(elemento => {
            elemento.classList.remove('hidden');
        });
    }
});
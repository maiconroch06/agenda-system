/* ============================================================
   ESTADO SERVIÇOS
   ============================================================ */
let barbers = JSON.parse(localStorage.getItem("barber")) || [];

/* ============================================================
   ELEMENTOS
   ============================================================ */
const els = {
    etapa:       document.getElementById("etapa"),
    fotoInput:   document.getElementById("pro-foto"),
    cpf:         document.getElementById("pro-cpf"),
    nome:        document.getElementById("pro-nome"),
    email:       document.getElementById("pro-email"),
    telefone:    document.getElementById("pro-telefone"),
    descricao:   document.getElementById("pro-descricao"),
    cep:         document.getElementById("pro-cep"),
    logradouro:  document.getElementById("pro-logradouro"),
    numero:      document.getElementById("pro-numero"),
    complemento: document.getElementById("pro-complemento"),
    bairro:      document.getElementById("pro-bairro"),
    cidade:      document.getElementById("pro-cidade"),
    uf:          document.getElementById("pro-uf"),
    container:   document.getElementById("lista-cards-profissionais"),
    vazia:       document.getElementById("vazia-profissionais"),
    aviso:       document.getElementById("aviso")
};

const estado = { etapaAtual: 2 };

/* ============================================================
   UTILITÁRIOS
   ============================================================ */
function mostrarAviso(msg) {
    if (!els.aviso) return;
    els.aviso.textContent = msg;
    els.aviso.classList.add("visivel");
    setTimeout(() => els.aviso.classList.remove("visivel"), 2500);
}

// CORREÇÃO: Função atualizada para comprimir a imagem e evitar QuotaExceededError
function lerArquivoBase64(input) {
    return new Promise((resolve) => {
        if (!input || !input.files || !input.files[0]) { resolve(null); return; }
        const file = input.files[0];
        const reader = new FileReader();

        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement("canvas");
                const MAX_WIDTH = 200; // Reduz a resolução para economizar espaço
                const scaleSize = MAX_WIDTH / img.width;
                canvas.width = MAX_WIDTH;
                canvas.height = img.height * scaleSize;

                const ctx = canvas.getContext("2d");
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

                // Converte para JPEG com 60% de qualidade
                const dataUrl = canvas.toDataURL("image/jpeg", 0.6);
                resolve(dataUrl);
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    });
}

function salvarEstado() {
    localStorage.setItem("barber", JSON.stringify(barbers));
    if (typeof sincronizarPainel === "function") sincronizarPainel();
}

function moverItem(tipo, id, direcao) {
    if (tipo !== 'barber') return;
    const indexAtual = barbers.findIndex(p => p.id === id);
    if (indexAtual === -1) return;

    const novoIndex = indexAtual + direcao;
    if (novoIndex < 0 || novoIndex >= barbers.length) return;

    const temp = barbers[indexAtual];
    barbers[indexAtual] = barbers[novoIndex];
    barbers[novoIndex] = temp;

    salvarEstado();
    renderizarCardsProfissionais();
}

/* ============================================================
   PREVIEW DA FOTO
   ============================================================ */
function configurarPreviewFoto() {
    if (!els.fotoInput) return;
    els.fotoInput.addEventListener('change', async (e) => {
        const fotoBase64 = await lerArquivoBase64(e.target);
        const label = e.target.closest('label');

        if (fotoBase64) {
            label.style.backgroundImage = `url(${fotoBase64})`;
            label.style.backgroundSize = 'cover';
            label.style.backgroundPosition = 'center';
            const spans = label.querySelectorAll('span');
            spans.forEach(span => span.style.opacity = '0');
        } else {
            label.style.backgroundImage = 'none';
            const spans = label.querySelectorAll('span');
            spans.forEach(span => span.style.opacity = '1');
        }
    });
}

/* ============================================================
   MÁSCARAS
   ============================================================ */
function aplicarMascaraTelefone() {
    if (!els.telefone) return;
    els.telefone.addEventListener("input", (event) => {
        let value = event.target.value.replace(/\D/g, "").slice(0, 11);
        value = value.replace(/^(\d{2})(\d)/, "($1) $2");
        value = value.replace(/(\d{4,5})(\d{4})$/, "$1-$2");
        event.target.value = value;
    });
}

function aplicarMascaraCPF() {
    if (!els.cpf) return;
    els.cpf.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "");
        if (value.length > 11) value = value.slice(0, 11);
        value = value.replace(/(\d{3})(\d)/, "$1.$2");
        value = value.replace(/(\d{3})(\d)/, "$1.$2");
        value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
        e.target.value = value;
    });
}

/* ============================================================
   BARBEIROS (CRUD)
   ============================================================ */
async function addBarber() {
    const cpf = els.cpf?.value.trim();
    const nome = els.nome?.value.trim();
    const email = els.email?.value.trim();
    const telefone = els.telefone?.value.trim();
    const descricao = els.descricao?.value.trim() || ""; // Agora é opcional
    
    // Campos de endereço
    const cep = els.cep?.value.trim() || "";
    const logradouro = els.logradouro?.value.trim() || "";
    const numero = els.numero?.value.trim() || "";
    const complemento = els.complemento?.value.trim() || "";
    const bairro = els.bairro?.value.trim() || "";
    const cidade = els.cidade?.value.trim() || "";
    const uf = els.uf?.value.trim() || "";

    if (!cpf) { mostrarAviso("Informe o CPF do barbeiro"); return; }
    if (!nome) { mostrarAviso("Informe o nome do barbeiro"); return; }
    if (!email) { mostrarAviso("Informe o e-mail do barbeiro"); return; }
    if (!telefone) { mostrarAviso("Informe o telefone do barbeiro"); return; }

    const foto = await lerArquivoBase64(els.fotoInput);

    const barber = {
        id: typeof gerarIdUnico === "function" ? gerarIdUnico() : Date.now().toString(),
        cpf, nome, email, telefone, descricao, foto,
        endereco: { cep, logradouro, numero, complemento, bairro, cidade, uf }
    };

    barbers.push(barber);
    salvarEstado();

    // Limpeza dos campos
    [els.cpf, els.nome, els.email, els.telefone, els.descricao, els.cep, els.logradouro, els.numero, els.complemento, els.bairro, els.cidade, els.uf].forEach(input => {
        if (input) input.value = "";
    });
    
    // Limpa o preview da imagem
    if (els.fotoInput) {
        els.fotoInput.value = "";
        const label = els.fotoInput.closest('label');
        if (label) {
            label.style.backgroundImage = 'none';
            label.querySelectorAll('span').forEach(span => span.style.opacity = '1');
        }
    }

    renderizarCardsProfissionais();
}

function renderizarCardsProfissionais(lista = barbers) {
    if (!els.container) return;

    if (lista.length === 0) {
        els.container.innerHTML = <p class="col-span-full text-center text-[14px] text-[#888780] py-6" id="vazia-profissionais">Nenhum barbeiro adicionado ainda.</p>;
        if (els.vazia) els.vazia.classList.remove("hidden");
        return;
    }

    if (els.vazia) els.vazia.classList.add("hidden");

    els.container.innerHTML = lista.map((p) => `
        <div class="relative flex flex-col items-center bg-white dark:bg-zinc-800 rounded-2xl p-5 shadow-sm hover:shadow-md border border-zinc-100 dark:border-zinc-700/60 transition-all duration-200" data-id="${p.id}">
            <div class="absolute top-3 right-3 flex gap-1">
                <button class="w-7 h-7 flex items-center justify-center rounded-lg bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-700 dark:hover:bg-zinc-600 text-zinc-600 dark:text-zinc-300 text-xs transition-colors" onclick="moverItem('barber', '${p.id}', -1)" title="Subir">▲</button>
                <button class="w-7 h-7 flex items-center justify-center rounded-lg bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-700 dark:hover:bg-zinc-600 text-zinc-600 dark:text-zinc-300 text-xs transition-colors" onclick="moverItem('barber', '${p.id}', 1)" title="Descer">▼</button>
            </div>

            ${p.foto
                ? `<img class="w-20 h-20 rounded-full object-cover mb-3 border-2 border-amber-500 shadow-sm" src="${p.foto}" alt="${p.nome}">`
                : `<div class="w-20 h-20 rounded-full bg-zinc-100 dark:bg-zinc-700 border border-zinc-200 dark:border-zinc-600 flex items-center justify-center text-3xl mb-3 text-zinc-400">👤</div>`
            }

            <h3 class="font-bold text-zinc-800 dark:text-zinc-100 text-base mb-1 text-center">${p.nome}</h3>
            <p class="text-xs text-zinc-500 dark:text-zinc-400 text-center mb-3 line-clamp-2">${p.descricao || 'Sem descrição'}</p>

            <div class="flex flex-col gap-1 w-full text-xs text-zinc-500 dark:text-zinc-400 mb-4 bg-zinc-50 dark:bg-zinc-800/50 p-2.5 rounded-xl border border-zinc-100 dark:border-zinc-700/40">
                <span class="truncate"><strong>E-mail:</strong> ${p.email || '-'}</span>
                <span><strong>Tel:</strong> ${p.telefone || '-'}</span>
                ${p.endereco?.cidade ? `<span class="truncate mt-1 border-t border-zinc-200 dark:border-zinc-700 pt-1"><strong>End:</strong> ${p.endereco.cidade}-${p.endereco.uf}</span>` : ''}
            </div>

            <div class="flex gap-2 w-full mt-auto pt-3 border-t border-zinc-100 dark:border-zinc-700/50">
                <button class="flex-1 py-2 px-3 bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-700 dark:hover:bg-zinc-600 text-zinc-700 dark:text-zinc-200 text-xs font-semibold rounded-xl transition-colors" onclick="editBarber('${p.id}')">Editar</button>
                <button class="flex-1 py-2 px-3 bg-red-50 hover:bg-red-100 dark:bg-red-950/40 text-red-600 dark:text-red-400 text-xs font-semibold rounded-xl transition-colors" onclick="removeBarber('${p.id}')">Remover</button>
            </div>
        </div>
    `).join("");
}

// Já estava no seu código, acionada pelo botão de "Remover" no card gerado acima
function removeBarber(id) {
    barbers = barbers.filter(p => p.id !== id);
    salvarEstado();
    renderizarCardsProfissionais();
}

function editBarber(id) {
    const p = barbers.find(p => p.id === id);
    if (!p) return;
    const novoNome = prompt("Nome do barbeiro:", p.nome);
    if (novoNome !== null && novoNome.trim()) p.nome = novoNome.trim();
    const novaDesc = prompt("Descrição:", p.descricao || "");
    if (novaDesc !== null) p.descricao = novaDesc.trim();
    salvarEstado();
    renderizarCardsProfissionais();
}

/* ============================================================
   INICIALIZAÇÃO
   ============================================================ */
renderizarCardsProfissionais();
configurarPreviewFoto();
aplicarMascaraTelefone();
aplicarMascaraCPF();
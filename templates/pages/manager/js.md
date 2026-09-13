// ESTADO GLOBAL
let estadoAbaAtual = 'inicio';
let visaoAgendaAtual = 'dia';
let dataAgendaSelecionada = new Date();

// INICIALIZAÇÃO
document.addEventListener('DOMContentLoaded', () => {
    carregarDadosUsuario();
    carregarKPIs();
    renderizarInicio();
    renderizarAgenda();
    renderizarServicos();
    mudarMes(0);
});

// NAVEGAÇÃO DE ABAS (Sidebar Desktop & Bottom-Nav Mobile)
function irParaAba(nomeAba) {
    if (nomeAba === 'mais') {
        abrirMenuMais();
        return;
    }

    estadoAbaAtual = nomeAba;

    // Alterna visibilidade das seções
    document.querySelectorAll('.aba-func').forEach(sec => sec.classList.add('hidden'));
    const abaAlvo = document.getElementById(`aba-${nomeAba}`);
    if (abaAlvo) abaAlvo.classList.remove('hidden');

    // Atualiza estados na Sidebar (Desktop)
    document.querySelectorAll('.sidebar-func__item').forEach(btn => {
        const ativo = btn.dataset.aba === nomeAba;
        btn.className = `sidebar-func__item flex items-center gap-2.5 p-2.5 px-3 rounded-lg border-none text-sm font-medium cursor-pointer text-left w-full transition-colors ${
            ativo ? 'bg-[#2a2825] text-[#f1efe8]' : 'bg-transparent text-[#888780] hover:bg-[#2a2825] hover:text-[#f1efe8]'
        }`;
    });

    // Atualiza estados na Barra Inferior (Mobile)
    document.querySelectorAll('.bottom-nav__item').forEach(btn => {
        const ativo = btn.dataset.aba === nomeAba;
        btn.classList.toggle('text-[#9fe1cb]', ativo);
        btn.classList.toggle('text-[#888780]', !ativo);
    });
}

// DADOS E KPIS DO PERFIL
function carregarDadosUsuario() {
    const usuario = JSON.parse(localStorage.getItem('usuario')) || { nome: 'Barbeiro' };
    const primeiroNome = usuario.nome.split(' ')[0];
    const elNome = document.getElementById('inicio-primeiro-nome');
    if (elNome) elNome.textContent = primeiroNome;
}

function carregarKPIs() {
    const elTotal = document.getElementById('kpi-total-hoje');
    const elProximo = document.getElementById('kpi-proximo');
    const elGanhos = document.getElementById('kpi-ganhos-hoje');
    const elAvaliacao = document.getElementById('kpi-avaliacao');

    if (elTotal) elTotal.textContent = '5';
    if (elProximo) elProximo.textContent = '14:30';
    if (elGanhos) elGanhos.textContent = 'R$ 180,00';
    if (elAvaliacao) elAvaliacao.textContent = '4.9 ★';
}

// RENDERIZAÇÃO DA ABA INÍCIO (CARDS PADRONIZADOS EM bg-[#232220])
function renderizarInicio() {
    const container = document.getElementById('lista-inicio-hoje');
    if (!container) return;

    const atendimentos = [
        { id: 1, cliente: 'Carlos Silva', servico: 'Corte + Barba', horario: '09:00', valor: 'R$ 60,00', status: 'concluido' },
        { id: 2, cliente: 'Marcos Souza', servico: 'Corte Degradê', horario: '10:30', valor: 'R$ 40,00', status: 'concluido' },
        { id: 3, cliente: 'Lucas Andrade', servico: 'Barba Terapia', horario: '14:30', valor: 'R$ 35,00', status: 'pendente' },
        { id: 4, cliente: 'João Pedro', servico: 'Corte Infantil', horario: '16:00', valor: 'R$ 45,00', status: 'pendente' }
    ];

    container.innerHTML = atendimentos.map(item => `
        <div onclick="abrirModalDetalhe(${item.id})" class="bg-[#232220] border border-[#38362f] rounded-2xl p-3.5 flex items-center justify-between cursor-pointer hover:border-[#4a473f] transition-colors">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-[#2a2825] flex items-center justify-center text-sm font-semibold text-[#f1efe8]">
                    ${item.cliente.charAt(0)}
                </div>
                <div>
                    <div class="text-sm font-medium text-[#f1efe8]">${item.cliente}</div>
                    <div class="text-xs text-[#888780]">${item.servico} • ${item.horario}</div>
                </div>
            </div>
            <div class="text-right">
                <div class="text-xs font-semibold text-[#9fe1cb]">${item.valor}</div>
                <span class="text-[10px] px-2 py-0.5 rounded-full ${
                    item.status === 'concluido' ? 'bg-[#0f6e56]/20 text-[#9fe1cb]' : 'bg-[#f0c05a]/20 text-[#f0c05a]'
                }">${item.status === 'concluido' ? 'Concluído' : 'Pendente'}</span>
            </div>
        </div>
    `).join('');
}

// CONTROLE DA AGENDA
function mudarVisaoAgenda(visao) {
    visaoAgendaAtual = visao;
    document.querySelectorAll('.filtro-btn').forEach(btn => {
        const ativo = btn.dataset.filtro === visao;
        btn.className = `filtro-btn px-3.5 py-1.5 rounded-full border text-xs font-medium cursor-pointer transition-all ${
            ativo ? 'border-[#f1efe8] bg-[#f1efe8] text-[#161513]' : 'border-[#4a473f] bg-transparent text-[#888780]'
        }`;
    });

    document.getElementById('agenda-visao-dia').classList.toggle('hidden', visao !== 'dia');
    document.getElementById('agenda-visao-semana').classList.toggle('hidden', visao !== 'semana');
    document.getElementById('agenda-visao-mes').classList.toggle('hidden', visao !== 'mes');

    renderizarAgenda();
}

function renderizarAgenda() {
    const containerDia = document.getElementById('lista-agenda-dia');
    if (!containerDia) return;

    const agendamentos = [
        { id: 101, cliente: 'Gabriel Lima', servico: 'Corte Social', horario: '11:00 - 11:40', valor: 'R$ 40,00' },
        { id: 102, cliente: 'Rafael Costa', servico: 'Barba Completa', horario: '13:00 - 13:30', valor: 'R$ 35,00' }
    ];

    containerDia.innerHTML = agendamentos.map(item => `
        <div onclick="abrirModalDetalhe(${item.id})" class="bg-[#232220] border border-[#38362f] rounded-2xl p-3.5 flex items-center justify-between cursor-pointer hover:border-[#4a473f] transition-colors">
            <div>
                <div class="text-sm font-medium text-[#f1efe8]">${item.cliente}</div>
                <div class="text-xs text-[#888780]">${item.servico}</div>
                <div class="text-xs text-[#9fe1cb] mt-1">🕒 ${item.horario}</div>
            </div>
            <div class="text-right font-medium text-sm text-[#f1efe8]">
                ${item.valor}
            </div>
        </div>
    `).join('');
}

function mudarMes(delta) {
    dataAgendaSelecionada.setMonth(dataAgendaSelecionada.getMonth() + delta);
    const titulo = document.getElementById('mes-titulo');
    if (titulo) {
        const mesExtenso = dataAgendaSelecionada.toLocaleString('pt-BR', { month: 'long', year: 'numeric' });
        titulo.textContent = mesExtenso.charAt(0).toUpperCase() + mesExtenso.slice(1);
    }
}

// ABA SERVIÇOS (CARDS PADRONIZADOS EM bg-[#232220])
function renderizarServicos() {
    const container = document.getElementById('lista-servicos-func');
    if (!container) return;

    const servicos = JSON.parse(localStorage.getItem('servicos')) || [
        { id: '1', nome: 'Corte Masculino', duracao: '30 min', preco: 'R$ 40,00', ativo: true },
        { id: '2', nome: 'Barba Terapia', duracao: '25 min', preco: 'R$ 35,00', ativo: true },
        { id: '3', nome: 'Combo Corte + Barba', duracao: '50 min', preco: 'R$ 65,00', ativo: false }
    ];

    container.innerHTML = servicos.map(servico => `
        <div class="bg-[#232220] border border-[#38362f] rounded-2xl p-3.5 flex items-center justify-between">
            <div>
                <div class="text-sm font-medium text-[#f1efe8]">${servico.nome}</div>
                <div class="text-xs text-[#888780]">${servico.duracao} • ${servico.preco}</div>
            </div>
            <label class="relative inline-block w-11 h-6 flex-shrink-0 cursor-pointer">
                <input type="checkbox" ${servico.ativo ? 'checked' : ''} class="sr-only peer" onchange="mostrarAviso('Status do serviço atualizado!')">
                <span class="absolute inset-0 bg-[#4a473f] rounded-full transition-colors peer-checked:bg-[#0f6e56] peer-checked:after:translate-x-[20px] peer-checked:after:bg-white after:content-[''] after:absolute after:w-[18px] after:h-[18px] after:rounded-full after:left-[3px] after:bottom-[3px] after:bg-[#888780] after:transition-all"></span>
            </label>
        </div>
    `).join('');
}

// GERENCIAMENTO DE MODAIS (DETALHES, BLOQUEIO, CONFIGS E MAIS)
function abrirModalDetalhe(id) {
    document.getElementById('detalhe-cliente').textContent = 'Cliente Exemplo';
    document.getElementById('detalhe-servico').textContent = 'Corte + Barba';
    document.getElementById('detalhe-horario').textContent = '14:30';
    document.getElementById('detalhe-valor').textContent = 'R$ 60,00';
    document.getElementById('detalhe-telefone').textContent = '(11) 98765-4321';
    document.getElementById('detalhe-obs').textContent = 'Sem barba no pescoço.';

    exibirModal('modal-detalhe', 'overlay-detalhe');
}
function fecharModalDetalhe() { ocultarModal('modal-detalhe', 'overlay-detalhe'); }

function abrirModalBloquear() { exibirModal('modal-bloquear', 'overlay-bloquear'); }
function fecharModalBloquear() { ocultarModal('modal-bloquear', 'overlay-bloquear'); }
function confirmarBloqueio() {
    fecharModalBloquear();
    mostrarAviso('Horário bloqueado com sucesso!');
}

function abrirModalConfig(tipo) {
    const titulo = document.getElementById('config-modal-titulo');
    const campoTexto = document.getElementById('config-campo-texto');
    const campoTextarea = document.getElementById('config-campo-textarea');
    const campoSenha = document.getElementById('config-campo-senha');

    campoTexto.classList.add('hidden');
    campoTextarea.classList.add('hidden');
    campoSenha.classList.add('hidden');

    if (tipo === 'telefone') {
        titulo.textContent = 'Alterar Telefone';
        campoTexto.classList.remove('hidden');
    } else if (tipo === 'descricao') {
        titulo.textContent = 'Editar Descrição Profissional';
        campoTextarea.classList.remove('hidden');
    } else if (tipo === 'senha') {
        titulo.textContent = 'Alterar Senha';
        campoSenha.classList.remove('hidden');
    }

    exibirModal('modal-config', 'overlay-config');
}
function fecharModalConfig() { ocultarModal('modal-config', 'overlay-config'); }
function salvarConfig() {
    fecharModalConfig();
    mostrarAviso('Configurações salvas!');
}

function abrirMenuMais() { exibirModal('modal-mais', 'overlay-mais'); }
function fecharMenuMais() { ocultarModal('modal-mais', 'overlay-mais'); }

// FUNÇÕES AUXILIARES
function exibirModal(modalId, overlayId) {
    document.getElementById(modalId)?.classList.remove('hidden');
    document.getElementById(overlayId)?.classList.remove('hidden');
}

function ocultarModal(modalId, overlayId) {
    document.getElementById(modalId)?.classList.add('hidden');
    document.getElementById(overlayId)?.classList.add('hidden');
}

function alternarNotificacoes() { mostrarAviso('Preferência de notificação salva.'); }
function alternarTema() { mostrarAviso('Tema atualizado.'); }
function sairDaConta() {
    if (confirm('Deseja realmente sair da conta?')) {
        window.location.href = '/';
    }
}

function mostrarAviso(msg) {
    const el = document.getElementById('aviso');
    if (!el) return;
    el.textContent = msg;
    el.classList.remove('opacity-0', 'pointer-events-none');
    el.classList.add('opacity-100');
    setTimeout(() => {
        el.classList.remove('opacity-100');
        el.classList.add('opacity-0', 'pointer-events-none');
    }, 2500);
}
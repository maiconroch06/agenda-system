<!DOCTYPE html>
<html lang="pt-br">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link rel="stylesheet" href="{{ url_for('static', filename='css/output.css') }}">

    <title>TMS Barbearia - Painel Administrativo</title>
</head>

<body class="min-h-screen
           bg-[#161513]
           text-[#f1efe8]
           font-sans
           antialiased">

    <!-- ============================================================
         TELA 6: PAINEL DO ADMINISTRADOR
         ============================================================ -->

    <div id="tela-painel" class="min-h-screen flex flex-col lg:flex-row">

        <!-- ========================================================
             SIDEBAR
             ======================================================== -->

        <aside id="sidebar" class="w-full
                   lg:w-64
                   lg:min-h-screen
                   shrink-0
                   bg-[#232220]
                   border-b
                   lg:border-b-0
                   lg:border-r
                   border-[#38362f]
                   flex
                   flex-col">

            <!-- Logo -->
            <div class="
                block
                       items-center
                       px-5
                       py-5
                       border-b
                       border-[#38362f]">

                <!-- logo componente reutilização-->
                {%set logo_class="h-16 md:h-20 lg:h-24"%}
                {% include "componetization/logo/logo-top-horizontal.html" %}
                <h1 class=" mt-4 text-2xl font-bold">Painel Administrativo</h1>
            </div>


            <!-- Navegação -->
            <nav class="flex
                       lg:flex-col
                       overflow-x-auto
                       lg:overflow-visible
                       p-3
                       gap-1">

                <button class="sidebar__item ativo
                           shrink-0
                           flex
                           items-center
                           gap-3
                           w-auto
                           lg:w-full
                           px-4
                           py-3
                           rounded-lg
                           bg-[#38362f]
                           text-[#f1efe8]
                           text-sm
                           font-medium
                           transition-colors
                           hover:bg-[#4a473f]" onclick="mudarAba(event, 'perfil')">
                    <span>🏢</span>
                    <span>Perfil da empresa</span>
                </button>


                <button class="sidebar__item
                           shrink-0
                           flex
                           items-center
                           gap-3
                           w-auto
                           lg:w-full
                           px-4
                           py-3
                           rounded-lg
                           bg-transparent
                           text-[#888780]
                           text-sm
                           font-medium
                           transition-colors
                           hover:bg-[#38362f]
                           hover:text-[#f1efe8]" onclick="mudarAba(event, 'servicos')">
                    <span>✂️</span>
                    <span>Serviços</span>
                </button>


                <button class="sidebar__item
                           shrink-0
                           flex
                           items-center
                           gap-3
                           w-auto
                           lg:w-full
                           px-4
                           py-3
                           rounded-lg
                           bg-transparent
                           text-[#888780]
                           text-sm
                           font-medium
                           transition-colors
                           hover:bg-[#38362f]
                           hover:text-[#f1efe8]" onclick="mudarAba(event, 'profissionais')">
                    <span>👤</span>
                    <span>Profissionais</span>
                </button>


                <button class="sidebar__item
                           shrink-0
                           flex
                           items-center
                           gap-3
                           w-auto
                           lg:w-full
                           px-4
                           py-3
                           rounded-lg
                           bg-transparent
                           text-[#888780]
                           text-sm
                           font-medium
                           transition-colors
                           hover:bg-[#38362f]
                           hover:text-[#f1efe8]" onclick="mudarAba(event, 'financeiro')">
                    <span>💰</span>
                    <span>Financeiro</span>
                </button>

            </nav>


            <!-- Sair -->
            <a class="hidden
                       lg:block
                       mt-auto
                       mx-3
                       mb-5
                       px-4
                       py-3
                       text-center
                       rounded-lg
                       border
                       border-[#38362f]
                       bg-transparent
                       text-[#888780]
                       text-sm
                       font-medium
                       transition-colors
                       hover:bg-[#38362f]
                       hover:text-[#f1efe8]" href="/">
                Sair
            </a>

        </aside>


        <!-- ========================================================
             CONTEÚDO PRINCIPAL
             ======================================================== -->

        <main class="flex-1
                   min-w-0
                   px-4
                   sm:px-6
                   lg:px-8
                   py-6
                   lg:py-8">

            <div class="w-full
                       max-w-6xl
                       mx-auto">


                <!-- ==================================================
                     ABA: PERFIL
                     ================================================== -->

                <section id="aba-perfil" class="aba ativa">

                    <div class="flex
                               flex-col
                               sm:flex-row
                               sm:items-center
                               sm:justify-between
                               gap-4
                               mb-6">

                        <div>
                            <h1 class="text-2xl
                                       sm:text-3xl
                                       font-bold">
                                Perfil da empresa
                            </h1>
                        </div>

                        <button class="btn-secundario
                                   w-full
                                   sm:w-auto
                                   h-11
                                   px-5
                                   rounded-lg
                                   bg-brand-gold
                                   hover:bg-brand-gold-hover
                                   text-black
                                   text-sm
                                   font-bold
                                   transition-all
                                   duration-300
                                   hover:scale-[1.02]
                                   active:scale-[0.98]" onclick="editarEmpresa()">
                            Editar dados
                        </button>

                    </div>


                    <!-- Cards do perfil -->
                    <div class="grid
                               grid-cols-1
                               sm:grid-cols-2
                               gap-4">

                        <div class="info-card
                                   rounded-xl
                                   bg-brand-bg-card
                                   border border-brand-border
                                   p-5">
                            <div class="text-xs
                                       uppercase
                                       tracking-wide
                                       text-brand-muted">
                                Nome
                            </div>

                            <div id="perfil-nome" class="mt-2
                                       text-base
                                       font-semibold
                                       break-words">
                                —
                            </div>
                        </div>


                        <div class="info-card
                                   rounded-xl
                                   bg-brand-bg-card
                                   border border-brand-border
                                   p-5">
                            <div class="text-xs
                                       uppercase
                                       tracking-wide
                                       text-brand-muted">
                                Categoria
                            </div>

                            <div id="perfil-categoria" class="mt-2
                                       text-base
                                       font-semibold">
                                —
                            </div>
                        </div>


                        <div class="info-card
                                   rounded-xl
                                   bg-brand-bg-card
                                   border border-brand-border
                                   p-5">
                            <div class="text-xs
                                       uppercase
                                       tracking-wide
                                       text-brand-muted">
                                CNPJ
                            </div>

                            <div id="perfil-cnpj" class="mt-2
                                       text-base
                                       font-semibold">
                                —
                            </div>
                        </div>


                        <div class="info-card
                                   rounded-xl
                                   bg-brand-bg-card
                                   border border-brand-border
                                   p-5">
                            <div class="text-xs
                                       uppercase
                                       tracking-wide
                                       text-brand-muted">
                                Expediente
                            </div>

                            <div id="perfil-expediente" class="mt-2
                                       text-base
                                       font-semibold">
                                —
                            </div>
                        </div>


                        <div class="info-card
                                   sm:col-span-2
                                   rounded-xl
                                   bg-brand-bg-card
                                   border border-brand-border
                                   p-5">
                            <div class="text-xs
                                       uppercase
                                       tracking-wide
                                       text-brand-muted">
                                Dias de funcionamento
                            </div>

                            <div id="perfil-dias" class="mt-2
                                       text-base
                                       font-semibold">
                                —
                            </div>
                        </div>

                    </div>


                    <!-- Código de acesso -->
                    <div class="mt-6
                               rounded-xl
                               bg-brand-bg-card
                               border border-brand-border
                               p-5 sm:p-6">

                        <div class="flex
                                   flex-col
                                   sm:flex-row
                                   sm:items-start
                                   sm:justify-between
                                   gap-4">

                            <div>

                                <h2 class="text-lg
                                           font-bold">
                                    Código de acesso para funcionários
                                </h2>

                                <p class="mt-1
                                           text-sm
                                           text-brand-muted">
                                    Compartilhe este código com seus
                                    funcionários para que entrem no sistema.
                                </p>

                            </div>


                            <button class="btn-ghost
                                       w-full
                                       sm:w-auto
                                       h-10
                                       px-4
                                       rounded-lg
                                       border border-brand-border
                                       bg-transparent
                                       text-gray-300
                                       text-sm
                                       font-semibold
                                       transition-colors
                                       hover:bg-[#38362f]
                                       hover:text-white" onclick="gerarCodigo()">
                                🔄 Gerar novo
                            </button>

                        </div>


                        <div id="codigo-acesso" class="mt-5
                                   rounded-lg
                                   bg-[#161513]
                                   border border-brand-border
                                   px-5
                                   py-4
                                   text-center
                                   text-2xl
                                   sm:text-3xl
                                   font-bold
                                   tracking-[0.2em]
                                   break-all">
                            —
                        </div>


                        <button class="btn-copiar
                                   mt-4
                                   w-full
                                   h-11
                                   rounded-lg
                                   border border-brand-border
                                   bg-transparent
                                   text-gray-300
                                   text-sm
                                   font-semibold
                                   transition-colors
                                   hover:bg-[#38362f]
                                   hover:text-white" onclick="copiarCodigo()">
                            Copiar código
                        </button>

                    </div>

                </section>


                <!-- ==================================================
                     ABA: SERVIÇOS
                     ================================================== -->

                <section id="aba-servicos" class="aba hidden">

                    <div class="flex
                               flex-col
                               sm:flex-row
                               sm:items-center
                               sm:justify-between
                               gap-4
                               mb-6">

                        <h1 class="text-2xl
                                   sm:text-3xl
                                   font-bold">
                            Serviços
                        </h1>

                        <button class="btn-secundario
                                   w-full
                                   sm:w-auto
                                   h-11
                                   px-5
                                   rounded-lg
                                   bg-brand-gold
                                   hover:bg-brand-gold-hover
                                   text-black
                                   text-sm
                                   font-bold
                                   transition-all
                                   hover:scale-[1.02]
                                   active:scale-[0.98]" onclick="abrirFormServico()">
                            + Novo serviço
                        </button>

                    </div>


                    <!-- Formulário -->
                    <div id="form-servico-painel" hidden class="mb-6">

                        <form class="form-inline form-inline--painel
                                   rounded-xl
                                   bg-brand-bg-card
                                   border border-brand-border
                                   p-5 sm:p-6" novalidate>

                            <div class="grid
                                       grid-cols-1
                                       sm:grid-cols-2
                                       lg:grid-cols-4
                                       gap-4">

                                <div class="campo">
                                    <label for="psrv-nome" class="block
                                               mb-2
                                               text-sm
                                               font-medium
                                               text-gray-300">
                                        Nome do serviço
                                    </label>

                                    <input type="text" id="psrv-nome" placeholder="Ex: Corte degradê" autocomplete="off"
                                        class="w-full
                                               h-11
                                               px-3
                                               rounded-lg
                                               bg-[#161513]
                                               border border-brand-border
                                               text-[#f1efe8]
                                               placeholder:text-[#66645e]
                                               outline-none
                                               focus:border-brand-gold">
                                </div>


                                <div class="campo">
                                    <label for="psrv-preco" class="block
                                               mb-2
                                               text-sm
                                               font-medium
                                               text-gray-300">
                                        Preço (R$)
                                    </label>

                                    <input type="number" id="psrv-preco" placeholder="0,00" min="0" step="0.01" class="w-full
                                               h-11
                                               px-3
                                               rounded-lg
                                               bg-[#161513]
                                               border border-brand-border
                                               text-[#f1efe8]
                                               placeholder:text-[#66645e]
                                               outline-none
                                               focus:border-brand-gold">
                                </div>


                                <div class="campo">
                                    <label for="psrv-tempo" class="block
                                               mb-2
                                               text-sm
                                               font-medium
                                               text-gray-300">
                                        Duração (min)
                                    </label>

                                    <input type="number" id="psrv-tempo" placeholder="30" min="5" step="5" class="w-full
                                               h-11
                                               px-3
                                               rounded-lg
                                               bg-[#161513]
                                               border border-brand-border
                                               text-[#f1efe8]
                                               placeholder:text-[#66645e]
                                               outline-none
                                               focus:border-brand-gold">
                                </div>


                                <div class="campo">
                                    <label for="psrv-foto" class="block
                                               mb-2
                                               text-sm
                                               font-medium
                                               text-gray-300">
                                        Imagem
                                    </label>

                                    <input type="file" id="psrv-foto" accept="image/*" class="w-full
                                               h-11
                                               px-3
                                               py-2
                                               rounded-lg
                                               bg-[#161513]
                                               border border-brand-border
                                               text-gray-300
                                               text-sm">
                                </div>

                            </div>


                            <div class="flex
                                       flex-col-reverse
                                       sm:flex-row
                                       sm:justify-end
                                       gap-3
                                       mt-5">

                                <button type="button" class="btn-ghost
                                           w-full
                                           sm:w-auto
                                           h-11
                                           px-5
                                           rounded-lg
                                           border border-brand-border
                                           bg-transparent
                                           text-gray-300
                                           text-sm
                                           font-semibold
                                           hover:bg-[#111215]
                                           hover:text-white
                                           transition-colors" onclick="fecharFormServico()">
                                    Cancelar
                                </button>

                                <button type="button" class="btn-secundario
                                           w-full
                                           sm:w-auto
                                           h-11
                                           px-5
                                           rounded-lg
                                           bg-brand-gold
                                           hover:bg-brand-gold-hover
                                           text-black
                                           text-sm
                                           font-bold
                                           transition-all" onclick="adicionarServicoPainel()">
                                    Salvar serviço
                                </button>

                            </div>

                        </form>

                    </div>


                    <div class="cards-lista
                               space-y-3" id="lista-servicos-painel">
                        <p class="lista-vazia
                                   rounded-xl
                                   border border-brand-border
                                   bg-brand-bg-card
                                   p-8
                                   text-center
                                   text-sm
                                   text-brand-muted">
                            Nenhum serviço cadastrado.
                        </p>
                    </div>

                </section>


                <!-- ==================================================
                     ABA: PROFISSIONAIS
                     ================================================== -->

                <section id="aba-profissionais" class="aba hidden">

                    <div class="flex
                               flex-col
                               sm:flex-row
                               sm:items-center
                               sm:justify-between
                               gap-4
                               mb-6">

                        <h1 class="text-2xl
                                   sm:text-3xl
                                   font-bold">
                            Profissionais
                        </h1>

                    </div>


                    <div id="form-profissional-painel" hidden class="mb-6">

                        <form class="form-inline form-inline--painel
                                   rounded-xl
                                   bg-brand-bg-card
                                   border border-brand-border
                                   p-5 sm:p-6" novalidate>

                            <div class="grid
                                       grid-cols-1
                                       sm:grid-cols-2
                                       lg:grid-cols-3
                                       gap-4">

                                <div class="campo">
                                    <label for="ppro-nome" class="block
                                               mb-2
                                               text-sm
                                               font-medium
                                               text-gray-300">
                                        Nome completo
                                    </label>

                                    <input type="text" id="ppro-nome" placeholder="Nome do profissional"
                                        autocomplete="off" class="w-full
                                               h-11
                                               px-3
                                               rounded-lg
                                               bg-[#161513]
                                               border border-brand-border
                                               text-[#f1efe8]
                                               placeholder:text-[#66645e]
                                               outline-none
                                               focus:border-brand-gold">
                                </div>


                                <div class="campo">
                                    <label for="ppro-cargo" class="block
                                               mb-2
                                               text-sm
                                               font-medium
                                               text-gray-300">
                                        Cargo
                                    </label>

                                    <input type="text" id="ppro-cargo" placeholder="Ex: Barbeiro" autocomplete="off"
                                        class="w-full
                                               h-11
                                               px-3
                                               rounded-lg
                                               bg-[#161513]
                                               border border-brand-border
                                               text-[#f1efe8]
                                               placeholder:text-[#66645e]
                                               outline-none
                                               focus:border-brand-gold">
                                </div>


                                <div class="campo">
                                    <label for="ppro-foto" class="block
                                               mb-2
                                               text-sm
                                               font-medium
                                               text-gray-300">
                                        Foto
                                    </label>

                                    <input type="file" id="ppro-foto" accept="image/*" class="w-full
                                               h-11
                                               px-3
                                               py-2
                                               rounded-lg
                                               bg-[#161513]
                                               border border-brand-border
                                               text-gray-300
                                               text-sm">
                                </div>

                            </div>


                            <div class="flex
                                       flex-col-reverse
                                       sm:flex-row
                                       sm:justify-end
                                       gap-3
                                       mt-5">

                                <button type="button" class="btn-ghost
                                           w-full
                                           sm:w-auto
                                           h-11
                                           px-5
                                           rounded-lg
                                           border border-brand-border
                                           bg-transparent
                                           text-gray-300
                                           font-semibold
                                           hover:bg-[#111215]
                                           hover:text-white" onclick="fecharFormProfissional()">
                                    Cancelar
                                </button>

                                <button type="button" class="btn-secundario
                                           w-full
                                           sm:w-auto
                                           h-11
                                           px-5
                                           rounded-lg
                                           bg-brand-gold
                                           hover:bg-brand-gold-hover
                                           text-black
                                           font-bold" onclick="adicionarProfissionalPainel()">
                                    Salvar profissional
                                </button>

                            </div>

                        </form>

                    </div>


                    <div class="cards-lista
                               space-y-3" id="lista-profissionais-painel">
                        <p class="lista-vazia
                                   rounded-xl
                                   border border-brand-border
                                   bg-brand-bg-card
                                   p-8
                                   text-center
                                   text-sm
                                   text-brand-muted">
                            Nenhum profissional cadastrado.
                        </p>
                    </div>

                </section>


                <!-- ==================================================
                     ABA: FINANCEIRO
                     ================================================== -->

                <section id="aba-financeiro" class="aba hidden">

                    <div class="mb-6">

                        <h1 class="text-2xl
                                   sm:text-3xl
                                   font-bold">
                            Dashboard financeiro
                        </h1>

                    </div>


                    <!-- Resumo -->
                    <div class="grid
                               grid-cols-1
                               sm:grid-cols-2
                               xl:grid-cols-4
                               gap-4
                               mb-6">

                        <div class="financeiro-card
                                   rounded-xl
                                   bg-brand-bg-card
                                   border border-brand-border
                                   p-5">
                            <div class="text-xs
                                       uppercase
                                       tracking-wide
                                       text-brand-muted">
                                Receita do mês
                            </div>

                            <div id="fin-receita-mes" class="mt-2
                                       text-2xl
                                       font-bold">
                                R$ 0,00
                            </div>
                        </div>


                        <div class="financeiro-card
                                   rounded-xl
                                   bg-brand-bg-card
                                   border border-brand-border
                                   p-5">
                            <div class="text-xs
                                       uppercase
                                       tracking-wide
                                       text-brand-muted">
                                Total de cortes
                            </div>

                            <div id="fin-total-cortes" class="mt-2
                                       text-2xl
                                       font-bold">
                                0
                            </div>
                        </div>


                        <div class="financeiro-card
                                   rounded-xl
                                   bg-brand-bg-card
                                   border border-brand-border
                                   p-5">
                            <div class="text-xs
                                       uppercase
                                       tracking-wide
                                       text-brand-muted">
                                Ticket médio
                            </div>

                            <div id="fin-ticket-medio" class="mt-2
                                       text-2xl
                                       font-bold">
                                R$ 0,00
                            </div>
                        </div>


                        <div class="financeiro-card
                                   rounded-xl
                                   bg-brand-bg-card
                                   border border-brand-border
                                   p-5">
                            <div class="text-xs
                                       uppercase
                                       tracking-wide
                                       text-brand-muted">
                                Serviço mais realizado
                            </div>

                            <div id="fin-mais-realizado" class="mt-2
                                       text-xl
                                       font-bold
                                       break-words">
                                —
                            </div>
                        </div>

                    </div>


                    <!-- Tabela -->
                    <div class="rounded-xl
                               bg-brand-bg-card
                               border border-brand-border
                               overflow-hidden">

                        <div class="px-5
                                   py-4
                                   border-b border-brand-border">
                            <h2 class="text-lg
                                       font-bold">
                                Histórico de atendimentos
                            </h2>
                        </div>


                        <div class="overflow-x-auto">

                            <table class="financeiro-tabela
                                       w-full
                                       min-w-[700px]
                                       text-left">

                                <thead>
                                    <tr class="border-b
                                               border-brand-border
                                               text-xs
                                               uppercase
                                               tracking-wide
                                               text-brand-muted">

                                        <th class="px-5 py-4">
                                            Data
                                        </th>

                                        <th class="px-5 py-4">
                                            Cliente
                                        </th>

                                        <th class="px-5 py-4">
                                            Serviço
                                        </th>

                                        <th class="px-5 py-4">
                                            Profissional
                                        </th>

                                        <th class="px-5 py-4">
                                            Valor
                                        </th>

                                    </tr>
                                </thead>


                                <tbody id="fin-tabela-corpo">

                                    <tr>
                                        <td colspan="5" class="px-5
                                                   py-10
                                                   text-center
                                                   text-sm
                                                   text-brand-muted">
                                            Nenhum atendimento registrado ainda.
                                        </td>
                                    </tr>

                                </tbody>

                            </table>

                        </div>

                    </div>

                </section>

            </div>

        </main>

    </div>


    <!-- ============================================================
         MODAL DE EDIÇÃO DA EMPRESA
         ============================================================ -->

    <div id="modal-empresa" class="fixed
               inset-0
               z-50
               flex
               items-center
               justify-center
               p-4
               bg-black/70
               backdrop-blur-sm" hidden>

        <div class="w-full
                   max-w-lg
                   max-h-[90vh]
                   overflow-y-auto
                   rounded-xl
                   bg-brand-bg-card
                   border border-brand-border
                   shadow-2xl">

            <!-- Cabeçalho -->
            <div class="flex
                       items-center
                       justify-between
                       px-5
                       py-4
                       border-b border-brand-border">

                <h2 class="text-lg
                           font-bold">
                    Editar dados da empresa
                </h2>

                <button class="modal__fechar
                           w-9
                           h-9
                           flex
                           items-center
                           justify-center
                           rounded-lg
                           text-gray-400
                           hover:text-white
                           hover:bg-[#38362f]
                           transition-colors" onclick="fecharModalEmpresa()">
                    ✕
                </button>

            </div>


            <!-- Formulário -->
            <form class="form-auth
                       p-5
                       space-y-4" novalidate>

                <div class="campo">

                    <label for="edit-emp-nome" class="block
                               mb-2
                               text-sm
                               font-medium
                               text-gray-300">
                        Nome da empresa
                    </label>

                    <input type="text" id="edit-emp-nome" autocomplete="off" class="w-full
                               h-11
                               px-3
                               rounded-lg
                               bg-[#161513]
                               border border-brand-border
                               text-[#f1efe8]
                               outline-none
                               focus:border-brand-gold">

                </div>


                <div class="campo">

                    <label for="edit-emp-categoria" class="block
                               mb-2
                               text-sm
                               font-medium
                               text-gray-300">
                        Categoria
                    </label>

                    <select id="edit-emp-categoria" class="w-full
                               h-11
                               px-3
                               rounded-lg
                               bg-[#161513]
                               border border-brand-border
                               text-[#f1efe8]
                               outline-none
                               focus:border-brand-gold">

                        <option value="barbearia">
                            Barbearia
                        </option>

                        <option value="salao">
                            Salão de beleza
                        </option>

                        <option value="estetica">
                            Estética
                        </option>

                        <option value="clinica">
                            Clínica
                        </option>

                        <option value="outro">
                            Outro
                        </option>

                    </select>

                </div>


                <div class="campo">

                    <label for="edit-emp-cnpj" class="block
                               mb-2
                               text-sm
                               font-medium
                               text-gray-300">
                        CNPJ
                    </label>

                    <input type="text" id="edit-emp-cnpj" maxlength="18" autocomplete="off" class="w-full
                               h-11
                               px-3
                               rounded-lg
                               bg-[#161513]
                               border border-brand-border
                               text-[#f1efe8]
                               outline-none
                               focus:border-brand-gold">

                </div>


                <div class="grid
                           grid-cols-1
                           sm:grid-cols-2
                           gap-4">

                    <div class="campo">

                        <label for="edit-emp-abertura" class="block
                                   mb-2
                                   text-sm
                                   font-medium
                                   text-gray-300">
                            Abertura
                        </label>

                        <input type="time" id="edit-emp-abertura" class="w-full
                                   h-11
                                   px-3
                                   rounded-lg
                                   bg-[#161513]
                                   border border-brand-border
                                   text-[#f1efe8]
                                   outline-none
                                   focus:border-brand-gold">

                    </div>


                    <div class="campo">

                        <label for="edit-emp-fechamento" class="block
                                   mb-2
                                   text-sm
                                   font-medium
                                   text-gray-300">
                            Fechamento
                        </label>

                        <input type="time" id="edit-emp-fechamento" class="w-full
                                   h-11
                                   px-3
                                   rounded-lg
                                   bg-[#161513]
                                   border border-brand-border
                                   text-[#f1efe8]
                                   outline-none
                                   focus:border-brand-gold">

                    </div>

                </div>


                <button type="button" class="btn-primario
                           w-full
                           h-11
                           rounded-lg
                           bg-brand-gold
                           hover:bg-brand-gold-hover
                           text-black
                           text-sm
                           font-bold
                           transition-all
                           duration-300
                           hover:scale-[1.01]
                           active:scale-[0.98]" onclick="salvarEdicaoEmpresa()">
                    Salvar alterações
                </button>

            </form>

        </div>

    </div>


    <!-- Overlay -->
    <div id="modal-overlay" class="fixed
               inset-0
               z-40
               bg-black/70" hidden onclick="fecharModalEmpresa()"></div>


    <!-- Aviso -->
    <div class="aviso
               fixed
               left-1/2
               bottom-5
               z-[60]
               w-[calc(100%-2rem)]
               max-w-md
               -translate-x-1/2
               rounded-lg
               bg-[#232220]
               border border-brand-border
               px-4
               py-3
               text-sm
               text-[#f1efe8]
               shadow-xl" id="aviso"></div>


    <script src="{{ url_for('static', filename='js/manager-panel.js') }}"></script>

</body>

</html>
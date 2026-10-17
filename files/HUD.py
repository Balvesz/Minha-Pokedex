import os
import re
import tkinter as tk
from urllib.request import urlopen

import database_pokemons as database


def iniciar_hud():
    cores_tipos = {
        'Normal': '#a8a77a',
        'Fogo': '#ee8130',
        'Água': '#6390f0',
        'Elétrico': '#c9a600',
        'Grama': '#5f9e3e',
        'Gelo': '#62aaa7',
        'Lutador': '#c22e28',
        'Venenoso': '#a33ea1',
        'Terra': '#b89b3c',
        'Voador': '#8068c4',
        'Psíquico': '#d63e71',
        'Inseto': '#879915',
        'Pedra': '#9c872b',
        'Fantasma': '#735797',
        'Dragão': '#6030d8',
        'Sombrio': '#705746',
        'Aço': '#77778e',
        'Fada': '#c56596',
    }

    imagem_atual = None
    imagem_shiny_atual = None
    imagens_evolucoes = []

    def separar_tipos(texto):
        return [
            parte.strip()
            for parte in re.split(r',|\s+e\s+', texto)
            if parte.strip()
        ]

    def atualizar_etiquetas(container, texto):
        for widget in container.winfo_children():
            widget.destroy()

        tipos = separar_tipos(texto)
        linha = tk.Frame(container, bg=azul_tela)
        linha.pack(anchor='center')
        for indice, tipo in enumerate(tipos):
            nome_tipo = re.sub(r'\s*\([^)]*\)', '', tipo)
            nome_tipo = {'Rock': 'Pedra'}.get(nome_tipo, nome_tipo.capitalize())
            texto_tipo = tipo.replace('Rock', 'Rocha')
            tk.Label(
                linha,
                text=texto_tipo,
                font=('Arial', 9),
                bg=cores_tipos.get(nome_tipo, '#607d8b'),
                fg='#263238' if nome_tipo == 'Elétrico' else 'white',
                padx=6,
                pady=3,
            ).pack(side='left', padx=(0, 5) if indice < len(tipos) - 1 else 0)

    def buscar_pokemon():
        entrada = entrada_busca.get().strip().lower()
        codigo = entrada.replace(' ', '')
        busca = (
            codigo[:-1]
            if re.fullmatch(r'\d+\.', codigo)
            else database.codigos_formas.get(codigo, entrada)
        )

        for pokemon in database.pokemons:
            if busca.isdigit():
                encontrado = int(pokemon.num) == int(busca)
            else:
                encontrado = pokemon.name.lower() == busca

            if encontrado:
                titulo_pokemon.config(
                    text=f'{pokemon.name} | Nº {pokemon.num} | {pokemon.geracao_base}'
                )
                categoria_pokemon.config(text=f'Pokémon {pokemon.categoria}')
                geracao_forma.config(text=pokemon.geracao_forma)
                atualizar_etiquetas(etiquetas_tipos, pokemon.types)
                atualizar_etiquetas(etiquetas_fraquezas, pokemon.fraq)
                resultado.config(text=pokemon.description)
                carregar_imagem(pokemon)
                carregar_evolucoes(pokemon)
                return

        imagem_pokemon.config(image='', text='A imagem aparecerá aqui')
        imagem_shiny.config(image='', text='A imagem aparecerá aqui')
        titulo_pokemon.config(text='Pokémon não encontrado')
        categoria_pokemon.config(text='')
        geracao_forma.config(text='')
        atualizar_etiquetas(etiquetas_tipos, '')
        atualizar_etiquetas(etiquetas_fraquezas, '')
        resultado.config(text='Pokémon não encontrado na pokédex.')
        for widget in evolucoes_lista.winfo_children():
            widget.destroy()
        for widget in formas_lista.winfo_children():
            widget.destroy()

    def carregar_imagem(pokemon):
        nonlocal imagem_atual, imagem_shiny_atual

        pasta_imagens = os.path.join(os.path.dirname(__file__), 'imagens')
        nome_pokemon = pokemon.name.lower()
        caminho_relativo = database.imagens_formas.get(nome_pokemon, f'{int(pokemon.num)}.png')
        nome_arquivo = caminho_relativo.replace('/', '_')
        caminho_imagem = os.path.join(pasta_imagens, nome_arquivo)

        try:
            if not os.path.exists(caminho_imagem):
                os.makedirs(pasta_imagens, exist_ok=True)
                url = (
                    'https://raw.githubusercontent.com/PokeAPI/sprites/master/'
                    f'sprites/pokemon/{caminho_relativo}'
                )
                with urlopen(url, timeout=10) as resposta:
                    with open(caminho_imagem, 'wb') as arquivo:
                        arquivo.write(resposta.read())

            imagem_atual = tk.PhotoImage(file=caminho_imagem)
            imagem_pokemon.config(image=imagem_atual, text='')
        except (OSError, ValueError, tk.TclError):
            imagem_atual = None
            imagem_pokemon.config(image='', text='Imagem indisponível')

        correspondencia_id = re.fullmatch(r'(\d+)\.png', caminho_relativo)
        id_sprite = (
            correspondencia_id.group(1)
            if correspondencia_id
            else database.ids_sprites_formas.get(nome_pokemon, str(int(pokemon.num)))
        )
        nome_arquivo_shiny = f'shiny_{id_sprite}.png'
        caminho_imagem_shiny = os.path.join(pasta_imagens, nome_arquivo_shiny)

        try:
            if not os.path.exists(caminho_imagem_shiny):
                os.makedirs(pasta_imagens, exist_ok=True)
                url = (
                    'https://raw.githubusercontent.com/PokeAPI/sprites/master/'
                    f'sprites/pokemon/shiny/{id_sprite}.png'
                )
                with urlopen(url, timeout=10) as resposta:
                    with open(caminho_imagem_shiny, 'wb') as arquivo:
                        arquivo.write(resposta.read())

            imagem_shiny_atual = tk.PhotoImage(file=caminho_imagem_shiny)
            imagem_shiny.config(image=imagem_shiny_atual, text='')
        except (OSError, ValueError, tk.TclError):
            imagem_shiny_atual = None
            imagem_shiny.config(image='', text='Shiny indisponível')

    def carregar_evolucoes(pokemon):
        nonlocal imagens_evolucoes

        imagens_evolucoes = []
        for widget in evolucoes_lista.winfo_children():
            widget.destroy()
        for widget in formas_lista.winfo_children():
            widget.destroy()

        def adicionar_cartao(item, etiqueta='', container=evolucoes_lista, codigo=''):
            nome = item.name
            caminho_relativo = database.imagens_formas.get(nome.lower(), f'{int(item.num)}.png')
            caminho_imagem = os.path.join(
                os.path.dirname(__file__), 'imagens', caminho_relativo.replace('/', '_')
            )

            try:
                if not os.path.exists(caminho_imagem):
                    os.makedirs(os.path.dirname(caminho_imagem), exist_ok=True)
                    url = (
                        'https://raw.githubusercontent.com/PokeAPI/sprites/master/'
                        f'sprites/pokemon/{caminho_relativo}'
                    )
                    with urlopen(url, timeout=10) as resposta:
                        with open(caminho_imagem, 'wb') as arquivo:
                            arquivo.write(resposta.read())
                imagem = tk.PhotoImage(file=caminho_imagem)
                imagens_evolucoes.append(imagem)
            except (OSError, ValueError, tk.TclError):
                imagens_evolucoes.append(None)

            cartao = tk.Frame(container, bg='#263238', padx=6, pady=5)
            cartao.pack(fill='x', pady=(0, 8))
            imagem = imagens_evolucoes[-1]
            imagem_evolucao = tk.Label(
                cartao,
                image=imagem,
                text='' if imagem else '?',
                font=('Arial', 22, 'bold'),
                bg='#90caf9',
                fg='#263238',
                width=110,
                height=100,
            )
            imagem_evolucao.image = imagem
            imagem_evolucao.pack()
            tk.Label(
                cartao,
                text=(
                    f'{etiqueta}{item.name}\nNº {item.num}'
                    f'{f" · {codigo}" if codigo else ""}'
                ),
                font=('Arial', 9, 'bold'),
                bg='#263238',
                fg='white',
                justify='center',
            ).pack(pady=(4, 0))

        familia_eevee = {'Eevee', 'Vaporeon', 'Jolteon', 'Flareon'}
        if pokemon.name in familia_eevee:
            eevee = next(item for item in database.pokemons if item.name == 'Eevee')
            adicionar_cartao(eevee)
            evolucoes_eevee = (
                ('PEDRA DE ÁGUA', 'Vaporeon'),
                ('PEDRA DO TROVÃO', 'Jolteon'),
                ('PEDRA DE FOGO', 'Flareon'),
            )
            for indice, (metodo, nome) in enumerate(evolucoes_eevee):
                ramificacao = '└─' if indice == len(evolucoes_eevee) - 1 else '├─'
                tk.Label(
                    evolucoes_lista,
                    text=f'{ramificacao} {metodo} ↓',
                    font=('Arial', 9, 'bold'),
                    bg=vermelho_escuro,
                    fg='#ffcdd2',
                    anchor='w',
                ).pack(fill='x', pady=(0, 3))
                evolucao = next(item for item in database.pokemons if item.name == nome)
                adicionar_cartao(evolucao)
        else:
            cadeia = database.cadeias_evolucao.get(
                pokemon.name, [pokemon.name]
            )
            for indice, nome in enumerate(cadeia):
                evolucao = next(item for item in database.pokemons if item.name == nome)
                adicionar_cartao(evolucao)
                if indice < len(cadeia) - 1:
                    transicao = tk.Frame(evolucoes_lista, bg=vermelho_escuro)
                    transicao.pack(pady=(0, 8))
                    tk.Label(
                        transicao,
                        text='↓',
                        font=('Arial', 18, 'bold'),
                        bg=vermelho_escuro,
                        fg='white',
                    ).pack(side='left')
                    if evolucao.niveis_ev:
                        nivel = evolucao.niveis_ev[0]
                        transicao_texto = f'LVL {nivel}'
                    elif evolucao.metodo_ev:
                        transicao_texto = evolucao.metodo_ev
                    else:
                        transicao_texto = 'LVL -'
                    tk.Label(
                        transicao,
                        text=transicao_texto,
                        font=('Arial', 9, 'bold'),
                        bg=vermelho_escuro,
                        fg='#ffcdd2',
                    ).pack(side='left', padx=(5, 0))

        formas_alternativas = [] if pokemon.mega or pokemon.gigantamax else [
            item for item in database.pokemons
            if item.num == pokemon.num and item is not pokemon and (
                item.mega or item.gigantamax or item.alolan or item.galarian or
                item.hisuian or item.paldean
            )
        ]
        if formas_alternativas:
            for forma in formas_alternativas:
                codigo_tauros = ''
                if forma.mega:
                    etiqueta = 'MEGA · '
                elif forma.gigantamax:
                    etiqueta = 'GIGANTAMAX · '
                elif forma.alolan:
                    etiqueta = 'ALOLA · '
                elif forma.hisuian:
                    etiqueta = 'HISUI · '
                elif forma.galarian:
                    etiqueta = 'GALAR · '
                else:
                    etiqueta = 'PALDEA · '
                    codigo_tauros = {
                        'Tauros de Paldea (Raça de combate)': '128.p',
                        'Tauros de Paldea (Raça de fogo)': '128.p.f',
                        'Tauros de Paldea (Raça de água)': '128.p.a',
                    }.get(forma.name, '')
                adicionar_cartao(
                    forma, etiqueta, formas_lista, codigo=codigo_tauros
                )
        else:
            tk.Label(
                formas_lista,
                text='Sem formas\nespeciais.',
                font=('Arial', 10),
                bg=vermelho_escuro,
                fg='#ffcdd2',
                justify='center',
            ).pack(pady=28)

    janela = tk.Tk()
    janela.title('Pokédex')
    janela.geometry('1400x820')
    janela.minsize(1100, 680)
    janela.configure(bg='#4e1118')

    icone_pokebola = tk.PhotoImage(width=32, height=32)
    centro_icone = 15.5
    for y in range(32):
        for x in range(32):
            distancia = ((x - centro_icone) ** 2 + (y - centro_icone) ** 2) ** 0.5
            if distancia <= 14:
                if distancia >= 13.2:
                    cor = '#171717'
                elif distancia >= 12.2:
                    cor = '#7d858c'
                elif distancia <= 5:
                    cor = '#171717'
                elif distancia <= 3.7:
                    cor = '#cfd8dc'
                elif distancia <= 2.4:
                    cor = '#f5f7f8'
                elif abs(y - centro_icone) <= 1.5:
                    cor = '#171717'
                else:
                    cor = '#e53935' if y < centro_icone else '#e8edf0'
                icone_pokebola.put(cor, (x, y))
            elif ((x - 17) ** 2 + (y - 17) ** 2) ** 0.5 <= 14:
                icone_pokebola.put('#4b0d12', (x, y))
    janela.iconphoto(True, icone_pokebola)

    base = tk.Frame(janela, bg='#4e1118')
    base.pack(fill='both', expand=True, padx=22, pady=22)
    base.columnconfigure(0, weight=3)
    base.columnconfigure(1, weight=2)
    base.rowconfigure(0, weight=1)

    vermelho = '#c62828'
    vermelho_escuro = '#8e1b1b'
    preto = '#171717'
    azul_tela = '#90caf9'

    lado_esquerdo = tk.Frame(base, bg=vermelho, padx=24, pady=20)
    lado_esquerdo.grid(row=0, column=0, sticky='nsew')
    lado_esquerdo.columnconfigure(0, weight=1)
    lado_esquerdo.rowconfigure(1, weight=1)

    cabecalho = tk.Frame(lado_esquerdo, bg=vermelho)
    cabecalho.grid(row=0, column=0)

    indicador = tk.Canvas(
        cabecalho,
        width=54,
        height=54,
        bg=vermelho,
        highlightthickness=0,
    )
    indicador.create_oval(5, 5, 49, 49, fill='#42a5f5', outline='#e3f2fd', width=3)
    indicador.pack(side='left')

    titulo = tk.Canvas(
        cabecalho,
        width=300,
        height=64,
        bg=vermelho,
        highlightthickness=0,
    )
    for deslocamento_x, deslocamento_y in ((-2, -2), (0, -2), (2, -2), (-2, 0), (2, 0), (-2, 2), (0, 2), (2, 2)):
        titulo.create_text(
            150 + deslocamento_x,
            32 + deslocamento_y,
            text='POKÉDEX',
            font=('Arial', 30, 'bold'),
            fill='#174ea6',
        )
    titulo.create_text(
        150,
        32,
        text='POKÉDEX',
        font=('Arial', 30, 'bold'),
        fill='#ffca28',
    )
    titulo.pack(side='left', padx=14)
    visor_area = tk.Frame(lado_esquerdo, bg=vermelho)
    visor_area.grid(row=1, column=0, pady=(18, 12), sticky='nsew')

    visor_sombra = tk.Frame(visor_area, bg='#5b1015', padx=14, pady=14)
    visor_sombra.place(x=8, y=8, relwidth=1, relheight=1, width=-8, height=-8)

    visor_moldura = tk.Frame(visor_area, bg=vermelho_escuro, padx=14, pady=14)
    visor_moldura.place(relwidth=1, relheight=1, width=-8, height=-8)

    visor = tk.Frame(visor_moldura, bg=preto, padx=14, pady=14)
    visor.pack(fill='both', expand=True)

    imagens_pokemon = tk.Frame(visor, bg=azul_tela)
    imagens_pokemon.pack(pady=(0, 10))

    coluna_imagem_normal = tk.Frame(imagens_pokemon, bg=azul_tela)
    coluna_imagem_normal.pack(side='left', padx=12)
    tk.Label(
        coluna_imagem_normal,
        text='Normal',
        font=('Arial', 10, 'bold'),
        bg=azul_tela,
        fg='#263238',
    ).pack()
    imagem_pokemon = tk.Label(
        coluna_imagem_normal,
        text='A imagem aparecerá aqui',
        font=('Arial', 11),
        bg=azul_tela,
        fg='#263238',
        padx=12,
        pady=12,
    )
    imagem_pokemon.pack()

    coluna_imagem_shiny = tk.Frame(imagens_pokemon, bg=azul_tela)
    coluna_imagem_shiny.pack(side='left', padx=12)
    tk.Label(
        coluna_imagem_shiny,
        text='Shiny',
        font=('Arial', 10, 'bold'),
        bg=azul_tela,
        fg='#263238',
    ).pack()
    imagem_shiny = tk.Label(
        coluna_imagem_shiny,
        text='A imagem aparecerá aqui',
        font=('Arial', 11),
        bg=azul_tela,
        fg='#263238',
        padx=12,
        pady=12,
    )
    imagem_shiny.pack()

    painel_informacoes = tk.Frame(visor, bg=azul_tela, padx=12, pady=10)
    painel_informacoes.pack(fill='both', expand=True)

    informacoes_cabecalho = tk.Frame(painel_informacoes, bg=azul_tela)
    informacoes_cabecalho.pack(fill='x')

    titulo_pokemon = tk.Label(
        informacoes_cabecalho,
        text='Pokémon',
        font=('Arial', 18, 'bold'),
        bg=azul_tela,
        fg='#171717',
        wraplength=520,
        justify='center',
        anchor='center',
    )
    titulo_pokemon.pack(fill='x', pady=(0, 2))

    categoria_pokemon = tk.Label(
        informacoes_cabecalho,
        text='Pokémon',
        font=('Arial', 12, 'bold'),
        bg=azul_tela,
        fg='#171717',
        anchor='center',
    )
    categoria_pokemon.pack(fill='x', pady=(0, 2))

    geracao_forma = tk.Label(
        informacoes_cabecalho,
        text='',
        font=('Arial', 9, 'italic'),
        bg=azul_tela,
        fg='#607d8b',
        anchor='center',
    )
    geracao_forma.pack(fill='x')

    tk.Label(
        painel_informacoes,
        text='Tipo',
        font=('Arial', 12),
        bg=azul_tela,
        fg='#263238',
        anchor='center',
    ).pack(fill='x', pady=(8, 4))

    etiquetas_tipos = tk.Frame(painel_informacoes, bg=azul_tela)
    etiquetas_tipos.pack(fill='x')

    tk.Label(
        painel_informacoes,
        text='Fraquezas',
        font=('Arial', 12),
        bg=azul_tela,
        fg='#263238',
        anchor='center',
    ).pack(fill='x', pady=(8, 4))

    etiquetas_fraquezas = tk.Frame(painel_informacoes, bg=azul_tela)
    etiquetas_fraquezas.pack(fill='x')

    resultado = tk.Label(
        painel_informacoes,
        text='Digite um nome ou número para pesquisar.',
        wraplength=520,
        justify='center',
        font=('Arial', 12),
        bg=azul_tela,
        fg='#263238',
        anchor='n',
    )
    resultado.pack(fill='both', expand=True, pady=(8, 0))

    evolucoes_moldura = tk.Frame(base, bg='#5b1015', padx=7, pady=7)
    evolucoes_moldura.grid(row=0, column=1, sticky='nsew', padx=(18, 0))

    evolucoes_visor = tk.Frame(evolucoes_moldura, bg=vermelho_escuro, padx=12, pady=14)
    evolucoes_visor.pack(fill='both', expand=True)

    titulo_evolucoes = tk.Label(
        evolucoes_visor,
        text='EVOLUÇÕES',
        font=('Arial', 16, 'bold'),
        bg=vermelho_escuro,
        fg='white',
    )
    titulo_evolucoes.pack(anchor='w', pady=(0, 12))

    painel_colunas = tk.Frame(evolucoes_visor, bg=vermelho_escuro)
    painel_colunas.pack(fill='both', expand=True)

    evolucoes_conteudo = tk.Frame(painel_colunas, bg=vermelho_escuro)
    evolucoes_conteudo.pack(side='left', fill='both', expand=True, padx=(0, 10))

    tk.Frame(painel_colunas, bg='#b71c1c', width=2).pack(side='left', fill='y', padx=(0, 10))

    formas_conteudo = tk.Frame(painel_colunas, bg=vermelho_escuro)
    formas_conteudo.pack(side='left', fill='both', expand=True)

    tk.Label(
        evolucoes_conteudo,
        text='EVOLUÇÕES',
        font=('Arial', 10, 'bold'),
        bg=vermelho_escuro,
        fg='#ffcdd2',
    ).pack(anchor='w', pady=(4, 6))

    evolucoes_lista = tk.Frame(evolucoes_conteudo, bg=vermelho_escuro)
    evolucoes_lista.pack(fill='both', expand=True)

    tk.Label(
        evolucoes_lista,
        text='Pesquise um Pokémon\npara ver sua cadeia.',
        font=('Arial', 11),
        bg=vermelho_escuro,
        fg='#ffcdd2',
        justify='center',
    ).pack(pady=28)

    tk.Label(
        formas_conteudo,
        text='FORMAS',
        font=('Arial', 10, 'bold'),
        bg=vermelho_escuro,
        fg='#ffcdd2',
    ).pack(anchor='w', pady=(4, 6))

    formas_lista = tk.Frame(formas_conteudo, bg=vermelho_escuro)
    formas_lista.pack(fill='both', expand=True)

    tk.Label(
        formas_lista,
        text='Pesquise um Pokémon\npara ver suas formas.',
        font=('Arial', 10),
        bg=vermelho_escuro,
        fg='#ffcdd2',
        justify='center',
    ).pack(pady=28)

    tabela_codigos = tk.Frame(evolucoes_visor, bg='#263238', padx=8, pady=7)
    tabela_codigos.pack(fill='x', pady=(10, 0))

    tk.Label(
        tabela_codigos,
        text='COMO PESQUISAR FORMAS',
        font=('Arial', 9, 'bold'),
        bg='#263238',
        fg='white',
    ).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 4))

    tk.Label(
        tabela_codigos,
        text=(
            'Mega: [número].m; Mega X/Y: [número].x/.y    G-Max: [número].gg\n'
            'Alola: [número].a    Galar: [número].g\n'
            'Hisui: [número].h    Paldea: [número].p'
        ),
        font=('Courier New', 8, 'bold'),
        bg='#263238',
        fg='#90caf9',
        justify='left',
    ).grid(row=1, column=0, columnspan=2, sticky='w')

    controles_busca = tk.Frame(lado_esquerdo, bg=vermelho)
    controles_busca.grid(row=2, column=0)

    entrada_busca = tk.Entry(
        controles_busca,
        width=38,
        font=('Arial', 13),
        bg='#eceff1',
        fg='#263238',
        relief='flat',
    )
    entrada_busca.grid(row=0, column=0, padx=(0, 10))
    entrada_busca.focus()

    botao_buscar = tk.Button(
        controles_busca,
        text='BUSCAR',
        command=buscar_pokemon,
        font=('Arial', 10, 'bold'),
        bg='#fdd835',
        fg='#263238',
        activebackground='#ffee58',
        relief='flat',
        padx=18,
        pady=7,
    )
    botao_buscar.grid(row=0, column=1)

    pokebola = tk.Canvas(
        lado_esquerdo,
        width=54,
        height=54,
        bg=vermelho,
        highlightthickness=0,
    )
    pokebola.create_oval(5, 7, 49, 51, fill='#4b0d12', outline='#4b0d12')
    pokebola.create_oval(4, 4, 48, 48, fill='#7d858c', outline='#171717', width=2)
    pokebola.create_oval(6, 6, 46, 46, fill='#e8edf0', outline='#b0b8bd', width=2)
    pokebola.create_arc(6, 6, 46, 46, start=0, extent=180, fill='#e53935', outline='#b71c1c', width=2)
    pokebola.create_line(7, 26, 45, 26, fill='#171717', width=5)
    pokebola.create_oval(16, 16, 36, 36, fill='#5c6268', outline='#171717', width=2)
    pokebola.create_oval(19, 19, 33, 33, fill='#f5f7f8', outline='#cfd8dc', width=1)
    pokebola.create_oval(21, 21, 27, 27, fill='white', outline='white')
    pokebola.bind('<Button-1>', lambda evento: entrada_busca.focus_set())
    pokebola.bind('<Enter>', lambda evento: pokebola.config(cursor='hand2'))
    pokebola.grid(row=3, column=0, pady=(14, 0), sticky='s')

    janela.bind('<Return>', lambda evento: buscar_pokemon())
    janela.mainloop()

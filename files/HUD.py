import os
import queue
import re
import threading
import tkinter as tk
import unicodedata
from tkinter import messagebox, ttk
from urllib.request import urlopen

import pygame

if __package__:
    from . import database_pokemons as database
    from . import pokemon_stats
else:
    import database_pokemons as database
    import pokemon_stats


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
    animacoes_botoes = {}
    estado_navegacao = {
        'detalhe_tipo': False,
        'janela_tipos': None,
        'canvas_resultados': None,
        'pokemon_atual': None,
        'historico_pokemon': [],
    }

    def animar_cor_botao(botao, cor_destino):
        trabalho_anterior = animacoes_botoes.pop(botao, None)
        if trabalho_anterior:
            try:
                botao.after_cancel(trabalho_anterior)
            except tk.TclError:
                pass

        cor_atual = botao.cget('bg')
        inicio = tuple(int(cor_atual[indice:indice + 2], 16) for indice in (1, 3, 5))
        destino = tuple(int(cor_destino[indice:indice + 2], 16) for indice in (1, 3, 5))
        etapas = 6

        def animar(etapa):
            proporcao = etapa / etapas
            cor = '#{:02x}{:02x}{:02x}'.format(*(
                round(origem + (fim - origem) * proporcao)
                for origem, fim in zip(inicio, destino)
            ))
            try:
                botao.config(bg=cor)
            except tk.TclError:
                animacoes_botoes.pop(botao, None)
                return

            if etapa < etapas:
                animacoes_botoes[botao] = botao.after(18, animar, etapa + 1)
            else:
                animacoes_botoes.pop(botao, None)

        animar(1)

    def adicionar_hover_botao(botao, cor_normal, cor_hover):
        botao.config(cursor='hand2')
        botao.bind(
            '<Enter>',
            lambda evento: animar_cor_botao(botao, cor_hover),
        )
        botao.bind(
            '<Leave>',
            lambda evento: animar_cor_botao(botao, cor_normal),
        )

    def obter_pasta_imagens():
        diretorio_modulo = os.path.dirname(__file__)
        candidatas = (
            os.path.join(diretorio_modulo, 'imagens'),
            os.path.join(os.path.dirname(diretorio_modulo), 'imagens'),
        )
        return next((pasta for pasta in candidatas if os.path.isdir(pasta)), candidatas[0])

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
        estado_navegacao['detalhe_tipo'] = False
        estado_navegacao['historico_pokemon'].clear()
        botao_voltar_pagina.place_forget()
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
                exibir_detalhes_pokemon(pokemon)
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

        pasta_imagens = obter_pasta_imagens()
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

        def adicionar_cartao(
            item,
            etiqueta='',
            container=evolucoes_lista,
            codigo='',
            clicavel=False,
        ):
            nome = item.name
            caminho_relativo = database.imagens_formas.get(nome.lower(), f'{int(item.num)}.png')
            caminho_imagem = os.path.join(
                obter_pasta_imagens(), caminho_relativo.replace('/', '_')
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
            texto_cartao = (
                f'{etiqueta}{item.name}\nNº {item.num}'
                f'{f" · {codigo}" if codigo else ""}'
            )
            if clicavel:
                botao_forma = tk.Button(
                    cartao,
                    text=texto_cartao,
                    command=comando_com_som(
                        lambda selecionado=item: abrir_pokemon_relacionado(
                            selecionado
                        )
                    ),
                    font=('Arial', 9, 'bold'),
                    bg='#263238',
                    fg='white',
                    activebackground='#455a64',
                    activeforeground='white',
                    relief='flat',
                    justify='center',
                )
                botao_forma.pack(fill='x', pady=(4, 0))
                adicionar_hover_botao(botao_forma, '#263238', '#455a64')
                imagem_evolucao.bind(
                    '<Button-1>',
                    lambda evento, selecionado=item: comando_com_som(
                        lambda: abrir_pokemon_relacionado(selecionado)
                    )(),
                )
                imagem_evolucao.config(cursor='hand2')
                imagem_evolucao.bind(
                    '<Enter>',
                    lambda evento, imagem=imagem_evolucao: imagem.config(
                        highlightthickness=2, highlightbackground='#fdd835'
                    ),
                )
                imagem_evolucao.bind(
                    '<Leave>',
                    lambda evento, imagem=imagem_evolucao: imagem.config(
                        highlightthickness=0
                    ),
                )
            else:
                tk.Label(
                    cartao,
                    text=texto_cartao,
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
                adicionar_cartao(evolucao, clicavel=True)
        else:
            cadeia = database.cadeias_evolucao.get(
                pokemon.name, [pokemon.name]
            )
            for indice, nome in enumerate(cadeia):
                evolucao = next(item for item in database.pokemons if item.name == nome)
                adicionar_cartao(evolucao, clicavel=True)
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

        formas_alternativas = [
            item for item in database.pokemons
            if item.num == pokemon.num and item is not pokemon
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
                elif forma.paldean:
                    etiqueta = 'PALDEA · '
                    codigo_tauros = {
                        'Tauros de Paldea (Raça de combate)': '128.p',
                        'Tauros de Paldea (Raça de fogo)': '128.p.f',
                        'Tauros de Paldea (Raça de água)': '128.p.a',
                    }.get(forma.name, '')
                else:
                    etiqueta = 'NORMAL · '
                adicionar_cartao(
                    forma,
                    etiqueta,
                    formas_lista,
                    codigo=codigo_tauros,
                    clicavel=True,
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

    def exibir_detalhes_pokemon(pokemon):
        estado_navegacao['pokemon_atual'] = pokemon
        titulo_pokemon.config(
            text=f'{pokemon.name} | Nº {int(pokemon.num)} | {pokemon.geracao_base}'
        )
        categoria_pokemon.config(text=f'Pokémon {pokemon.categoria}')
        geracao_forma.config(text=pokemon.geracao_forma)
        atualizar_etiquetas(etiquetas_tipos, pokemon.types)
        atualizar_etiquetas(etiquetas_fraquezas, pokemon.fraq)
        resultado.config(text=pokemon.description)
        carregar_imagem(pokemon)
        carregar_evolucoes(pokemon)

    def abrir_pokemon_relacionado(pokemon):
        pokemon_atual = estado_navegacao['pokemon_atual']
        if pokemon_atual is not None:
            estado_navegacao['historico_pokemon'].append(pokemon_atual)
        botao_voltar_pagina.place(x=238, y=12)
        exibir_detalhes_pokemon(pokemon)

    def voltar_pagina():
        historico = estado_navegacao['historico_pokemon']
        if historico:
            pokemon_anterior = historico.pop()
            if not historico and not estado_navegacao['detalhe_tipo']:
                botao_voltar_pagina.place_forget()
            exibir_detalhes_pokemon(pokemon_anterior)
            return

        if estado_navegacao['detalhe_tipo']:
            voltar_a_busca_por_tipo()

    def voltar_direto_ao_menu():
        janela_tipos = estado_navegacao['janela_tipos']
        if janela_tipos is not None and janela_tipos.winfo_exists():
            janela_tipos.destroy()
            for botao in botoes_mute[:]:
                if not botao.winfo_exists():
                    botoes_mute.remove(botao)

        estado_navegacao['janela_tipos'] = None
        estado_navegacao['canvas_resultados'] = None
        estado_navegacao['detalhe_tipo'] = False
        estado_navegacao['pokemon_atual'] = None
        estado_navegacao['historico_pokemon'].clear()
        botao_voltar_pagina.place_forget()
        botao_voltar_menu_tipo.place_forget()
        base.pack_forget()
        controles_busca.grid()
        if not tabela_codigos.winfo_manager():
            tabela_codigos.pack(fill='x', pady=(10, 0))
        evolucoes_moldura.grid()
        voltar_ao_menu()
        janela.deiconify()
        janela.lift()

    janela = tk.Tk()
    janela.title('Pokédex')
    janela.configure(bg='#4e1118')

    def ajustar_janela(largura, altura, minimo_largura, minimo_altura):
        janela.resizable(True, True)
        janela.minsize(minimo_largura, minimo_altura)
        janela.maxsize(janela.winfo_screenwidth(), janela.winfo_screenheight())
        x = max(0, (janela.winfo_screenwidth() - largura) // 2)
        y = max(0, (janela.winfo_screenheight() - altura) // 2)
        janela.geometry(f'{largura}x{altura}+{x}+{y}')

    def fixar_tamanho_janela_pokemon():
        largura = min(1600, janela.winfo_screenwidth() - 80)
        altura = min(940, janela.winfo_screenheight() - 120)
        janela.resizable(False, False)
        janela.minsize(largura, altura)
        janela.maxsize(largura, altura)
        x = max(0, (janela.winfo_screenwidth() - largura) // 2)
        y = max(0, (janela.winfo_screenheight() - altura) // 2)
        janela.geometry(f'{largura}x{altura}+{x}+{y}')

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

    vermelho = '#c62828'
    vermelho_escuro = '#8e1b1b'
    preto = '#171717'
    azul_tela = '#90caf9'
    volume_musica = tk.IntVar(value=10)
    estado_audio = {'mudo': False}
    efeitos_ativos = {'ativo': True}
    botoes_mute = []
    botoes_efeitos = []

    caminho_musica = os.path.join(
        os.path.dirname(__file__), 'audio', 'menu_music.ogg'
    )
    caminho_efeito_botao = os.path.join(
        os.path.dirname(__file__), 'audio', 'button_select.ogg'
    )
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(caminho_musica)
        efeito_botao = pygame.mixer.Sound(caminho_efeito_botao)
    except pygame.error as erro:
        messagebox.showerror(
            'Erro de áudio',
            f'Não foi possível carregar o áudio da Pokédex:\n{erro}',
            parent=janela,
        )
        pygame.mixer.quit()
        janela.destroy()
        return

    efeito_botao.set_volume(0.22)

    def atualizar_volume_musica(_valor=None):
        volume = volume_musica.get() / 100
        pygame.mixer.music.set_volume(0 if estado_audio['mudo'] else volume)
        efeito_botao.set_volume(
            0
            if estado_audio['mudo'] or not efeitos_ativos['ativo']
            else 0.22
        )

    def atualizar_botoes_mute():
        texto = 'SOM: OFF' if estado_audio['mudo'] else 'SOM: ON'
        for botao in botoes_mute[:]:
            try:
                botao.config(text=texto)
            except tk.TclError:
                botoes_mute.remove(botao)

    def atualizar_botoes_efeitos():
        texto = (
            'EFEITOS SONOROS: ON'
            if efeitos_ativos['ativo']
            else 'EFEITOS SONOROS: OFF'
        )
        for botao in botoes_efeitos:
            botao.config(text=texto)

    def tocar_som_botao():
        if not estado_audio['mudo'] and efeitos_ativos['ativo']:
            efeito_botao.play()

    def comando_com_som(comando):
        def executar():
            tocar_som_botao()
            comando()

        return executar

    def alternar_mute():
        estado_audio['mudo'] = not estado_audio['mudo']
        atualizar_volume_musica()
        atualizar_botoes_mute()

    def alternar_efeitos():
        efeitos_ativos['ativo'] = not efeitos_ativos['ativo']
        atualizar_volume_musica()
        atualizar_botoes_efeitos()

    def fechar_aplicacao():
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        janela.destroy()

    janela.protocol('WM_DELETE_WINDOW', fechar_aplicacao)
    pygame.mixer.music.set_volume(volume_musica.get() / 100)
    pygame.mixer.music.play(loops=-1)

    menu_inicial = tk.Frame(janela, bg='#4e1118', padx=24, pady=24)
    menu_inicial.pack(fill='both', expand=True)
    menu_inicial.rowconfigure(0, weight=1)
    menu_inicial.columnconfigure(0, weight=1)

    menu_sombra = tk.Frame(menu_inicial, bg='#5b1015', padx=8, pady=8)
    menu_sombra.grid(row=0, column=0)

    menu_moldura = tk.Frame(menu_sombra, bg=vermelho_escuro, padx=12, pady=12)
    menu_moldura.pack()

    menu_visor = tk.Frame(menu_moldura, bg=preto, padx=12, pady=12)
    menu_visor.pack()

    painel_menu = tk.Frame(menu_visor, bg=azul_tela, padx=34, pady=24)
    painel_menu.pack()

    titulo_menu = tk.Canvas(
        painel_menu,
        width=330,
        height=58,
        bg=azul_tela,
        highlightthickness=0,
    )
    for deslocamento_x, deslocamento_y in (
        (-2, -2), (0, -2), (2, -2), (-2, 0), (2, 0), (-2, 2), (0, 2), (2, 2)
    ):
        titulo_menu.create_text(
            165 + deslocamento_x,
            29 + deslocamento_y,
            text='POKÉDEX',
            font=('Arial', 30, 'bold'),
            fill='#174ea6',
        )
    titulo_menu.create_text(
        165,
        29,
        text='POKÉDEX',
        font=('Arial', 30, 'bold'),
        fill='#ffca28',
    )
    titulo_menu.pack(pady=(0, 4))

    opcoes_menu = tk.Frame(painel_menu, bg=azul_tela)
    opcoes_menu.pack()

    titulo_opcoes_menu = tk.Label(
        opcoes_menu,
        text='SELECIONE O MODO',
        font=('Arial', 12, 'bold'),
        bg=azul_tela,
        fg='#263238',
    )
    titulo_opcoes_menu.pack(pady=(0, 14))

    menu_botoes = tk.Frame(opcoes_menu, bg=azul_tela)
    menu_botoes.pack()
    configuracoes_painel = tk.Frame(opcoes_menu, bg=azul_tela)

    def abrir_busca():
        estado_navegacao['detalhe_tipo'] = False
        estado_navegacao['historico_pokemon'].clear()
        botao_voltar_pagina.place_forget()
        botao_voltar_menu_tipo.place(x=96, y=12)
        menu_inicial.pack_forget()
        fixar_tamanho_janela_pokemon()
        base.pack(fill='both', expand=True, padx=22, pady=22)
        entrada_busca.focus_set()

    def voltar_ao_menu():
        estado_navegacao['historico_pokemon'].clear()
        estado_navegacao['pokemon_atual'] = None
        botao_voltar_pagina.place_forget()
        botao_voltar_menu_tipo.place_forget()
        base.pack_forget()
        ajustar_janela(760, 650, 680, 580)
        configuracoes_painel.pack_forget()
        titulo_opcoes_menu.config(text='SELECIONE O MODO')
        menu_botoes.pack()
        menu_inicial.pack(fill='both', expand=True)

    def normalizar_tipo(tipo):
        nome = re.sub(r'\s*\([^)]*\)', '', tipo).strip()
        nome = {
            'Veneno': 'Venenoso',
            'Planta': 'Grama',
            'Metal': 'Aço',
            'Noturno': 'Sombrio',
        }.get(
            nome, nome
        )
        return nome.capitalize()

    def obter_pokemon_base_por_tipo(tipo):
        resultado_tipo = []
        for pokemon in database.pokemons:
            if any((
                pokemon.mega,
                pokemon.gigantamax,
                pokemon.alolan,
                pokemon.galarian,
                pokemon.hisuian,
                pokemon.paldean,
            )):
                continue
            tipos_pokemon = {
                normalizar_tipo(parte) for parte in separar_tipos(pokemon.types)
            }
            if tipo in tipos_pokemon:
                resultado_tipo.append(pokemon)
        return sorted(
            resultado_tipo,
            key=lambda pokemon: (
                int(re.search(r'\d+', pokemon.geracao_base).group()),
                int(pokemon.num),
                any((
                    pokemon.mega,
                    pokemon.gigantamax,
                    pokemon.alolan,
                    pokemon.galarian,
                    pokemon.hisuian,
                    pokemon.paldean,
                )),
                pokemon.name,
            ),
        )

    def abrir_busca_tipo():
        botao_voltar_pagina.place_forget()
        botao_voltar_menu_tipo.place_forget()
        janela_tipos = tk.Toplevel(janela)
        estado_navegacao['janela_tipos'] = janela_tipos
        janela_tipos.title('Pokédex · Busca por tipo')
        janela_tipos.configure(bg='#4e1118')
        janela_tipos.geometry('760x650')
        janela_tipos.minsize(680, 580)

        def fechar_busca_tipo():
            voltar_direto_ao_menu()

        janela_tipos.protocol('WM_DELETE_WINDOW', fechar_busca_tipo)

        moldura_tipos = tk.Frame(
            janela_tipos, bg=vermelho_escuro, padx=12, pady=12
        )
        moldura_tipos.pack(fill='both', expand=True, padx=24, pady=24)

        visor_tipos = tk.Frame(moldura_tipos, bg=preto, padx=12, pady=12)
        visor_tipos.pack(fill='both', expand=True)

        painel_tipos = tk.Frame(visor_tipos, bg=azul_tela, padx=18, pady=16)
        painel_tipos.pack(fill='both', expand=True)
        painel_tipos.columnconfigure(0, weight=1)
        painel_tipos.rowconfigure(1, weight=1)

        tk.Label(
            painel_tipos,
            text='POKÉDEX · BUSCA POR TIPO',
            font=('Arial', 18, 'bold'),
            bg=azul_tela,
            fg='#174ea6',
        ).grid(row=0, column=0, sticky='ew', pady=(0, 12))

        area_paginas = tk.Frame(painel_tipos, bg=azul_tela)
        area_paginas.grid(row=1, column=0, sticky='nsew')
        area_paginas.rowconfigure(0, weight=1)
        area_paginas.columnconfigure(0, weight=1)

        pagina_selecao = tk.Frame(area_paginas, bg=azul_tela)
        pagina_selecao.grid(row=0, column=0, sticky='nsew')
        pagina_resultados = tk.Frame(area_paginas, bg=azul_tela)
        pagina_resultados.grid(row=0, column=0, sticky='nsew')
        pagina_resultados.grid_remove()
        pagina_selecao.columnconfigure((0, 1, 2), weight=1)

        tk.Label(
            pagina_selecao,
            text='SELECIONE UM TIPO',
            font=('Arial', 12, 'bold'),
            bg=azul_tela,
            fg='#263238',
        ).grid(row=0, column=0, columnspan=3, sticky='ew', pady=(2, 12))

        tipos_disponiveis = list(cores_tipos)

        def mostrar_resultados(tipo):
            estado_navegacao['canvas_resultados'] = None
            for widget in pagina_resultados.winfo_children():
                widget.destroy()

            pokemon_tipo = obter_pokemon_base_por_tipo(tipo)
            tk.Label(
                pagina_resultados,
                text=f'TIPO {tipo.upper()} · {len(pokemon_tipo)} POKÉMON',
                font=('Arial', 12, 'bold'),
                bg=azul_tela,
                fg='#263238',
            ).pack(fill='x', pady=(2, 8))

            if not pokemon_tipo:
                tk.Label(
                    pagina_resultados,
                    text='Nenhum Pokémon deste tipo está no catálogo atual.',
                    font=('Arial', 10),
                    bg=azul_tela,
                    fg='#455a64',
                    pady=20,
                ).pack(fill='x')
                botao_voltar_tipos.grid()
                pagina_selecao.grid_remove()
                pagina_resultados.grid()
                return

            lista_canvas = tk.Canvas(
                pagina_resultados,
                bg=azul_tela,
                highlightthickness=0,
            )
            barra_rolagem = tk.Scrollbar(
                pagina_resultados,
                orient='vertical',
                command=lista_canvas.yview,
            )
            lista_canvas.configure(yscrollcommand=barra_rolagem.set)
            estado_navegacao['canvas_resultados'] = lista_canvas
            barra_rolagem.pack(side='right', fill='y')
            lista_canvas.pack(side='left', fill='both', expand=True)

            lista_pokemon = tk.Frame(lista_canvas, bg=azul_tela)
            janela_lista = lista_canvas.create_window(
                (0, 0), window=lista_pokemon, anchor='nw'
            )
            lista_pokemon.bind(
                '<Configure>',
                lambda evento: lista_canvas.configure(
                    scrollregion=lista_canvas.bbox('all')
                ),
            )
            lista_canvas.bind(
                '<Configure>',
                lambda evento: lista_canvas.itemconfigure(
                    janela_lista, width=evento.width
                ),
            )

            por_geracao = {}
            for pokemon in pokemon_tipo:
                por_geracao.setdefault(pokemon.geracao_base, []).append(pokemon)

            for geracao, lista in por_geracao.items():
                tk.Label(
                    lista_pokemon,
                    text=geracao.upper(),
                    font=('Arial', 11, 'bold'),
                    bg=vermelho_escuro,
                    fg='white',
                    padx=8,
                    pady=5,
                ).pack(fill='x', pady=(8, 4))
                grade_pokemon = tk.Frame(lista_pokemon, bg=azul_tela)
                grade_pokemon.pack(fill='x')
                grade_pokemon.columnconfigure((0, 1), weight=1)
                for indice, pokemon in enumerate(lista):
                    botao_pokemon = tk.Button(
                        grade_pokemon,
                        text=f'{pokemon.name} · Nº {int(pokemon.num)}',
                        command=comando_com_som(
                            lambda selecionado=pokemon: abrir_detalhe_tipo(
                                selecionado
                            )
                        ),
                        font=('Arial', 10, 'bold'),
                        bg='#263238',
                        fg='white',
                        activebackground='#455a64',
                        activeforeground='white',
                        relief='flat',
                        padx=6,
                        pady=6,
                    )
                    botao_pokemon.grid(
                        row=indice // 2,
                        column=indice % 2,
                        sticky='ew',
                        padx=4,
                        pady=3,
                    )
                    adicionar_hover_botao(botao_pokemon, '#263238', '#455a64')

            botao_voltar_tipos.grid()
            pagina_selecao.grid_remove()
            pagina_resultados.grid()

        for indice, tipo in enumerate(tipos_disponiveis):
            cor_tipo = cores_tipos.get(tipo, '#607d8b')
            botao_tipo = tk.Button(
                pagina_selecao,
                text=tipo.upper(),
                command=comando_com_som(
                    lambda tipo_selecionado=tipo: mostrar_resultados(
                        tipo_selecionado
                    )
                ),
                font=('Arial', 10, 'bold'),
                bg=cor_tipo,
                fg='#263238' if tipo in ('Elétrico', 'Normal') else 'white',
                activebackground=cor_tipo,
                activeforeground='white',
                relief='flat',
                pady=8,
            )
            botao_tipo.grid(
                row=1 + indice // 3,
                column=indice % 3,
                sticky='ew',
                padx=5,
                pady=5,
            )
            adicionar_hover_botao(botao_tipo, cor_tipo, '#455a64')

        def voltar_aos_tipos():
            estado_navegacao['canvas_resultados'] = None
            pagina_resultados.grid_remove()
            pagina_selecao.grid()
            botao_voltar_tipos.grid_remove()

        barra_volta = tk.Frame(painel_tipos, bg=azul_tela)
        barra_volta.grid(row=2, column=0, sticky='ew', pady=(12, 0))
        barra_volta.columnconfigure(0, weight=1)
        botao_voltar_tipos = tk.Button(
            barra_volta,
            text='VOLTAR AOS TIPOS',
            command=comando_com_som(voltar_aos_tipos),
            font=('Arial', 10, 'bold'),
            bg='#fdd835',
            fg='#263238',
            activebackground='#fff176',
            relief='flat',
            pady=7,
        )
        botao_voltar_tipos.grid(row=0, column=0, sticky='ew')
        adicionar_hover_botao(botao_voltar_tipos, '#fdd835', '#fff176')
        botao_voltar_tipos.grid_remove()

        moldura_botao_menu = tk.Frame(barra_volta, bg=azul_tela)
        moldura_botao_menu.grid(row=1, column=0, sticky='ew', pady=(8, 0))
        botao_voltar_menu = tk.Button(
            moldura_botao_menu,
            text='VOLTAR AO MENU',
            command=comando_com_som(fechar_busca_tipo),
            font=('Arial', 10, 'bold'),
            bg='#b71c1c',
            fg='white',
            activebackground='#e53935',
            relief='flat',
            pady=7,
        )
        botao_voltar_menu.pack(anchor='center')
        adicionar_hover_botao(botao_voltar_menu, '#b71c1c', '#e53935')

        botao_mute_tipos = tk.Button(
            janela_tipos,
            text='',
            command=comando_com_som(alternar_mute),
            font=('Arial', 9, 'bold'),
            bg='#263238',
            fg='white',
            activebackground='#455a64',
            activeforeground='white',
            relief='flat',
            padx=10,
            pady=5,
        )
        botao_mute_tipos.place(x=12, y=12)
        botoes_mute.append(botao_mute_tipos)
        atualizar_botoes_mute()
        janela_tipos.protocol(
            'WM_DELETE_WINDOW', comando_com_som(fechar_busca_tipo)
        )
        janela_tipos.bind(
            '<Escape>', lambda evento: comando_com_som(fechar_busca_tipo)()
        )
        janela.withdraw()
        janela_tipos.lift()

    def abrir_detalhe_tipo(pokemon):
        janela_tipos = estado_navegacao['janela_tipos']
        if janela_tipos is None or not janela_tipos.winfo_exists():
            return

        estado_navegacao['detalhe_tipo'] = True
        estado_navegacao['historico_pokemon'].clear()
        botao_voltar_pagina.place(x=238, y=12)
        botao_voltar_menu_tipo.place(x=96, y=12)
        janela_tipos.withdraw()
        janela.deiconify()
        janela.lift()
        menu_inicial.pack_forget()
        fixar_tamanho_janela_pokemon()
        entrada_busca.delete(0, 'end')
        controles_busca.grid_remove()
        tabela_codigos.pack_forget()
        evolucoes_moldura.grid()
        base.pack(fill='both', expand=True, padx=22, pady=22)
        pokebola.grid()
        exibir_detalhes_pokemon(pokemon)

    def voltar_a_busca_por_tipo():
        janela_tipos = estado_navegacao['janela_tipos']
        if janela_tipos is None or not janela_tipos.winfo_exists():
            estado_navegacao['detalhe_tipo'] = False
            voltar_ao_menu()
            return

        estado_navegacao['detalhe_tipo'] = False
        estado_navegacao['canvas_resultados'] = None
        estado_navegacao['pokemon_atual'] = None
        estado_navegacao['historico_pokemon'].clear()
        botao_voltar_pagina.place_forget()
        botao_voltar_menu_tipo.place_forget()
        base.pack_forget()
        controles_busca.grid()
        tabela_codigos.pack(fill='x', pady=(10, 0))
        evolucoes_moldura.grid()
        janela.withdraw()
        janela_tipos.deiconify()
        janela_tipos.lift()

    def acionar_botao_voltar():
        if (
            estado_navegacao['historico_pokemon']
            or estado_navegacao['detalhe_tipo']
        ):
            voltar_pagina()
        elif botao_voltar_menu_tipo.winfo_ismapped():
            voltar_direto_ao_menu()
        else:
            voltar_ao_menu()

    def voltar_ao_menu_da_busca_tipo():
        voltar_direto_ao_menu()

    def abrir_visualizador_stats(pokemon_inicial=None):
        janela_stats = tk.Toplevel(janela)
        janela_stats.title('Pokédex · Stats e moves')
        janela_stats.configure(bg='#4e1118')
        janela_stats.geometry('1180x850')
        janela_stats.minsize(940, 680)
        janela.withdraw()

        estado_stats = {'dados': None, 'carregando': False}
        fila_resultados = queue.Queue()

        def fechar_visualizador():
            if janela_stats.winfo_exists():
                janela_stats.destroy()
            janela.deiconify()
            janela.lift()

        janela_stats.protocol('WM_DELETE_WINDOW', fechar_visualizador)
        janela_stats.bind('<Escape>', lambda evento: fechar_visualizador())

        botao_mute_stats = tk.Button(
            janela_stats,
            text='',
            command=comando_com_som(alternar_mute),
            font=('Arial', 9, 'bold'),
            bg='#263238',
            fg='white',
            activebackground='#455a64',
            activeforeground='white',
            relief='flat',
            padx=10,
            pady=5,
        )
        botao_mute_stats.place(x=12, y=12)
        botoes_mute.append(botao_mute_stats)
        atualizar_botoes_mute()

        tk.Label(
            janela_stats,
            text='VISUALIZADOR DE STATS E MOVES',
            font=('Arial', 20, 'bold'),
            bg='#4e1118',
            fg='#ffca28',
        ).pack(padx=24, pady=(20, 14))

        moldura_stats = tk.Frame(
            janela_stats, bg=vermelho_escuro, padx=10, pady=10
        )
        moldura_stats.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        painel_stats = tk.Frame(moldura_stats, bg=azul_tela, padx=16, pady=14)
        painel_stats.pack(fill='both', expand=True)
        painel_stats.columnconfigure(0, weight=1)
        painel_stats.rowconfigure(3, weight=1)

        tk.Label(
            painel_stats,
            text='Insira o nome ou o número do pokémon',
            font=('Arial', 11, 'bold'),
            bg=azul_tela,
            fg='#263238',
        ).grid(row=0, column=0, sticky='w', pady=(0, 6))

        barra_pesquisa_stats = tk.Frame(painel_stats, bg=azul_tela)
        barra_pesquisa_stats.grid(row=1, column=0, sticky='ew')
        barra_pesquisa_stats.columnconfigure(0, weight=1)

        entrada_stats = ttk.Combobox(
            barra_pesquisa_stats,
            values=[pokemon.name for pokemon in database.pokemons],
            font=('Arial', 11),
        )
        entrada_stats.grid(row=0, column=0, sticky='ew', padx=(0, 8))
        if pokemon_inicial is not None:
            entrada_stats.set(pokemon_inicial.name)

        status_stats = tk.Label(
            painel_stats,
            text='Os dados de stats e moves são carregados da internet.',
            font=('Arial', 9),
            bg=azul_tela,
            fg='#455a64',
            anchor='w',
        )
        status_stats.grid(row=2, column=0, sticky='ew', pady=(6, 10))

        ttk_style = ttk.Style(janela_stats)
        ttk_style.configure(
            'Stats.Treeview',
            rowheight=25,
            font=('Arial', 9),
        )
        ttk_style.configure(
            'Stats.Treeview.Heading',
            font=('Arial', 9, 'bold'),
        )

        conteudo_stats = tk.Frame(painel_stats, bg=azul_tela)
        conteudo_stats.grid(row=3, column=0, sticky='nsew')
        conteudo_stats.columnconfigure(0, weight=1)

        tk.Label(
            conteudo_stats,
            text='STATS BASE',
            font=('Arial', 12, 'bold'),
            bg=azul_tela,
            fg='#263238',
        ).grid(row=0, column=0, sticky='w')

        tabela_stats = tk.Frame(conteudo_stats, bg=azul_tela)
        tabela_stats.grid(row=1, column=0, sticky='ew', pady=(4, 0))
        tabela_stats.columnconfigure(2, weight=1)
        for indice, texto in enumerate(
            ('STAT', 'BASE', 'DISTRIBUIÇÃO', 'MÍN. LVL 100', 'MÁX. LVL 100')
        ):
            tk.Label(
                tabela_stats,
                text=texto,
                font=('Arial', 8, 'bold'),
                bg='#263238',
                fg='white',
                padx=6,
                pady=5,
                anchor='center',
            ).grid(row=0, column=indice, sticky='ew', padx=(0, 1))

        widgets_stats = []
        for indice, nome_stat in enumerate(pokemon_stats.STAT_ORDER, start=1):
            tk.Label(
                tabela_stats,
                text=pokemon_stats.STAT_LABELS[nome_stat],
                font=('Arial', 9),
                bg=azul_tela,
                fg='#263238',
                anchor='w',
                padx=6,
            ).grid(row=indice, column=0, sticky='ew', pady=2)

            valor_base = tk.Label(
                tabela_stats,
                text='—',
                font=('Arial', 9, 'bold'),
                bg=azul_tela,
                fg='#263238',
                padx=8,
            )
            valor_base.grid(row=indice, column=1, pady=2)

            barra_stat = tk.Canvas(
                tabela_stats,
                height=18,
                bg='#d7eaf8',
                highlightthickness=0,
            )
            barra_stat.grid(
                row=indice,
                column=2,
                sticky='ew',
                padx=6,
                pady=2,
            )
            valor_minimo = tk.Label(
                tabela_stats,
                text='—',
                font=('Arial', 9),
                bg=azul_tela,
                fg='#263238',
                padx=8,
            )
            valor_minimo.grid(row=indice, column=3, pady=2)
            valor_maximo = tk.Label(
                tabela_stats,
                text='—',
                font=('Arial', 9),
                bg=azul_tela,
                fg='#263238',
                padx=8,
            )
            valor_maximo.grid(row=indice, column=4, pady=2)
            widgets_stats.append(
                (valor_base, barra_stat, valor_minimo, valor_maximo)
            )

        total_stats = tk.Label(
            tabela_stats,
            text='TOTAL: —',
            font=('Arial', 10, 'bold'),
            bg=azul_tela,
            fg='#263238',
            anchor='e',
        )
        total_stats.grid(
            row=len(pokemon_stats.STAT_ORDER) + 1,
            column=0,
            columnspan=5,
            sticky='e',
            pady=(3, 10),
        )

        tk.Label(
            conteudo_stats,
            text=(
                'Mínimo: natureza desfavorável, 0 IVs e 0 EVs. '
                'Máximo: natureza favorável, 31 IVs e 252 EVs. Nível 100.'
            ),
            font=('Arial', 8),
            bg=azul_tela,
            fg='#455a64',
            anchor='w',
        ).grid(row=2, column=0, sticky='ew', pady=(0, 12))

        titulo_moves = tk.Label(
            conteudo_stats,
            text='MOVES APRENDIDOS',
            font=('Arial', 12, 'bold'),
            bg=azul_tela,
            fg='#263238',
        )
        titulo_moves.grid(row=3, column=0, sticky='w', pady=(0, 5))

        barra_filtros = tk.Frame(conteudo_stats, bg=azul_tela)
        barra_filtros.grid(row=4, column=0, sticky='ew', pady=(0, 5))
        barra_filtros.columnconfigure(1, weight=1)
        tk.Label(
            barra_filtros,
            text='Método:',
            font=('Arial', 9, 'bold'),
            bg=azul_tela,
            fg='#263238',
        ).grid(row=0, column=0, padx=(0, 6))

        metodo_selecionado = tk.StringVar(value='Todos')
        filtro_metodo = ttk.Combobox(
            barra_filtros,
            textvariable=metodo_selecionado,
            state='readonly',
            values=('Todos',),
            width=24,
        )
        filtro_metodo.grid(row=0, column=1, sticky='w')
        chave_por_filtro = {}

        total_moves = tk.Label(
            barra_filtros,
            text='0 moves',
            font=('Arial', 9),
            bg=azul_tela,
            fg='#455a64',
            anchor='e',
        )
        total_moves.grid(row=0, column=2, sticky='e')

        tabela_moves_frame = tk.Frame(conteudo_stats, bg=azul_tela)
        tabela_moves_frame.grid(row=5, column=0, sticky='nsew')
        tabela_moves_frame.columnconfigure(0, weight=1)
        tabela_moves_frame.rowconfigure(0, weight=1)
        conteudo_stats.rowconfigure(5, weight=1)

        colunas_moves = (
            'method',
            'level',
            'move',
            'type',
            'category',
            'power',
            'accuracy',
        )
        tabela_moves = ttk.Treeview(
            tabela_moves_frame,
            columns=colunas_moves,
            show='headings',
            style='Stats.Treeview',
        )
        titulos_colunas = {
            'method': 'MÉTODO',
            'level': 'NÍVEL',
            'move': 'MOVE',
            'type': 'TIPO',
            'category': 'CATEGORIA',
            'power': 'PODER',
            'accuracy': 'PRECISÃO',
        }
        larguras_colunas = {
            'method': 150,
            'level': 70,
            'move': 240,
            'type': 115,
            'category': 120,
            'power': 85,
            'accuracy': 100,
        }
        for coluna in colunas_moves:
            tabela_moves.heading(coluna, text=titulos_colunas[coluna])
            tabela_moves.column(
                coluna,
                width=larguras_colunas[coluna],
                minwidth=60,
                stretch=coluna == 'move',
                anchor='w' if coluna in ('method', 'move') else 'center',
            )

        barra_vertical_moves = ttk.Scrollbar(
            tabela_moves_frame,
            orient='vertical',
            command=tabela_moves.yview,
        )
        barra_horizontal_moves = ttk.Scrollbar(
            tabela_moves_frame,
            orient='horizontal',
            command=tabela_moves.xview,
        )
        tabela_moves.configure(
            yscrollcommand=barra_vertical_moves.set,
            xscrollcommand=barra_horizontal_moves.set,
        )
        tabela_moves.grid(row=0, column=0, sticky='nsew')
        barra_vertical_moves.grid(row=0, column=1, sticky='ns')
        barra_horizontal_moves.grid(row=1, column=0, sticky='ew')
        tabela_moves_frame.rowconfigure(0, weight=1)

        nomes_tipos = {
            'normal': 'Normal',
            'fighting': 'Lutador',
            'flying': 'Voador',
            'poison': 'Venenoso',
            'ground': 'Terra',
            'rock': 'Pedra',
            'bug': 'Inseto',
            'ghost': 'Fantasma',
            'steel': 'Aço',
            'fire': 'Fogo',
            'water': 'Água',
            'grass': 'Grama',
            'electric': 'Elétrico',
            'psychic': 'Psíquico',
            'ice': 'Gelo',
            'dragon': 'Dragão',
            'dark': 'Sombrio',
            'fairy': 'Fada',
        }
        nomes_categorias = {
            'physical': 'Físico',
            'special': 'Especial',
            'status': 'Status',
        }

        def atualizar_tabela_moves(_evento=None):
            dados = estado_stats['dados']
            if dados is None:
                return

            filtro = metodo_selecionado.get()
            linhas = [
                move for move in dados['moves']
                if filtro == 'Todos'
                or (
                    filtro == 'Outros'
                    and move['method_label'] not in {
                        'Subindo de nível',
                        'Máquina (TM/HM)',
                        'Ovo',
                        'Tutor',
                        'Treinamento',
                    }
                )
                or move['method'] == chave_por_filtro.get(filtro)
            ]
            tabela_moves.delete(*tabela_moves.get_children())
            for move in linhas:
                tabela_moves.insert(
                    '',
                    'end',
                    values=(
                        move['method_label'],
                        move['level'] if move['level'] else '—',
                        move['name'],
                        nomes_tipos.get(move['type'], move['type'].title()),
                        nomes_categorias.get(
                            move['category'], move['category'].title()
                        ),
                        move['power'] if move['power'] is not None else '—',
                        move['accuracy']
                        if move['accuracy'] is not None else '—',
                    ),
                )
            if not linhas:
                tabela_moves.insert(
                    '',
                    'end',
                    values=(
                        '—',
                        '—',
                        'Nenhum move encontrado para este learnset.',
                        '—',
                        '—',
                        '—',
                        '—',
                    ),
                )
            total_moves.config(text=f'{len(linhas)} moves')

        filtro_metodo.bind('<<ComboboxSelected>>', atualizar_tabela_moves)

        def desenhar_barra_stat(canvas, valor):
            canvas.delete('all')
            largura = canvas.winfo_width()
            if largura <= 1:
                return
            preenchimento = max(1, (largura - 4) * min(valor, 255) / 255)
            cor = '#ffd54f' if valor >= 100 else '#ff8f00'
            canvas.create_rectangle(
                2, 3, 2 + preenchimento, 15, fill=cor, outline=''
            )

        def apresentar_dados(pokemon, dados):
            estado_stats['dados'] = dados
            titulo_moves.config(
                text=f'MOVES APRENDIDOS · {dados["learnset_game"]}'
            )
            status_stats.config(
                text=(
                    f'{pokemon.name} · Nº {int(pokemon.num):03d} · '
                    'Fonte: PokéAPI'
                ),
                fg='#455a64',
            )
            if dados['cached']:
                status_stats.config(
                    text=f'{status_stats.cget("text")} · cache local'
                )
            if dados['stale_cache']:
                status_stats.config(
                    text=(
                        f'{pokemon.name} · dados do cache local estão '
                        'desatualizados; a conexão com a API falhou.'
                    ),
                    fg='#b71c1c',
                )

            for widget_stats, stat in zip(widgets_stats, dados['stats']):
                valor_base, barra_stat, valor_minimo, valor_maximo = widget_stats
                valor_base.config(text=str(stat['base']))
                valor_minimo.config(text=str(stat['minimum']))
                valor_maximo.config(text=str(stat['maximum']))
                barra_stat.bind(
                    '<Configure>',
                    lambda evento, canvas=barra_stat, valor=stat['base']:
                    desenhar_barra_stat(canvas, valor),
                )
                desenhar_barra_stat(barra_stat, stat['base'])
            total_stats.config(text=f'TOTAL: {dados["total"]}')

            metodos = sorted({
                move['method'] for move in dados['moves']
            }, key=lambda method: (
                pokemon_stats.LEARN_METHOD_ORDER.get(method, 4),
                method.casefold(),
            ))
            rotulos_filtro = {
                'level-up': 'Nivel',
                'machine': 'Maquina (TM/HM)',
                'egg': 'Ovo',
                'tutor': 'Tutor',
                'train': 'Treinamento',
            }
            chave_por_filtro.clear()
            opcoes_filtro = ['Todos']
            for metodo in metodos:
                rotulo = rotulos_filtro.get(
                    metodo, metodo.replace('-', ' ').title()
                )
                chave_por_filtro[rotulo] = metodo
                opcoes_filtro.append(rotulo)
            if any(metodo not in rotulos_filtro for metodo in metodos):
                opcoes_filtro.append('Outros')
            filtro_metodo.configure(values=opcoes_filtro)
            metodo_selecionado.set('Todos')
            atualizar_tabela_moves()

        def concluir_pesquisa(pokemon, resultado):
            estado_stats['carregando'] = False
            botao_pesquisar.config(state='normal')
            entrada_stats.config(state='normal')
            if isinstance(resultado, pokemon_stats.StatsDataError):
                status_stats.config(
                    text=f'Erro ao carregar os dados: {resultado}',
                    fg='#b71c1c',
                )
                return
            apresentar_dados(pokemon, resultado)

        def verificar_resultado():
            if not janela_stats.winfo_exists():
                return
            try:
                pokemon, resultado = fila_resultados.get_nowait()
            except queue.Empty:
                janela_stats.after(100, verificar_resultado)
                return
            concluir_pesquisa(pokemon, resultado)

        def normalizar_nome_pokemon(nome):
            sem_acentos = ''.join(
                caractere
                for caractere in unicodedata.normalize('NFD', nome.casefold())
                if not unicodedata.combining(caractere)
            )
            return ' '.join(
                re.sub(r'[^a-z0-9♀♂]+', ' ', sem_acentos).split()
            )

        def resolver_pokemon(entrada):
            consulta = entrada.strip()
            codigo = consulta.casefold().replace(' ', '')
            nome_codificado = database.codigos_formas.get(codigo)
            if nome_codificado:
                chave = normalizar_nome_pokemon(nome_codificado)
                return next(
                    pokemon for pokemon in database.pokemons
                    if normalizar_nome_pokemon(pokemon.name) == chave
                )

            if consulta.isdigit():
                numero = int(consulta)
                encontrados = [
                    pokemon for pokemon in database.pokemons
                    if int(pokemon.num) == numero
                ]
                return next(
                    (
                        pokemon for pokemon in encontrados
                        if not any((
                            pokemon.mega,
                            pokemon.gigantamax,
                            pokemon.alolan,
                            pokemon.galarian,
                            pokemon.hisuian,
                            pokemon.paldean,
                        ))
                    ),
                    encontrados[0] if encontrados else None,
                )

            chave = normalizar_nome_pokemon(consulta)
            return next(
                (
                    pokemon for pokemon in database.pokemons
                    if normalizar_nome_pokemon(pokemon.name) == chave
                ),
                None,
            )

        def obter_id_api(pokemon):
            nome = pokemon.name.lower()
            caminho = database.imagens_formas.get(nome, '')
            sprite_id = os.path.splitext(os.path.basename(caminho))[0]
            if sprite_id.isdigit():
                return int(sprite_id)
            return int(
                database.ids_sprites_formas.get(nome, str(int(pokemon.num)))
            )

        def pesquisar_stats(_evento=None):
            if estado_stats['carregando']:
                return
            pokemon = resolver_pokemon(entrada_stats.get())
            if pokemon is None:
                status_stats.config(
                    text='Pokémon não encontrado. Pesquise pelo nome ou número do catálogo.',
                    fg='#b71c1c',
                )
                return

            api_id = obter_id_api(pokemon)
            estado_stats['carregando'] = True
            botao_pesquisar.config(state='disabled')
            entrada_stats.config(state='disabled')
            status_stats.config(
                text=f'Carregando stats e moves de {pokemon.name}...',
                fg='#174ea6',
            )

            def carregar():
                try:
                    resultado = pokemon_stats.buscar_dados(api_id)
                except pokemon_stats.StatsDataError as erro:
                    resultado = erro
                fila_resultados.put((pokemon, resultado))

            threading.Thread(target=carregar, daemon=True).start()
            janela_stats.after(100, verificar_resultado)

        botao_pesquisar = tk.Button(
            barra_pesquisa_stats,
            text='PESQUISAR',
            command=comando_com_som(pesquisar_stats),
            font=('Arial', 10, 'bold'),
            bg='#fdd835',
            fg='#263238',
            activebackground='#fff176',
            relief='flat',
            padx=16,
            pady=5,
        )
        botao_pesquisar.grid(row=0, column=1)
        adicionar_hover_botao(botao_pesquisar, '#fdd835', '#fff176')
        entrada_stats.bind('<Return>', pesquisar_stats)

        botao_voltar_stats = tk.Button(
            painel_stats,
            text='VOLTAR AO MENU',
            command=comando_com_som(fechar_visualizador),
            font=('Arial', 9, 'bold'),
            bg='#b71c1c',
            fg='white',
            activebackground='#e53935',
            relief='flat',
            padx=12,
            pady=5,
        )
        botao_voltar_stats.grid(row=4, column=0, sticky='e', pady=(8, 0))
        adicionar_hover_botao(botao_voltar_stats, '#b71c1c', '#e53935')

        if pokemon_inicial is not None:
            janela_stats.after_idle(pesquisar_stats)
        else:
            janela_stats.after(100, lambda: entrada_stats.focus_set())

    def abrir_configuracoes():
        menu_botoes.pack_forget()
        titulo_opcoes_menu.config(text='CONFIGURAÇÕES')
        configuracoes_painel.pack()

        for widget in configuracoes_painel.winfo_children():
            if widget in botoes_efeitos:
                botoes_efeitos.remove(widget)
            widget.destroy()

        tk.Label(
            configuracoes_painel,
            text='VOLUME DA MÚSICA',
            font=('Arial', 12, 'bold'),
            bg=azul_tela,
            fg='#263238',
        ).pack(pady=(0, 4))

        tk.Scale(
            configuracoes_painel,
            from_=0,
            to=100,
            orient='horizontal',
            variable=volume_musica,
            command=atualizar_volume_musica,
            showvalue=True,
            bg=azul_tela,
            fg='#263238',
            troughcolor='#607d8b',
            highlightthickness=0,
            length=280,
        ).pack(pady=(0, 8))

        botao_efeitos = tk.Button(
            configuracoes_painel,
            text='',
            command=comando_com_som(alternar_efeitos),
            font=('Arial', 10, 'bold'),
            bg='#607d8b',
            fg='white',
            activebackground='#78909c',
            activeforeground='white',
            relief='flat',
            width=24,
            pady=6,
        )
        botao_efeitos.pack(fill='x', pady=4)
        botoes_efeitos.append(botao_efeitos)
        atualizar_botoes_efeitos()
        adicionar_hover_botao(botao_efeitos, '#607d8b', '#78909c')

        botao_voltar_configuracoes = tk.Button(
            configuracoes_painel,
            text='VOLTAR AO MENU',
            command=comando_com_som(voltar_ao_menu),
            font=('Arial', 10, 'bold'),
            bg='#fdd835',
            fg='#263238',
            activebackground='#fff176',
            relief='flat',
            width=24,
            pady=6,
        )
        botao_voltar_configuracoes.pack(fill='x', pady=(10, 0))
        adicionar_hover_botao(botao_voltar_configuracoes, '#fdd835', '#fff176')

    estilo_botao_menu = {
        'font': ('Arial', 11, 'bold'),
        'width': 32,
        'pady': 8,
        'relief': 'flat',
    }
    botao_modo_busca = tk.Button(
        menu_botoes,
        text='BUSCA POR NOME OU NÚMERO',
        command=comando_com_som(abrir_busca),
        bg='#fdd835',
        fg='#263238',
        activebackground='#ffee58',
        activeforeground='#171717',
        **estilo_botao_menu,
    )
    botao_modo_busca.pack(fill='x', pady=5)
    adicionar_hover_botao(botao_modo_busca, '#fdd835', '#fff176')

    botao_busca_tipo = tk.Button(
        menu_botoes,
        text='BUSCA POR TIPO',
        command=comando_com_som(abrir_busca_tipo),
        bg='#fdd835',
        fg='#263238',
        activebackground='#ffee58',
        activeforeground='#171717',
        **estilo_botao_menu,
    )
    botao_busca_tipo.pack(fill='x', pady=5)
    adicionar_hover_botao(botao_busca_tipo, '#fdd835', '#fff176')

    botao_visualizador_stats = tk.Button(
        menu_botoes,
        text='VISUALIZADOR DE STATS',
        command=comando_com_som(abrir_visualizador_stats),
        bg='#fdd835',
        fg='#263238',
        activebackground='#ffee58',
        activeforeground='#171717',
        **estilo_botao_menu,
    )
    botao_visualizador_stats.pack(fill='x', pady=5)
    adicionar_hover_botao(botao_visualizador_stats, '#fdd835', '#fff176')

    botao_configuracoes = tk.Button(
        menu_botoes,
        text='CONFIGURAÇÕES',
        command=comando_com_som(abrir_configuracoes),
        bg='#fdd835',
        fg='#263238',
        activebackground='#ffee58',
        activeforeground='#171717',
        **estilo_botao_menu,
    )
    botao_configuracoes.pack(fill='x', pady=5)
    adicionar_hover_botao(botao_configuracoes, '#fdd835', '#fff176')

    botao_sair = tk.Button(
        menu_botoes,
        text='SAIR',
        command=comando_com_som(fechar_aplicacao),
        bg='#b71c1c',
        fg='white',
        activebackground='#e53935',
        activeforeground='white',
        **estilo_botao_menu,
    )
    botao_sair.pack(fill='x', pady=(12, 0))
    adicionar_hover_botao(botao_sair, '#b71c1c', '#e53935')

    base = tk.Frame(janela, bg='#4e1118')
    base.columnconfigure(0, weight=3)
    base.columnconfigure(1, weight=2)
    base.rowconfigure(0, weight=1)

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
        command=comando_com_som(buscar_pokemon),
        font=('Arial', 10, 'bold'),
        bg='#fdd835',
        fg='#263238',
        activebackground='#ffee58',
        relief='flat',
        padx=18,
        pady=7,
    )
    botao_buscar.grid(row=0, column=1)
    adicionar_hover_botao(botao_buscar, '#fdd835', '#fff176')

    pokebola = tk.Canvas(
        lado_esquerdo,
        width=54,
        height=54,
        bg=vermelho,
        highlightthickness=0,
    )
    pokebola.create_oval(5, 7, 49, 51, fill='#4b0d12', outline='#4b0d12', tags='bola')
    pokebola.create_oval(4, 4, 48, 48, fill='#7d858c', outline='#171717', width=2, tags='bola')
    pokebola.create_oval(6, 6, 46, 46, fill='#e8edf0', outline='#b0b8bd', width=2, tags='bola')
    arco_pokebola = pokebola.create_arc(
        6, 6, 46, 46, start=0, extent=180, fill='#e53935',
        outline='#b71c1c', width=2, tags='bola',
    )
    pokebola.create_line(7, 26, 45, 26, fill='#171717', width=5, tags='bola')
    pokebola.create_oval(16, 16, 36, 36, fill='#5c6268', outline='#171717', width=2, tags='bola')
    pokebola.create_oval(19, 19, 33, 33, fill='#f5f7f8', outline='#cfd8dc', width=1, tags='bola')
    pokebola.create_oval(21, 21, 27, 27, fill='white', outline='white', tags='bola')
    estado_hover_pokebola = {'fator': 1.0, 'trabalho': None}

    def animar_hover_pokebola(hover):
        trabalho_anterior = estado_hover_pokebola['trabalho']
        if trabalho_anterior:
            try:
                pokebola.after_cancel(trabalho_anterior)
            except tk.TclError:
                pass

        fator_inicial = estado_hover_pokebola['fator']
        fator_final = 1.1 if hover else 1.0
        etapas = 6
        cor_inicial = pokebola.itemcget(arco_pokebola, 'fill')
        cor_final = '#ff7043' if hover else '#e53935'
        inicio = tuple(int(cor_inicial[indice:indice + 2], 16) for indice in (1, 3, 5))
        destino = tuple(int(cor_final[indice:indice + 2], 16) for indice in (1, 3, 5))

        def animar(etapa):
            progresso = etapa / etapas
            novo_fator = fator_inicial + (fator_final - fator_inicial) * progresso
            escala = novo_fator / estado_hover_pokebola['fator']
            pokebola.scale('bola', 27, 27, escala, escala)
            estado_hover_pokebola['fator'] = novo_fator
            cor = '#{:02x}{:02x}{:02x}'.format(*(
                round(origem + (fim - origem) * progresso)
                for origem, fim in zip(inicio, destino)
            ))
            pokebola.itemconfigure(arco_pokebola, fill=cor)
            if etapa < etapas:
                estado_hover_pokebola['trabalho'] = pokebola.after(
                    18, animar, etapa + 1
                )
            else:
                estado_hover_pokebola['trabalho'] = None

        animar(1)

    pokebola.bind('<Enter>', lambda evento: (
        animar_hover_pokebola(True),
    ))
    pokebola.bind('<Leave>', lambda evento: animar_hover_pokebola(False))
    pokebola.configure(cursor='hand2')

    def abrir_stats_pokemon_atual():
        abrir_visualizador_stats(estado_navegacao['pokemon_atual'])

    pokebola.bind(
        '<Button-1>',
        lambda evento: comando_com_som(abrir_stats_pokemon_atual)(),
    )
    pokebola.grid(row=3, column=0, pady=(14, 0), sticky='s')

    def atualizar_wrap_texto(evento):
        largura_disponivel = max(160, min(520, evento.width - 28))
        for etiqueta in (titulo_pokemon, resultado):
            if int(etiqueta.cget('wraplength')) != largura_disponivel:
                etiqueta.config(wraplength=largura_disponivel)

    painel_informacoes.bind('<Configure>', atualizar_wrap_texto, add='+')

    def rolar_lista_com_mouse(evento):
        canvas = estado_navegacao['canvas_resultados']
        if canvas is None or not canvas.winfo_exists():
            return

        widget = janela.winfo_containing(evento.x_root, evento.y_root)
        while widget is not None:
            if widget == canvas:
                if getattr(evento, 'num', None) == 4:
                    unidades = -1
                elif getattr(evento, 'num', None) == 5:
                    unidades = 1
                else:
                    unidades = -int(evento.delta / 120)
                    if unidades == 0:
                        unidades = -1 if evento.delta > 0 else 1
                canvas.yview_scroll(unidades, 'units')
                return 'break'
            widget = widget.master

    janela.bind_all('<MouseWheel>', rolar_lista_com_mouse, add='+')
    janela.bind_all('<Button-4>', rolar_lista_com_mouse, add='+')
    janela.bind_all('<Button-5>', rolar_lista_com_mouse, add='+')

    tela_abertura = tk.Frame(janela, bg='#4e1118')
    tela_abertura.place(relwidth=1, relheight=1)

    animacao_abertura = tk.Canvas(
        tela_abertura,
        bg='#4e1118',
        highlightthickness=0,
    )
    animacao_abertura.pack(fill='both', expand=True)
    animacao_abertura.create_rectangle(
        180, 118, 580, 520, fill='#5b1015', outline='#171717', width=5
    )
    animacao_abertura.create_rectangle(
        197, 135, 563, 504, fill=vermelho_escuro, outline='#171717', width=4
    )
    animacao_abertura.create_rectangle(
        218, 158, 542, 394, fill='#171717', outline='#263238', width=8
    )
    animacao_abertura.create_rectangle(
        231, 171, 529, 381, fill=azul_tela, outline='#607d8b', width=3
    )
    animacao_abertura.create_text(
        380,
        256,
        text='POKÉDEX',
        font=('Arial', 32, 'bold'),
        fill='#ffca28',
    )
    animacao_abertura.create_text(
        380,
        306,
        text='Prepare-se para explorar!',
        font=('Arial', 13, 'bold'),
        fill='#263238',
    )
    animacao_abertura.create_oval(
        350, 421, 410, 481, fill='#171717', outline='#7d858c', width=4
    )
    animacao_abertura.create_oval(
        367, 438, 393, 464, fill='#e8edf0', outline='#171717', width=3
    )
    animacao_abertura.create_rectangle(
        218, 158, 542, 394, fill=vermelho, outline='#171717', width=5,
        tags='tampa',
    )
    animacao_abertura.create_line(
        220, 276, 540, 276, fill='#171717', width=8, tags='tampa'
    )
    animacao_abertura.create_oval(
        353, 259, 407, 313, fill='#7d858c', outline='#171717', width=4,
        tags='tampa',
    )
    animacao_abertura.create_oval(
        366, 272, 394, 300, fill='#e8edf0', outline='#171717', width=3,
        tags='tampa',
    )

    estado_abertura = {'ativa': True, 'trabalho': None, 'deslocamento': 0}

    def pular_abertura():
        if not estado_abertura['ativa']:
            return
        estado_abertura['ativa'] = False
        if estado_abertura['trabalho'] is not None:
            janela.after_cancel(estado_abertura['trabalho'])
            estado_abertura['trabalho'] = None
        tela_abertura.destroy()

    botao_pular_abertura = tk.Button(
        tela_abertura,
        text='PULAR ABERTURA »',
        command=comando_com_som(pular_abertura),
        font=('Arial', 9, 'bold'),
        bg='#fdd835',
        fg='#263238',
        activebackground='#fff176',
        relief='flat',
        padx=10,
        pady=6,
    )
    botao_pular_abertura.place(relx=1, x=-16, y=16, anchor='ne')

    def animar_abertura(etapa=0):
        if not estado_abertura['ativa']:
            return
        etapas = 28
        progresso = etapa / etapas
        deslocamento = round(450 * progresso)
        movimento = deslocamento - estado_abertura['deslocamento']
        animacao_abertura.move('tampa', 0, -movimento)
        estado_abertura['deslocamento'] = deslocamento
        if etapa < etapas:
            estado_abertura['trabalho'] = janela.after(
                50, animar_abertura, etapa + 1
            )
        else:
            estado_abertura['trabalho'] = janela.after(350, pular_abertura)

    botao_mute = tk.Button(
        janela,
        text='',
        command=comando_com_som(alternar_mute),
        font=('Arial', 9, 'bold'),
        bg='#263238',
        fg='white',
        activebackground='#455a64',
        activeforeground='white',
        relief='flat',
        padx=10,
        pady=5,
    )
    botao_mute.place(x=12, y=12)
    botoes_mute.append(botao_mute)
    atualizar_botoes_mute()

    botao_voltar_menu_tipo = tk.Button(
        janela,
        text='VOLTAR AO MENU',
        command=comando_com_som(voltar_ao_menu_da_busca_tipo),
        font=('Arial', 9, 'bold'),
        bg='#b71c1c',
        fg='white',
        activebackground='#e53935',
        activeforeground='white',
        relief='flat',
        padx=10,
        pady=5,
    )
    botao_voltar_menu_tipo.place(x=96, y=12)
    botao_voltar_menu_tipo.place_forget()
    adicionar_hover_botao(botao_voltar_menu_tipo, '#b71c1c', '#e53935')

    botao_voltar_pagina = tk.Button(
        janela,
        text='VOLTAR',
        command=comando_com_som(voltar_pagina),
        font=('Arial', 9, 'bold'),
        bg='#fdd835',
        fg='#263238',
        activebackground='#fff176',
        activeforeground='#171717',
        relief='flat',
        padx=10,
        pady=5,
    )
    botao_voltar_pagina.place_forget()
    adicionar_hover_botao(botao_voltar_pagina, '#fdd835', '#fff176')

    janela.bind(
        '<Return>',
        lambda evento: (
            buscar_pokemon()
            if base.winfo_ismapped() and not estado_navegacao['detalhe_tipo']
            else None
        ),
    )
    janela.bind(
        '<Escape>',
        lambda evento: (
            pular_abertura()
            if estado_abertura['ativa']
            else acionar_botao_voltar()
        ),
    )
    ajustar_janela(760, 650, 680, 580)
    base.pack_forget()
    janela.after(100, animar_abertura)
    janela.mainloop()

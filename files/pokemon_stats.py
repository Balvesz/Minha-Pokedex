import json
import os
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = 'https://pokeapi.co/api/v2'
LEARNSET_GAMES = (
    (
        'Pokémon Scarlet/Violet',
        ('the-indigo-disk', 'the-teal-mask', 'scarlet-violet'),
    ),
    ('Pokémon Legends: Arceus', ('legends-arceus',)),
    (
        'Pokémon Brilliant Diamond/Shining Pearl',
        ('brilliant-diamond-shining-pearl',),
    ),
    (
        'Pokémon Sword/Shield',
        ('the-crown-tundra', 'the-isle-of-armor', 'sword-shield'),
    ),
    (
        "Pokémon Let's Go Pikachu/Let's Go Eevee",
        ('lets-go-pikachu-lets-go-eevee',),
    ),
    ('Pokémon Ultra Sun/Ultra Moon', ('ultra-sun-ultra-moon',)),
    ('Pokémon Sun/Moon', ('sun-moon',)),
    ('Pokémon Omega Ruby/Alpha Sapphire', ('omega-ruby-alpha-sapphire',)),
    ('Pokémon X/Y', ('x-y',)),
    ('Pokémon Black 2/White 2', ('black-2-white-2',)),
    ('Pokémon Black/White', ('black-white',)),
    ('Pokémon HeartGold/SoulSilver', ('heartgold-soulsilver',)),
    ('Pokémon Platinum', ('platinum',)),
    ('Pokémon Diamond/Pearl', ('diamond-pearl',)),
    ('Pokémon FireRed/LeafGreen', ('firered-leafgreen',)),
    ('Pokémon Emerald', ('emerald',)),
    ('Pokémon Ruby/Sapphire', ('ruby-sapphire',)),
    ('Pokémon Crystal', ('crystal',)),
    ('Pokémon Gold/Silver', ('gold-silver',)),
    ('Pokémon Yellow', ('yellow',)),
    ('Pokémon Red/Blue', ('red-blue',)),
)
CACHE_MAX_AGE = 30 * 24 * 60 * 60
STAT_ORDER = (
    'hp',
    'attack',
    'defense',
    'special-attack',
    'special-defense',
    'speed',
)
STAT_LABELS = {
    'hp': 'HP',
    'attack': 'Ataque',
    'defense': 'Defesa',
    'special-attack': 'Ataque Especial',
    'special-defense': 'Defesa Especial',
    'speed': 'Velocidade',
}
LEARN_METHOD_ORDER = {
    'level-up': 0,
    'machine': 1,
    'egg': 2,
    'tutor': 3,
    'train': 3,
}
LEARN_METHOD_LABELS = {
    'level-up': 'Subindo de nível',
    'machine': 'Máquina (TM/HM)',
    'egg': 'Ovo',
    'tutor': 'Tutor',
    'train': 'Treinamento',
}


class StatsDataError(Exception):
    pass


def _cache_directory():
    local_app_data = os.environ.get('LOCALAPPDATA')
    base_directory = Path(local_app_data) if local_app_data else Path.home() / '.cache'
    return base_directory / 'MinhaPokedex' / 'pokeapi'


def _cache_path(resource):
    return _cache_directory() / f'{resource.replace("/", "_")}.json'


def _request_json(resource):
    request = Request(
        f'{API_URL}/{resource}/',
        headers={
            'Accept': 'application/json',
            'User-Agent': 'MinhaPokedex/1.0 (educational desktop application)',
        },
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    except HTTPError as erro:
        raise StatsDataError(
            f'A PokéAPI respondeu com erro HTTP {erro.code} ao buscar {resource}.'
        ) from erro
    except (URLError, TimeoutError) as erro:
        raise StatsDataError(
            'Não foi possível conectar à PokéAPI. Verifique sua conexão com a internet.'
        ) from erro
    except (json.JSONDecodeError, UnicodeDecodeError) as erro:
        raise StatsDataError(
            f'A resposta recebida da PokéAPI para {resource} está inválida.'
        ) from erro


def _get_json(resource):
    caminho_cache = _cache_path(resource)
    cache = None

    try:
        cache_existe = caminho_cache.exists()
    except OSError as erro:
        raise StatsDataError(
            f'Não foi possível acessar o cache da PokéAPI em "{caminho_cache}".'
        ) from erro

    if cache_existe:
        try:
            with caminho_cache.open(encoding='utf-8') as arquivo:
                cache = json.load(arquivo)
            dados_cache = cache['data']
            idade_cache = time.time() - cache['fetched_at']
        except (OSError, json.JSONDecodeError, KeyError, TypeError) as erro:
            raise StatsDataError(
                f'O cache de {resource} está inválido. Apague-o em '
                f'"{caminho_cache}" e tente novamente.'
            ) from erro

        if idade_cache < CACHE_MAX_AGE:
            return dados_cache, 'cache'

    try:
        dados = _request_json(resource)
    except StatsDataError:
        if cache is not None:
            return cache['data'], 'cache-antigo'
        raise

    caminho_temporario = None
    try:
        caminho_cache.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            dir=caminho_cache.parent,
            delete=False,
        ) as arquivo:
            caminho_temporario = Path(arquivo.name)
            json.dump(
                {'fetched_at': time.time(), 'data': dados},
                arquivo,
                ensure_ascii=False,
            )
        os.replace(caminho_temporario, caminho_cache)
    except OSError as erro:
        raise StatsDataError(
            f'Não foi possível salvar o cache da PokéAPI em "{caminho_cache}".'
        ) from erro
    finally:
        if caminho_temporario is not None and caminho_temporario.exists():
            try:
                caminho_temporario.unlink()
            except OSError as erro:
                raise StatsDataError(
                    f'Não foi possível remover o arquivo temporário '
                    f'"{caminho_temporario}".'
                ) from erro

    return dados, 'internet'


def _stat_range(base_stat, is_hp):
    if is_hp:
        minimum = 2 * base_stat + 110
        maximum = 2 * base_stat + 204
    else:
        minimum = int((2 * base_stat + 5) * 0.9)
        maximum = int((2 * base_stat + 99) * 1.1)
    return minimum, maximum


def _move_summary(move_slug):
    move, fonte_dados = _get_json(f'move/{move_slug}')
    english_name = next(
        (
            entry['name']
            for entry in move.get('names', [])
            if entry.get('language', {}).get('name') == 'en'
        ),
        move['name'].replace('-', ' ').title(),
    )
    return move_slug, {
        'name': english_name,
        'type': move['type']['name'],
        'category': move['damage_class']['name'],
        'power': move['power'],
        'accuracy': move['accuracy'],
        'data_source': fonte_dados,
    }


def _buscar_dados(pokemon_id):
    pokemon, fonte_pokemon = _get_json(f'pokemon/{pokemon_id}')
    version_details = {}
    for pokemon_move in pokemon['moves']:
        for detalhe in pokemon_move['version_group_details']:
            grupo = detalhe['version_group']['name']
            version_details.setdefault(grupo, []).append(
                (
                    pokemon_move['move']['name'],
                    detalhe['move_learn_method']['name'],
                    detalhe['level_learned_at'],
                )
            )

    learnset_game = 'Nenhum jogo compatível encontrado'
    selected_groups = ()
    for game_name, game_groups in LEARNSET_GAMES:
        if any(version_details.get(group) for group in game_groups):
            learnset_game = game_name
            selected_groups = game_groups
            break

    moves_por_metodo = {
        move for group in selected_groups
        for move in version_details.get(group, ())
    }

    slugs = sorted({chave[0] for chave in moves_por_metodo})
    dados_moves = {}
    if slugs:
        with ThreadPoolExecutor(max_workers=6) as executor:
            for slug, resumo in executor.map(_move_summary, slugs):
                dados_moves[slug] = resumo

    stats_base = {
        stat['stat']['name']: stat['base_stat']
        for stat in pokemon['stats']
    }
    if set(stats_base) != set(STAT_ORDER):
        raise StatsDataError(
            f'A PokéAPI não retornou os seis stats esperados para {pokemon["name"]}.'
        )

    stats = []
    for nome_stat in STAT_ORDER:
        base_stat = stats_base[nome_stat]
        minimum, maximum = _stat_range(
            base_stat, nome_stat == 'hp'
        )
        stats.append({
            'name': STAT_LABELS[nome_stat],
            'base': base_stat,
            'minimum': minimum,
            'maximum': maximum,
        })

    ordem_metodos = lambda chave: (
        LEARN_METHOD_ORDER.get(chave[1], 4),
        chave[2] if chave[1] == 'level-up' else 0,
        dados_moves[chave[0]]['name'].casefold(),
    )
    moves = []
    for slug, metodo, nivel in sorted(moves_por_metodo, key=ordem_metodos):
        dados = dados_moves[slug]
        metodo_label = LEARN_METHOD_LABELS.get(
            metodo, metodo.replace('-', ' ').title()
        )
        moves.append({
            'method': metodo,
            'method_label': metodo_label,
            'level': nivel,
            **dados,
        })

    return {
        'api_name': pokemon['name'],
        'learnset_game': learnset_game,
        'stats': stats,
        'total': sum(stats_base.values()),
        'moves': moves,
        'stale_cache': fonte_pokemon == 'cache-antigo' or any(
            move['data_source'] == 'cache-antigo'
            for move in dados_moves.values()
        ),
        'cached': fonte_pokemon == 'cache' and all(
            move['data_source'] == 'cache'
            for move in dados_moves.values()
        ),
    }


def buscar_dados(pokemon_id):
    try:
        return _buscar_dados(pokemon_id)
    except StatsDataError:
        raise
    except (IndexError, KeyError, TypeError, ValueError) as erro:
        raise StatsDataError(
            'A PokéAPI retornou dados em um formato inesperado.'
        ) from erro

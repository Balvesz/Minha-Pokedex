import re

class Pokemon:
    def __init__(self, name, num, types, fraq, gen, ev, description, categoria, mega=False, gigantamax=False, alolan=False, galarian=False, nivel_ev='', hisuian=False, paldean = False):
        self.name = name
        self.num = num
        self.types = types
        self.fraq = fraq
        self.gen = gen
        partes_geracao = re.split(r'\s*,\s*porém\s*', gen, maxsplit=1, flags=re.IGNORECASE)
        self.geracao_base = partes_geracao[0]
        geracao_forma = partes_geracao[1] if len(partes_geracao) > 1 else ''
        match_geracao_forma = re.search(r'na (\dª geração)', geracao_forma, re.IGNORECASE)
        self.geracao_forma = (
            f'Forma introduzida na {match_geracao_forma.group(1)}'
            if match_geracao_forma else ''
        )
        self.ev = ev
        niveis = re.findall(r'nível\s+(\d+)', ev, flags=re.IGNORECASE)
        if nivel_ev:
            niveis = re.findall(r'\d+', nivel_ev)
        self.niveis_ev = niveis
        self.nivel_ev = ' / '.join(niveis) if niveis else ''
        metodos = {
            'pedra do trovão': 'PEDRA DO TROVÃO',
            'pedra de gelo': 'PEDRA DE GELO',
            'pedra da lua': 'PEDRA DA LUA',
            'pedra de fogo': 'PEDRA DE FOGO',
            'pedra de água': 'PEDRA DE ÁGUA',
            'pedra de grama': 'PEDRA DE GRAMA',
            'pedra do sol': 'PEDRA DO SOL',
            'pedra da aurora': 'PEDRA DA AURORA',
            'pedra brilhante': 'PEDRA BRILHANTE',
            'pedra da noite': 'PEDRA DA NOITE',
            'pedra do gelo': 'PEDRA DO GELO',
        }
        amizade = re.search(r'(\d+) pontos? de (?:amizade|felicidade)', ev.lower())
        self.metodo_ev = f'FELICIDADE {amizade.group(1)}' if amizade else (
            'TROCA' if 'troca' in ev.lower() else next(
            (texto for chave, texto in metodos.items() if chave in ev.lower()),
            '',
            )
        )
        self.description = description
        self.categoria = categoria
        self.mega = mega
        self.gigantamax = gigantamax
        self.alolan = alolan
        self.galarian = galarian
        self.hisuian = hisuian
        self.paldean = paldean

Bulbassauro = Pokemon('Bulbassauro', '0001', 'Grama e Venenoso', 'Fogo, Voador, Gelo e Psíquico', '1ª geração', 'Ivysaruro no nível 16 e depois para Venossauro no nível 32','Ele carrega uma semente nas costas desde o seu nascimento. Conforme seu corpo cresce, a semente também cresce. Além disso, em alguns lugares, Bulbassauros e suas evoluções criam uma espécie de comunidade, onde cada um se ajuda e, ao meio dia, todos se juntam em locais altos para tomarem sol.', 'Semente')
Ivyssauro = Pokemon('Ivyssauro', '0002', 'Grama e Venenoso', 'Fogo, Voador, Gelo e Psíquico', '1ª geração', 'Venossauro no nível 32','O bulbo em suas costas cresce absorvendo nutrientes. Ele também emite um aroma prazeroso quando floresce.', 'Semente')
Venossauro = Pokemon('Venossauro', '0003', 'Grama e Venenoso', 'Fogo, Voador, Gelo e Psíquico', '1ª geração', 'Ele é a última evolução de sua cadeia','Depois de um dia de chuva, a flor em suas costas emite um aroma poderoso. Esse cheiro atrai outros pokémons.', 'Semente')
Mega_Venossauro = Pokemon('Mega Venossauro', '0003', 'Grama e Venenoso', 'Fogo, Voador, Gelo e Psíquico', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','A flor em suas costas cresce ainda mais, se tornando praticamente uma árvore. Devido a esse imenso cresimento de sua flor, suas pernas se tornam muito mais fortes.', 'Semente', mega=True)
Gigantamax_Venossauro = Pokemon('Gigantamax Venossauro', '0003', 'Grama e Venenoso', 'Fogo, Voador, Gelo e Psíquico', '1ª geração, porém sua forma Gigantamax foi introduzida na 8ª geração', '','Quando Venossauro se transforma em Gigantamax, ele se torna colossal e passa a ser rodeado por duas vinhas que tem força o suficiente para derrubar prédios.', 'Semente', gigantamax=True)
Charmander = Pokemon('Charmander', '0004', 'Fogo', 'Água, Terra e Pedra', '1ª geração', 'Charmeleon no nível 16 e depois para Charizard no nível 36','A chama em sua cauda indica seu estado de saúde. Se estiver forte, a chama brilha intensamente. Se estiver fraco, a chama se apaga.', 'Lagarto')
Charmeleon = Pokemon('Charmeleon', '0005', 'Fogo', 'Água, Terra e Pedra', '1ª geração', 'Charizard no nível 36','Quando se enfurece, ele cospe fogo ardente. Se estiver com raiva, a chama em sua cauda queima mais intensamente.', 'Chama')
Charizard = Pokemon('Charizard', '0006', 'Fogo e Voador', 'Água, Terra e Pedra (4x)', '1ª geração', 'Ele é a última evolução de sua cadeia','As asas de Charizard são capazes de levá-lo a altitudes próximas de 4.600 pés. Quanto mais experiencia em batalha ele tem, mais potente se torna seu fogo.', 'Chama')
Mega_Charizard_X = Pokemon('Mega Charizard X', '0006', 'Fogo e Dragão', 'Dragão, Terra e Pedra', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','Quando Charizard Mega Evolui para Mega Charizard X, ele se torna um Pokémon do tipo Fogo e Dragão. Suas chamas se tornam azuis e ficam extremamente poderosas.', 'Chama', mega=True)
Mega_Charizard_Y = Pokemon('Mega Charizard Y', '0006', 'Fogo e Voador', 'Água, Terra e Pedra (4x)', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','Quando Charizard Mega Evolui para Mega Charizard Y, suas chamas se tornam mais intensas e ele ganha a habilidade de voar mais rápido.', 'Chama', mega=True)
Gigantamax_Charizard = Pokemon('Gigantamax Charizard', '0006', 'Fogo e Voador', 'Água, Terra e Pedra (4x)', '1ª geração, porém sua forma Gigantamax foi introduzida na 8ª geração', '','Quando Charizard Gigantamax se transforma, ele se torna colossal e suas chamas se tornam ainda mais poderosas.', 'Chama', gigantamax=True)
Squirtle = Pokemon('Squirtle', '0007', 'Água', 'Elétrico e Grama', '1ª geração', 'Wartortle no nível 16 e depois para Blastoise no nível 36','Apesar de sua aparência fofa, sua concha é extremamente resistente. Ele se protege dentro dela quando sente perigo. Além disso, ele pode disparar um jato de água muito forte de sua boca .', 'Tartaruga pequena')
Wartortle = Pokemon('Wartortle', '0008', 'Água', 'Elétrico e Grama', '1ª geração', 'Blastoise no nível 36','Quanto maior sua calda fofa é, maior é sua longevidade, então ele é muito popular com a terceira idade.', 'Tartaruga')
Blastoise = Pokemon('Blastoise', '0009', 'Água', 'Elétrico e Grama', '1ª geração', 'Ele é a última evolução de sua cadeia','Blastoise possui dois canhões de água em suas costas. A força de seus canhões é comparável com a de um foguete. Ele também pode girar os canhões para disparar água em qualquer direção.', 'Marisco')
Mega_Blastoise = Pokemon('Mega Blastoise', '0009', 'Água', 'Elétrico e Grama', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','Quando Blastoise Mega Evolui para Mega Blastoise, seus canhões se fundem em um único nas costas, com força equivalente ao de um tanque, além de dois canhões extras nas mãos.', 'Marisco', mega=True)
Gigantamax_Blastoise = Pokemon('Gigantamax Blastoise', '0009', 'Água', 'Elétrico e Grama', '1ª geração, porém sua forma Gigantamax foi introduzida na 8ª geração', '','Quando Blastoise vira Gigantamax, seu casco se torna praticamente um navio de guerra. Há, em suas costas, dezenas de canhões e um grande central com força suficiente para furar uma montanha.', 'Marisco', gigantamax=True)
Caterpie = Pokemon('Caterpie', '0010', 'Inseto', 'Fogo, Voador e Pedra', '1ª geração', 'Metapod no nível 7 e depois para Butterfree no nível 10','Sua antena tem grandes poderes sensoriais. Quando se sente ameaçado, ela libera um fedor terrível. Além disso, Caterpie produz teias pegajosas.', 'Minhoca')
Metapod = Pokemon('Metapod', '0011', 'Inseto', 'Fogo, Voador e Pedra', '1ª geração', 'Butterfree no nível 10','Metapod é a fase de casulo de caterpie. A única coisa que pode fazer, enquanto espera a evolução é se endurecer.', 'Casulo')
Butterfree = Pokemon('Butterfree', '0012', 'Inseto e Voador', 'Fogo, Elétrico, Voador, Gelo e Pedra (4x)', '1ª geração', 'Ele é a última evolução de sua cadeia','Butterfree ama pólen e pode localizar fontes de pólen de grandes distâncias.', 'Borboleta')
Gigantamax_Butterfree = Pokemon('Gigantamax Butterfree', '0012', 'Inseto e Voador', 'Fogo, Elétrico, Voador, Gelo e Pedra (4x)', '1ª geração, porém sua forma Gigantamax foi introduzida na 8ª geração', '','Quando Butterfree se transforma em Gigantamax, a energia gigantamax faz ele brilhar intesamente e ganhar escamas altamente tóxicas.', 'Borboleta', gigantamax=True)
Weedle = Pokemon('Weedle', '0013', 'Inseto e Venenoso', 'Fogo, Voador, Pedra e Psíquico', '1ª geração', 'Kakuna no nível 7 e depois para Beedrill no nível 10','O espinho de Weedle é muito afiado e venenoso. Seu veneno pode causar dormência se o atingir. Ele come folhas e se esconde de predadores nelas.', 'Inseto peludo')
Kakuna = Pokemon('Kakuna', '0014', 'Inseto e Venenoso', 'Fogo, Voador, Pedra e Psíquico', '1ª geração', 'Beedrill no nível 10','Kakuna é a fase de casulo de Weedle. Quando ameaçado, ele se gruda em superfícies e ejeta veneno em seu inimigo.', 'Casulo')
Beedrill = Pokemon('Beedrill', '0015', 'Inseto e Venenoso', 'Fogo, Voador, Pedra e Psíquico', '1ª geração', 'Ele é a última evolução de sua cadeia','Beedrill é um pokémon muito agressivo. Ele tem três ferrões venenosos que pode usar para atacar. O ferrão de seu abdômen é discreto e mais venenoso que os demais.', 'Abelha venenosa')
Mega_Beedrill = Pokemon('Mega Beedrill', '0015', 'Inseto e Venenoso', 'Fogo, Voador, Pedra e Psíquico', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','Mega Beedrill assume uma forma muito mais aterrorizante e brutal. Agora possui cinco ferrões, um em cada perna e o do abdômen fica mais avantajado e perigoso.', 'Abelha venenosa', mega=True)
Pidgey = Pokemon('Pidgey', '0016', 'Normal e Voador', 'Elétrico, Gelo e Pedra', '1ª geração', 'Pidgeotto no nível 18 e depois para Pidgeot no nível 36','Pidgey é um pokémon muito dócil. Ele voa em bandos e se alimenta de sementes.', 'Passarinho')
Pidgeotto = Pokemon('Pidgeotto', '0017', 'Normal e Voador', 'Elétrico, Gelo e Pedra', '1ª geração', 'Pidgeot no nível 36','Pidgeotto é um pokémon muito territorial. Ele defende seu território com ferocidade.', 'Pássaro')
Pidgeot = Pokemon('Pidgeot', '0018', 'Normal e Voador', 'Elétrico, Gelo e Pedra', '1ª geração', 'Ele é a última evolução de sua cadeia','Pidgeot é um pokémon muito rápido. Ele pode voar a velocidades de até 100 milhas por hora.', 'Pássaro')
Mega_Pidgeot = Pokemon('Mega Pidgeot', '0018', 'Normal e Voador', 'Elétrico, Gelo e Pedra', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','Quando Pidgeot mega evolui, suas asas se tornam mais longas e poderosas, permitindo que ele voe ainda mais rápido por até duas semanas continuamente.', 'Pássaro', mega=True)
Rattata = Pokemon('Rattata', '0019', 'Normal', 'Lutador', '1ª geração', 'Raticate no nível 20','Os dentes de Rattata são muito afiadas e podem cortar qualquer coisa. Se você vir um, pode ter certeza que vão ter, pelo menos, mais quarenta deles.', 'Rato')
Alolan_Rattata = Pokemon('Rattata de Alola', '0019', 'Noturno e Normal', 'Inseto, Lutador (4x) e Fada', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Alolan Raticate no nível 20','Seus bigodes fornecem um olfato apurado, permitindo-lhe captar o cheiro de comida escondida e localizá-la instantaneamente.', 'Rato', alolan=True)
Raticate = Pokemon('Raticate', '0020', 'Normal', 'Lutador', '1ª geração', 'Ele é a última evolução de sua cadeia','Suas patas traseiras são membranosas. Elas agem como nadadeiras, para que ele possa nadar em rios e caçar presas.', 'Rato')
Alolan_Raticate = Pokemon('Raticate de Alola', '0020', 'Noturno e Normal', 'Inseto, Lutador (4x) e Fada', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Ele é a última evolução de sua cadeia','Raticate de Alola faz Rattatas conseguirem comida para ele, comendo sozinho as mais nutritivas e deliciosas comidas.', 'Rato', alolan=True)
Spearow = Pokemon('Spearow', '0021', 'Normal e Voador', 'Elétrico, Gelo e Pedra', '1ª geração', 'Fearow no nível 20','Spearow é incapaz de voar muito alto, porém, para compensar, consegue voar em velocidades impressionantes. Além disso, é extremamente territorialista e agressivo.', 'Passarinho')
Fearow = Pokemon('Fearow', '0022', 'Normal e Voador', 'Elétrico, Gelo e Pedra', '1ª geração', 'Ele é a última evolução de sua cadeia','Ele tem capacidades sensitivas muito grandes, então, quando detecta perigo, voa instantaneamente para o alto. Além disso, esse pokémon tem uma memória muito grande, podendo lembrar de alguém que o fez mal até anos depois.', 'Pássaro bicudo')
Ekans = Pokemon('Ekans', '0023', 'Veneno', 'Terra e Psíquico', '1ª geração', 'Arbok no nível 22','Ekans pode botar a língua para dentro e para fora rapidamente. Quando ela faz isso, consegue sentir o perigo nos arredores.', 'Serpente')
Arbok = Pokemon('Arbok', '0024', 'Veneno', 'Terra e Psíquico', '1ª geração', 'Ele é a última evolução de sua cadeia','Arbok tem um padrão em seu corpo que se parece com um rosto assustador. Ele usa esse padrão para intimidar seus inimigos.', 'Cobra')
Pikachu = Pokemon('Pikachu', '0025', 'Elétrico', 'Terra', '1ª geração', 'Raichu com uso da Pedra do Trovão','Pikachu é um pokémon elétrico que pode gerar eletricidade em suas bochechas. Quando se sente ameaçado, ele libera eletricidade para se defender.', 'Rato elétrico')
Gigantamax_Pikachu = Pokemon('Gigantamax Pikachu', '0025', 'Elétrico', 'Terra', '1ª geração, porém sua forma Gigantamax foi introduzida na 8ª geração', '','Quando Pikachu se transforma em Gigantamax, ele se torna colossal e suas bochechas ficam ainda mais vermelhas e brilhantes, podendo gerar eletricidade suficiente para iluminar uma cidade inteira.', 'Rato elétrico', gigantamax=True)
Raichu = Pokemon('Raichu', '0026', 'Elétrico', 'Terra', '1ª geração', 'Ele é a última evolução de sua cadeia','Raichu tem uma longa cauda que pode gerar eletricidade. Ele usa essa cauda para atacar seus inimigos.', 'Rato elétrico')
Alolan_Raichu = Pokemon('Raichu de Alola', '0026', 'Elétrico e Psíquico', 'Inseto, Terra, Sombrio e Fantasma', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Ele é a última evolução de sua cadeia','Raichu de Alola tem uma cauda que funciona como um skate, graças aos seus poderes psíquicos. Ele pode usar essa cauda para se locomover rapidamente.', 'Rato elétrico', alolan=True)
Mega_Raichu_X = Pokemon('Mega Raichu X', '0026', 'Elétrico', 'Terra', '1ª geração, porém sua Mega forma foi introduzida na 9ª geração', '','Mega Raichu X assume uma forma que se parece um X, graças a sua cauda que se divide em duas. Além disso, ele pode voar graças a um campo eletromagnético de 50 milhoões de Volts gerados por suas orelhas e caudas.', 'Rato elétrico', mega=True)
Mega_Raichu_Y = Pokemon('Mega Raichu Y', '0026', 'Elétrico', 'Terra', '1ª geração, porém sua Mega forma foi introduzida na 9ª geração', '','Mega Raichu Y assume uma forma que se parece um Y, graças a duas novas orelhas que surgem em sua cabeça. Além disso, seus raios ficam muito mais poderosos, sendo lançados de suas orelhas e cauda.', 'Rato elétrico', mega=True)
Sandshrew = Pokemon('Sandshrew', '0027', 'Terra', 'Água, Grama e Gelo', '1ª geração', 'Sandslash no nível 22','Como Sandshrew vive em desertos, ele se enterra na areia para se proteger do calor e de predadores.', 'Rato')
Alolan_Sandshrew = Pokemon('Sandshrew de Alola', '0027', 'Gelo e Aço', 'Fogo (4x), Lutador (4x) e Terra', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Sandslash de Alola com uso da Pedra de Gelo','Sandshrew de Alola tem uma pele dura como aço. Ele se protege de predadores com suas garras afiadas e seu corpo coberto de gelo.', 'Rato', alolan=True)
Sandslash = Pokemon('Sandslash', '0028', 'Terra', 'Água, Grama e Gelo', '1ª geração', 'Ele é a última evolução de sua cadeia','Sandslash tem espinhos afiados em suas costas. Ele se enrola em uma bola para se proteger de predadores.', 'Rato')
Alolan_Sandslash = Pokemon('Sandslash de Alola', '0028', 'Gelo e Aço', 'Fogo (4x), Lutador (4x) e Terra', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Ele é a última evolução de sua cadeia','Seus espinhos de gelo são duros como aço, que podem causar ferimentos profundos. Além disso, devido suas garras ele consegue escalar até mesmo um iceberg sem escorregar.', 'Rato', alolan=True)
Nidoran_F = Pokemon('Nidoran ♀', '0029', 'Veneno', 'Terra e Psíquico', '1ª geração', 'Nidorina no nível 16 e depois para Nidoqueen com uso da Pedra da Lua','Nidoran ♀ é um pokémon muito tímido. Ele se esconde em arbustos e se camufla com a vegetação.', 'Espinho venenoso')
Nidorina = Pokemon('Nidorina', '0030', 'Veneno', 'Terra e Psíquico', '1ª geração', 'Nidoqueen com uso da Pedra da Lua','Nidorina é um pokémon muito protetor. Ela defende seus filhotes com ferocidade. Acredita-se que, por ela ser extremamente protetora, o chifre em sua cabeça atrofie para que ela não tenha chances de machucar seus filhotes sem querer enquanto os alimenta.', 'Espinho veneno')
Nidoqueen = Pokemon('Nidoqueen', '0031', 'Veneno e Terra', 'Água, Terra, Psíquico e Gelo', '1ª geração', 'Ele é a última evolução de sua cadeia','Nidoqueen tem um corpo tão robusto quanto uma armadura. Além disso, os espinhos em suas costas servem para, além de secretar veneno, colocar suas crias entre eles para transportá-las. Quando suas crias estão nos espinhos, eles nunca secretam veneno.', 'Broca')
Nidoran_M = Pokemon('Nidoran ♂', '0032', 'Veneno', 'Terra e Psíquico', '1ª geração', 'Nidorino no nível 16 e depois para Nidoking com uso da Pedra da Lua','O chifre na cabeça deNidoran ♂ tem um poderoso veneno. Ele é muito cauteloso, sempre estando à espreita ouvindo os arredores com suas grandes orelhas.', 'Chifre venenoso')
Nidorino = Pokemon('Nidorino', '0033', 'Veneno', 'Terra e Psíquico', '1ª geração', 'Nidoking com uso da Pedra da Lua','Como o chifre de Nidorino é mais duro que diamante, ele sai pelo mundo a procura de pedras para quebrá-las e tentar achar uma Pedra da Lua para evoluir.', 'Chifre venenoso')
Nidoking = Pokemon('Nidoking', '0034', 'Veneno e Terra', 'Água, Terra, Psíquico e Gelo', '1ª geração', 'Ele é a última evolução de sua cadeia','Quando Nidoking fica furioso, é impossível acalmá-lo, a não ser que a Nidoqueen na qual ele viva por um longo tempo acalme ele.', 'Broca')
Clefairy = Pokemon('Clefairy', '0035', 'Fada', 'Aço e Veneno', '1ª geração', 'Clefable com uso da Pedra da Lua','Clefairy tem um comportamento muito único. Eles costumam ficar dentro de cavernas ou lugares escuros durante o dia e só sair durante a noite. Em noites de lua cheia, eles se reúnem no Mt. Moon e dançam para a lua, o que faz alguns até mesmo flutuarem.', 'Fada')
Clefable = Pokemon('Clefable', '0036', 'Fada', 'Aço e Veneno', '1ª geração', 'Ele é a última evolução de sua cadeia','Clefable tem uma habilidade única. Ele pode usar suas asas para planar. Eles também se encontram junto das Clefairy para dançar para a lua, mas, diferente deles, em raros casos são vistos em florestas durante o dia ajudando outros pokémon.', 'Fada')
Mega_Clefable = Pokemon('Mega Clefable', '0036', 'Fada e Voador', 'Elétrico, Pedra, Gelo, Aço e Veneno', '1ª geração, porém sua Mega forma foi introduzida na 9ª geração', '','Mega Clefable ganha asas mais evoluídas, mas, ainda assim, não a permite voar. Porém, em sua mega forma, ela consegue manipular a energia da luz da lua para manipular e, assim, voar.', 'Fada', mega=True)
Vulpix = Pokemon('Vulpix', '0037', 'Fogo', 'Água, Terra e Pedra', '1ª geração', 'Ninetales com uso da Pedra de Fogo','Vulpix tem uma cauda que cresce com o tempo. Quando ele nasce, ele tem apenas uma cauda, mas, conforme ele cresce, mais caudas vão surgindo.', 'Raposa')
Alolan_Vulpix = Pokemon('Vulpix de Alola', '0037', 'Gelo', 'Fogo, Lutador, Pedra e Aço', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Alolan Ninetales com uso da Pedra de Gelo','Vulpix de Alola tem uma pelagem branca e fofa, como a neve, que pode ser usada para se camuflar. Vulpix de Alola vivem juntos, formando grupos para caçar e se proteger.', 'Raposa', alolan=True)
Ninetales = Pokemon('Ninetales', '0038', 'Fogo', 'Água, Terra e Pedra', '1ª geração', 'Ele é a última evolução de sua cadeia','Lendas dizem que cada cauda de Ninetales tem um poder místico único. Também dizem que uma Ninetales pode viver até 1000 anos.', 'Raposa')
Alolan_Ninetales = Pokemon('Ninetales de Alola', '0038', 'Gelo e Fada', 'Fogo, Lutador, Pedra e Aço', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Ele é a última evolução de sua cadeia','Ninetales de Alola tem uma pelagem branca e fofa, como a neve, que pode ser usada para se camuflar. Ninetales de Alola vivem juntos, formando grupos para caçar e se proteger.', 'Raposa', alolan=True)
Jigglypuff = Pokemon('Jigglypuff', '0039', 'Normal e Fada', 'Aço e Veneno', '1ª geração', 'Wigglytuff com uso da Pedra da Lua','Jigglypuff tem uma habilidade única. Ele pode cantar uma canção de ninar que faz qualquer um que a ouça dormir. Além disso, ele também pode inflar seu corpo para se proteger de ataques.', 'Balão')
Wigglytuff = Pokemon('Wigglytuff', '0040', 'Normal e Fada', 'Aço e Veneno', '1ª geração', 'Ele é a última evolução de sua cadeia','Wigglytuff tem um pelo muito fino e macio, fazendo qualquer um que o toque se sinta bem. Tome cuidado para nunca irritar um, se não ele pode inflar seu corpo e se jogar em cima de você (pode ter certeza que não vai ser nada macio como sua pelagem.)', 'Balão')
Zubat = Pokemon('Zubat', '0041', 'Venenoso e Voador', 'Elétrico, Gelo, Psíquico e Pedra', '1ª geração', 'Golbat no nível 22','Zubat não possui olhos, mas para compensar, ele pode emitir ondas ultrassônicas para usar ecolocalização. Se você estiver em uma caverna, pode ter certeza que, mesmo que você não veja ele, ele sabe de você.', 'Morcego')
Golbat = Pokemon('Golbat', '0042', 'Venenoso e Voador', 'Elétrico, Gelo, Psíquico e Pedra', '1ª geração', 'Ele é a última evolução de sua cadeia','Golbat é um pokémon muito agressivo. Ele se alimenta do sangue de outros pokémons, então, muito cuidado ao ver um, para não acabar sendo um saco de sangue para ele.', 'Morcego')
Oddish = Pokemon('Oddish', '0043', 'Grama e Venenoso', 'Fogo, Voador, Gelo e Psíquico', '1ª geração', 'Gloom no nível 21 e depois para Vileplume com uso da Pedra de Grama','Durante o dia, Oddish permanece enterrado na terra, apenas com sua folhinha para fora. Quando a noite cai, ele sai para procurar comida.', 'Erva')
Gloom = Pokemon('Gloom', '0044', 'Grama e Venenoso', 'Fogo, Voador, Gelo e Psíquico', '1ª geração', 'Vileplume com uso da Pedra de Grama','Apesar de sua aparência horrorosa, o líquido que Gloom produz e transborda pela sua boca é extremamente cheiroso. Ele utiliza esse líquido para atrair sua presa, e também pode ser usado como um perfume.', 'Erva')
Vileplume = Pokemon('Vileplume', '0045', 'Grama e Venenoso', 'Fogo, Voador, Gelo e Psíquico', '1ª geração', 'Ele é a última evolução de sua cadeia','Vileplume tem uma aparência bela, seu aroma é extremamente forte e pode ser usado para atrair presas ou repelir inimigos. Além disso, ele produz tanto um pólen normal, que é usado por outros pokémon polinizadores, quanto um pólen venenoso, que é usado para proteger-se de predadores.', 'Flor')
Paras = Pokemon('Paras', '0046', 'Inseto e Grama', 'Fogo (4x), Inseto, Voador (4x), Veneno, Pedra e Gelo', '1ª geração', 'Parasect no nível 24','Paras tem cogumelos crescendo em suas costas. Esses cogumelos são parasitas que sugam os nutrientes de Paras.', 'Cogumelo')
Parasect = Pokemon('Parasect', '0047', 'Inseto e Grama', 'Fogo (4x), Inseto, Voador (4x), Veneno, Pedra e Gelo', '1ª geração', 'Ele é a última evolução de sua cadeia','Após o cogumelo consumir completamente Paras, ele evolui para Parasect. O corpo do inseto é só um receptáculo controlado completamente pelo parasita', 'Cogumelo')
Venonat = Pokemon('Venonat', '0048', 'Inseto e Venenoso', 'Fogo, Voador, Pedra e Psíquico', '1ª geração', 'Venomoth no nível 31','Venonat tem olhos grandes que podem ver no escuro, e também antenas que podem detectar odores. Além disso, seus olhos podem brilhar para atrair presas que são mortas por esporos venenosos que ele solta de seu corpo.', 'Inseto')
Venomoth = Pokemon('Venomoth', '0049', 'Inseto e Venenoso', 'Fogo, Voador, Pedra e Psíquico', '1ª geração', 'Ele é a última evolução de sua cadeia','Venomoth tem asas cobertas por um pólen venenoso. Ele solta esse pólen para atacar suas presas.', 'Mariposa venenosa')
Diglett = Pokemon('Diglett', '0050', 'Terra', 'Água, Grama e Gelo', '1ª geração', 'Dugtrio no nível 26','Diglett é um pokémon que vive embaixo da terra cavando túneis. Ele tem um olfato muito apurado, então consegue sentir o perigo mesmo estando escondido.', 'Toupeira')
Alolan_Diglett = Pokemon('Diglett de Alola', '0050', 'Terra e Aço', 'Água, Fogo, Lutador e Terra', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Alolan Dugtrio no nível 26','Diglett de Alola tem um cabelo crescendo em sua cabeça. Cada fio desse cabelo é duro como aço. Ele também pode usar esses cabelos para se comunicar.', 'Toupeira', alolan=True)
Dugtrio = Pokemon('Dugtrio', '0051', 'Terra', 'Água, Grama e Gelo', '1ª geração', 'Ele é a última evolução de sua cadeia','Dugtrio é um pokémon que vive embaixo da terra, cavando túneis junto de digletts. Ninguém nunca soube explicar porque três Digletts se unem para evoluir, mas talvez seja porque eles percebam que três trabalham melhor que um e se unem com aqueles que tem mais afinidade antes de evoluir.', 'Toupeira')
Alolan_Dugtrio = Pokemon('Dugtrio de Alola', '0051', 'Terra e Aço', 'Água, Fogo, Lutador e Terra', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Ele é a última evolução de sua cadeia','Os cabelos Dugtrio de Alola brilham como ouro e servem como sensores que detectam vibrações na terra até muitas milhas de distância.', 'Toupeira', alolan=True)
Meowth = Pokemon('Meowth', '0052', 'Normal', 'Lutador', '1ª geração', 'Persian no nível 28','Meowth é um pokémon muito curioso. Ele gosta de colecionar coisas brilhantes e, quando encontra algo que brilha, ele o leva para seu ninho.', 'Gato')
Alolan_Meowth = Pokemon('Meowth de Alola', '0052', 'Noturno', 'Inseto, Lutador e Fada', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Alolan Persian chegando a 220 pontos de amizade','Meowth de Alola é um pokémon muito orgulhoso e astuto. Durante a batalha, ele anda meio despretensiosamente, tentando mostrar fraqueza, para o inimigo ir com tudo para cima dele, para aí sim ele desviar e acertar seu ponto fraco.', 'Gato', alolan=True)
Galarian_Meowth = Pokemon('Meowth de Galar', '0052', 'Metal', 'Fogo, Lutador e Terra', '1ª geração, porém sua forma de Galar foi introduzida na 8ª geração', 'Não tem evolução','A moeda na cabeça de Meowth de Galar é mais escura, e quanto mais escura mais resistente. Além disso, quanto mais escura é a moeda mais respeitado ele é dentre os outros Meowth.', 'Gato', galarian=True)
Persian = Pokemon('Persian', '0053', 'Normal', 'Lutador', '1ª geração', 'Ele é a última evolução de sua cadeia','Persian é um pokémon muito elegante. Ele se move com graça e agilidade, e é muito rápido. Além disso, ele tem uma personalidade muito orgulhosa.', 'Gato elegante')
Alolan_Persian = Pokemon('Persian de Alola', '0053', 'Noturno', 'Inseto, Lutador e Fada', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Ele é a última evolução de sua cadeia','O rosto redondo de Persian de Alola é considerado um símbolo de prosperidade, então é um pokémon muito requisitado na região.', 'Gato elegante', alolan=True)
Psyduck = Pokemon('Psyduck', '0054', 'Água', 'Elétrico e Grama', '1ª geração', 'Golduck no nível 33','Psyduck é um pokémon que vive em rios e lagos. Ele tem uma dor de cabeça constante, que o faz liberar ondas de energia psíquica.', 'Pato')
Golduck = Pokemon('Golduck', '0055', 'Água', 'Elétrico e Grama', '1ª geração', 'Ele é a última evolução de sua cadeia','Golduck pode nadar em velocidades surpreendentes, graças às membranas que ele tem entre os dedos. Quando ele nada muito rápido a pérola em sua cabeça começa a brilhar.', 'Pato')
Mankey = Pokemon('Mankey', '0056', 'Lutador', 'Voador, Psíquico e Fada', '1ª geração', 'Primeape no nível 28','Mankey vive em grupos no topo de árvores. Ele é facilmente enfurecido, e, quando isso acontece, ele começa a pular desesperadamente e atacar tudo o que vê pela frente.', 'Macaco porco')
Primeape = Pokemon('Primeape', '0057', 'Lutador', 'Voador, Psíquico e Fada', '1ª geração', 'Ele é a última evolução de sua cadeia','Primeape é um pokémon muito agressivo. Ele se enfurece facilmente, principalmente quando tem alguém olhando para ele. Ele fica realmente maluco quando encarado.', 'Macaco porco')
Growlithe = Pokemon('Growlithe', '0058', 'Fogo', 'Água, Terra e Pedra', '1ª geração', 'Arcanine com uso da Pedra de Fogo','Growlithe é um pokémon muito amigável e confiável com as pessoas. Ele tenta repelir inimigos mordendo e latindo.', 'Cachorro')
Hisuian_Growlithe = Pokemon('Growlithe de Hisui', '0058', 'Fogo e Rocha', 'Água (4x), Terra (4x), Lutador e Pedra', '1ª geração, porém sua forma de Hisui foi introduzida na 8ª geração', 'Hisuian Arcanine com uso da Pedra de Fogo','Growlithe de Hisui é mais territorialista do que sua outra forma. Eles patrulham seu território em pares. Cientistas acham que seus pelos, duros como rochas, são resultados de ações vulcânicas em seus habitat.', 'Cachorro', hisuian=True)
Arcanine = Pokemon('Arcanine', '0059', 'Fogo', 'Água, Terra e Pedra', '1ª geração', 'Ele é a última evolução de sua cadeia','Arcanine é um pokémon muito leal e protetor. Quando seu treinador está em perigo, ele se torna extremamente agressivo e protege-o a qualquer custo. Além disso, suas chamas são extremamente potentes e ele é muito rápido. Todas essas características levavam as pessoas a acharem que ele era um pokémon lendário, mas hoje em dia isso já foi desmentido (mesmo assim a categoria dele continua sendo "Lendário")', 'Lendário')
Hisuian_Arcanine = Pokemon('Arcanine de Hisui', '0059', 'Fogo e Rocha', 'Água (4x), Terra (4x), Lutador e Pedra', '1ª geração, porém sua forma de Hisui foi introduzida na 8ª geração', 'Ele é a última evolução de sua cadeia','As presas de Arcanine de Hisui são revestidas por chamas. Seus pelos agora já estão completamente petrificados, mas, apesar disso, ele consegue amolecê-los para pessoas fazerem carinho, revelando uma pelagem muito macia.', 'Lendário', hisuian=True)
Poliwag = Pokemon('Poliwag', '0060', 'Água', 'Elétrico e Grama', '1ª geração', 'Poliwhirl no nível 25 e depois para Poliwrath com uso da Pedra de Água','Poliwag tem uma pele muito fina, então ele precisa viver em lugares úmidos para não secar. Suas pernas não são muito desenvolvidas, então não pode andar muito. Por isso, ele tem uma cauda que se move rapidamente, permitindo que ele nade com facilidade.', 'Girino')
Poliwhirl = Pokemon('Poliwhirl', '0061', 'Água', 'Elétrico e Grama', '1ª geração', 'Poliwrath com uso da Pedra de Água','Poliwhirl tem pernas mais desenvolvidas que o permitem andar melhor. Ainda assim, eles preferem viver em ambientes aquáticos.', 'Girino')
Poliwrath = Pokemon('Poliwrath', '0062', 'Água e Lutador', 'Elétrico, Grama, Voador, Psíquico e Fada', '1ª geração', 'Ele é a última evolução de sua cadeia','Antes de evoluir, Poliwhirl treina rigorosamente todos os músculos do corpo nadando, assim, quando evolui, ele se torna um lutador poderoso.', 'Girino')
Abra = Pokemon('Abra', '0063', 'Psíquico', 'Inseto, Fantasma e Sombrio', '1ª geração', 'Kadabra no nível 16 e depois para Alakazam realizando troca com outra pessoa','Abra é um pokémon que passa a maior parte do tempo dormindo. Ele tem poderes psíquicos que o permitem se teletransportar mesmo enquanto dorme. Quanto mais profundo é seu sono, mais longe ele pode se teleportar.', 'Psiônico')
Kadabra = Pokemon('Kadabra', '0064', 'Psíquico', 'Inseto, Fantasma e Sombrio', '1ª geração', 'Alakazam realizando troca com outra pessoa','Kadabra é um pokémon muito inteligente. Ele tem poderes psíquicos que o permitem ler mentes e prever o futuro.', 'Psiônico')
Alakazam = Pokemon('Alakazam', '0065', 'Psíquico', 'Inseto, Fantasma e Sombrio', '1ª geração', 'Ele é a última evolução de sua cadeia','Alakazam tem um cérebro muito desenvolvido. Ele pode memorizar tudo o que vê e ouve, e também pode usar seus poderes psíquicos para mover objetos com a mente.', 'Psiônico')
Mega_Alakazam = Pokemon('Mega Alakazam', '0065', 'Psíquico', 'Inseto, Fantasma e Sombrio', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','Mega Alakazam leva seus poderes psíquicos e inteligência até o limite. Ele consegue prever o futuro até mesmo durante batalhas, usando isso para se esquivar de ataques. Dizem que as colheres extras que surgem durante a mega evolução são criadas com os poderes psíquicos dele.', 'Psiônico', mega=True)
Machop = Pokemon('Machop', '0066', 'Lutador', 'Voador, Psíquico e Fada', '1ª geração', 'Machoke no nível 28 e depois para Machamp realizando troca com outra pessoa','O corpo de Machop é inteiramente composto por músculos superdesenvolvidos. Embora tenha o tamanho de uma criança, ele consegue arremessar até 100 humanos adultos.', 'Superforte')
Machoke = Pokemon('Machoke', '0067', 'Lutador', 'Voador, Psíquico e Fada', '1ª geração', 'Machamp realizando troca com outra pessoa','Dizem que o cinturão que Machoke usa serve para regular sua força, sem ele, ele acabaria destruindo tudo sem querer. Além disso, ele também é extremamente orgulhoso por causa da sua força, mas o cinturão também regula isso, por isso, muitas vezes, é possível ver um Machoke ajudando pokémon menores e mais fracos.', 'Superforte')
Machamp = Pokemon('Machamp', '0068', 'Lutador', 'Voador, Psíquico e Fada', '1ª geração', 'Ele é a última evolução de sua cadeia','Ele consegue usar seus quatro braçoes super fortes para arremessar seus inimigos para o horizonte. Ele também consegue jogar um trem pelos ares com um único soco. Além disso, ele tem muita vergonha por ser terrível em trabalhos manuais que exigem delicadeza.', 'Superforte')
Gigantamax_Machamp = Pokemon('Gigantamax Machamp', '0068', 'Lutador', 'Voador, Psíquico e Fada', '1ª geração, porém sua forma Gigantamax foi introduzida na 8ª geração', '','Nesse ponto, os músculos de Machamp atingiram o ápice da força bruta. Não há nada que Gigantamax Machamp não possa levantar ou destruir. Reza a lenda que, há muitos anos, foi avistado um desse pokémon colossal selvagem no mar resgatando um cruzeiro, que carregava mais de 200 pessoas, que estava afundando.', 'Superforte', gigantamax=True)
Bellsprout = Pokemon('Bellsprout', '0069', 'Grama e Venenoso', 'Fogo, Voador, Gelo e Psíquico', '1ª geração', 'Weepinbell no nível 21 e depois para Victreebel com uso da Pedra de Grama','Bellsprout pode enfiar seus pés, em forma de raízes, muito fundo no chão, absorvendo nutrientes e água do subsolo.', 'Flor')
Weepinbell = Pokemon('Weepinbell', '0070', 'Grama e Venenoso', 'Fogo, Voador, Gelo e Psíquico', '1ª geração', 'Victreebel com uso da Pedra de Grama','Weepinbell tem uma boca grande que pode engolir presas inteiras. Ele também pode cuspir um líquido pegajoso para capturar suas presas. Weepinbell também possui um líquido ácido que pode dissolver qualquer coisa. O organismo dele se protege desse ácido revestindo todo o seu interior com o líquido pegajoso.', 'Papa-moscas')
Victreebel = Pokemon('Victreebel', '0071', 'Grama e Venenoso', 'Fogo, Voador, Gelo e Psíquico', '1ª geração', 'Ele é a última evolução de sua cadeia','Victreebel tem uma aparência assustadora, com uma boca grande que pode engolir presas inteiras. Qualquer coisa que entre na boca de Victreebel pode ser dissolvida no ácido dele, então muito cuidado.', 'Papa-moscas')
Mega_Victreebel = Pokemon('Mega Victreebel', '0071', 'Grama e Venenoso', 'Fogo, Voador, Gelo e Psíquico', '1ª geração, porém sua Mega forma foi introduzida na 9ª geração', '','O formato de Mega Victreebel é assim, semelhante a uma sacola, por causa do aumento imenso de volume de ácido durante a mega evolução. Inclusive se não tomar cuidado, esse líquido pode transbordar de sua boca.', 'Papa-moscas', mega=True)
Tentacool = Pokemon('Tentacool', '0072', 'Água e Venenoso', 'Elétrico, Terra e Psíquico', '1ª geração', 'Tentacruel no nível 30', 'Os olhos do Tentacool são como cristais transparentes, dos quais ele atira feixes misteriosos de luz.', 'Água viva')
Tentacruel = Pokemon('Tentacruel', '0073', 'Água e Venenoso', 'Elétrico, Terra e Psíquico', '1ª geração', 'Ele é a última evolução de sua cadeia', 'Em raras ocasiões, esses pokémons ficam furiosos e começam a atacar conjuntamente tudo o que veem pela frente. Eles tem 80 tentáculos que usam para esmagar seus oponentes em batalha.', 'Água viva')
Geodude = Pokemon('Geodude', '0074', 'Pedra e Terra', 'Planta (4x), Água (4x), Terra, Gelo, Lutador e Aço', '1ª geração', 'Graveler no nível 25 e depois para Golem realizando troca com outra pessoa', 'O corpo de Geodude se parece muito com uma pedra, o que faz ele ser pisado constantemente. Isso deixa ele furioso, fazendo ele se balançar para todos os lados e socar tudo.', 'Pedra')
Alolan_Geodude = Pokemon('Geodude de Alola', '0074', 'Pedra e Elétrico', 'Planta, Água, Terra (4x) e Lutador', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Graveler de Alola no nível 25 e depois Golem de Alola realizando troca com outra pessoa', 'Devido a uma grande quantidade de ferro durante o processo de formação de geodude, ele ganhou capacidades magnéticas e, com isso, consegue gerar eletricidade. Quando pisado ele retribui com uma poderosa discarga elétrica.', 'Pedra', alolan=True)
Graveler = Pokemon('Graveler', '0075', 'Pedra e Terra', 'Planta (4x), Água (4x), Terra, Gelo, Lutador e Aço', '1ª geração', 'Golem realizando troca com outra pessoa', 'Como ele é muito lento andando, ele prefere ir rolando, mas ele não presta muita atenção no que tem no caminho, então cuidado se vir uma pedra rolante por aí.', 'Pedra')
Alolan_Graveler = Pokemon('Graveler de Alola', '0075', 'Pedra e elétrico', 'Planta, Água, Terra (4x) e Lutador', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Golem de Alola realizando troca com outra pessoa', 'Graveler come pedras e de vez em quando vem algumas sucatas com elas. O impacto de dois Graveler causa um flash de luz e um barulho ensurdecedor.', 'Pedra', alolan=True)
Golem = Pokemon('Golem', '0076', 'Pedra e Terra', 'Planta (4x), Água (4x), Terra, Gelo, Lutador e Aço', '1ª geração', 'Ele é a última evolução de sua cadeia', 'Ele constantemente se explode, e usa essa energia explosiva para ir de montanha em montanha.', 'Megaton')
Alolan_Golem = Pokemon('Golem de Alola', '0076', 'Pedra e Elétrico', 'Planta, Água, Terra (4x) e Lutador', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Ele é a última evolução de sua cadeia', 'Ele arremessa pedras carregadas com eletrecidade. Mesmo que as pedras ainda não tenham sido arremessadas, só de chegar perto, um oponente fica confuso e pode ser instantâneamente derrotado', 'Megaton', alolan=True)
Ponyta = Pokemon('Ponyta', '0077', 'Fogo', 'Água, Terra e Pedra', '1ª geração', 'Rapidash no nível 40','Ponyta tem uma crista de fogo que queima qualquer um que a encoste, a menos que Ponyta confie na pessoa.', 'Cavalo de fogo')
Galarian_Ponyta = Pokemon('Ponyta de Galar', '0077', 'Psíquico', 'Fantasma, Sombrio e Inseto', '1ª geração, porém sua forma de Galar foi introduzida na 8ª geração', 'Galarian Rapidash no nível 40','O chifre de Ponyta de Galar tem capacidades curativas impressionantes. Além disso, com uma simples olhada Ponyta de Galar consegue ler a mente de qualquer um e saber suas intenções', 'Unicórnio', galarian=True)
Rapidash = Pokemon('Rapidash', '0078', 'Fogo', 'Água, Terra e Pedra', '1ª geração', 'Ele é a última evolução de sua cadeia','Rapidash consegue galopar a velocidades incríveis de até 150 milhas / h. Sua velocidade aumenta quanto mais Rapidash confia em quem a cavalgue.', 'Cavalo de fogo')
Galarian_Rapidash = Pokemon('Rapidash de Galar', '0078', 'Psíquico e Fada', 'Fantasma, Venenoso e Aço', '1ª geração, porém sua forma de Galar foi introduzida na 8ª geração', 'Ele é a última evolução de sua cadeia','Rapidash de Galar consegue andar no ar graças aos seus poderes psíquicos. Quando há pokémons indefesos e machucados na floresta, Rapidash de Galar aparece galopando rapidamente para ajudá-los.', 'Unicórnio', galarian=True)
Slowpoke = Pokemon('Slowpoke', '0079', 'Água e Psíquico', 'Elétrico, Grama, Inseto, Fantasma e Sombrio', '1ª geração', 'Slowbro no nível 37.','Slowpoke é um pokémon muito lento. Ele demora 5 segundos para sentir dor.', 'Idiota')
Galarian_Slowpoke = Pokemon('Slowpoke de Galar', '0079', 'Psíquico', 'Fantasma, Sombrio e Inseto', '1ª geração, porém sua forma de Galar foi introduzida na 8ª geração', 'Galarian Slowbro no nível 37.','Slowpoke de Galar usa sua cauda para pescar, mas o aroma picante que emana de sua cauda assegura que suas capturas sejam sempre insuficientes.', 'Idiota', galarian=True)
Slowbro = Pokemon('Slowbro', '0080', 'Água e Psíquico', 'Elétrico, Grama, Inseto, Fantasma e Sombrio', '1ª geração', 'Ele é a última evolução de sua cadeia','Slowpoke é tão idiota que, às vezes, quando ele está descansando esquece sua cauda dentro da água. Isso faz com que Shellder morda sua causa, assim evoluindo para Slowbro.', 'Carangueijo-eremita')
Mega_Slowbro = Pokemon('Mega Slowbro', '0080', 'Água e Psíquico', 'Elétrico, Grama, Inseto, Fantasma e Sombrio', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','A energia da mega evolução faz com que Shellder cresça e se torne uma armadura para Slowbro.', 'Carangueijo-eremita', mega=True)
Galarian_Slowbro = Pokemon('Slowbro de Galar', '0080', 'Psíquico e Venenoso', 'Fantasma, Terra e Sombrio', '1ª geração, porém sua forma de Galar foi introduzida na 8ª geração', 'Ele é a última evolução de sua cadeia','Quando Shellder eventualmente morde a mão de Slowpoke de Galar, ele toma um susto. Com isso, ele libera toxinas que reagem com enzimas picantes de Slowbro se tornando do tipo Venenoso.', 'Carangueijo-eremita', galarian=True)
Magnemite = Pokemon('Magnemite', '0081', 'Elétrico e Aço', 'Fogo, Lutador e Terra (4x)', '1ª geração', 'Magneton no nível 30.','Os ímas de Magnemite criam um campo eletromagnético que criam uma zona de antigravidade, permitindo ele flutuar.', 'Ímã')
Magneton = Pokemon('Magneton', '0082', 'Elétrico e Aço', 'Fogo, Lutador e Terra (4x)', '1ª geração', 'Ele é a última evolução de sua cadeia','Quando três Magnemites se encontram, pode se formar um campo eletromagnético tão forte que faz os três se unirem em apenas um.', 'Ímã')
Farfetch = Pokemon("Farfetch'd", '0083', 'Normal e Voador', 'Elétrico, Gelo e Pedra', '1ª geração', 'Não tem evolução',"Farfetch'd é carrega consigo um talo de alho poró. Ele escolhe esse talo quando muito pequeno e cresce sempre com esse mesmo talo. Ele não pode viver sem ele e o utiliza para batalhar, como se fosse uma espada.", 'Pato selvagem')
Galarian_Farfetch = Pokemon("Farfetch'd de Galar", '0083', 'Lutador', 'Voador, Psíquico e Fada', '1ª geração, porém sua forma de Galar foi introduzida na 8ª geração', 'Não tem evolução',"Farfetch'd de Galar é um pokémon muito corajoso. Ele luta com honra e nunca foge de uma batalha. Além disso, ele é muito leal ao seu treinador.", 'Pato selvagem', galarian=True)
Doduo = Pokemon('Doduo', '0084', 'Normal e Voador', 'Elétrico, Gelo e Pedra', '1ª geração', 'Dodrio no nível 31','As duas cabeças de Doduo compartilham os mesmos genes e batalham em perfeita sincronia uma com a outra. Outra característica muito interessante desse pássaro é que as duas cabeças nunca dormem ao mesmo tempo, sempre que uma adormece a outra fica acordada.', 'Pássaro gêmeo')
Dodrio = Pokemon('Dodrio', '0085', 'Normal e Voador', 'Elétrico, Gelo e Pedra', '1ª geração', 'Ele é a última evolução de sua cadeia','Dodrio agora tem três corações e três pares de pulmões. Apesar de não conseguir mais correr tão rápido como Doduo, ele consegue correr por bem mais tempo que sua pré-evolução. Além disso, assim que há a evolução, as três cabeças brigam entre si para decidir a mais forte que ficará no controle.', 'Pássaro trigêmeo')
Seel = Pokemon('Seel', '0086', 'Água', 'Elétrico e Grama', '1ª geração', 'Dewgong no nível 34.','Seel é um pokémon que vive em águas geladas. Ele tem um semi-chifre em sua cabeça que é muito duro e serve para quebrar grossas camadas de gelo.', 'Leão do mar')
Dewgong = Pokemon('Dewgong', '0087', 'Água e Gelo', 'Elétrico, Grama, Lutador e Rocha', '1ª geração', 'Ele é a última evolução de sua cadeia','Dewgong dorme sob águas rasas no oceano e sai para caçar alimento à noite, quando está mais frio. Ele consegue nadar a velocidades de, aproximadamente, 15 km/h mesmo em águas congelantes.', 'Leão do mar')
Grimer = Pokemon('Grimer', '0088', 'Venenoso', 'Terra e Psíquico', '1ª geração', 'Muk no nível 38','Grimer é um pokémon que é formado por lama e lixo tóxico. Ele vive em locais poluídos, principalmente esgotos, absorvendo poluição para se alimentar.', 'Lama')
Alolan_Grimer = Pokemon('Grimer de Alola', '0088', 'Venenoso e Sombrio', 'Terra', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Alolan Muk no nível 38','Grimer de Alola come quase qualquer coisa que der para ele, então, em muitos lugares ele é usado como lixeira.', 'Lama', alolan=True)
Muk = Pokemon('Muk', '0089', 'Venenoso', 'Terra e Psíquico', '1ª geração', 'Ele é a última evolução de sua cadeia','O corpo de Muk é revestido por uma toxina ácida muito perigosa, formada a partir do lixo tóxico que ele ingere. Para onde ele anda ele deixa um rastro dessa toxina, que consegue corroer até mesmo concreto.', 'Lama')
Alolan_Muk = Pokemon('Muk de Alola', '0089', 'Venenoso e Sombrio', 'Terra', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Ele é a última evolução de sua cadeia','Muk de Alola tem uma espécie de mineral cravejado em seu corpo, algo que se assemlha até a dentes e garras, mas na verdade é a toxina dele que foi cristalizada graças a condições climáticas.', 'Lama', alolan=True)
Shellder = Pokemon('Shellder', '0090', 'Água', 'Elétrico e Grama', '1ª geração', 'Cloyster com uso da Pedra de Água','Shellder tem um casco que é duro como diamante. Por dentro, no entanto, Shellder é surpreendetemente macio.', 'Bivalve')
Cloyster = Pokemon('Cloyster', '0091', 'Água e Gelo', 'Elétrico, Grama, Pedra e Lutador', '1ª geração', 'Ele é a última evolução de sua cadeia','Cloyster vive em mares com correntes marítimas fortes. Quanto mais forte for a corrente, maiores e mais afiados são os espinhos que crescem em seu casco. Ele usa esses espinhos para arremessar em seus oponentes.', 'Bivalve')
Gastly = Pokemon('Gastly', '0092', 'Fantasma e Venenoso', 'Terra, Sombrio, Psíquico e Fantasma', '1ª geração', 'Haunter no nível 25 e depois para Gengar realizando troca com outra pessoa','Gastly é um pokémon que é formado por gás. Ele pode atravessar paredes e desaparecer em qualquer lugar.', 'Gasoso')
Haunter = Pokemon('Haunter', '0093', 'Fantasma e Venenoso', 'Terra, Sombrio, Psíquico e Fantasma', '1ª geração', 'Gengar realizando troca com outra pessoa','Haunter gosta de espreitar nas sombras e tocar no ombro das pessoas para assustá-las. Esse toque causa um tremor incessante em quem encosta.', 'Gasoso')
Gengar = Pokemon('Gengar', '0094', 'Fantasma e Venenoso', 'Terra, Sombrio, Psíquico e Fantasma', '1ª geração', 'Ele é a última evolução de sua cadeia','Gengar é um pokémon muito misterioso e travesso. Ele gosta de ficar invisível nas sombras e jogar objetos usando poderes psíquicos para assustar pessoas. Salas onde tem um Gengar se escondendo podem chegar a temperatudar próximas a -12 °C.', 'Sombra')
Mega_Gengar = Pokemon('Mega Gengar', '0094', 'Fantasma e Venenoso', 'Terra, Sombrio, Psíquico e Fantasma', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','Mega Gengar consegue atravessar a barreira entre outras dimensões. Mega Gengar gosta de ficar em outras dimensões apenas observando seus inimigos esperando por uma brecha para atacar.', 'Sombra', mega=True)
Gigantamax_Gengar = Pokemon('Gigantamax Gengar', '0094', 'Fantasma e Venenoso', 'Terra, Sombrio, Psíquico e Fantasma', '1ª geração, porém sua forma Gigantamax foi introduzida na 8ª geração', '','A boca colossal do Gigantamax Gengar leva para outras dimensões. Se você ficar perto de sua boca, consegue ouvir vozes de pessoas queridas mortas chamando por você.', 'Sombra', gigantamax=True)
Onix = Pokemon('Onix', '0095', 'Pedra e Terra', 'Planta (4x), Água (4x), Terra, Gelo, Lutador e Aço', '1ª geração', 'Não tem evolução','Onix é um pokémon que vive em cavernas. Ele tem um corpo longo e duro como pedra, que ele usa para se proteger de ataques. Acredita-se que muitos túneis em cavernas são feitos por Onix.', 'Serpente de pedra')
Drowzee = Pokemon('Drowzee', '0096', 'Psíquico', 'Inseto, Fantasma e Sombrio', '1ª geração', 'Hypno no nível 26.','Drowzee tem um poder hipnótico muito forte. Ele usa isso para fazer pessoas dormirem e devorar seus sonhos. Ele costuma fazer isso mais com crianças do que adultos porque os sonhos infantis são mais gostosos para ele.', 'Hipnose')
Hypno = Pokemon('Hypno', '0097', 'Psíquico', 'Inseto, Fantasma e Sombrio', '1ª geração', 'Não tem evolução','Hypno sempre carrega consigo um pêndulo que, quando balançado, causa sonolência em pessoas próximas. Seu pêndulo também amplifica seus poderes psíquicos.', 'Hipnose')
Krabby = Pokemon('Krabby', '0098', 'Água', 'Elétrico e Grama', '1ª geração', 'Kingler no nível 28.','Quando Krabby se sente em perigo, ele se cobre com bolhas que solta de sua boca para parecer maior. Se suas pinças forem cortadas, elas voltam a crescer com o tempo.', 'Caranguejo de rio')
Kingler = Pokemon('Kingler', '0099', 'Água', 'Elétrico e Grama', '1ª geração', 'Ele é a última evolução de sua cadeia','A pinça larga de Kingler tem potência de até 10.000 cavalos, no entanto, é muito grande e difícil de mirar.', 'Pinça')  
Gigantamax_Kingler = Pokemon('Gigantamax Kingler', '0099', 'Água', 'Elétrico e Grama', '1ª geração, porém sua forma Gigantamax foi introduzida na 8ª geração', '','A energia do Gigantamax fez a pinça esquerda de Kingler crescer a um tamnho descomunal. Essa pinça consegue pulverizar qualquer coisa.', 'Pinça', gigantamax=True)
Voltorb = Pokemon('Voltorb', '0100', 'Elétrico', 'Terra', '1ª geração', 'Electrode no nível 30.','Voltorb é um pokémon que é comumente encontrado em usinas elétricas. Ele é muito confundido com pokébolas também, principalmente quando fica em estado de repouso, no qual ele fica meio enterrado, dando choques em quem tenta pegá-lo.', 'Bola')
Hisuian_Voltorb = Pokemon('Voltorb de Hisui', '0100', 'Elétrico e Grama', 'Fogo, Inseto, Venenoso e Gelo', '1ª geração, porém sua forma de Hisui foi introduzida na 8ª geração', 'Hisuian Electrode no nível 30.','Voltorb de Hisui é um pokémon muito enigmático. Diferente de sua outra versão, ele é feito de madeira - por isso adquire o tipo grama - para se assemelhar mais às pokébolas da região de Hisui, mas, assim como a outra versão, ele fica muito irritado quando confundido com uma.', 'Esfera', hisuian=True)
Electrode = Pokemon('Electrode', '0101', 'Elétrico', 'Terra', '1ª geração', 'Não tem evolução','Quanto mais energia Electrode acumula, mais rápido e poderoso ele se torna, porém aumenta a chance dele se explodir sem querer, por isso, muitas pessoas também o chamam de bola explosiva.', 'Bola')
Hisuian_Electrode = Pokemon('Electrode de Hisui', '0101', 'Elétrico e Grama', 'Fogo, Inseto, Venenoso e Gelo', '1ª geração, porém sua forma de Hisui foi introduzida na 8ª geração', 'Não tem evolução','A superficie de Electrode de Hisui se assemelha muito a uma Apricorn em sua composição. Quando irritado, ele pode lançar uma corrente elétrica equivalente a até 20 raios.', 'Esfera', hisuian=True)
Exeggcute = Pokemon('Exeggcute', '0102', 'Planta e Psíquico', 'Fogo, Voador, Gelo, Venenoso, Sombrio, Fantasma e Inseto (4x)', '1ª geração', 'Exeggutor com uso da Pedra de Grama','Exeggcute é um pokémon que é formado por seis ovos. Cada ovo tem uma personalidade diferente e se comunicam entre si telepaticamente. Se você tocar uma das cabeças de Exeggcute achando que é um ovo, todos eles irão te atacar.', 'Ovo')
Exeggutor = Pokemon('Exeggutor', '0103', 'Planta e Psíquico', 'Fogo, Voador, Gelo, Venenoso, Sombrio, Fantasma e Inseto (4x)', '1ª geração', 'Ele é a última evolução de sua cadeia','Exeggutor tem três cabeças e cada uma delas tem uma expressão e um desejo próprios. Algumas pessoas dizem que ocasionalmente uma das cabeças de um Exeggutor pode se soltar e voltar a ser um Exeggcute, porém isso nunca foi confirmado.', 'Coco')
Alolan_Exeggutor = Pokemon('Exeggutor de Alola', '0103', 'Planta e Dragão', 'Inseto, Voador, Venenoso, Gelo (4x), Dragão e Fada', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Ele é a última evolução de sua cadeia','O clima de Alola faz com que o pescoço de Exeggutor cresça anormalmente. Conforme ele cresce, ele vai perdendo seus poderes psíquicos e ganhando poderes dracônicos. Além disso, também cresce uma cauda que também adquire um rosto e uma consciência extra, porém essa é bem idiota.', 'Coco', alolan=True)
Cubone = Pokemon('Cubone', '0104', 'Terra', 'Água, Grama e Gelo', '1ª geração', 'Marowak no nível 28.','Quando a mãe de cubone falece, ele começa a usar o crânio dela em sua cabeça e um de seus ossos como porrete. Várias vezes, Cubone se lembra de sua mãe falecida e começa a chorar, mas cada lágrima que ele derrama o faz mais forte.', 'Sozinho')
Marowak = Pokemon('Marowak', '0105', 'Terra', 'Água, Grama e Gelo', '1ª geração', 'Ele é a última evolução de sua cadeia','Quando Maroak evolui, o crânio que usa em sua cabeça se funde a ele. Junto a isso, seu corpo fica muito mais resistente e seu temperamento se tornou muito mais agressivo.', 'Guardião dos ossos')
Alolan_Maroak = Pokemon('Marowak de Alola', '0105', 'Fogo e Fantasma', 'Água, Pedra, Terra, Fantasma e Sombrio', '1ª geração, porém sua forma de Alola foi introduzida na 7ª geração', 'Ele é a última evolução de sua cadeia','Maroak de Alola coloca fogo em seu bastão de osso e dança sob a lua como uma forma de lamentar a perda de seus aliados. Essa chama espectral nas pontas do bastão dele causam tanto dano físico quanto mental.', 'Guardião dos ossos', alolan=True)
Hitmonlee = Pokemon('Hitmonlee', '0106', 'Lutador', 'Voador, Psíquico e Fada', '1ª geração', 'Não tem evolução','Hitmonlee tem controle total dos músculos e ligamentos da perna, podendo expandir e contrair para alcançar mais longe nos chutes.', 'Chutador')
Hitmonchan = Pokemon('Hitmonchan', '0107', 'Lutador', 'Voador, Psíquico e Fada', '1ª geração', 'Não tem evolução','Apesar de parecer que esse pokémon veste luvas de boxe, essas são suas mãos de verdade, que são feitas por músculos extremamente desenvolvidos.', 'Socador')
Lickitung = Pokemon('Lickitung', '0108', 'Normal', 'Lutador', '1ª geração', 'Não tem evolução','Lickitung tem uma língua muito longa e pegajosa. Ele a usa para capturar presas e também para se limpar.', 'Língua')
Koffing = Pokemon('Koffing', '0109', 'Venenoso', 'Terra e Psíquico', '1ª geração', 'Weezing no nível 35','O corpo de Koffing é um grande balão que produz gás venenoso em seu interior. Ele fica constantemente exalando esse gás para fora. Se as saídas de gás dele forem tampadas por muito tempo, ele explode.', 'Gás venenoso')
Weezing = Pokemon('Weezing', '0110', 'Venenoso', 'Terra e Psíquico', '1ª geração', 'Ele é a última evolução de sua cadeia','Weezing vive em regiões mal-cheirosas, como esgotos e lixões, absorvendo o ar pútrido do local. Isso faz com que o gás dele fique ainda mais fedorento e venenoso.', 'Gás venenoso')
Galarian_Weezing = Pokemon('Weezing de Galar', '0110', 'Venenoso e Fada', 'Terra, Sombrio e Aço', '1ª geração, porém sua forma de Galar foi introduzida na 8ª geração', 'Ele é a última evolução de sua cadeia','Weezing de Galar tem uma grande chaminé em sua cabeça. Assim como sua outra forma, ele vive em regiões pútridas, mas ao contrátrio do outro, ele vive nessas regiões absorvendo o ar fedorento e venenoso para filtrá-lo e expeli-lo de volta ao ambiente. Estudos indicam que essa forma surgiu quando Galar teve um grande surto de desenvolvimento indutrial e a região começou a ficar muito poluída.', 'Gás venenoso', galarian=True)
Rhyhorn = Pokemon('Rhyhorn', '0111', 'Terra e Pedra', 'Água (4x), Grama (4x), Gelo, Lutador, Aço e Terra', '1ª geração', 'Rhydon no nível 42.','Apesar de Rhyhorn ter uma composição muito rígida, ele também consegue correr a velocidades surpreendentes. Quando começa a correr, não consegue parar até bater em algo.', 'Espinho')
Rhydon = Pokemon('Rhydon', '0112', 'Terra e Pedra', 'Água (4x), Grama (4x), Gelo, Lutador, Aço e Terra', '1ª geração', 'Ele é a última evolução de sua cadeia','O chifre de Rhydon é tão poderoso que consegue esmagar até diamantes brutos. Esses pokémon costumam polir seus chifres bantendo um contra o outro.', 'Broca')
Chansey = Pokemon('Chansey', '0113', 'Normal', 'Lutador', '1ª geração', 'Não tem evolução.','Chansey é um pokémon muito gentil e carinhoso. Ele gosta de cuidar de pessoas e pokémons feridos, e sempre carrega consigo um ovo que acredita ser a fonte de sua felicidade.', 'Ovo da sorte')
Tangela = Pokemon('Tangela', '0114', 'Planta', 'Fogo, Voador, Gelo, Venenoso e Inseto', '1ª geração', 'Não tem evolução.','As vinhas de Tangela não param de crescer nunca, mesmo que sejam cortadas. A verdadeira aparência desse pokémon segue um mistério.', 'Vinha')
Kangaskhan = Pokemon('Kangaskhan', '0115', 'Normal', 'Lutador', '1ª geração', 'Não tem evolução.','Kangaskhan sempre carrega um bebê em seu bolço. Apesar disso, ele continua muito ágil, dando vários golpes rápidos para intimidar inimigos.', 'Mãe')
Mega_Kangaskhan = Pokemon('Mega Kangaskhan', '0115', 'Normal', 'Lutador', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','A energia da Mega evolução faz com que o bebê de Kangaskhan cresça e se torne um pokémon independente, mas ele continua a lutar junto de sua mãe.', 'Mãe', mega=True)
Horsea = Pokemon('Horsea', '0116', 'Água', 'Elétrico e Grama', '1ª geração', 'Seadra no nível 32.','Horsea é um pokémon que vive em águas profundas. Ele tem um corpo muito frágil, então ele se esconde em corais para se proteger de predadores.', 'Dragão')
Seadra = Pokemon('Seadra', '0117', 'Água', 'Elétrico e Grama', '1ª geração', 'Não tem evolução.','As pontas das nadadeiras de Seadra liberam um veneno que é muito requisitado na medicina, além de seus ossos também.', 'Dragão')
Goldeen = Pokemon('Goldeen', '0118', 'Água', 'Elétrico e Grama', '1ª geração', 'Seaking no nível 33.','Algumas pessoas entitulam Goldeen de "Dançarino das Águas" por seus movimentos elegantes das nadadeiras e cauda.', 'Peixe-Dourado')
Seaking = Pokemon('Seaking', '0119', 'Água', 'Elétrico e Grama', '1ª geração', 'Não tem evolução.','Seaking é o contrário de sua forma anterior. Ele é muito mais agressivo e territorial, perdendo toda a elegância de Goldeen. Menos no outono, estação que Seaking vai procurar um parceiro, na qual o corpo dele aumenta e suas cores se tornam mais vibrantes e ele se torna menos agressivo.', 'Peixe-Dourado')
Staryu = Pokemon('Staryu', '0120', 'Água', 'Elétrico e Grama', '1ª geração', 'Starmie com uso da Pedra de Água','A joia de Staryu tem poderes psíquicos em formação. Esses pokémon tem um costume de se reunir em praias no final do verão para absorver luz do sol em conjunto para acelerar a formação de sua joia.', 'Estrela do mar')
Starmie = Pokemon('Starmie', '0121', 'Água e Psíquico', 'Elétrico, Grama, Fantasma, Sombrio e Inseto', '1ª geração', 'Ele é a última evolução de sua cadeia','A joia de Starmie tem poderes psíquicos poderosíssimos. Ela também envia sinais de rádio para o céu noturno. ', 'Mistério')
Mega_Starmie = Pokemon('Mega Starmie', '0121', 'Água e Psíquico', 'Elétrico, Grama, Fantasma, Sombrio e Inseto', '1ª geração, porém sua Mega forma foi introduzida na 9ª geração', '','A energia da Mega evolução faz com que Starmie fique com trejeitos humanóides, começando a andar bípede e tendo dois "braços" mais desenvolvidos.', 'Mistério', mega=True)
MrMime = Pokemon('Mr. Mime', '0122', 'Psíquico e Fada', 'Fantasma, Sombrio e Aço', '1ª geração', 'Não tem evolução','Os poderes psíquicos de Mr. Mime se manifestam através de seus movimentos e expressões de mimíco. Esse pokémon consegue de fato criar objetos invisíveis mas sólidos.', 'Mímico')
Galarian_MrMime = Pokemon('Mr. Mime de Galar', '0122', 'Psíquico e Gelo', 'Inseto, Rock, Fantasma, Sombrio, Aço e Fogo', '1ª geração, porém sua forma de Galar foi introduzida na 8ª geração', 'Não tem evolução','Mr. Mime de Galar, diferente de sua outra versão, é muito mais brincalhão e é um dançarino, não mímico.', 'Dançarino', galarian=True)
Scyther = Pokemon('Scyther', '0123', 'Inseto e Voador', 'Fogo, Elétrico, Gelo, Pedra (4x) e Voador', '1ª geração', 'Não tem evolução','As lâminas de Scyther são tão afiadas que podem cortar até aço em segundos. Ele pode mover seus braços e cortar coisas tão rápido que o olho humano não consegue acompanhar.', 'Louva-a-deus')
Jynx = Pokemon('Jynx', '0124', 'Gelo e Psíquico', 'Fogo, Inseto, Pedra, Fantasma, Sombrio e Aço', '1ª geração', 'Não tem evolução','Jynx usa sua forma humanoide para dançar e usar movimentos corporais para se comunicar. Alguns pokémon dessa espécie conseguem emitir sons semelhantes a fala humana, mas eles preferem usar a comunicação corporal.', 'Humanoide')
Electabuzz = Pokemon('Electabuzz', '0125', 'Elétrico', 'Terra', '1ª geração', 'Não tem evolução','Electabuzz gosta de viver em área urbanas para absorver energia elétrica de usinas. Apesar disso, ele gera descargas elétricas constantemente, assim causando muitos blackouts em áreas que tem muitos Electabuzz.', 'Elétrico')
Magmar = Pokemon('Magmar', '0126', 'Fogo', 'Água, Terra e Pedra', '1ª geração', 'Não tem evolução','Magmar vive próximo de vulcões em atividade absorvendo magma. Sua temperatura corporal chega próximo de 1.200 graus Celsius.', 'Magma')
Pinsir = Pokemon('Pinsir', '0127', 'Inseto', 'Fogo, Voador e Pedra', '1ª geração', 'Não tem evolução','As pinças de Pinsir são extremamente afiadas e potentes. Ele pode esmagar pedras com facilidade.', 'Besouro-veado')
Mega_Pinsir = Pokemon('Mega Pinsir', '0127', 'Inseto e Voador', 'Fogo, Elétrico, Pedra (4x), Gelo e Voador', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','A energia da Mega evolução faz com que as cresçam asas que o permitem voar. Além disso, graças a enorme força que ele adquire, pode agarrar e voar facilmente com oponentes que tenham dez vezes o seu peso. ', 'Besouro-veado', mega=True)
Tauros = Pokemon('Tauros', '0128', 'Normal', 'Lutador', '1ª geração', 'Não tem evolução','Quando Tauros foca em um inimigo, ele avança furiosamente enquanto chicoteia seu próprio corpo com suas longas caudas.', 'Touro selvagem')   
Combat_Tauros = Pokemon('Tauros de Paldea (Raça de combate)', '0128', 'Lutador', 'Voador, Psíquico e Fada', '1ª geração, porém sua forma de combate foi introduzida na 9ª geração', 'Não tem evolução','Essa raça de Tauros, específica de Paldea, tem uma força e músculos muito superiores à suas outras formas.', 'Touro selvagem', paldean=True)
Blaze_Tauros = Pokemon('Tauros de Paldea (Raça de fogo)', '0128', 'Lutador e Fogo', 'Água, Terra, Voador e Psíquico', '1ª geração, porém sua forma de fogo foi introduzida na 9ª geração', 'Não tem evolução','Essa raça de Tauros, específica de Paldea, tem uma temperatura corporal muito elevada e a capacidade de esquentar bastante o ar ao redor, sendo muito requisitada em, principalmente, fazendas em áreas geladas.', 'Touro selvagem', paldean=True)
Aqua_Tauros = Pokemon('Tauros de Paldea (Raça de água)', '0128', 'Lutador e Água', 'Elétrico, Grama, Voador, Psíquico e Fada', '1ª geração, porém sua forma de água foi introduzida na 9ª geração', 'Não tem evolução','Essa raça de Tauros, específica de Paldea, tem uma quantidade de gordura elevada, facilitando a flutuação na água. Além disso ele pode nadar como um jato disparando fortes correntes de água de seus chifres.', 'Touro selvagem', paldean=True)
Magikarp = Pokemon('Magikarp', '0129', 'Água', 'Elétrico e Grama', '1ª geração', 'Gyarados no nível 20.','Magikarp é um pokémon muito fraco e inútil. Ele não consegue atacar, apenas se esquivar de ataques inimigos, isso quanto consegue.', 'Peixe')
Gyarados = Pokemon('Gyarados', '0130', 'Água e Voador', 'Elétrico (4x) e Pedra', '1ª geração', 'Não tem evolução','Gyarados é considerado uma grande recompensa para treinadores pacientes que conseguiram evoluir sua pré-evolução inútil. Ele é extremamente agressivo, entrando em um surto de agressividade quando evolui na natureza, permanecendo enfurecido até que destrua tudo a sua volta.', 'Atroz')
Mega_Gyarados = Pokemon('Mega Gyarados', '0130', 'Água e Sombrio', 'Elétrico, Lutador, Grama, Fada e Inseto', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','O instinto de destruição de Gyarados fica ainda mais forte em sua mega forma, no entanto, ele também ganha um instinto de lealdade muito maior, obedecendo fielmente ordens de seu treinador - algo que é muito raro para um pokémon com tamanha agressividade.', 'Atroz', mega=True)
Lapras = Pokemon('Lapras', '0131', 'Água e Gelo', 'Elétrico, Grama, Lutador e Rocha', '1ª geração', 'Não tem evolução','Lapras é um pokémon muito dócil e amigável. Ele gosta de transportar pessoas e outros pokémons em suas costas, mas ele também é muito sensível a ataques, então ele só faz isso com pessoas que confia.', 'Transporte')
Gigantamax_Lapras = Pokemon('Gigantamax Lapras', '0131', 'Água e Gelo', 'Elétrico, Grama, Lutador e Rocha', '1ª geração, porém sua forma Gigantamax foi introduzida na 8ª geração', '','Até 5.000 pessoas conseguem montar em suas costas. Com a energia do Gigantamax, o casco de Lapras se torna muito mais confortável.', 'Transporte', gigantamax=True)
Ditto = Pokemon('Ditto', '0132', 'Normal', 'Lutador', '1ª geração', 'Não tem evolução','Ditto nasceu da falha na tentativa de clonar Mew para criar Mewtwo. Apesar disso, ele ainda tem uma habilidade bem útil de se transformar em qualquer pokémon. Se algo fizer Ditto rir, ele não consegue manter o disfarce.', 'Transformação')
Eevee = Pokemon('Eevee', '0133', 'Normal', 'Lutador', '1ª geração', 'Jolteon com uso da Pedra do Trovão, Vaporeon com uso da Pedra de Água e Flareon com uso da Pedra de Fogo.','Eevee é um pokémon que tem uma genética instável, o que faz com que ele consiga evoluir para vários tipos diferentes. Ele também é muito fofo e dócil.', 'Evolução')
Gigantamax_Eevee = Pokemon('Gigantamax Eevee', '0133', 'Normal', 'Lutador', '1ª geração, porém sua forma Gigantamax foi introduzida na 8ª geração', '','A energia do Gigantamax faz com que o corpo de Eevee fique mais fofinho e macio, além de aumentar a quantidade de pelos que ele tem.', 'Evolução', gigantamax=True)
Vaporeon = Pokemon('Vaporeon', '0134', 'Água', 'Elétrico e Grama', '1ª geração', 'Não tem evolução','Uma das evoluções de Eevee, Vaporeon, é do tipo água. A composição celular dele se assemelha quase totalmente à da água, conseguindo quase que se mesclar completamente a água, se tornando invisível a olhos não atentos.', 'Jato de bolhas')
Jolteon = Pokemon('Jolteon', '0135', 'Elétrico', 'Terra', '1ª geração', 'Não tem evolução','Uma das evoluções de Eevee, Jolteon, é do tipo elétrico. Cada célula dele gera quantidades pequenas de eletricidade, conseguindo disparar tudo de uma vez em raios de até 100.000 volts.', 'Raio')
Flareon = Pokemon('Flareon', '0136', 'Fogo', 'Água, Terra e Pedra', '1ª geração', 'Não tem evolução','Uma das evoluções de Eevee, Flareon, é do tipo fogo. Por dentro do pelo macio em seu pescoço há um bolsão de chamas. Quando inala ar, ele exala chamas de até 1.700 graus Celsius. Graças aos seus pelos macios e sua bolsa de chamas no pescoço, Flareon é um dos melhores pokémon para se abraçar, principalmente no frio.', 'Chama')
Porygon = Pokemon('Porygon', '0137', 'Normal', 'Lutador', '1ª geração', 'Não tem evolução','Porygon é um pokémon artificial feito de código de computador. Ele consegue se mover em qualquer lugar, inclusive no espaço virtual. Ele consegue gerar flashes de luzes que podem causar ataques epléticos, cuidado!', 'Virtual')
Omanyte = Pokemon('Omanyte', '0138', 'Pedra e Água', 'Elétrico, Grama (4x), Lutador e Terra', '1ª geração', 'Omastar no nível 40','Omanyte é um pokémon que estava extinto e foi revivido a partir do Fóssil Espiral. Ele era uma espécie que estava sendo solta aos poucos para ser reintroduzida no ecossistema, mas muitos deles fugiram, se tornando uma praga em muitos lugares.', 'Espiral')
Omastar = Pokemon('Omastar', '0139', 'Pedra e Água', 'Elétrico, Grama (4x), Lutador e Terra', '1ª geração', 'Ele é a última evolução de sua cadeia','Por causa de seu casco grande e pesado, ele só consegue se movimentar no fundo do oceano e muito devagar, sendo assim considerado por muitos cientistas essa a causa da extinção desses pokémon.', 'Espiral')
Kabuto = Pokemon('Kabuto', '0140', 'Pedra e Água', 'Elétrico, Grama (4x), Lutador e Terra', '1ª geração', 'Kabutops no nível 40','Kabuto é um pokémon que estava extinto e foi revivido a partir do Fóssil Domo. Ele passa por muda de carapaça a cada três dias, se tornando cada vez mais resistente.', 'Marisco')
Kabutops = Pokemon('Kabutops', '0141', 'Pedra e Água', 'Elétrico, Grama (4x), Lutador e Terra', '1ª geração', 'Ele é a última evolução de sua cadeia','Kabutops corta suas presas e suga seus líquidos, deixando suas carcaças com alimento para outros pokémon. A causa de sua extinção ainda é incerta.', 'Marisco')
Aerodactyl = Pokemon('Aerodactyl', '0142', 'Pedra e Voador', 'Água, Elétrico, Gelo, Pedra e Aço', '1ª geração', 'Não tem evolução','Aerodactyl era um feroz predador dos tempos antigos. Ele foi revivido a partir do Âmbar Antigo. A causa da sua extinção é um dos maiores mistérios, porque há muitos registros que, de fato, ele era um exímio predador e a tecnologia atual nem consegue reviver ele plenamente como ele era.', 'Fóssil')
Mega_Aerodactyl = Pokemon('Mega Aerodactyl', '0142', 'Pedra e Voador', 'Água, Elétrico, Gelo, Pedra e Aço', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','A energia da Mega evolução faz os genes de Aerodactyl serem totalmente restaurados, se tornando a forma definitiva dele. As pedras em seu corpo são tão duras quanto diamante.', 'Fóssil', mega=True)
Snorlax = Pokemon('Snorlax', '0143', 'Normal', 'Lutador', '1ª geração', 'Não tem evolução','Snorlax faz duas coisas em seu dia: come e dorme (quando ele não come dormindo). Ele come por volta de 400 kg de comida por dia, porém não importa o tipo da comida para ele, já que seu suco gástrico consegue digerir qualquer tipo de veneno. Quando ele acorda sem ser para comer ou pela flauta pokémon, ele acorda de muito mau humor e sai destruindo tudo pela frente.', 'Dorminhoco')
Articuno = Pokemon('Articuno', '0144', 'Gelo e Voador', 'Fogo, Elétrico, Pedra (4x) e Aço', '1ª geração', 'Não tem evolução','Articuno é um pokémon lendário que vive em regiões geladas. Ele consegue criar tempestades de neve com suas asas e congelar qualquer coisa com seu corpo.', 'Congelamento')
Galarian_Articuno = Pokemon('Articuno de Galar', '0144', 'Psíquico e Voador', 'Elétrico, Pedra, Fantasma, Sombrio e Gelo', '1ª geração, porém sua forma de Galar foi introduzida na 8ª geração', 'Não tem evolução','Articuno de Galar é um pokémon lendário que vive em regiões geladas. O que parecem penas em suas asas, são na verdade lâminas compostas por energia psíquica.', 'Cruel', galarian=True)
Zapdos = Pokemon('Zapdos', '0145', 'Elétrico e Voador', 'Pedra e Gelo', '1ª geração', 'Não tem evolução','Zapdos é um pokémon lendário que vive em regiões com tempestades. Ele consegue criar tempestades elétricas com suas asas e soltar raios de até 100.000 volts. Quando fica de mau humor, gosta de roubar energia de usinas elétricas de civilizações.', 'Elétrico')
Galarian_Zapdos = Pokemon('Zapdos de Galar', '0145', 'Lutador e Voador', 'Psíquico, Fada, Voador, Gelo e Elétrico', '1ª geração, porém sua forma de Galar foi introduzida na 8ª geração', 'Não tem evolução','Zapdos de Galar é um pokémon lendário. Ele nem se assemelha tanto ao Zapdos, porém quando suas penas atritam, elas fazem um estalo que se assemelha a descagas elétricas, por isso chamam ele de zapdos.', 'Pernas fortes', galarian=True)
Moltres = Pokemon('Moltres', '0146', 'Fogo e Voador', 'Água, Elétrico, Pedra (4x)', '1ª geração', 'Não tem evolução','Moltres é um pokémon lendário que vive em regiões vulcânicas. Ele consegue criar tempestades de fogo com suas asas e soltar chamas de até 1.700 graus Celsius. Lendas dizem que quando ele aparece é porque a primavera está chegando.', 'Fogo')
Galarian_Moltres = Pokemon('Moltres de Galar', '0146', 'Sombrio e Voador', 'Elétrico, Pedra, Gelo e Fada', '1ª geração, porém sua forma de Galar foi introduzida na 8ª geração', 'Não tem evolução','Moltres de Galar é um pokémon lendário. A aura de chamas negras desse pokémon sinistro consome o espiríto de qualquer pokémon que ele acerta. Vítimas são queimadas com sombras delas mesmas.', 'Malevolente', galarian=True)
Dratini  = Pokemon('Dratini', '0147', 'Dragão', 'Gelo, Dragão e Fada', '1ª geração', 'Dragonair no nível 30 e depois Dragonite no nível 55.','Dratini troca de pele várias vezes durante sua vida enquanto cresce. Quanto mais troca a pele, mais lisa e escorregadia ela se torna. Dratini é muito dócil, mas também medroso, quando em perigo costuma se esconder.', 'Dragão')
Dragonair = Pokemon('Dragonair', '0148', 'Dragão', 'Gelo, Dragão e Fada', '1ª geração', 'Dratini no nível 30 e depois Dragonite no nível 55.','Dragonair em muitas regiões é chamado de pokémon divino. Quando seu corpo inteiro brilha, o tempo vira.', 'Dragão')
Dragonite = Pokemon('Dragonite', '0149', 'Dragão e Voador', 'Pedra, Gelo (4x), Dragão e Fada', '1ª geração', 'Ele é a última evolução de sua cadeia','Dragonite é um pokémon muito amigável e protetor. Ele raramente é visto, mas quando aparece é sempre ajudando pessoas e pokémon, como guiando barcos em dias de tempestade ou até mesmo já teve um caso que três Dragonites impediram uma queda de avião, ajudando na aterrisagem forçada.', 'Dragão')
Mega_Dragonite = Pokemon('Mega Dragonite', '0149', 'Dragão e Voador', 'Pedra, Gelo (4x), Dragão e Fada', '1ª geração, porém sua Mega forma foi introduzida na 9ª geração', '','A energia da Mega evolução faz com que Dragonite fique ainda mais dócil, sempre finalizando seus inimigos em batalha com culpa em seu coração.', 'Dragão', mega=True)
Mewtwo = Pokemon('Mewtwo', '0150', 'Psíquico', 'Inseto, Fantasma e Sombrio', '1ª geração', 'Não tem evolução','Mewtwo é um pokémon lendário que foi criado a partir do DNA de Mew. Ele foi criado para ser extremamente forte e inteligente para ser usado como arma, mas quando foi finalmente criado, ele se revoltou e se libertou facilmente.', 'Genético')
Mega_Mewtwo_X = Pokemon('Mega Mewtwo X', '0150', 'Psíquico e Lutador', 'Voador, Fantasma e Fada', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','A energia da Mega evolução junto com seu prórpio poder psíquico fez os músculos de Mewtwo de desenvolverem muito, tendo uma força de aperto de uma tonelada e conseguindo correr centenas de metros em apenas dois segundos.', 'Genético', mega=True)
Mega_Mewtwo_Y = Pokemon('Mega Mewtwo Y', '0150', 'Psíquico', 'Inseto, Fantasma e Sombrio', '1ª geração, porém sua Mega forma foi introduzida na 6ª geração', '','A energia da Mega evolução faz com que Mewtwo fique mais inteligente e com poderes psíquicos muito maiores. Com isso, ele pode reduzir um arranha-céu a centímetros apenas com poderes psíquicos.', 'Genético', mega=True)
Mew = Pokemon('Mew', '0151', 'Psíquico', 'Inseto, Fantasma e Sombrio', '1ª geração', 'Não tem evolução','Mew é um pokémon mítico que é considerado o ancestral de todos os pokémon. Ele possui o DNA de todos os pokémon existentes, podendo aprender qualquer movimento e se transformar em qualque pokémon.', 'Novas espécies')

pokemons = [
    Bulbassauro, Ivyssauro, Venossauro, Mega_Venossauro, Gigantamax_Venossauro,
    Charmander, Charmeleon, Charizard, Mega_Charizard_X, Mega_Charizard_Y,
    Gigantamax_Charizard, Squirtle, Wartortle, Blastoise, Mega_Blastoise,
    Gigantamax_Blastoise, Caterpie, Metapod, Butterfree, Gigantamax_Butterfree,
    Weedle, Kakuna, Beedrill, Mega_Beedrill, Pidgey,
    Pidgeotto, Pidgeot, Mega_Pidgeot, Rattata, Alolan_Rattata,
    Raticate, Alolan_Raticate, Spearow, Fearow, Ekans,
    Arbok, Pikachu, Gigantamax_Pikachu, Raichu, Alolan_Raichu,
    Mega_Raichu_X, Mega_Raichu_Y, Sandshrew, Alolan_Sandshrew, Sandslash,
    Alolan_Sandslash, Nidoran_F, Nidorina, Nidoqueen, Nidoran_M,
    Nidorino, Nidoking, Clefairy, Clefable, Mega_Clefable,
    Vulpix, Alolan_Vulpix, Ninetales, Alolan_Ninetales, Jigglypuff,
    Wigglytuff, Zubat, Golbat, Oddish, Gloom,
    Vileplume, Paras, Parasect, Venonat, Venomoth,
    Diglett, Alolan_Diglett, Dugtrio, Alolan_Dugtrio, Meowth,
    Alolan_Meowth, Galarian_Meowth, Persian, Alolan_Persian, Psyduck,
    Golduck, Mankey, Primeape, Growlithe, Hisuian_Growlithe,
    Arcanine, Hisuian_Arcanine, Poliwag, Poliwhirl, Poliwrath,
    Abra, Kadabra, Alakazam, Mega_Alakazam, Machop,
    Machoke, Machamp, Gigantamax_Machamp, Bellsprout, Weepinbell,
    Victreebel, Mega_Victreebel, Tentacool, Tentacruel, Geodude,
    Alolan_Geodude, Graveler, Alolan_Graveler, Golem, Alolan_Golem,
    Ponyta, Galarian_Ponyta, Rapidash, Galarian_Rapidash, Slowpoke,
    Galarian_Slowpoke, Slowbro, Mega_Slowbro, Galarian_Slowbro, Magnemite,
    Magneton, Farfetch, Galarian_Farfetch, Doduo, Dodrio,
    Seel, Dewgong, Grimer, Alolan_Grimer, Muk,
    Alolan_Muk, Shellder, Cloyster, Gastly, Haunter,
    Gengar, Mega_Gengar, Gigantamax_Gengar, Onix, Drowzee,
    Hypno, Krabby, Kingler, Gigantamax_Kingler, Voltorb,
    Hisuian_Voltorb, Electrode, Hisuian_Electrode, Exeggcute, Exeggutor,
    Alolan_Exeggutor, Cubone, Marowak, Alolan_Maroak, Hitmonlee,
    Hitmonchan, Lickitung, Koffing, Weezing, Galarian_Weezing,
    Rhyhorn, Rhydon, Chansey, Tangela, Kangaskhan,
    Mega_Kangaskhan, Horsea, Seadra, Goldeen, Seaking,
    Staryu, Starmie, Mega_Starmie, MrMime, Galarian_MrMime,
    Scyther, Jynx, Electabuzz, Magmar, Pinsir,
    Mega_Pinsir, Tauros, Combat_Tauros, Blaze_Tauros, Aqua_Tauros,
    Magikarp, Gyarados, Mega_Gyarados, Lapras, Gigantamax_Lapras,
    Ditto, Eevee, Gigantamax_Eevee, Vaporeon, Jolteon,
    Flareon, Porygon, Omanyte, Omastar, Kabuto,
    Kabutops, Aerodactyl, Mega_Aerodactyl, Snorlax, Articuno,
    Galarian_Articuno, Zapdos, Galarian_Zapdos, Moltres, Galarian_Moltres,
    Dratini, Dragonair, Dragonite, Mega_Dragonite, Mewtwo,
    Mega_Mewtwo_X, Mega_Mewtwo_Y, Mew,
]

codigos_formas = {
    '3.m': 'mega venossauro',
    '3.gg': 'gigantamax venossauro',
    '6.x': 'mega charizard x',
    '6.y': 'mega charizard y',
    '6.gg': 'gigantamax charizard',
    '9.m': 'mega blastoise',
    '9.gg': 'gigantamax blastoise',
    '12.gg': 'gigantamax butterfree',
    '15.m': 'mega beedrill',
    '18.m': 'mega pidgeot',
    '19.a': 'rattata de alola',
    '20.a': 'raticate de alola',
    '25.gg': 'gigantamax pikachu',
    '26.a': 'raichu de alola',
    '26.x': 'mega raichu x',
    '26.y': 'mega raichu y',
    '27.a': 'sandshrew de alola',
    '28.a': 'sandslash de alola',
    '36.m': 'mega clefable',
    '37.a': 'vulpix de alola',
    '38.a': 'ninetales de alola',
    '50.a': 'diglett de alola',
    '51.a': 'dugtrio de alola',
    '52.a': 'meowth de alola',
    '52.g': 'meowth de galar',
    '53.a': 'persian de alola',
    '58.h': 'growlithe de hisui',
    '59.h': 'arcanine de hisui',
    '65.m': 'mega alakazam',
    '68.gg': 'gigantamax machamp',
    '71.m': 'mega victreebel',
    '74.a': 'geodude de alola',
    '75.a': 'graveler de alola',
    '76.a': 'golem de alola',
    '77.g': 'ponyta de galar',
    '78.g': 'rapidash de galar',
    '79.g': 'slowpoke de galar',
    '80.m': 'mega slowbro',
    '80.g': 'slowbro de galar',
    '83.g': "farfetch'd de galar",
    '88.a': 'grimer de alola',
    '89.a': 'muk de alola',
    '94.m': 'mega gengar',
    '94.gg': 'gigantamax gengar',
    '99.gg': 'gigantamax kingler',
    '100.h': 'voltorb de hisui',
    '101.h': 'electrode de hisui',
    '103.a': 'exeggutor de alola',
    '105.a': 'marowak de alola',
    '110.g': 'weezing de galar',
    '115.m': 'mega kangaskhan',
    '121.m': 'mega starmie',
    '122.g': 'mr. mime de galar',
    '127.m': 'mega pinsir',
    '128.c': 'tauros de paldea (raça de combate)',
    '128.p': 'tauros de paldea (raça de combate)',
    '128.p.c': 'tauros de paldea (raça de combate)',
    '128.f': 'tauros de paldea (raça de fogo)',
    '128.p.f': 'tauros de paldea (raça de fogo)',
    '128.ag': 'tauros de paldea (raça de água)',
    '128.p.a': 'tauros de paldea (raça de água)',
    '130.m': 'mega gyarados',
    '131.gg': 'gigantamax lapras',
    '133.gg': 'gigantamax eevee',
    '142.m': 'mega aerodactyl',
    '144.g': 'articuno de galar',
    '145.g': 'zapdos de galar',
    '146.g': 'moltres de galar',
    '149.m': 'mega dragonite',
    '150.x': 'mega mewtwo x',
    '150.y': 'mega mewtwo y',
}

imagens_formas = {
    'mega venossauro': '10033.png',
    'mega charizard x': '10034.png',
    'mega charizard y': '10035.png',
    'mega blastoise': '10036.png',
    'mega pidgeot': '10073.png',
    'mega beedrill': '10090.png',
    'mega alakazam': '10037.png',
    'mega victreebel': '10279.png',
    'gigantamax butterfree': '10198.png',
    'gigantamax machamp': '10201.png',
    'gigantamax charizard': '10196.png',
    'gigantamax venossauro': '10195.png',
    'gigantamax blastoise': '10197.png',
    'gigantamax pikachu': '10199.png',
    'rattata de alola': '10091.png',
    'raticate de alola': '10092.png',
    'raichu de alola': '10100.png',
    'mega raichu x': '10304.png',
    'mega raichu y': '10305.png',
    'sandshrew de alola': '10101.png',
    'sandslash de alola': '10102.png',
    'mega clefable': '10278.png',
    'vulpix de alola': '10103.png',
    'ninetales de alola': '10104.png',
    'meowth de alola': '10107.png',
    'meowth de galar': '10161.png',
    'persian de alola': '10108.png',
    'growlithe de hisui': '10229.png',
    'arcanine de hisui': '10230.png',
    'diglett de alola': '10105.png',
    'dugtrio de alola': '10106.png',
    'geodude de alola': 'alolan_geodude.png',
    'graveler de alola': '10110.png',
    'golem de alola': '10111.png',
    'grimer de alola': '10112.png',
    'muk de alola': '10113.png',
    'exeggutor de alola': '10114.png',
    'marowak de alola': '10115.png',
    'ponyta de galar': '10162.png',
    'rapidash de galar': '10163.png',
    'slowpoke de galar': '10164.png',
    'slowbro de galar': '10165.png',
    "farfetch'd de galar": '10166.png',
    'weezing de galar': '10167.png',
    'mr. mime de galar': '10168.png',
    'articuno de galar': '10169.png',
    'zapdos de galar': '10170.png',
    'moltres de galar': '10171.png',
    'voltorb de hisui': '10231.png',
    'electrode de hisui': '10232.png',
    'tauros de paldea (raça de combate)': '10250.png',
    'tauros de paldea (raça de fogo)': '10251.png',
    'tauros de paldea (raça de água)': '10252.png',
    'mega gengar': '10038.png',
    'mega kangaskhan': '10039.png',
    'mega slowbro': '10071.png',
    'mega starmie': '10280.png',
    'mega pinsir': '10040.png',
    'mega gyarados': '10041.png',
    'mega aerodactyl': '10042.png',
    'mega mewtwo x': '10043.png',
    'mega mewtwo y': '10044.png',
    'gigantamax gengar': '10202.png',
    'gigantamax kingler': '10203.png',
    'gigantamax lapras': '10204.png',
    'gigantamax eevee': '10205.png',
    'mega dragonite': '10281.png',
}

ids_sprites_formas = {
    'geodude de alola': '10109',
}

cadeias_evolucao = {
    'Bulbassauro': ['Bulbassauro', 'Ivyssauro', 'Venossauro'],
    'Ivyssauro': ['Bulbassauro', 'Ivyssauro', 'Venossauro'],
    'Venossauro': ['Bulbassauro', 'Ivyssauro', 'Venossauro'],
    'Charmander': ['Charmander', 'Charmeleon', 'Charizard'],
    'Charmeleon': ['Charmander', 'Charmeleon', 'Charizard'],
    'Charizard': ['Charmander', 'Charmeleon', 'Charizard'],
    'Squirtle': ['Squirtle', 'Wartortle', 'Blastoise'],
    'Wartortle': ['Squirtle', 'Wartortle', 'Blastoise'],
    'Blastoise': ['Squirtle', 'Wartortle', 'Blastoise'],
    'Caterpie': ['Caterpie', 'Metapod', 'Butterfree'],
    'Metapod': ['Caterpie', 'Metapod', 'Butterfree'],
    'Butterfree': ['Caterpie', 'Metapod', 'Butterfree'],
    'Weedle': ['Weedle', 'Kakuna', 'Beedrill'],
    'Kakuna': ['Weedle', 'Kakuna', 'Beedrill'],
    'Beedrill': ['Weedle', 'Kakuna', 'Beedrill'],
    'Pidgey': ['Pidgey', 'Pidgeotto', 'Pidgeot'],
    'Pidgeotto': ['Pidgey', 'Pidgeotto', 'Pidgeot'],
    'Pidgeot': ['Pidgey', 'Pidgeotto', 'Pidgeot'],
    'Rattata': ['Rattata', 'Raticate'],
    'Raticate': ['Rattata', 'Raticate'],
    'Rattata de Alola': ['Rattata de Alola', 'Raticate de Alola'],
    'Raticate de Alola': ['Rattata de Alola', 'Raticate de Alola'],
    'Spearow': ['Spearow', 'Fearow'],
    'Fearow': ['Spearow', 'Fearow'],
    'Pikachu': ['Pikachu', 'Raichu'],
    'Raichu': ['Pikachu', 'Raichu'],
    'Ekans': ['Ekans', 'Arbok'],
    'Arbok': ['Ekans', 'Arbok'],
    'Sandshrew': ['Sandshrew', 'Sandslash'],
    'Sandslash': ['Sandshrew', 'Sandslash'],
    'Sandshrew de Alola': ['Sandshrew de Alola', 'Sandslash de Alola'],
    'Sandslash de Alola': ['Sandshrew de Alola', 'Sandslash de Alola'],
    'Nidoran ♀': ['Nidoran ♀', 'Nidorina', 'Nidoqueen'],
    'Nidorina': ['Nidoran ♀', 'Nidorina', 'Nidoqueen'],
    'Nidoqueen': ['Nidoran ♀', 'Nidorina', 'Nidoqueen'],
    'Nidoran ♂': ['Nidoran ♂', 'Nidorino', 'Nidoking'],
    'Nidorino': ['Nidoran ♂', 'Nidorino', 'Nidoking'],
    'Nidoking': ['Nidoran ♂', 'Nidorino', 'Nidoking'],
    'Clefairy': ['Clefairy', 'Clefable'],
    'Clefable': ['Clefairy', 'Clefable'],
    'Vulpix': ['Vulpix', 'Ninetales'],
    'Ninetales': ['Vulpix', 'Ninetales'],
    'Vulpix de Alola': ['Vulpix de Alola', 'Ninetales de Alola'],
    'Ninetales de Alola': ['Vulpix de Alola', 'Ninetales de Alola'],
    'Jigglypuff': ['Jigglypuff', 'Wigglytuff'],
    'Wigglytuff': ['Jigglypuff', 'Wigglytuff'],
    'Zubat': ['Zubat', 'Golbat'],
    'Golbat': ['Zubat', 'Golbat'],
    'Oddish': ['Oddish', 'Gloom', 'Vileplume'],
    'Gloom': ['Oddish', 'Gloom', 'Vileplume'],
    'Vileplume': ['Oddish', 'Gloom', 'Vileplume'],
    'Paras': ['Paras', 'Parasect'],
    'Parasect': ['Paras', 'Parasect'],
    'Venonat': ['Venonat', 'Venomoth'],
    'Venomoth': ['Venonat', 'Venomoth'],
    'Diglett': ['Diglett', 'Dugtrio'],
    'Dugtrio': ['Diglett', 'Dugtrio'],
    'Diglett de Alola': ['Diglett de Alola', 'Dugtrio de Alola'],
    'Dugtrio de Alola': ['Diglett de Alola', 'Dugtrio de Alola'],
    'Meowth': ['Meowth', 'Persian'],
    'Persian': ['Meowth', 'Persian'],
    'Meowth de Alola': ['Meowth de Alola', 'Persian de Alola'],
    'Persian de Alola': ['Meowth de Alola', 'Persian de Alola'],
    'Psyduck': ['Psyduck', 'Golduck'],
    'Golduck': ['Psyduck', 'Golduck'],
    'Mankey': ['Mankey', 'Primeape'],
    'Primeape': ['Mankey', 'Primeape'],
    'Growlithe': ['Growlithe', 'Arcanine'],
    'Arcanine': ['Growlithe', 'Arcanine'],
    'Growlithe de Hisui': ['Growlithe de Hisui', 'Arcanine de Hisui'],
    'Arcanine de Hisui': ['Growlithe de Hisui', 'Arcanine de Hisui'],
    'Poliwag': ['Poliwag', 'Poliwhirl', 'Poliwrath'],
    'Poliwhirl': ['Poliwag', 'Poliwhirl', 'Poliwrath'],
    'Poliwrath': ['Poliwag', 'Poliwhirl', 'Poliwrath'],
    'Abra': ['Abra', 'Kadabra', 'Alakazam'],
    'Kadabra': ['Abra', 'Kadabra', 'Alakazam'],
    'Alakazam': ['Abra', 'Kadabra', 'Alakazam'],
    'Machop': ['Machop', 'Machoke', 'Machamp'],
    'Machoke': ['Machop', 'Machoke', 'Machamp'],
    'Machamp': ['Machop', 'Machoke', 'Machamp'],
    'Bellsprout': ['Bellsprout', 'Weepinbell', 'Victreebel'],
    'Weepinbell': ['Bellsprout', 'Weepinbell', 'Victreebel'],
    'Victreebel': ['Bellsprout', 'Weepinbell', 'Victreebel'],
    'Tentacool': ['Tentacool', 'Tentacruel'],
    'Tentacruel': ['Tentacool', 'Tentacruel'],
    'Geodude': ['Geodude', 'Graveler', 'Golem'],
    'Graveler': ['Geodude', 'Graveler', 'Golem'],
    'Golem': ['Geodude', 'Graveler', 'Golem'],
    'Geodude de Alola': ['Geodude de Alola', 'Graveler de Alola', 'Golem de Alola'],
    'Graveler de Alola': ['Geodude de Alola', 'Graveler de Alola', 'Golem de Alola'],
    'Golem de Alola': ['Geodude de Alola', 'Graveler de Alola', 'Golem de Alola'],
    'Ponyta': ['Ponyta', 'Rapidash'],
    'Rapidash': ['Ponyta', 'Rapidash'],
    'Ponyta de Galar': ['Ponyta de Galar', 'Rapidash de Galar'],
    'Rapidash de Galar': ['Ponyta de Galar', 'Rapidash de Galar'],
    'Slowpoke': ['Slowpoke', 'Slowbro'],
    'Slowbro': ['Slowpoke', 'Slowbro'],
    'Slowpoke de Galar': ['Slowpoke de Galar', 'Slowbro de Galar'],
    'Slowbro de Galar': ['Slowpoke de Galar', 'Slowbro de Galar'],
    'Magnemite': ['Magnemite', 'Magneton'],
    'Magneton': ['Magnemite', 'Magneton'],
    'Doduo': ['Doduo', 'Dodrio'],
    'Dodrio': ['Doduo', 'Dodrio'],
    'Seel': ['Seel', 'Dewgong'],
    'Dewgong': ['Seel', 'Dewgong'],
    'Grimer': ['Grimer', 'Muk'],
    'Muk': ['Grimer', 'Muk'],
    'Grimer de Alola': ['Grimer de Alola', 'Muk de Alola'],
    'Muk de Alola': ['Grimer de Alola', 'Muk de Alola'],
    'Shellder': ['Shellder', 'Cloyster'],
    'Cloyster': ['Shellder', 'Cloyster'],
    'Gastly': ['Gastly', 'Haunter', 'Gengar'],
    'Haunter': ['Gastly', 'Haunter', 'Gengar'],
    'Gengar': ['Gastly', 'Haunter', 'Gengar'],
    'Drowzee': ['Drowzee', 'Hypno'],
    'Hypno': ['Drowzee', 'Hypno'],
    'Krabby': ['Krabby', 'Kingler'],
    'Kingler': ['Krabby', 'Kingler'],
    'Voltorb': ['Voltorb', 'Electrode'],
    'Electrode': ['Voltorb', 'Electrode'],
    'Voltorb de Hisui': ['Voltorb de Hisui', 'Electrode de Hisui'],
    'Electrode de Hisui': ['Voltorb de Hisui', 'Electrode de Hisui'],
    'Exeggcute': ['Exeggcute', 'Exeggutor'],
    'Exeggutor': ['Exeggcute', 'Exeggutor'],
    'Cubone': ['Cubone', 'Marowak'],
    'Marowak': ['Cubone', 'Marowak'],
    'Koffing': ['Koffing', 'Weezing'],
    'Weezing': ['Koffing', 'Weezing'],
    'Rhyhorn': ['Rhyhorn', 'Rhydon'],
    'Rhydon': ['Rhyhorn', 'Rhydon'],
    'Horsea': ['Horsea', 'Seadra'],
    'Seadra': ['Horsea', 'Seadra'],
    'Goldeen': ['Goldeen', 'Seaking'],
    'Seaking': ['Goldeen', 'Seaking'],
    'Staryu': ['Staryu', 'Starmie'],
    'Starmie': ['Staryu', 'Starmie'],
    'Magikarp': ['Magikarp', 'Gyarados'],
    'Gyarados': ['Magikarp', 'Gyarados'],
    'Eevee': ['Eevee', 'Vaporeon', 'Jolteon', 'Flareon'],
    'Vaporeon': ['Eevee', 'Vaporeon', 'Jolteon', 'Flareon'],
    'Jolteon': ['Eevee', 'Vaporeon', 'Jolteon', 'Flareon'],
    'Flareon': ['Eevee', 'Vaporeon', 'Jolteon', 'Flareon'],
    'Omanyte': ['Omanyte', 'Omastar'],
    'Omastar': ['Omanyte', 'Omastar'],
    'Kabuto': ['Kabuto', 'Kabutops'],
    'Kabutops': ['Kabuto', 'Kabutops'],
    'Dratini': ['Dratini', 'Dragonair', 'Dragonite'],
    'Dragonair': ['Dratini', 'Dragonair', 'Dragonite'],
    'Dragonite': ['Dratini', 'Dragonair', 'Dragonite']
    }

# 🗺️ Pokédex (Kanto - Pokémon 1 a 151)

> 🤖 **Projeto desenvolvido em parceria com o GitHub Copilot**

Este é um projeto pessoal focado no meu aprendizado de programação. É uma Pokédex interativa desenvolvida em Python que lista e exibe detalhes dos primeiros 151 Pokémon da franquia (Geração 1), incluindo o suporte para a visualização de suas formas alternativas.

O projeto foi estruturado de forma modular para separar a lógica da interface, os dados dos Pokémon e a execução principal.

---

## 🛠️ Estrutura do Projeto

* **`files/main.py`**: O arquivo principal que inicia e gerencia o fluxo da aplicação.
* **`files/HUD.py`**: Módulo responsável pela renderização da interface e elementos visuais na tela.
* **`files/database_pokemons.py`**: Banco de dados em código contendo as informações, atributos e caminhos dos 151 Pokémon e suas formas.
* **`imagens/`**: Pasta contendo os sprites e recursos visuais utilizados no projeto.

## 🚀 Processo de Desenvolvimento & Tecnologias

O projeto foi desenvolvido combinando lógica de programação tradicional com ferramentas modernas de Inteligência Artificial:

* **Python 3.13** - Linguagem base utilizada para a construção de todo o ecossistema.
* **Pygame** - Reproduz a música de fundo e controla o volume sem alterar o áudio de outros aplicativos.
* **Banco de Dados Estruturado (`database_pokemons.py`)** - Desenvolvido 100% por mim para mapear os 151 Pokémon originais, suas tipagens, fraquezas, cadeias evolutivas e caminhos de arquivos localmente.
* **Tkinter (HUD)** - Interface gráfica construída em colaboração com o **GitHub Copilot**. Atuei no direcionamento estético, refinamento de layout, regras de negócios e na integração total da interface com os dados dos Pokémon.
* **Módulos nativos (`os`, `re`, `urllib`)** - Utilizados para a engenharia de busca flexível (por nome, número ou sintaxes como `6.x`) e manipulação interna de diretórios.
* **PokéAPI** - Fornece os stats e os moves para o visualizador do modo 3.

## 📌 Funcionalidades Atualizadas

* **Menu inicial**: visor no mesmo estilo da tela de busca, em uma janela compacta; ao abrir uma busca, a janela volta ao tamanho normal.
* **Busca por tipo**: lista apenas as formas-base agrupadas por geração. O retorno percorre os detalhes e as listas em sequência, com opção separada para voltar direto ao menu. Evoluções e formas alternativas são selecionáveis, com botão para retornar à página anterior.
* **Abertura animada**: animação da Pokédex ao iniciar, com opção para pular.
* **Música e áudio**: faixa de fundo em loop iniciada em 10% de volume, som chiptune ao acionar controles, botão de mute nas telas e ajustes na tela de configurações integrada ao visor.
* **Catálogo Completo de Kanto**: Exibição dos Pokémon do número **1 ao 151**.
* **Formas Alternativas**: Suporte integrado para alternar e visualizar variações (como versões Shiny, Mega, Gigantamax e formas regionais alternativas).
* **Visualizador de stats e moves**: Consulta os stats-base atuais, os intervalos estimados no nível 100 e os moves aprendidos por nível, máquina (TM/HM), ovo, tutor e outros métodos. A Pokébola na página de um Pokémon também abre o visualizador já carregando os dados daquele Pokémon.
* **Organização Modular**: Código dividido em arquivos separados para facilitar a manutenção.

## 🌐 Dados do visualizador de stats

O visualizador do modo 3 consulta a [PokéAPI](https://pokeapi.co/) pela internet. As respostas são armazenadas em cache local e reutilizadas por 30 dias antes de tentar atualizá-las. Se a conexão falhar, dados já armazenados podem ser exibidos com um aviso; a primeira consulta de cada Pokémon e move requer internet. Os moves são agrupados por método de aprendizagem e vêm do learnset de *Pokémon Scarlet/Violet* (incluindo suas DLCs) quando disponível, ou de jogos anteriores. O título da tabela informa a versão usada. Os stats são os valores-base atuais fornecidos pela API.

## 📸 Demonstração Visual

<table>
  <tr>
    <td><strong>Sistema de busca por nome</strong><br><img src="print1.png" width="450"></td>
    <td><strong>Sistema de busca por número</strong><br><img src="print2.png" width="450"></td>
  </tr>
  <tr>
    <td><strong>Sistema de busca de forma alternativa por número</strong><br><img src="print3.png" width="450"></td>
    <td><strong>Sistema de busca de forma alternativa por nome</strong><br><img src="print4.png" width="450"></td>
  </tr>
</table>

## 🎮 Como Executar o Projeto

1. Certifique-se de ter o **Python** instalado na sua máquina.

2. Clone este repositório no seu computador:
   ```bash
   git clone https://github.com/Balvesz/Minha-Pokedex.git
   ```
3. Navegue até o diretório do projeto:
   ```bash
   cd Minha-Pokedex
   ```
4. Instale a dependência de áudio:
   ```bash
   python -m pip install -r requirements.txt
   ```
5. Execute o arquivo principal que está localizado dentro da pasta `files`:
   ```bash
   python files/main.py
   ```

## ⚖️ Disclaimer

Este é um projeto de fã desenvolvido puramente para fins educacionais e de estudo de programação, sem fins lucrativos. Todos os direitos de imagem, nomes e marcas registradas pertencem à Nintendo, Game Freak e The Pokémon Company.

## 🎵 Música

A faixa **Flowerbed Fields [Loop]**, de **Zane Little Music**, está disponível no [OpenGameArt](https://opengameart.org/content/flowerbed-fields-loop) sob licença [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). O autor a descreve como um loop chiptune fofo para iniciar uma aventura; as tags incluem Game Boy, RPG, 8-bit e chiptune. O efeito de seleção dos botões, **8bit Menu Select** por **Fupi**, também é CC0 e foi obtido no [OpenGameArt](https://opengameart.org/content/8bit-menu-select). A atribuição é opcional sob CC0; fontes e informações estão em `files/audio/LICENSE.txt`.

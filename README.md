# msxRead

Leitor, visualizador e editor de arquivos MSX BASIC e arquivos do Graphos III, com interface gráfica moderna baseada em `customtkinter`.

![Screenshot do msxRead](read-00.png)

## Novidade: Protótipo de Editor MSX-BASIC
O projeto agora inclui um editor completo inspirado no estilo **QuickBasic**, projetado para facilitar o desenvolvimento de software para MSX.

![Screenshot do msxRead](read-01.png)

### Principais Funcionalidades do Editor:
- **Destaque de Sintaxe (Syntax Highlighting):** Realce em tempo real de comandos, funções, strings, comentários e números de linha. Cores totalmente personalizáveis.
- **Auto-Formatação (Beautify):** Organiza o código automaticamente ao digitar, inserindo espaços entre palavras-chave e operadores para melhor legibilidade.
- **Renumeração Inteligente (RENUM):** Função que utiliza **SQLite** para mapear e atualizar automaticamente todas as referências de salto (`GOTO`, `GOSUB`, `THEN`, `ELSE`, etc.) ao renumerar o programa.
- **Suporte ao MSX Basic Dignified:** Ferramentas para remover e adicionar números de linha, permitindo um fluxo de trabalho de edição moderna sem a necessidade de gerenciar números de linha manualmente.
- **Persistência de Configurações:** Preferências do editor (cores, incrementos de renumeração, preservação de caixa alta/baixa) são salvas no banco de dados local.
- **Compatibilidade:** Abre arquivos tokenizados (.bas) e salva/abre arquivos em formato ASCII (.asc/.txt) compatíveis com o comando `LOAD "FILE",A` do MSX.

## Visualizador de Arquivos
- **Graphos III:** Suporte para visualização de arquivos `.SHP` (Shapes), `.ALF` (Alfabeto), `.LAY` (Layout) e `.SCR` (Screen 2).
- **Disk Reader:** Interface para listar e visualizar arquivos diretamente de diretórios que simulam discos de MSX.

![Screenshot do msxRead](read-02.png)

## Tecnologias Utilizadas
- **Python 3.10+**
- **CustomTkinter:** Interface gráfica moderna e responsiva.
- **SQLite3:** Gerenciamento de configurações, histórico de arquivos e mapas de renumeração.
- **Pillow:** Processamento de imagens para os visualizadores.

## Instalação
Requer Python 3.10+ (testado com Tkinter no Windows).

```sh
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Execução
```sh
python main.py
```

## Projetos que inspiraram esta parte
- Basic Dignified Suite: https://github.com/farique1/basic-dignified
- MSX Converter: https://github.com/fgroen/msxconverter

## Ferramenta de IA usada
- Junie (JetBrains AI Agent)
